"""EmDash - Graph-based coding intelligence system.

DEPRECATED: This package now re-exports from emdash_core.
Import directly from emdash_core for new code.

The business logic has been consolidated into:
- emdash-core: All agents, tools, analytics, etc.
- emdash-cli: CLI that calls the emdash-core FastAPI server

The `em` and `emdash` commands now use emdash-cli.
"""

import warnings

warnings.warn(
    "Importing from 'emdash' is deprecated. "
    "Use 'emdash_core' for business logic or 'emdash_cli' for CLI.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export common items from emdash_core for backwards compatibility
try:
    from emdash_core.agent.toolkit import AgentToolkit
    from emdash_core.agent.events import AgentEventEmitter
    from emdash_core.agent.providers import get_provider
    from emdash_core.analytics.engine import AnalyticsEngine
    from emdash_core.graph.connection import get_connection
except ImportError:
    pass  # emdash_core may not be installed

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("emdash-ai")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
