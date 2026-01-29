"""Tests for export/import functionality."""

from scp_sdk import (
    SCPManifest,
    System,
    Ownership,
    Contact,
    Capability,
    Dependency,
    Classification,
    export_graph_json,
    import_graph_json,
)


def test_export_simple_manifest():
    """Test exporting a simple manifest to JSON."""
    manifest = SCPManifest(
        scp="0.1.0",
        system=System(urn="urn:scp:test:service-a", name="Service A"),
    )

    result = export_graph_json([manifest])

    assert "nodes" in result
    assert "edges" in result
    assert "meta" in result
    assert result["meta"]["systems_count"] == 1
    assert len(result["nodes"]) == 1
    assert result["nodes"][0]["id"] == "urn:scp:test:service-a"
    assert result["nodes"][0]["name"] == "Service A"


def test_export_with_classification():
    """Test exporting manifest with classification."""
    manifest = SCPManifest(
        scp="0.1.0",
        system=System(
            urn="urn:scp:test:service-a",
            name="Service A",
            classification=Classification(tier=1, domain="payments"),
        ),
    )

    result = export_graph_json([manifest])

    node = result["nodes"][0]
    assert node["tier"] == 1
    assert node["domain"] == "payments"


def test_export_with_ownership():
    """Test exporting manifest with ownership."""
    manifest = SCPManifest(
        scp="0.1.0",
        system=System(urn="urn:scp:test:service-a", name="Service A"),
        ownership=Ownership(
            team="platform",
            contacts=[Contact(type="email", ref="team@example.com")],
            escalation=["lead", "manager"],
        ),
    )

    result = export_graph_json([manifest])

    node = result["nodes"][0]
    assert node["team"] == "platform"
    assert len(node["contacts"]) == 1
    assert node["contacts"][0]["type"] == "email"
    assert node["escalation"] == ["lead", "manager"]


def test_export_with_dependencies():
    """Test exporting manifest with dependencies."""
    manifest = SCPManifest(
        scp="0.1.0",
        system=System(urn="urn:scp:test:service-a", name="Service A"),
        depends=[
            Dependency(
                system="urn:scp:test:service-b",
                capability="api",
                type="rest",
                criticality="required",
                failure_mode="circuit-break",
            )
        ],
    )

    result = export_graph_json([manifest])

    # Should have 2 nodes (service-a + stub for service-b)
    assert len(result["nodes"]) == 2
    systems = [n for n in result["nodes"] if n["type"] == "System"]
    assert len(systems) == 2

    # Check stub node
    stub = next(n for n in systems if n.get("stub"))
    assert stub["id"] == "urn:scp:test:service-b"

    # Check dependency edge
    assert len(result["edges"]) == 1
    edge = result["edges"][0]
    assert edge["from"] == "urn:scp:test:service-a"
    assert edge["to"] == "urn:scp:test:service-b"
    assert edge["type"] == "DEPENDS_ON"
    assert edge["capability"] == "api"


def test_export_with_capabilities():
    """Test exporting manifest with capabilities."""
    manifest = SCPManifest(
        scp="0.1.0",
        system=System(urn="urn:scp:test:service-a", name="Service A"),
        provides=[Capability(capability="user-api", type="rest")],
    )

    result = export_graph_json([manifest])

    # Should have 2 nodes (system + capability)
    assert len(result["nodes"]) == 2
    cap = next(n for n in result["nodes"] if n["type"] == "Capability")
    assert cap["name"] == "user-api"
    assert cap["capability_type"] == "rest"

    # Check PROVIDES edge
    provides_edges = [e for e in result["edges"] if e["type"] == "PROVIDES"]
    assert len(provides_edges) == 1


def test_roundtrip_with_security_extension():
    """Test that x-security extension survives export/import roundtrip."""
    from scp_sdk import SecurityExtension

    manifest = SCPManifest(
        scp="0.1.0",
        system=System(urn="urn:scp:test:security-tool", name="Security Tool"),
        provides=[
            Capability(
                capability="threat-detection",
                type="rest",
                **{
                    "x-security": SecurityExtension(
                        actuator_profile="edr",
                        actions=["query", "contain"],
                        targets=["device", "process"],
                    )
                },
            )
        ],
    )

    # Export then import
    exported = export_graph_json([manifest])
    imported = import_graph_json(exported)

    # Verify x-security was preserved
    assert len(imported) == 1
    assert imported[0].provides is not None
    assert len(imported[0].provides) == 1
    cap = imported[0].provides[0]
    assert cap.x_security is not None
    assert cap.x_security.actuator_profile == "edr"
    assert cap.x_security.actions == ["query", "contain"]
    assert cap.x_security.targets == ["device", "process"]


def test_export_replaces_stubs():
    """Test that real nodes replace stub nodes."""
    manifest_a = SCPManifest(
        scp="0.1.0",
        system=System(urn="urn:scp:test:service-a", name="Service A"),
        depends=[
            Dependency(
                system="urn:scp:test:service-b", type="rest", criticality="required"
            )
        ],
    )

    manifest_b = SCPManifest(
        scp="0.1.0",
        system=System(
            urn="urn:scp:test:service-b",
            name="Service B Real Name",
            classification=Classification(tier=2),
        ),
    )

    result = export_graph_json([manifest_a, manifest_b])

    # Service B should be real, not stub
    service_b = next(n for n in result["nodes"] if n["id"] == "urn:scp:test:service-b")
    assert not service_b.get("stub")
    assert service_b["name"] == "Service B Real Name"
    assert service_b["tier"] == 2


def test_import_simple_graph():
    """Test importing a simple graph."""
    data = {
        "nodes": [
            {
                "id": "urn:scp:test:service-a",
                "type": "System",
                "name": "Service A",
                "tier": None,
                "domain": None,
                "team": None,
                "contacts": [],
                "escalation": [],
            }
        ],
        "edges": [],
    }

    manifests = import_graph_json(data)

    assert len(manifests) == 1
    assert manifests[0].system.urn == "urn:scp:test:service-a"
    assert manifests[0].system.name == "Service A"


def test_import_with_classification():
    """Test importing graph with classification."""
    data = {
        "nodes": [
            {
                "id": "urn:scp:test:service-a",
                "type": "System",
                "name": "Service A",
                "tier": 1,
                "domain": "payments",
            }
        ],
        "edges": [],
    }

    manifests = import_graph_json(data)

    assert manifests[0].system.classification is not None
    assert manifests[0].system.classification.tier == 1
    assert manifests[0].system.classification.domain == "payments"


def test_import_with_ownership():
    """Test importing graph with ownership."""
    data = {
        "nodes": [
            {
                "id": "urn:scp:test:service-a",
                "type": "System",
                "name": "Service A",
                "team": "platform",
                "contacts": [{"type": "email", "ref": "team@example.com"}],
                "escalation": ["lead"],
            }
        ],
        "edges": [],
    }

    manifests = import_graph_json(data)

    assert manifests[0].ownership is not None
    assert manifests[0].ownership.team == "platform"
    assert len(manifests[0].ownership.contacts) == 1
    assert manifests[0].ownership.contacts[0].type == "email"


def test_import_skips_stubs():
    """Test that stub nodes are not imported."""
    data = {
        "nodes": [
            {
                "id": "urn:scp:test:service-a",
                "type": "System",
                "name": "Service A",
                "stub": False,
            },
            {
                "id": "urn:scp:test:external",
                "type": "System",
                "name": "External",
                "stub": True,  # Stub, should be skipped
            },
        ],
        "edges": [],
    }

    manifests = import_graph_json(data)

    # Only service-a should be imported
    assert len(manifests) == 1
    assert manifests[0].system.urn == "urn:scp:test:service-a"


def test_roundtrip_preservation():
    """Test that export->import preserves data."""
    original = SCPManifest(
        scp="0.1.0",
        system=System(
            urn="urn:scp:test:service-a",
            name="Service A",
            classification=Classification(tier=2, domain="payments"),
        ),
        ownership=Ownership(
            team="platform-team",
            contacts=[Contact(type="email", ref="team@example.com")],
        ),
    )

    # Export then import
    exported = export_graph_json([original])
    imported = import_graph_json(exported)

    # Verify preservation
    assert len(imported) == 1
    manifest = imported[0]
    assert manifest.system.urn == original.system.urn
    assert manifest.system.name == original.system.name
    assert manifest.system.classification.tier == original.system.classification.tier
    assert manifest.ownership.team == original.ownership.team
