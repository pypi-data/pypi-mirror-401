"""Export and import functions for SCP graph data.

This module provides vendor-neutral export/import for the unified JSON graph format,
enabling integration interchange and transformation workflows.
"""

from typing import Any

from .models import (
    SCPManifest,
    System,
    Classification,
    Ownership,
    Contact,
    Capability,
    Dependency,
    SecurityExtension,
)


def export_graph_json(manifests: list[SCPManifest]) -> dict[str, Any]:
    """Export manifests to unified JSON graph format.

    Creates a standardized graph representation with nodes and edges that
    can be consumed by integrations, visualizations, and analysis tools.

    System nodes are deduplicated (last wins), and stub nodes are created
    for external dependencies.

    Args:
        manifests: List of SCP manifests to export

    Returns:
        Dictionary with 'nodes', 'edges', and 'meta' keys:
            - nodes: List of system and capability nodes
            - edges: List of dependency and provides edges
            - meta: Counts and statistics

    Example:
        >>> from scp_sdk import Manifest, export_graph_json
        >>> manifests = [Manifest.from_file("scp.yaml")]
        >>> graph_data = export_graph_json(manifests)
        >>> print(graph_data["meta"]["systems_count"])
    """
    nodes: list[dict] = []
    edges: list[dict] = []
    system_nodes: dict[str, dict] = {}  # Track by URN for stub replacement

    for manifest in manifests:
        urn = manifest.system.urn

        # Add or update system node (replaces stub if exists)
        system_nodes[urn] = {
            "id": urn,
            "type": "System",
            "name": manifest.system.name,
            "tier": manifest.system.classification.tier
            if manifest.system.classification
            else None,
            "domain": manifest.system.classification.domain
            if manifest.system.classification
            else None,
            "team": manifest.ownership.team if manifest.ownership else None,
            "contacts": [
                {"type": c.type, "ref": c.ref} for c in manifest.ownership.contacts
            ]
            if manifest.ownership and manifest.ownership.contacts
            else [],
            "escalation": manifest.ownership.escalation if manifest.ownership else [],
        }

        # Add dependency edges (create stub only if not already known)
        if manifest.depends:
            for dep in manifest.depends:
                # Create stub node for dependency target if not seen
                if dep.system not in system_nodes:
                    system_nodes[dep.system] = {
                        "id": dep.system,
                        "type": "System",
                        "name": dep.system.split(":")[-1],  # Extract name from URN
                        "stub": True,
                    }

                edges.append(
                    {
                        "from": urn,
                        "to": dep.system,
                        "type": "DEPENDS_ON",
                        "capability": dep.capability,
                        "criticality": dep.criticality,
                        "failure_mode": dep.failure_mode,
                    }
                )

        # Add capability nodes and PROVIDES edges
        if manifest.provides:
            for cap in manifest.provides:
                cap_id = f"{urn}:{cap.capability}"
                cap_node: dict[str, Any] = {
                    "id": cap_id,
                    "type": "Capability",
                    "name": cap.capability,
                    "capability_type": cap.type,
                }
                # Include security extension if present
                if cap.x_security:
                    cap_node["x_security"] = {
                        "actuator_profile": cap.x_security.actuator_profile,
                        "actions": cap.x_security.actions,
                        "targets": cap.x_security.targets,
                    }
                nodes.append(cap_node)
                edges.append(
                    {
                        "from": urn,
                        "to": cap_id,
                        "type": "PROVIDES",
                    }
                )

    # Combine system nodes (from dict) with capability nodes (from list)
    all_nodes = list(system_nodes.values()) + nodes

    return {
        "nodes": all_nodes,
        "edges": edges,
        "meta": {
            "systems_count": len(system_nodes),
            "capabilities_count": len(nodes),
            "dependencies_count": len([e for e in edges if e["type"] == "DEPENDS_ON"]),
        },
    }


def import_graph_json(data: dict[str, Any]) -> list[SCPManifest]:
    """Import manifests from unified JSON graph format.

    Reconstructs SCPManifest objects from the export_graph_json() format,
    enabling transformation workflows without re-scanning source manifests.

    Stub nodes (external dependencies) are ignored during reconstruction.

    Args:
        data: Dictionary from export_graph_json() output

    Returns:
        List of reconstructed SCP manifests

    Raises:
        ValueError: If data format is invalid

    Example:
        >>> import json
        >>> with open("graph.json") as f:
        >>>     data = json.load(f)
        >>> manifests = import_graph_json(data)
        >>> print(len(manifests))
    """
    manifests: list[SCPManifest] = []
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    # Build lookup maps
    system_nodes = {
        n["id"]: n for n in nodes if n.get("type") == "System" and not n.get("stub")
    }
    capability_nodes = {n["id"]: n for n in nodes if n.get("type") == "Capability"}

    # Group edges by source system
    provides_by_system: dict[str, list[dict]] = {}
    depends_by_system: dict[str, list[dict]] = {}

    for edge in edges:
        if edge["type"] == "PROVIDES":
            provides_by_system.setdefault(edge["from"], []).append(edge)
        elif edge["type"] == "DEPENDS_ON":
            depends_by_system.setdefault(edge["from"], []).append(edge)

    # Reconstruct manifests
    for urn, node in system_nodes.items():
        # Build classification
        classification = None
        if node.get("tier") or node.get("domain"):
            classification = Classification(
                tier=node.get("tier"),
                domain=node.get("domain"),
            )

        # Build ownership
        ownership = None
        if node.get("team"):
            contacts = []
            if node.get("contacts"):
                for c in node["contacts"]:
                    contacts.append(Contact(type=c["type"], ref=c["ref"]))

            ownership = Ownership(
                team=node["team"],
                contacts=contacts if contacts else None,
                escalation=node.get("escalation"),
            )

        # Build capabilities
        provides = []
        for edge in provides_by_system.get(urn, []):
            cap_node = capability_nodes.get(edge["to"])
            if cap_node:
                # Check for security extension in capability node
                x_security = None
                if cap_node.get("x_security"):
                    sec = cap_node["x_security"]
                    x_security = SecurityExtension(
                        actuator_profile=sec.get("actuator_profile"),
                        actions=sec.get("actions", []),
                        targets=sec.get("targets", []),
                    )

                cap_data = {
                    "capability": cap_node["name"],
                    "type": cap_node.get("capability_type", "rest"),
                }
                if x_security:
                    cap_data["x-security"] = x_security
                provides.append(Capability.model_validate(cap_data))

        # Build dependencies
        depends = []
        for edge in depends_by_system.get(urn, []):
            depends.append(
                Dependency(
                    system=edge["to"],
                    capability=edge.get("capability"),
                    type="rest",  # Default, as type isn't stored in edge
                    criticality=edge.get("criticality", "required"),
                    failure_mode=edge.get("failure_mode"),
                )
            )

        manifest = SCPManifest(
            scp="0.1.0",
            system=System(
                urn=urn,
                name=node["name"],
                classification=classification,
            ),
            ownership=ownership,
            provides=provides if provides else None,
            depends=depends if depends else None,
        )
        manifests.append(manifest)

    return manifests
