"""Plugin registry for integrations."""

from typing import Callable
import logging

_REGISTRY: dict[str, type] = {}

logger = logging.getLogger(__name__)


def register_integration(name: str) -> Callable:
    """Decorator to register an integration plugin.

    Example:
        @register_integration("pagerduty")
        class PagerDutyIntegration(IntegrationBase):
            ...

    Args:
        name: Integration name/identifier

    Returns:
        Decorator function
    """

    def decorator(cls: type) -> type:
        """Register the class."""
        _REGISTRY[name] = cls
        logger.debug(f"Registered integration: {name} -> {cls.__name__}")
        return cls

    return decorator


def get_integration(name: str) -> type | None:
    """Get a registered integration class by name.

    Args:
        name: Integration name

    Returns:
        Integration class or None if not found
    """
    return _REGISTRY.get(name)


def list_integrations() -> list[str]:
    """List all registered integration names.

    Returns:
        List of integration names
    """
    return list(_REGISTRY.keys())


def clear_registry() -> None:
    """Clear all registered integrations (mainly for testing)."""
    _REGISTRY.clear()
