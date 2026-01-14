"""Local Transformers-based LLM provider.

Uses HuggingFace transformers to run models locally without API calls.
Requires: pip install transformers torch accelerate
"""

import logging
from typing import Any, Optional

from .base import LLMProvider, LLMResponse, ToolCall

log = logging.getLogger(__name__)


# Model specifications: model_id -> (context_limit, description)
LOCAL_MODELS = {
    "microsoft/Phi-3-mini-4k-instruct": (4096, "Phi-3 Mini 4K - 3.8B params, good for summaries"),
    "microsoft/Phi-3-mini-128k-instruct": (131072, "Phi-3 Mini 128K - 3.8B params, long context"),
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0": (2048, "TinyLlama - 1.1B params, very fast"),
    "Qwen/Qwen2.5-1.5B-Instruct": (32768, "Qwen 2.5 1.5B - fast and capable"),
    "Qwen/Qwen2.5-3B-Instruct": (32768, "Qwen 2.5 3B - balanced speed/quality"),
}

DEFAULT_LOCAL_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"


class TransformersProvider(LLMProvider):
    """
    Local LLM provider using HuggingFace Transformers.

    Runs models locally - no API key or network required.
    Models are lazy-loaded on first use to avoid startup overhead.

    Usage:
        provider = TransformersProvider("Qwen/Qwen2.5-1.5B-Instruct")
        response = provider.chat([{"role": "user", "content": "Hello"}])
        print(response.content)

    Or via factory:
        provider = get_provider("local:Qwen/Qwen2.5-1.5B-Instruct")
    """

    def __init__(self, model: str = DEFAULT_LOCAL_MODEL):
        """Initialize with a model name.

        Args:
            model: HuggingFace model ID (e.g., "Qwen/Qwen2.5-1.5B-Instruct")
        """
        # Strip local: prefix if present
        if model.startswith("local:"):
            model = model[6:]
        elif model.startswith("transformers:"):
            model = model[13:]

        super().__init__(model)
        self._pipeline = None
        self._tokenizer = None

    @property
    def is_available(self) -> bool:
        """Check if transformers is installed."""
        try:
            import transformers
            import torch
            return True
        except ImportError:
            return False

    def _get_pipeline(self):
        """Lazy-load the text generation pipeline."""
        if self._pipeline is None:
            if not self.is_available:
                raise ImportError(
                    "transformers and torch are required for local LLM. "
                    "Install with: pip install transformers torch accelerate"
                )

            from transformers import pipeline
            import torch

            log.info(f"Loading local model: {self.model}")

            # Determine device and dtype
            if torch.cuda.is_available():
                device_map = "auto"
                torch_dtype = torch.float16
                log.info("Using CUDA GPU")
            elif torch.backends.mps.is_available():
                device_map = "mps"
                torch_dtype = torch.float16
                log.info("Using Apple MPS")
            else:
                device_map = "cpu"
                torch_dtype = torch.float32
                log.info("Using CPU (slower)")

            self._pipeline = pipeline(
                "text-generation",
                model=self.model,
                device_map=device_map,
                torch_dtype=torch_dtype,
                trust_remote_code=True,
            )
            log.info(f"Model loaded: {self.model}")

        return self._pipeline

    def chat(
        self,
        messages: list[dict],
        tools: Optional[list[dict]] = None,
        system: Optional[str] = None,
        reasoning: bool = False,
    ) -> LLMResponse:
        """Generate response using local model.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Tool schemas (not supported for local models)
            system: Optional system prompt
            reasoning: Enable reasoning mode (not supported)

        Returns:
            LLMResponse with generated content
        """
        if tools:
            log.warning("Tool calling not supported with local transformers models")

        pipe = self._get_pipeline()

        # Build messages list with system prompt
        chat_messages = []
        if system:
            chat_messages.append({"role": "system", "content": system})
        chat_messages.extend(messages)

        # Use the pipeline's chat template
        try:
            result = pipe(
                chat_messages,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                return_full_text=False,
            )

            content = result[0]["generated_text"]

            # Handle case where result is a list of messages
            if isinstance(content, list) and len(content) > 0:
                content = content[-1].get("content", "")

            return LLMResponse(content=content.strip(), raw=result)

        except Exception as e:
            log.error(f"Generation failed: {e}")
            # Fallback to simple prompt format
            return self._fallback_generate(chat_messages)

    def _fallback_generate(self, messages: list[dict]) -> LLMResponse:
        """Fallback generation using simple prompt format."""
        pipe = self._get_pipeline()

        # Build a simple prompt
        parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                parts.append(f"System: {content}")
            elif role == "user":
                parts.append(f"User: {content}")
            elif role == "assistant":
                parts.append(f"Assistant: {content}")
        parts.append("Assistant:")

        prompt = "\n".join(parts)

        result = pipe(
            prompt,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            return_full_text=False,
        )

        content = result[0]["generated_text"]
        return LLMResponse(content=content.strip(), raw=result)

    def get_context_limit(self) -> int:
        """Get the context window size for this model."""
        if self.model in LOCAL_MODELS:
            return LOCAL_MODELS[self.model][0]
        # Default conservative limit
        return 2048

    def format_tool_result(self, tool_call_id: str, result: str) -> dict:
        """Format a tool result message (not supported)."""
        return {"role": "tool", "content": result, "tool_call_id": tool_call_id}

    def format_assistant_message(self, response: LLMResponse) -> dict:
        """Format an assistant response for message history."""
        return {"role": "assistant", "content": response.content or ""}

    @classmethod
    def list_models(cls) -> list[dict]:
        """List available local models."""
        return [
            {
                "id": model_id,
                "context_limit": spec[0],
                "description": spec[1],
            }
            for model_id, spec in LOCAL_MODELS.items()
        ]
