"""SCP SDK - Python SDK for System Capability Protocol.

Provides programmatic access to SCP manifests and graphs, plus a framework
for building integrations and runtime instrumentation.
"""

__version__ = "0.1.0"

# Core models
from .core.models import (
    SCPManifest,
    System,
    Ownership,
    Capability,
    Dependency,
    Classification,
    Contact,
    Contract,
    SLA,
    Constraints,
    Runtime,
    Environment,
    FailureMode,
)

# High-level APIs
from .core.manifest import Manifest
from .core.graph import Graph, SystemNode, DependencyEdge

__all__ = [
    "__version__",
    # Models
    "SCPManifest",
    "System",
    "Ownership",
    "Capability",
    "Dependency",
    "Classification",
    "Contact",
    "Contract",
    "SLA",
    "Constraints",
    "Runtime",
    "Environment",
    "FailureMode",
    # High-level APIs
    "Manifest",
    "Graph",
    "SystemNode",
    "DependencyEdge",
]
