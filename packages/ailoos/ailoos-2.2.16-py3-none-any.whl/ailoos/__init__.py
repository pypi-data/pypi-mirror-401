"""
Ailoos SDK - Decentralized AI Training Platform
===============================================

A comprehensive SDK for federated learning and decentralized AI training.
Provides zero-configuration setup with embedded IPFS, P2P coordination,
automatic node discovery, and seamless model management.
"""

__version__ = "2.2.5"
__author__ = "Ailoos Technologies & Empoorio Ecosystem"
__license__ = "Proprietary"

# Core imports with proper error handling
from .core.lazy_imports import (
    flwr, tensorflow, kubernetes, pymongo,
    torch, transformers, numpy, pandas,
    require_module, lazy_import
)

# Optional components with lazy loading
try:
    from .setup.auto_setup import AutoSetup, get_embedded_ipfs, start_ipfs_daemon
except ImportError:
    AutoSetup = None
    get_embedded_ipfs = None
    start_ipfs_daemon = None

# Model components - imported lazily to avoid circular dependencies

def _get_p2p_coordinator():
    """Lazy import of P2PCoordinator."""
    from .coordinator.p2p_coordinator import P2PCoordinator, get_p2p_coordinator
    return P2PCoordinator, get_p2p_coordinator

def _get_node_discovery():
    """Lazy import of NodeDiscovery."""
    from .discovery.node_discovery import NodeDiscovery, get_node_discovery
    return NodeDiscovery, get_node_discovery

def _get_update_manager():
    """Lazy import of UpdateManager."""
    from .updates.auto_updates import UpdateManager, get_update_manager
    return UpdateManager, get_update_manager

def _get_ipfs_manager():
    """Lazy import of IPFSManager."""
    from .infrastructure.ipfs_embedded import IPFSManager
    return IPFSManager

# Lazy-loaded classes
class LazyP2PCoordinator:
    def __new__(cls, *args, **kwargs):
        P2PCoordinator, _ = _get_p2p_coordinator()
        return P2PCoordinator(*args, **kwargs)

class LazyNodeDiscovery:
    def __new__(cls, *args, **kwargs):
        NodeDiscovery, _ = _get_node_discovery()
        return NodeDiscovery(*args, **kwargs)

class LazyUpdateManager:
    def __new__(cls, *args, **kwargs):
        UpdateManager, _ = _get_update_manager()
        return UpdateManager(*args, **kwargs)

class LazyIPFSManager:
    def __new__(cls, *args, **kwargs):
        IPFSManager = _get_ipfs_manager()
        return IPFSManager(*args, **kwargs)

# Assign to module level for backward compatibility
P2PCoordinator = LazyP2PCoordinator
NodeDiscovery = LazyNodeDiscovery
UpdateManager = LazyUpdateManager
IPFSManager = LazyIPFSManager

# Lazy functions
def get_p2p_coordinator():
    """Get P2P coordinator instance."""
    _, get_p2p_coordinator_func = _get_p2p_coordinator()
    return get_p2p_coordinator_func()

def get_node_discovery():
    """Get node discovery instance."""
    _, get_node_discovery_func = _get_node_discovery()
    return get_node_discovery_func()

def get_update_manager():
    """Get update manager instance."""
    _, get_update_manager_func = _get_update_manager()
    return get_update_manager_func()

def __getattr__(name: str):
    """Lazy-load heavy optional modules to avoid import-time side effects."""
    if name in ("rag", "financial"):
        import importlib
        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# Convenience functions for quick setup
def quick_setup(verbose: bool = True) -> bool:
    """
    Quick setup for Ailoos - configures everything automatically.

    Args:
        verbose: Whether to show detailed progress

    Returns:
        True if setup successful
    """
    setup = AutoSetup()
    return setup.setup_everything(verbose=verbose)

async def start_federated_node():
    """Start a federated learning node with all services."""
    from .setup.auto_setup import AutoSetup

    setup = AutoSetup()
    if setup.setup_everything():
        # Start all services
        from .discovery.node_discovery import start_node_discovery
        from .updates.auto_updates import schedule_automatic_updates

        await start_node_discovery()
        schedule_automatic_updates(enabled=True)

        print("🎯 Federated learning node started successfully!")
        print("Your node is now participating in the Ailoos network.")
        return True

    return False

# Export main classes and modules
__all__ = [
    # Core classes
    'AutoSetup',
    'P2PCoordinator',
    'NodeDiscovery',
    'UpdateManager',
    'IPFSManager',

    # Lazy imports for optional modules
    'flwr', 'tensorflow', 'kubernetes', 'pymongo',
    'torch', 'transformers', 'numpy', 'pandas',

    # Utility functions
    'require_module', 'lazy_import',

    # RAG system
    'rag',

    # Financial compliance
    'financial',

    # Convenience functions
    'quick_setup',
    'start_federated_node',
    'get_embedded_ipfs',
    'get_p2p_coordinator',
    'get_node_discovery',
    'get_update_manager',
    'start_ipfs_daemon',
]
