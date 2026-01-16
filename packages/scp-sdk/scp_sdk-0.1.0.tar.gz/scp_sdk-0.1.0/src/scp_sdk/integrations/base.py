"""Base class for all SCP integrations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
import logging

from ..core.graph import Graph, SystemNode, DependencyEdge
from .config import IntegrationConfig
from .utils import IDCache


@dataclass
class SyncResult:
    """Results from a sync operation."""

    systems_synced: int = 0
    dependencies_synced: int = 0
    errors: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        """Check if sync completed without errors."""
        return len(self.errors) == 0

    def add_error(self, item: Any, error: Exception) -> None:
        """Add an error to the result.

        Args:
            item: The item that failed (system, edge, etc.)
            error: The exception that occurred
        """
        self.errors.append({"item": str(item), "error": str(error)})

    def add_warning(self, message: str) -> None:
        """Add a warning to the result.

        Args:
            message: Warning message
        """
        self.warnings.append(message)


class IntegrationBase(ABC):
    """Abstract base class for SCP integrations.

    Provides standard sync workflow and utilities. Subclasses implement
    vendor-specific logic in sync_system() and sync_dependency().

    Example:
        class MyIntegration(IntegrationBase):
            def sync_system(self, system: SystemNode) -> None:
                # Push system to vendor API
                pass

            def sync_dependency(self, edge: DependencyEdge) -> None:
                # Push dependency to vendor API
                pass
    """

    def __init__(self, config: IntegrationConfig):
        """Initialize integration.

        Args:
            config: Integration configuration
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._id_cache = IDCache()

    def sync(self, graph: Graph, dry_run: bool = False) -> SyncResult:
        """Sync graph to vendor system.

        Standard workflow:
        1. Call pre_sync hook
        2. Sync all systems
        3. Sync all dependencies
        4. Call post_sync hook

        Args:
            graph: Architecture graph to sync
            dry_run: If True, validate but don't make changes

        Returns:
            SyncResult with statistics and errors
        """
        self.logger.info(
            f"Starting sync: {len(graph)} systems, dry_run={dry_run}"
        )

        result = SyncResult()

        try:
            # Pre-sync hook
            self.pre_sync(graph, dry_run)

            # Sync systems
            for system in graph.systems():
                try:
                    if not dry_run:
                        self.sync_system(system)
                    else:
                        self.logger.debug(f"[DRY RUN] Would sync system: {system.name}")

                    result.systems_synced += 1
                except Exception as e:
                    self.logger.error(f"Failed to sync system {system.name}: {e}")
                    result.add_error(system, e)
                    self.on_error(system, e)

            # Sync dependencies
            for edge in graph.dependencies():
                try:
                    if not dry_run:
                        self.sync_dependency(edge)
                    else:
                        self.logger.debug(
                            f"[DRY RUN] Would sync dependency: {edge.from_urn} -> {edge.to_urn}"
                        )

                    result.dependencies_synced += 1
                except Exception as e:
                    self.logger.error(
                        f"Failed to sync dependency {edge.from_urn} -> {edge.to_urn}: {e}"
                    )
                    result.add_error(edge, e)
                    self.on_error(edge, e)

            # Post-sync hook
            self.post_sync(graph, result, dry_run)

        except Exception as e:
            self.logger.error(f"Sync failed: {e}")
            result.add_error(graph, e)

        self.logger.info(
            f"Sync complete: {result.systems_synced} systems, "
            f"{result.dependencies_synced} dependencies, "
            f"{len(result.errors)} errors"
        )

        return result

    @abstractmethod
    def sync_system(self, system: SystemNode) -> None:
        """Sync a system to the vendor platform.

        Subclasses must implement this method.

        Args:
            system: System node to sync
        """
        pass

    @abstractmethod
    def sync_dependency(self, edge: DependencyEdge) -> None:
        """Sync a dependency relationship to the vendor platform.

        Subclasses must implement this method.

        Args:
            edge: Dependency edge to sync
        """
        pass

    def pre_sync(self, graph: Graph, dry_run: bool) -> None:
        """Hook called before syncing begins.

        Override to perform setup (e.g., authenticate, validate config).

        Args:
            graph: The graph being synced
            dry_run: Whether this is a dry run
        """
        pass

    def post_sync(self, graph: Graph, result: SyncResult, dry_run: bool) -> None:
        """Hook called after syncing completes.

        Override to perform cleanup or reporting.

        Args:
            graph: The graph that was synced
            result: Sync results
            dry_run: Whether this was a dry run
        """
        pass

    def on_error(self, item: Any, error: Exception) -> None:
        """Hook called when an error occurs.

        Override to implement custom error handling.

        Args:
            item: The item that failed
            error: The exception
        """
        pass

    def get_vendor_id(self, urn: str) -> str | None:
        """Get cached vendor ID for a system URN.

        Args:
            urn: System URN

        Returns:
            Vendor ID if cached, None otherwise
        """
        return self._id_cache.get(urn)

    def cache_vendor_id(self, urn: str, vendor_id: str) -> None:
        """Cache a vendor ID for a system URN.

        Args:
            urn: System URN
            vendor_id: Vendor's system ID
        """
        self._id_cache.set(urn, vendor_id)
