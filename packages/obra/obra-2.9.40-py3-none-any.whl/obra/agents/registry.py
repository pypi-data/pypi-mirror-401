"""Agent type registry for dynamic agent discovery.

This module provides a registry for agent types, enabling dynamic agent
discovery and instantiation. Agents can be registered by type and retrieved
by name.

Pattern:
    Registry pattern with singleton instance for global access.
    Per-agent lazy loading (ISSUE-CLI-011) - agents import only when requested.

Example:
    >>> from obra.agents.registry import get_registry, register_agent
    >>>
    >>> @register_agent(AgentType.SECURITY)
    ... class MySecurityAgent(BaseAgent):
    ...     pass
    >>>
    >>> registry = get_registry()
    >>> agent_class = registry.get_agent(AgentType.SECURITY)
    >>> agent = agent_class(Path("/workspace"))

Related:
    - obra/agents/base.py
    - obra/api/protocol.py
    - ISSUE-CLI-011: Lazy loading + decorator registration fix
"""

import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

from obra.agents.base import BaseAgent
from obra.api.protocol import AgentType

logger = logging.getLogger(__name__)


class AgentRegistrationError(Exception):
    """Raised when a critical agent fails to load."""

    def __init__(self, agent_type: AgentType, reason: str):
        """Initialize with agent type and failure reason.

        Args:
            agent_type: Agent that failed to load
            reason: Why registration failed
        """
        self.agent_type = agent_type
        self.reason = reason
        super().__init__(
            f"Critical agent '{agent_type.value}' failed to load: {reason}"
        )


class AgentRegistry:
    """Registry for agent types with per-agent lazy loading.

    Maintains a mapping of AgentType to agent class. Agents can be
    registered using the @register_agent decorator or by calling
    register() directly.

    Lazy Loading (ISSUE-CLI-011):
        Agents are loaded on-demand when first accessed via get_agent().
        This preserves fast package import while ensuring decorator
        registration happens before use.

    Critical Agents:
        Security agent is critical - failure to load raises exception.
        Other agents are optional - failure to load logs warning but continues.

    Attributes:
        _agents: Internal mapping of type to class
        _AGENT_MODULES: Mapping of AgentType to module path for lazy loading
        _CRITICAL_AGENTS: Set of agents that must load successfully
    """

    # Lazy loading mapping: AgentType -> module path (ISSUE-CLI-011)
    # Note: claude_code agent is not part of AgentType enum (not a review agent)
    _AGENT_MODULES = {
        AgentType.SECURITY: "obra.agents.security",
        AgentType.TESTING: "obra.agents.testing",
        AgentType.CODE_QUALITY: "obra.agents.code_quality",
        AgentType.DOCS: "obra.agents.docs",
        AgentType.TEST_EXECUTION: "obra.agents.test_execution",
    }

    # Critical agents that must load successfully (Priority 3)
    _CRITICAL_AGENTS = {
        AgentType.SECURITY,  # Security checks are non-negotiable
    }

    def __init__(self) -> None:
        """Initialize empty registry."""
        self._agents: dict[AgentType, type[BaseAgent]] = {}
        self._lazy_load_attempted: set[AgentType] = set()  # Track load attempts
        logger.debug("AgentRegistry initialized with lazy loading")

    # adr-042-skip - registry methods outside Phase 2 scope
    def register(
        self,
        agent_type: AgentType,
        agent_class: type[BaseAgent],
    ) -> None:
        """Register an agent class for a type.

        Args:
            agent_type: Agent type to register
            agent_class: Agent class to register

        Raises:
            ValueError: If agent_type is already registered
        """
        if agent_type in self._agents:
            existing = self._agents[agent_type].__name__
            logger.warning(
                f"Overwriting agent registration for {agent_type.value}: "
                f"{existing} -> {agent_class.__name__}"
            )

        self._agents[agent_type] = agent_class
        logger.info(f"Registered agent: {agent_type.value} -> {agent_class.__name__}")

    # adr-042-skip - registry methods outside Phase 2 scope
    def get_agent(
        self,
        agent_type: AgentType,
        required: bool = False,
    ) -> type[BaseAgent] | None:
        """Get agent class for type with lazy registration (ISSUE-CLI-011).

        If agent not registered, attempts to lazy-load the agent module
        to trigger @register_agent() decorator. This preserves lazy loading
        benefits while ensuring agents are available when needed.

        Args:
            agent_type: Agent type to look up
            required: If True, raise exception if agent fails to load
                      (overrides critical agent check)

        Returns:
            Agent class or None if not registered/failed to load

        Raises:
            AgentRegistrationError: If required=True or agent is critical and fails to load
        """
        # Check if already registered
        if agent_type in self._agents:
            return self._agents[agent_type]

        # Try lazy registration for this specific agent
        success = self._lazy_register_agent(agent_type)

        # Handle failure based on criticality
        if not success:
            is_critical = required or agent_type in self._CRITICAL_AGENTS
            if is_critical:
                reason = "Module import failed or decorator missing"
                raise AgentRegistrationError(agent_type, reason)

        # Return agent if registration succeeded, None otherwise
        return self._agents.get(agent_type)

    def get_agent_by_name(self, name: str) -> type[BaseAgent] | None:
        """Get agent class by type name string.

        Args:
            name: Agent type name (e.g., "security", "testing")

        Returns:
            Agent class or None if not registered
        """
        try:
            agent_type = AgentType(name)
            return self.get_agent(agent_type)
        except ValueError:
            logger.warning(f"Unknown agent type: {name}")
            return None

    # adr-042-skip - registry methods outside Phase 2 scope
    def create_agent(
        self,
        agent_type: AgentType,
        working_dir: Path,
        llm_config: dict[str, Any] | None = None,
        log_event: Callable[..., None] | None = None,
    ) -> BaseAgent | None:
        """Create an agent instance.

        Args:
            agent_type: Type of agent to create
            working_dir: Working directory for agent
            llm_config: Optional LLM configuration dict for CLI-based analysis.
                       If None, agent returns empty results (no analysis performed).
            log_event: Optional callback for event logging (observability)

        Returns:
            Agent instance or None if type not registered
        """
        agent_class = self.get_agent(agent_type)
        if agent_class is None:
            logger.warning(f"No agent registered for type: {agent_type.value}")
            return None

        try:
            return agent_class(working_dir, llm_config=llm_config, log_event=log_event)
        except Exception as e:
            logger.error(f"Failed to create agent {agent_type.value}: {e}")
            return None

    def list_agents(self) -> list[AgentType]:
        """List all registered agent types.

        Returns:
            List of registered agent types
        """
        return list(self._agents.keys())

    def is_registered(self, agent_type: AgentType) -> bool:
        """Check if agent type is registered.

        Args:
            agent_type: Agent type to check

        Returns:
            True if registered, False otherwise
        """
        return agent_type in self._agents

    def clear(self) -> None:
        """Clear all registered agents (for testing)."""
        self._agents.clear()
        self._lazy_load_attempted.clear()

    def _lazy_register_agent(self, agent_type: AgentType) -> bool:
        """Attempt to lazy-load and register a single agent (ISSUE-CLI-011).

        This method implements per-agent lazy loading. When an agent is requested
        but not yet registered, we import its module to trigger the @register_agent()
        decorator, then verify registration succeeded.

        Args:
            agent_type: Agent type to register

        Returns:
            True if registration succeeded, False otherwise
        """
        import importlib

        # Avoid repeated load attempts for failed agents
        if agent_type in self._lazy_load_attempted:
            return agent_type in self._agents

        self._lazy_load_attempted.add(agent_type)

        # Get module path for this agent
        module_path = self._AGENT_MODULES.get(agent_type)
        if not module_path:
            logger.error(
                f"No module mapping for agent type '{agent_type.value}'. "
                f"Update AgentRegistry._AGENT_MODULES to include this agent."
            )
            return False

        try:
            # Import module to trigger @register_agent() decorator
            logger.debug(f"Lazy-loading agent module: {module_path}")
            importlib.import_module(module_path)

            # Verify registration succeeded
            if agent_type in self._agents:
                logger.info(f"Lazy-registered agent: {agent_type.value}")
                return True
            # Module imported but decorator didn't register - configuration error
            logger.error(
                f"Agent module '{module_path}' imported successfully but "
                f"agent '{agent_type.value}' was not registered. "
                f"Verify @register_agent({agent_type}) decorator is present."
            )
            return False

        except ImportError as e:
            # Module import failed - missing dependency or file
            is_critical = agent_type in self._CRITICAL_AGENTS
            log_level = logger.error if is_critical else logger.warning

            log_level(
                f"Failed to lazy-load agent '{agent_type.value}': {e}. "
                f"{'CRITICAL - Review phase will fail. ' if is_critical else ''}"
                f"Review phase will skip {agent_type.value} checks."
            )
            return False

        except Exception as e:
            # Unexpected error during import
            logger.error(
                f"Unexpected error loading agent '{agent_type.value}': {e}",
                exc_info=True,
            )
            return False


# Global registry instance
_registry: AgentRegistry | None = None


def get_registry() -> AgentRegistry:
    """Get the global agent registry.

    Returns:
        Global AgentRegistry instance
    """
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
    return _registry


def register_agent(
    agent_type: AgentType,
) -> Callable[[type[BaseAgent]], type[BaseAgent]]:
    """Decorator to register an agent class.

    Usage:
        >>> @register_agent(AgentType.SECURITY)
        ... class SecurityAgent(BaseAgent):
        ...     pass

    Args:
        agent_type: Agent type to register

    Returns:
        Decorator function
    """

    def decorator(cls: type[BaseAgent]) -> type[BaseAgent]:
        registry = get_registry()
        registry.register(agent_type, cls)
        return cls

    return decorator


__all__ = ["AgentRegistrationError", "AgentRegistry", "get_registry", "register_agent"]
