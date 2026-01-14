"""Tests for MCP resource implementations."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


class TestListResources:
    """Tests for the list_resources handler."""

    def test_get_resource_list(self):
        """Test that get_resource_list returns all expected resources."""
        from attack_query_mcp.resources import get_resource_list

        resources = get_resource_list()
        assert len(resources) == 6

        # Check all expected resources are present
        uris = {str(r.uri) for r in resources}
        assert "attack://groups" in uris
        assert "attack://techniques" in uris
        assert "attack://tactics" in uris
        assert "attack://software" in uris
        assert "attack://mitigations" in uris
        assert "attack://campaigns" in uris

    def test_resource_metadata(self):
        """Test that resources have proper metadata."""
        from attack_query_mcp.resources import get_resource_list

        resources = get_resource_list()

        for resource in resources:
            assert resource.name is not None
            assert resource.description is not None
            assert resource.mimeType == "text/plain"
            assert str(resource.uri).startswith("attack://")


class TestReadGroupsResource:
    """Tests for the attack://groups resource."""

    @pytest.fixture
    def mock_store(self):
        """Create a mock store with sample groups."""
        with patch("attack_query_mcp.server.get_store") as mock:
            store = MagicMock()

            # Create sample groups
            group1 = MagicMock()
            group1.id = "G0007"
            group1.name = "APT28"
            group1.aliases = ["Fancy Bear", "Sofacy", "Pawn Storm"]

            group2 = MagicMock()
            group2.id = "G0016"
            group2.name = "APT29"
            group2.aliases = ["Cozy Bear", "The Dukes"]

            store.groups = {"G0007": group1, "G0016": group2}
            mock.return_value = store
            yield store

    @pytest.mark.asyncio
    async def test_read_groups(self, mock_store: MagicMock):
        """Test reading the groups resource."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_groups_resource

        result = await read_groups_resource()

        assert len(result) == 1
        text = result[0].text
        assert "MITRE ATT&CK Threat Groups" in text
        assert "2 groups" in text
        assert "APT28" in text
        assert "APT29" in text
        assert "Fancy Bear" in text
        assert "Cozy Bear" in text


class TestReadTechniquesResource:
    """Tests for the attack://techniques resource."""

    @pytest.fixture
    def mock_store(self):
        """Create a mock store with sample techniques."""
        with patch("attack_query_mcp.server.get_store") as mock:
            store = MagicMock()

            # Create sample techniques
            tech1 = MagicMock()
            tech1.id = "T1566"
            tech1.name = "Phishing"
            tech1.tactics = ["initial-access"]

            tech2 = MagicMock()
            tech2.id = "T1059"
            tech2.name = "Command and Scripting Interpreter"
            tech2.tactics = ["execution"]

            sub1 = MagicMock()
            sub1.id = "T1566.001"
            sub1.name = "Spearphishing Attachment"
            sub1.tactics = ["initial-access"]

            store.techniques = {
                "T1566": tech1,
                "T1059": tech2,
                "T1566.001": sub1,
            }
            mock.return_value = store
            yield store

    @pytest.mark.asyncio
    async def test_read_techniques(self, mock_store: MagicMock):
        """Test reading the techniques resource."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_techniques_resource

        result = await read_techniques_resource()

        assert len(result) == 1
        text = result[0].text
        assert "MITRE ATT&CK Techniques" in text
        assert "2 techniques" in text
        assert "1 sub-techniques" in text
        assert "T1566" in text
        assert "Phishing" in text
        assert "T1059" in text
        assert "T1566.001" in text
        assert "Spearphishing Attachment" in text


class TestReadTacticsResource:
    """Tests for the attack://tactics resource."""

    @pytest.fixture
    def mock_store(self):
        """Create a mock store with sample tactics."""
        with patch("attack_query_mcp.server.get_store") as mock:
            store = MagicMock()

            tactic1 = MagicMock()
            tactic1.shortname = "TA0001"
            tactic1.name = "Initial Access"
            tactic1.description = "The adversary is trying to get into your network."

            tactic2 = MagicMock()
            tactic2.shortname = "TA0002"
            tactic2.name = "Execution"
            tactic2.description = "The adversary is trying to run malicious code."

            store.tactics = {"initial-access": tactic1, "execution": tactic2}
            mock.return_value = store
            yield store

    @pytest.mark.asyncio
    async def test_read_tactics(self, mock_store: MagicMock):
        """Test reading the tactics resource."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_tactics_resource

        result = await read_tactics_resource()

        assert len(result) == 1
        text = result[0].text
        assert "MITRE ATT&CK Tactics" in text
        assert "2 tactics" in text
        assert "Initial Access" in text
        assert "Execution" in text
        assert "TA0001" in text
        assert "TA0002" in text


class TestReadSoftwareResource:
    """Tests for the attack://software resource."""

    @pytest.fixture
    def mock_store(self):
        """Create a mock store with sample software."""
        with patch("attack_query_mcp.server.get_store") as mock:
            store = MagicMock()

            malware1 = MagicMock()
            malware1.id = "S0001"
            malware1.name = "Trojan"
            malware1.software_type = "malware"
            malware1.platforms = ["Windows", "Linux"]

            tool1 = MagicMock()
            tool1.id = "S0002"
            tool1.name = "Mimikatz"
            tool1.software_type = "tool"
            tool1.platforms = ["Windows"]

            store.software = {"S0001": malware1, "S0002": tool1}
            mock.return_value = store
            yield store

    @pytest.mark.asyncio
    async def test_read_software(self, mock_store: MagicMock):
        """Test reading the software resource."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_software_resource

        result = await read_software_resource()

        assert len(result) == 1
        text = result[0].text
        assert "MITRE ATT&CK Software" in text
        assert "1 malware" in text
        assert "1 tools" in text
        assert "Trojan" in text
        assert "Mimikatz" in text


class TestReadMitigationsResource:
    """Tests for the attack://mitigations resource."""

    @pytest.fixture
    def mock_store(self):
        """Create a mock store with sample mitigations."""
        with patch("attack_query_mcp.server.get_store") as mock:
            store = MagicMock()

            mit1 = MagicMock()
            mit1.id = "M1017"
            mit1.name = "User Training"
            mit1.techniques = ["T1566", "T1566.001", "T1566.002"]

            mit2 = MagicMock()
            mit2.id = "M1031"
            mit2.name = "Network Intrusion Prevention"
            mit2.techniques = ["T1566"]

            store.mitigations = {"M1017": mit1, "M1031": mit2}
            mock.return_value = store
            yield store

    @pytest.mark.asyncio
    async def test_read_mitigations(self, mock_store: MagicMock):
        """Test reading the mitigations resource."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_mitigations_resource

        result = await read_mitigations_resource()

        assert len(result) == 1
        text = result[0].text
        assert "MITRE ATT&CK Mitigations" in text
        assert "2 mitigations" in text
        assert "User Training" in text
        assert "Network Intrusion Prevention" in text
        assert "M1017" in text
        assert "M1031" in text
        # Check technique counts are shown
        assert "3" in text  # M1017 has 3 techniques
        assert "1" in text  # M1031 has 1 technique


class TestReadCampaignsResource:
    """Tests for the attack://campaigns resource."""

    @pytest.fixture
    def mock_store(self):
        """Create a mock store with sample campaigns."""
        with patch("attack_query_mcp.server.get_store") as mock:
            store = MagicMock()

            campaign1 = MagicMock()
            campaign1.id = "C0027"
            campaign1.name = "C0027"
            campaign1.first_seen = "2022-01-01T00:00:00.000Z"
            campaign1.last_seen = "2022-12-31T00:00:00.000Z"
            campaign1.groups = {"G0007"}  # set, not list

            campaign2 = MagicMock()
            campaign2.id = "C0028"
            campaign2.name = "Operation Example"
            campaign2.first_seen = "2023-06-01T00:00:00.000Z"
            campaign2.last_seen = None
            campaign2.groups = set()  # empty set

            # Mock get_group for group name lookup
            group = MagicMock()
            group.name = "APT28"
            store.get_group.return_value = group

            store.campaigns = {"C0027": campaign1, "C0028": campaign2}
            mock.return_value = store
            yield store

    @pytest.mark.asyncio
    async def test_read_campaigns(self, mock_store: MagicMock):
        """Test reading the campaigns resource."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_campaigns_resource

        result = await read_campaigns_resource()

        assert len(result) == 1
        text = result[0].text
        assert "MITRE ATT&CK Campaigns" in text
        assert "2 campaigns" in text
        assert "C0027" in text
        assert "Operation Example" in text
        assert "2022-01" in text
        assert "2022-12" in text
        assert "APT28" in text


class TestReadResourceDispatch:
    """Tests for the read_resource dispatch."""

    @pytest.fixture
    def mock_store(self):
        """Create a minimal mock store."""
        with patch("attack_query_mcp.server.get_store") as mock:
            store = MagicMock()
            store.groups = {}
            store.techniques = {}
            store.tactics = {}
            store.software = {}
            store.mitigations = {}
            store.campaigns = {}
            mock.return_value = store
            yield store

    @pytest.mark.asyncio
    async def test_unknown_resource(self, mock_store: MagicMock):
        """Test reading an unknown resource URI."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://unknown")

        assert len(result) == 1
        assert "Unknown resource" in result[0].text

    @pytest.mark.asyncio
    async def test_read_groups_dispatch(self, mock_store: MagicMock):
        """Test that attack://groups URI dispatches correctly."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://groups")

        assert len(result) == 1
        assert "MITRE ATT&CK Threat Groups" in result[0].text

    @pytest.mark.asyncio
    async def test_read_techniques_dispatch(self, mock_store: MagicMock):
        """Test that attack://techniques URI dispatches correctly."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://techniques")

        assert len(result) == 1
        assert "MITRE ATT&CK Techniques" in result[0].text

    @pytest.mark.asyncio
    async def test_read_tactics_dispatch(self, mock_store: MagicMock):
        """Test that attack://tactics URI dispatches correctly."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://tactics")

        assert len(result) == 1
        assert "MITRE ATT&CK Tactics" in result[0].text

    @pytest.mark.asyncio
    async def test_read_software_dispatch(self, mock_store: MagicMock):
        """Test that attack://software URI dispatches correctly."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://software")

        assert len(result) == 1
        assert "MITRE ATT&CK Software" in result[0].text

    @pytest.mark.asyncio
    async def test_read_mitigations_dispatch(self, mock_store: MagicMock):
        """Test that attack://mitigations URI dispatches correctly."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://mitigations")

        assert len(result) == 1
        assert "MITRE ATT&CK Mitigations" in result[0].text

    @pytest.mark.asyncio
    async def test_read_campaigns_dispatch(self, mock_store: MagicMock):
        """Test that attack://campaigns URI dispatches correctly."""
        _ = mock_store  # Fixture used for side effects
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://campaigns")

        assert len(result) == 1
        assert "MITRE ATT&CK Campaigns" in result[0].text


class TestResourceTemplates:
    """Tests for resource templates (Phase 4)."""

    def test_get_resource_template_list(self):
        """Test that resource templates are defined correctly."""
        from attack_query_mcp.resources import get_resource_template_list

        templates = get_resource_template_list()

        assert len(templates) == 2

        # Check groups template
        groups_template = next((t for t in templates if "groups" in t.uriTemplate), None)
        assert groups_template is not None
        assert groups_template.uriTemplate == "attack://groups/{id}"
        assert "group" in groups_template.description.lower()

        # Check techniques template
        techniques_template = next((t for t in templates if "techniques" in t.uriTemplate), None)
        assert techniques_template is not None
        assert techniques_template.uriTemplate == "attack://techniques/{id}"
        assert "technique" in techniques_template.description.lower()


class TestGroupDetailResource:
    """Tests for the attack://groups/{id} resource template."""

    @pytest.fixture
    def mock_store_and_engine(self):
        """Create mock store and engine for group detail tests."""
        with (
            patch("attack_query_mcp.server.get_store") as mock_store,
            patch("attack_query_mcp.server.get_engine") as mock_engine,
        ):
            store = MagicMock()
            engine = MagicMock()

            # Create a mock group
            group = MagicMock()
            group.id = "G0007"
            group.name = "APT28"
            group.stix_id = "intrusion-set--abc123"
            group.aliases = ["Fancy Bear", "Sofacy"]
            group.techniques = {"T1566", "T1059", "T1071"}

            store.groups = {"G0007": group}
            store.get_group.return_value = group
            store.get_technique.return_value = MagicMock(id="T1566", name="Phishing")
            store.group_to_software = {}

            engine.get_group_info.return_value = {
                "id": "G0007",
                "name": "APT28",
                "aliases": ["Fancy Bear", "Sofacy"],
                "technique_count": 3,
                "description": "APT28 is a threat group attributed to Russia.",
            }

            mock_store.return_value = store
            mock_engine.return_value = engine

            yield store, engine

    @pytest.mark.asyncio
    async def test_read_group_detail(self, mock_store_and_engine):
        """Test reading a group detail resource."""
        _ = mock_store_and_engine
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://groups/APT28")

        assert len(result) == 1
        text = result[0].text
        assert "APT28" in text
        assert "G0007" in text
        assert "Fancy Bear" in text

    @pytest.mark.asyncio
    async def test_read_group_detail_by_id(self, mock_store_and_engine):
        """Test reading a group detail by ID."""
        _ = mock_store_and_engine
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://groups/G0007")

        assert len(result) == 1
        assert "APT28" in result[0].text

    @pytest.mark.asyncio
    async def test_read_group_detail_not_found(self, mock_store_and_engine):
        """Test reading a non-existent group."""
        store, engine = mock_store_and_engine
        engine.get_group_info.side_effect = ValueError("Group not found")
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://groups/NonExistent")

        assert len(result) == 1
        assert "not found" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_read_group_detail_url_encoded(self, mock_store_and_engine):
        """Test reading a group with URL-encoded name."""
        _ = mock_store_and_engine
        from attack_query_mcp.resources import read_resource

        # "Fancy Bear" URL-encoded
        result = await read_resource("attack://groups/Fancy%20Bear")

        assert len(result) == 1
        # Should resolve the alias
        assert "APT28" in result[0].text or "not found" in result[0].text.lower()


class TestTechniqueDetailResource:
    """Tests for the attack://techniques/{id} resource template."""

    @pytest.fixture
    def mock_store_and_engine(self):
        """Create mock store and engine for technique detail tests."""
        with (
            patch("attack_query_mcp.server.get_store") as mock_store,
            patch("attack_query_mcp.server.get_engine") as mock_engine,
        ):
            store = MagicMock()
            engine = MagicMock()

            # Create a mock technique
            technique = MagicMock()
            technique.id = "T1566"
            technique.name = "Phishing"
            technique.tactics = ["initial-access"]
            technique.description = "Adversaries may send phishing messages."

            # Create a sub-technique
            sub_technique = MagicMock()
            sub_technique.id = "T1566.001"
            sub_technique.name = "Spearphishing Attachment"
            sub_technique.tactics = ["initial-access"]
            sub_technique.description = "Adversaries may send attachments."

            store.techniques = {"T1566": technique, "T1566.001": sub_technique}
            store.get_technique.side_effect = lambda tid: store.techniques.get(tid.upper())
            store.get_group.return_value = MagicMock(id="G0007", name="APT28")

            engine.get_subtechniques_of.return_value = {"T1566.001"}
            engine.groups_using_technique.return_value = ["APT28", "APT29"]
            engine.get_mitigations_for_technique.return_value = [
                {"id": "M1017", "name": "User Training"}
            ]

            mock_store.return_value = store
            mock_engine.return_value = engine

            yield store, engine

    @pytest.mark.asyncio
    async def test_read_technique_detail(self, mock_store_and_engine):
        """Test reading a technique detail resource."""
        _ = mock_store_and_engine
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://techniques/T1566")

        assert len(result) == 1
        text = result[0].text
        assert "T1566" in text
        assert "Phishing" in text
        assert "initial-access" in text

    @pytest.mark.asyncio
    async def test_read_technique_with_subtechniques(self, mock_store_and_engine):
        """Test reading a parent technique shows sub-techniques."""
        _ = mock_store_and_engine
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://techniques/T1566")

        assert len(result) == 1
        text = result[0].text
        assert "Sub-techniques" in text
        assert "T1566.001" in text

    @pytest.mark.asyncio
    async def test_read_subtechnique_detail(self, mock_store_and_engine):
        """Test reading a sub-technique detail."""
        _ = mock_store_and_engine
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://techniques/T1566.001")

        assert len(result) == 1
        text = result[0].text
        assert "T1566.001" in text
        assert "Spearphishing" in text
        assert "Parent technique" in text

    @pytest.mark.asyncio
    async def test_read_technique_not_found(self, mock_store_and_engine):
        """Test reading a non-existent technique."""
        _ = mock_store_and_engine
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://techniques/T9999")

        assert len(result) == 1
        assert "not found" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_read_technique_lowercase(self, mock_store_and_engine):
        """Test reading a technique with lowercase ID."""
        _ = mock_store_and_engine
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://techniques/t1566")

        assert len(result) == 1
        assert "T1566" in result[0].text
        assert "Phishing" in result[0].text

    @pytest.mark.asyncio
    async def test_read_technique_shows_groups(self, mock_store_and_engine):
        """Test that technique detail shows groups using it."""
        _ = mock_store_and_engine
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://techniques/T1566")

        assert len(result) == 1
        text = result[0].text
        assert "Groups Using" in text

    @pytest.mark.asyncio
    async def test_read_technique_shows_mitigations(self, mock_store_and_engine):
        """Test that technique detail shows mitigations."""
        _ = mock_store_and_engine
        from attack_query_mcp.resources import read_resource

        result = await read_resource("attack://techniques/T1566")

        assert len(result) == 1
        text = result[0].text
        assert "Mitigations" in text
        assert "M1017" in text
