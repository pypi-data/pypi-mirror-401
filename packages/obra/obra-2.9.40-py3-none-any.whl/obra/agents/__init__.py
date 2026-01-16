"""Client-side agent deployment and execution.

This module provides infrastructure for deploying and managing review agents
for the Hybrid Orchestration architecture. Agents run on the client and analyze
code for quality, security, testing, and documentation issues.

Key Components:
    - AgentDeployer: Manages subprocess-based agent deployment
    - AgentRegistry: Registry of available agent types
    - Concrete agent implementations (ClaudeCode, Security, Testing, Docs, CodeQuality)

Protocol Flow (from PRD Section 2):
    1. Server sends ReviewRequest with agents_to_run
    2. Client deploys specified agents via AgentDeployer
    3. Each agent analyzes code and returns AgentReport
    4. AgentDeployer collects reports and returns to orchestrator

Example:
    >>> from obra.agents import AgentDeployer, AgentRegistry
    >>> deployer = AgentDeployer(Path("/workspace"))
    >>> reports = deployer.run_agents(
    ...     agents=["security", "testing"],
    ...     item_id="T1",
    ...     timeout_ms=60000
    ... )

Related:
    - docs/design/prds/UNIFIED_HYBRID_ARCHITECTURE_PRD.md Section 2
    - obra/hybrid/handlers/review.py
    - obra/api/protocol.py

Note:
    This package uses PEP 562 lazy loading (ADR-045, Rule 20) to minimize import time.
    Agent implementations and deployer are loaded on first access.
"""

# Eager imports: lightweight base classes and registry
from obra.agents.base import AgentResult, BaseAgent
from obra.agents.registry import (
    AgentRegistrationError,
    AgentRegistry,
    get_registry,  # Direct import - no wrapper needed (ISSUE-CLI-011 fixed in registry)
)

# Lazy loading registry: maps symbol names to their module paths
# Concrete agent implementations import heavy dependencies
#
# ISSUE-CLI-011: Agent registration now happens per-agent via AgentRegistry.get_agent()
# No need for bulk _ensure_agents_registered() - registry lazy-loads on demand
_LAZY_IMPORTS = {
    # Agent Deployer (subprocess management)
    "AgentDeployer": ".deployer",
    # Concrete agents (each imports specific tooling)
    "ClaudeCodeAgent": ".claude_code",
    "SecurityAgent": ".security",
    "TestingAgent": ".testing",
    "DocsAgent": ".docs",
    "CodeQualityAgent": ".code_quality",
}


def __getattr__(name: str):
    """Lazy load agent implementations on first access (PEP 562).

    This reduces package import time by deferring agent loading
    until actually needed. Users typically only need specific agents.
    """
    if name in _LAZY_IMPORTS:
        import importlib

        module = importlib.import_module(_LAZY_IMPORTS[name], __name__)
        value = getattr(module, name)
        # Cache in module globals for subsequent access
        globals()[name] = value
        return value

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """Return all public symbols for IDE autocomplete support."""
    return list(__all__)


__all__ = [
    # Eager imports (lightweight)
    "BaseAgent",
    "AgentResult",
    "AgentRegistry",
    "AgentRegistrationError",
    "get_registry",
    # Lazy imports (concrete agents - heavy)
    "AgentDeployer",
    "ClaudeCodeAgent",
    "SecurityAgent",
    "TestingAgent",
    "DocsAgent",
    "CodeQualityAgent",
]
