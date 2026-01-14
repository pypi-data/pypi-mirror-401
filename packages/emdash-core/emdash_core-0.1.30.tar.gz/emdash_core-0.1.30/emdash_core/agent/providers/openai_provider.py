"""OpenAI SDK-based provider - unified interface to OpenAI-compatible APIs."""

import os
import base64
from typing import Optional, Union

from openai import OpenAI

from .base import LLMProvider, LLMResponse, ToolCall, ImageContent
from .models import ChatModel
from ...utils.logger import log


# Provider configuration: base URLs and API key environment variables
PROVIDER_CONFIG = {
    "openai": {
        "base_url": None,  # Uses default OpenAI URL
        "api_key_env": "OPENAI_API_KEY",
    },
    "anthropic": {
        "base_url": "https://api.anthropic.com/v1",
        "api_key_env": "ANTHROPIC_API_KEY",
    },
    "fireworks": {
        "base_url": "https://api.fireworks.ai/inference/v1",
        "api_key_env": "FIREWORKS_API_KEY",
    },
}

# Providers that support the reasoning parameter via extra_body
REASONING_SUPPORTED_PROVIDERS = {"openai"}

# Providers that support extended thinking
THINKING_SUPPORTED_PROVIDERS = {"anthropic"}


class OpenAIProvider(LLMProvider):
    """
    Unified LLM provider using OpenAI SDK.

    Supports OpenAI, Anthropic, and Fireworks through their OpenAI-compatible APIs.
    Just change the model - the provider auto-configures based on the model's provider.
    """

    def __init__(self, model: Union[ChatModel, str]):
        """
        Initialize the provider.

        Args:
            model: ChatModel enum or model string
        """
        if isinstance(model, ChatModel):
            self.chat_model = model
            self.model = model.api_model
            self._context_limit = model.context_window
            self._provider = model.provider
        else:
            # Raw model string - try to parse it
            parsed = ChatModel.from_string(model)
            if parsed:
                self.chat_model = parsed
                self.model = parsed.api_model
                self._context_limit = parsed.context_window
                self._provider = parsed.provider
            else:
                # Fallback for unknown models
                self.chat_model = None
                self.model = model
                self._context_limit = 128000
                self._provider = self._infer_provider(model)

        # Override provider if OPENAI_BASE_URL is set (custom OpenAI-compatible API)
        if os.environ.get("OPENAI_BASE_URL"):
            self._provider = "openai"

        # Create OpenAI client with provider-specific configuration
        config = PROVIDER_CONFIG.get(self._provider, PROVIDER_CONFIG["openai"])

        # Check for provider-specific API key first, then fallback to OPENAI_API_KEY
        # if the provider is openai-compatible
        api_key_env = config["api_key_env"]
        raw_api_key = os.environ.get(api_key_env)

        if not raw_api_key and self._provider != "openai":
            # Fallback to OPENAI_API_KEY for third-party providers if their specific key is missing
            raw_api_key = os.environ.get("OPENAI_API_KEY")
            if raw_api_key:
                log.debug(
                    f"Using OPENAI_API_KEY fallback for provider '{self._provider}' "
                    f"because {api_key_env} is not set."
                )

        api_key = self._sanitize_api_key(raw_api_key)
        if not api_key:
            raise ValueError(
                f"Missing API key. Set {config['api_key_env']} for provider '{self._provider}'."
            )
        self._api_key = api_key
        if raw_api_key and api_key != raw_api_key:
            log.debug(
                f"Sanitized API key for provider={self._provider} env={config['api_key_env']} "
                "(trimmed whitespace/quotes)."
            )
        log_api_key = os.environ.get("EMDASH_LOG_LLM_API_KEY", "").strip().lower() in {
            "1",
            "true",
            "yes",
        }
        if log_api_key:
            log.debug(
                "LLM provider init provider={} model={} base_url={} key_env={} api_key={}",
                self._provider,
                self.model,
                config["base_url"] or "https://api.openai.com/v1",
                config["api_key_env"],
                api_key,
            )
        else:
            log.debug(
                "LLM provider init provider={} model={} base_url={} key_env={} key_len={} key_hint={}",
                self._provider,
                self.model,
                config["base_url"] or "https://api.openai.com/v1",
                config["api_key_env"],
                len(api_key),
                self._mask_api_key(api_key),
            )
        if len(api_key) < 20:
            log.warning(
                "API key for provider={} looks short (len={}). Verify {}.",
                self._provider,
                len(api_key),
                config["api_key_env"],
            )

        self._reasoning_override = self._parse_bool_env("EMDASH_LLM_REASONING")
        self._thinking_override = self._parse_bool_env("EMDASH_LLM_THINKING")
        self._thinking_budget = int(os.environ.get("EMDASH_THINKING_BUDGET", "10000"))

        self.client = OpenAI(
            api_key=api_key,
            base_url=config["base_url"],
        )

    @staticmethod
    def _sanitize_api_key(api_key: Optional[str]) -> Optional[str]:
        """Normalize API key values loaded from env/.env."""
        if api_key is None:
            return None
        cleaned = api_key.strip()
        if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {"'", '"'}:
            cleaned = cleaned[1:-1].strip()
        return cleaned or None

    @staticmethod
    def _parse_bool_env(name: str) -> Optional[bool]:
        """Parse a boolean environment variable."""
        raw = os.environ.get(name)
        if raw is None:
            return None
        cleaned = raw.strip().lower()
        if cleaned in {"1", "true", "yes", "y", "on"}:
            return True
        if cleaned in {"0", "false", "no", "n", "off"}:
            return False
        return None

    @staticmethod
    def _mask_api_key(api_key: str) -> str:
        """Mask API key for safe logging."""
        if len(api_key) <= 8:
            return "*" * len(api_key)
        return f"{api_key[:4]}...{api_key[-4:]}"

    def _infer_provider(self, model: str) -> str:
        """Infer provider from model string.

        If OPENAI_BASE_URL is set, always returns 'openai' to use the custom
        OpenAI-compatible API endpoint with OPENAI_API_KEY.
        """
        # If custom base URL is set, use openai provider (uses OPENAI_API_KEY)
        if os.environ.get("OPENAI_BASE_URL"):
            return "openai"

        model_lower = model.lower()
        if "claude" in model_lower or "anthropic" in model_lower:
            return "anthropic"
        elif "fireworks" in model_lower or "accounts/fireworks" in model_lower:
            return "fireworks"
        else:
            return "openai"  # Default

    def chat(
        self,
        messages: list[dict],
        tools: Optional[list[dict]] = None,
        system: Optional[str] = None,
        reasoning: bool = False,
        thinking: bool = False,
        images: Optional[list[ImageContent]] = None,
    ) -> LLMResponse:
        """
        Send a chat completion request via OpenAI SDK.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool schemas (OpenAI format)
            system: Optional system prompt
            reasoning: Enable reasoning mode (for models that support it)
            thinking: Enable extended thinking (for Anthropic models)
            images: Optional list of images for vision-capable models

        Returns:
            LLMResponse with content and/or tool calls
        """
        # Prepend system message if provided
        if system:
            messages = [{"role": "system", "content": system}] + messages

        if self._reasoning_override is not None:
            reasoning = self._reasoning_override
        if self._thinking_override is not None:
            thinking = self._thinking_override

        # Build completion kwargs
        kwargs = {
            "model": self.model,
            "messages": messages,
        }

        # Add tools if provided
        if tools:
            kwargs["tools"] = tools

        # Add reasoning support via extra_body for providers that support it
        # Skip reasoning for custom base URLs (they may not support it)
        is_custom_api = bool(os.environ.get("OPENAI_BASE_URL"))
        if reasoning and self._provider in REASONING_SUPPORTED_PROVIDERS and not is_custom_api:
            kwargs["extra_body"] = {"reasoning": {"enabled": True}}

        # Add extended thinking for Anthropic models
        # This uses Anthropic's native thinking parameter
        if thinking and self._provider in THINKING_SUPPORTED_PROVIDERS and not is_custom_api:
            extra_body = kwargs.get("extra_body", {})
            extra_body["thinking"] = {
                "type": "enabled",
                "budget_tokens": self._thinking_budget,
            }
            kwargs["extra_body"] = extra_body
            log.info(
                "Extended thinking enabled provider={} model={} budget={}",
                self._provider,
                self.model,
                self._thinking_budget,
            )

        # Add images if provided (vision support)
        if images:
            log.info(
                "Adding {} images to request provider={} model={}",
                len(images),
                self._provider,
                self.model,
            )
            # Find the last user message and add images to it
            for i in range(len(messages) - 1, -1, -1):
                if messages[i].get("role") == "user":
                    messages[i]["content"] = self._format_content_with_images(
                        messages[i].get("content", ""), images
                    )
                    break

        extra_headers = {}

        messages_summary = [
            {
                "role": m.get("role"),
                "content_len": len(str(m.get("content", ""))),
            }
            for m in messages
        ]
        log.info(
            "LLM request start provider={} model={} messages={} tools={} reasoning={}",
            self._provider,
            self.model,
            len(messages),
            bool(tools),
            reasoning,
        )
        log_payload = os.environ.get("EMDASH_LOG_LLM_PAYLOAD", "").strip().lower() in {
            "1",
            "true",
            "yes",
        }
        if log_payload:
            log.debug(
                "LLM request payload provider={} model={} headers={} payload={}",
                self._provider,
                self.model,
                sorted(extra_headers.keys()),
                kwargs,
            )
        else:
            log.debug(
                "LLM request provider={} model={} messages={} tools={} reasoning={} headers={}",
                self._provider,
                self.model,
                messages_summary,
                bool(tools),
                reasoning,
                sorted(extra_headers.keys()),
            )

        # Call OpenAI SDK
        try:
            response = self.client.chat.completions.create(**kwargs)
        except Exception as exc:  # pragma: no cover - defensive logging
            status = getattr(exc, "status_code", None)
            code = getattr(exc, "code", None)
            log.exception(
                "LLM request failed provider={} model={} status={} code={} error={}",
                self._provider,
                self.model,
                status,
                code,
                exc,
            )
            raise

        return self._to_llm_response(response)

    def _to_llm_response(self, response) -> LLMResponse:
        """Convert OpenAI response to our LLMResponse format."""
        response_model = getattr(response, "model", None)
        log.info(
            "LLM response received provider={} model={} response_model={}",
            self._provider,
            self.model,
            response_model,
        )
        log.debug(
            "LLM response provider={} model={} response_model={}",
            self._provider,
            self.model,
            response_model,
        )
        choice = response.choices[0]
        message = choice.message

        # Extract content and thinking
        content = None
        thinking = None

        # Check if content is a list of content blocks (Anthropic extended thinking)
        raw_content = message.content
        if isinstance(raw_content, list):
            # Content blocks format (Anthropic with extended thinking)
            text_parts = []
            thinking_parts = []
            for block in raw_content:
                if hasattr(block, "type"):
                    if block.type == "thinking":
                        thinking_parts.append(getattr(block, "thinking", ""))
                    elif block.type == "text":
                        text_parts.append(getattr(block, "text", ""))
                elif isinstance(block, dict):
                    if block.get("type") == "thinking":
                        thinking_parts.append(block.get("thinking", ""))
                    elif block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
            content = "\n".join(text_parts) if text_parts else None
            thinking = "\n".join(thinking_parts) if thinking_parts else None
        else:
            # Simple string content
            content = raw_content

        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=tc.function.arguments,
                ))

        # Extract token usage if available
        input_tokens = 0
        output_tokens = 0
        thinking_tokens = 0
        if hasattr(response, "usage") and response.usage:
            input_tokens = getattr(response.usage, "prompt_tokens", 0) or 0
            output_tokens = getattr(response.usage, "completion_tokens", 0) or 0
            # Anthropic returns thinking tokens in cache_creation_input_tokens or similar
            # For now, estimate from the thinking content length
            if thinking:
                thinking_tokens = len(thinking) // 4  # Rough estimate

        if thinking:
            log.info(
                "Extended thinking captured provider={} model={} thinking_len={}",
                self._provider,
                self.model,
                len(thinking),
            )

        return LLMResponse(
            content=content,
            thinking=thinking,
            tool_calls=tool_calls,
            raw=response,
            stop_reason=choice.finish_reason,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            thinking_tokens=thinking_tokens,
        )

    def get_context_limit(self) -> int:
        """Get the context window size for this model."""
        return self._context_limit

    def get_max_image_size(self) -> int:
        """Get maximum image size in bytes for this model."""
        # Different providers have different limits
        if self._provider == "anthropic":
            return 5 * 1024 * 1024  # 5MB for Claude
        elif self._provider == "openai":
            return 5 * 1024 * 1024  # 5MB for GPT-4o
        else:
            return 5 * 1024 * 1024  # Default

    def supports_vision(self) -> bool:
        """Check if this model supports image input."""
        if self.chat_model:
            return self.chat_model.spec.supports_vision

        # For unknown models, assume no vision support
        return False

    def supports_thinking(self) -> bool:
        """Check if this model supports extended thinking."""
        if self.chat_model:
            return self.chat_model.spec.supports_thinking

        # For unknown models, check if provider supports thinking
        return self._provider in THINKING_SUPPORTED_PROVIDERS

    def _format_image_for_api(self, image: ImageContent) -> dict:
        """Format an image for OpenAI/Anthropic API.

        Args:
            image: ImageContent with raw image data

        Returns:
            Dict with image_url for the API
        """
        encoded = base64.b64encode(image.image_data).decode("utf-8")
        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{image.format};base64,{encoded}"
            }
        }

    def _format_content_with_images(
        self,
        text: str,
        images: Optional[list[ImageContent]] = None
    ):
        """Format message content with optional images.

        For vision models, returns a list of content blocks.
        For non-vision models, returns text only.

        Args:
            text: Text content
            images: Optional list of images

        Returns:
            Content formatted for this provider
        """
        if not images:
            return text

        if not self.supports_vision():
            log.warning(
                "Model {} does not support vision, images will be stripped",
                self.model,
            )
            return text

        # Vision model: create content blocks
        content = [{"type": "text", "text": text}]
        for img in images:
            content.append(self._format_image_for_api(img))

        return content

    def format_tool_result(self, tool_call_id: str, result: str) -> dict:
        """
        Format a tool result message.

        Uses OpenAI format.
        """
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": result,
        }

    def format_assistant_message(self, response: LLMResponse) -> dict:
        """
        Format an assistant response to add back to messages.

        Uses OpenAI format.
        """
        message = {"role": "assistant"}

        if response.content:
            message["content"] = response.content

        if response.tool_calls:
            message["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.name,
                        "arguments": tc.arguments,
                    }
                }
                for tc in response.tool_calls
            ]

        return message
