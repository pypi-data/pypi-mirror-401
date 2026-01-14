"""MCP configuration schema and loading.

This module provides configuration classes for managing MCP servers,
compatible with Claude Desktop's mcp_config.json format.
"""

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ...utils.logger import log


@dataclass
class MCPServerConfig:
    """Configuration for a single MCP server.

    Attributes:
        name: Unique identifier for this server
        command: Command to run (e.g., "npx", "github-mcp-server")
        args: Arguments to pass to the command
        env: Environment variables (supports ${VAR} syntax)
        enabled: Whether this server is enabled
        timeout: Timeout in seconds for tool calls
    """

    name: str
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    enabled: bool = True
    timeout: int = 30

    def get_resolved_env(self) -> dict[str, str]:
        """Resolve environment variable references like ${VAR_NAME}.

        For GitHub tokens, also checks Rove auth config first.
        For graph DB path, uses emdash config default.

        Returns:
            Dictionary with resolved environment values
        """
        resolved = {}
        pattern = re.compile(r"\$\{([^}]+)\}")

        def get_env_value(var_name: str) -> str:
            """Get environment value, checking emdash config for special vars."""
            # Check for GitHub token - use emdash auth if available
            if var_name in ("GITHUB_TOKEN", "GITHUB_PERSONAL_ACCESS_TOKEN"):
                try:
                    from ...auth import get_github_token
                    token = get_github_token()
                    if token:
                        return token
                except ImportError:
                    pass
            # Check for graph DB path - use emdash config default
            if var_name == "EMDASH_GRAPH_DB_PATH":
                env_val = os.getenv(var_name)
                if env_val:
                    return env_val
                # Default to .emdash/index/kuzu_db in cwd
                default_path = Path.cwd() / ".emdash" / "index" / "kuzu_db"
                return str(default_path)
            # Fall back to environment variable
            return os.getenv(var_name, "")

        for key, value in self.env.items():
            match = pattern.fullmatch(value)
            if match:
                env_var = match.group(1)
                env_value = get_env_value(env_var)
                if not env_value:
                    log.warning(f"Environment variable {env_var} not set for MCP server {self.name}")
                resolved[key] = env_value
            else:
                # Check for partial substitution like "prefix_${VAR}_suffix"
                def replace_var(m):
                    return get_env_value(m.group(1))

                resolved[key] = pattern.sub(replace_var, value)

        return resolved

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "command": self.command,
            "args": self.args,
            "env": self.env,
            "enabled": self.enabled,
            "timeout": self.timeout,
        }

    @classmethod
    def from_dict(cls, name: str, data: dict) -> "MCPServerConfig":
        """Create from dictionary."""
        return cls(
            name=name,
            command=data.get("command", ""),
            args=data.get("args", []),
            env=data.get("env", {}),
            enabled=data.get("enabled", True),
            timeout=data.get("timeout", 30),
        )


@dataclass
class MCPConfigFile:
    """Root configuration for all MCP servers.

    This class handles loading and saving the MCP configuration file,
    which uses Claude Desktop's format:

    {
        "mcpServers": {
            "server-name": {
                "command": "...",
                "args": [...],
                "env": {...}
            }
        }
    }
    """

    servers: dict[str, MCPServerConfig] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "MCPConfigFile":
        """Load MCP configuration from file.

        Args:
            path: Path to the configuration file

        Returns:
            MCPConfigFile instance (empty if file doesn't exist)
        """
        if not path.exists():
            log.debug(f"MCP config file not found: {path}")
            return cls()

        try:
            with open(path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            log.error(f"Invalid JSON in MCP config file {path}: {e}")
            return cls()
        except Exception as e:
            log.error(f"Failed to read MCP config file {path}: {e}")
            return cls()

        servers = {}
        for name, config in data.get("mcpServers", {}).items():
            try:
                servers[name] = MCPServerConfig.from_dict(name, config)
            except Exception as e:
                log.warning(f"Invalid MCP server config '{name}': {e}")

        log.info(f"Loaded MCP config with {len(servers)} servers from {path}")
        return cls(servers=servers)

    def save(self, path: Path) -> None:
        """Save configuration to file.

        Args:
            path: Path to save the configuration file
        """
        data = {"mcpServers": {}}
        for name, server in self.servers.items():
            data["mcpServers"][name] = server.to_dict()

        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        log.info(f"Saved MCP config to {path}")

    def get_enabled_servers(self) -> list[MCPServerConfig]:
        """Get list of enabled server configurations.

        Returns:
            List of enabled MCPServerConfig instances
        """
        return [s for s in self.servers.values() if s.enabled]

    def add_server(self, config: MCPServerConfig) -> None:
        """Add or update a server configuration.

        Args:
            config: Server configuration to add
        """
        self.servers[config.name] = config

    def remove_server(self, name: str) -> bool:
        """Remove a server configuration.

        Args:
            name: Name of the server to remove

        Returns:
            True if server was removed, False if not found
        """
        if name in self.servers:
            del self.servers[name]
            return True
        return False

    def get_server(self, name: str) -> Optional[MCPServerConfig]:
        """Get a server configuration by name.

        Args:
            name: Name of the server

        Returns:
            MCPServerConfig or None if not found
        """
        return self.servers.get(name)


def get_default_mcp_config_path(repo_root: Optional[Path] = None) -> Path:
    """Get the default path for the MCP configuration file.

    Args:
        repo_root: Repository root directory (uses cwd if not provided)

    Returns:
        Path to .emdash/mcp.json
    """
    if repo_root is None:
        repo_root = Path.cwd()
    return repo_root / ".emdash" / "mcp.json"


def get_default_mcp_servers() -> dict[str, MCPServerConfig]:
    """Get the default MCP servers that ship with Rove.

    Returns:
        Dictionary of default server configurations
    """
    # Check if graph MCP is enabled via env flag
    enable_graph_mcp = os.getenv("ENABLE_GRAPH_MCP", "false").lower() == "true"

    return {
        "github": MCPServerConfig(
            name="github",
            command="github-mcp-server",
            args=["stdio"],
            env={
                "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}",
            },
            enabled=False,  # Disabled - use local tools for codebase exploration
            timeout=30,
        ),
        "emdash-graph": MCPServerConfig(
            name="emdash-graph",
            command="emdash-graph-mcp",
            args=["--db-path", "${EMDASH_GRAPH_DB_PATH}"],
            env={
                "EMDASH_GRAPH_DB_PATH": "${EMDASH_GRAPH_DB_PATH}",
            },
            enabled=enable_graph_mcp,
            timeout=30,
        ),
    }


def create_default_mcp_config(path: Path) -> MCPConfigFile:
    """Create a default MCP config file with pre-configured servers.

    This creates the .emdash/mcp.json file with GitHub MCP enabled
    by default for all new Rove installations.

    Args:
        path: Path to save the config file

    Returns:
        The created MCPConfigFile
    """
    config = MCPConfigFile(servers=get_default_mcp_servers())
    config.save(path)
    log.info(f"Created default MCP config with GitHub MCP at {path}")
    return config


def ensure_mcp_config(path: Path) -> MCPConfigFile:
    """Ensure MCP config exists, creating default if needed.

    Args:
        path: Path to the config file

    Returns:
        MCPConfigFile (loaded or newly created)
    """
    if path.exists():
        return MCPConfigFile.load(path)
    else:
        return create_default_mcp_config(path)
