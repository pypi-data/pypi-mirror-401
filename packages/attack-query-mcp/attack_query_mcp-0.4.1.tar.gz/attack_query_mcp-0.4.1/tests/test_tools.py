"""Tests for MCP tool implementations."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest


class TestQueryAttackTool:
    """Tests for the query_attack tool."""

    @pytest.fixture
    def mock_parser(self):
        """Create a mock parser."""
        with patch("attack_query_mcp.server.get_parser") as mock:
            parser = MagicMock()
            mock.return_value = parser
            yield parser

    @pytest.mark.asyncio
    async def test_simple_query(self, mock_parser: MagicMock):
        """Test a simple techniques query."""
        from attack_query_mcp.tools import handle_query_attack

        mock_parser.parse_and_execute.return_value = {
            "query_type": "techniques_by_groups",
            "groups": ["APT28"],
            "techniques": [
                {"id": "T1566", "name": "Phishing"},
                {"id": "T1059", "name": "Command and Scripting Interpreter"},
            ],
            "count": 2,
        }

        result = await handle_query_attack({"query": "techniques used by APT28"})

        assert len(result) == 1
        assert "T1566" in result[0].text
        assert "Phishing" in result[0].text
        assert "T1059" in result[0].text
        mock_parser.parse_and_execute.assert_called_once_with("techniques used by APT28")

    @pytest.mark.asyncio
    async def test_error_handling(self, mock_parser: MagicMock):
        """Test error response from parser."""
        from attack_query_mcp.tools import handle_query_attack

        mock_parser.parse_and_execute.return_value = {"error": "Unknown group: APT999"}

        result = await handle_query_attack({"query": "techniques used by APT999"})

        assert len(result) == 1
        assert "Error:" in result[0].text
        assert "APT999" in result[0].text

    @pytest.mark.asyncio
    async def test_empty_query(self):
        """Test empty query returns error."""
        from attack_query_mcp.tools import handle_query_attack

        result = await handle_query_attack({"query": ""})

        assert len(result) == 1
        assert "Error:" in result[0].text
        assert "required" in result[0].text

    @pytest.mark.asyncio
    async def test_missing_query(self):
        """Test missing query returns error."""
        from attack_query_mcp.tools import handle_query_attack

        result = await handle_query_attack({})

        assert len(result) == 1
        assert "Error:" in result[0].text


class TestGetTechniqueTool:
    """Tests for the get_technique tool."""

    @pytest.fixture
    def mock_store(self):
        """Create a mock store."""
        with patch("attack_query_mcp.server.get_store") as mock:
            store = MagicMock()
            mock.return_value = store
            yield store

    @pytest.fixture
    def mock_engine(self):
        """Create a mock engine."""
        with patch("attack_query_mcp.server.get_engine") as mock:
            engine = MagicMock()
            mock.return_value = engine
            yield engine

    @pytest.mark.asyncio
    async def test_get_technique(self, mock_store: MagicMock):
        """Test getting technique details."""
        from attack_query_mcp.tools import handle_get_technique

        # Create a mock technique
        technique = MagicMock()
        technique.id = "T1566"
        technique.name = "Phishing"
        technique.description = "Adversaries may send phishing messages to gain access."
        technique.tactics = ["initial-access"]

        mock_store.get_technique.return_value = technique

        result = await handle_get_technique({"technique_id": "T1566"})

        assert len(result) == 1
        assert "T1566" in result[0].text
        assert "Phishing" in result[0].text
        assert "initial-access" in result[0].text
        mock_store.get_technique.assert_called_once_with("T1566")

    @pytest.mark.asyncio
    async def test_get_technique_not_found(self, mock_store: MagicMock):
        """Test technique not found."""
        from attack_query_mcp.tools import handle_get_technique

        mock_store.get_technique.return_value = None

        result = await handle_get_technique({"technique_id": "T9999"})

        assert len(result) == 1
        assert "Error:" in result[0].text
        assert "T9999" in result[0].text

    @pytest.mark.asyncio
    async def test_get_technique_with_subtechniques(
        self, mock_store: MagicMock, mock_engine: MagicMock
    ):
        """Test getting technique with sub-techniques."""
        from attack_query_mcp.tools import handle_get_technique

        # Create parent technique
        parent = MagicMock()
        parent.id = "T1566"
        parent.name = "Phishing"
        parent.description = "Adversaries may send phishing messages."
        parent.tactics = ["initial-access"]

        # Create sub-technique
        subtechnique = MagicMock()
        subtechnique.id = "T1566.001"
        subtechnique.name = "Spearphishing Attachment"

        # Configure mocks
        mock_store.get_technique.side_effect = (
            lambda tid: parent if tid == "T1566" else subtechnique
        )
        mock_engine.get_subtechniques_of.return_value = {"T1566.001", "T1566.002"}

        result = await handle_get_technique(
            {"technique_id": "T1566", "include_subtechniques": True}
        )

        assert len(result) == 1
        assert "T1566" in result[0].text
        assert "Sub-techniques" in result[0].text
        assert "T1566.001" in result[0].text

    @pytest.mark.asyncio
    async def test_missing_technique_id(self):
        """Test missing technique_id returns error."""
        from attack_query_mcp.tools import handle_get_technique

        result = await handle_get_technique({})

        assert len(result) == 1
        assert "Error:" in result[0].text


class TestGetGroupTool:
    """Tests for the get_group tool."""

    @pytest.fixture
    def mock_engine(self):
        """Create a mock engine."""
        with patch("attack_query_mcp.server.get_engine") as mock:
            engine = MagicMock()
            mock.return_value = engine
            yield engine

    @pytest.fixture
    def mock_store(self):
        """Create a mock store."""
        with patch("attack_query_mcp.server.get_store") as mock:
            store = MagicMock()
            mock.return_value = store
            yield store

    @pytest.mark.asyncio
    async def test_get_group(self, mock_engine: MagicMock):
        """Test getting group details."""
        from attack_query_mcp.tools import handle_get_group

        mock_engine.get_group_info.return_value = {
            "id": "G0007",
            "name": "APT28",
            "description": "APT28 is a threat group attributed to Russia.",
            "aliases": ["Fancy Bear", "Sofacy"],
            "technique_count": 45,
            "resolved_from": None,
        }

        result = await handle_get_group({"group": "APT28"})

        assert len(result) == 1
        assert "APT28" in result[0].text
        assert "G0007" in result[0].text
        assert "Fancy Bear" in result[0].text
        assert "45" in result[0].text

    @pytest.mark.asyncio
    async def test_get_group_by_alias(self, mock_engine: MagicMock):
        """Test getting group by alias shows resolution."""
        from attack_query_mcp.tools import handle_get_group

        mock_engine.get_group_info.return_value = {
            "id": "G0007",
            "name": "APT28",
            "description": "APT28 is a threat group.",
            "aliases": ["Fancy Bear", "Sofacy"],
            "technique_count": 45,
            "resolved_from": "Fancy Bear",
        }

        result = await handle_get_group({"group": "Fancy Bear"})

        assert len(result) == 1
        assert "APT28" in result[0].text
        assert "Resolved from alias" in result[0].text
        assert "Fancy Bear" in result[0].text

    @pytest.mark.asyncio
    async def test_get_group_with_techniques(self, mock_engine: MagicMock, mock_store: MagicMock):
        """Test getting group with techniques list."""
        from attack_query_mcp.tools import handle_get_group

        mock_engine.get_group_info.return_value = {
            "id": "G0007",
            "name": "APT28",
            "description": "APT28 is a threat group.",
            "aliases": [],
            "technique_count": 2,
            "resolved_from": None,
        }

        # Create mock group with techniques
        group = MagicMock()
        group.techniques = {"T1566", "T1059"}
        mock_store.get_group.return_value = group

        # Create mock techniques
        t1566 = MagicMock()
        t1566.id = "T1566"
        t1566.name = "Phishing"

        t1059 = MagicMock()
        t1059.id = "T1059"
        t1059.name = "Command and Scripting Interpreter"

        mock_store.get_technique.side_effect = lambda tid: t1566 if tid == "T1566" else t1059

        result = await handle_get_group({"group": "APT28", "include_techniques": True})

        assert len(result) == 1
        assert "Techniques" in result[0].text
        assert "T1566" in result[0].text
        assert "Phishing" in result[0].text

    @pytest.mark.asyncio
    async def test_get_group_not_found(self, mock_engine: MagicMock):
        """Test group not found."""
        from attack_query_mcp.tools import handle_get_group

        mock_engine.get_group_info.side_effect = ValueError("Group not found: APT999")

        result = await handle_get_group({"group": "APT999"})

        assert len(result) == 1
        assert "Error:" in result[0].text
        assert "APT999" in result[0].text

    @pytest.mark.asyncio
    async def test_missing_group(self):
        """Test missing group returns error."""
        from attack_query_mcp.tools import handle_get_group

        result = await handle_get_group({})

        assert len(result) == 1
        assert "Error:" in result[0].text


class TestFormatQueryResults:
    """Tests for the format_query_results function."""

    def test_format_techniques_by_groups(self):
        """Test formatting techniques by groups."""
        from attack_query_mcp.tools import format_query_results

        results: dict[str, Any] = {
            "query_type": "techniques_by_groups",
            "groups": ["APT28"],
            "techniques": [
                {"id": "T1566", "name": "Phishing"},
                {"id": "T1059", "name": "Command and Scripting Interpreter"},
            ],
            "count": 2,
        }

        output = format_query_results(results)

        assert "APT28" in output
        assert "T1566" in output
        assert "Phishing" in output
        assert "2 techniques" in output

    def test_format_groups_using_technique(self):
        """Test formatting groups using technique."""
        from attack_query_mcp.tools import format_query_results

        results: dict[str, Any] = {
            "query_type": "groups_using_technique",
            "technique": "T1566",
            "groups": [
                {"id": "G0007", "name": "APT28"},
                {"id": "G0016", "name": "APT29"},
            ],
        }

        output = format_query_results(results)

        assert "T1566" in output
        assert "APT28" in output
        assert "APT29" in output

    def test_format_group_similarity(self):
        """Test formatting group similarity results."""
        from attack_query_mcp.tools import format_query_results

        results: dict[str, Any] = {
            "query_type": "group_similarity",
            "group1": "APT28",
            "group2": "APT29",
            "jaccard": 0.45,
            "overlap": 0.65,
            "shared_count": 25,
        }

        output = format_query_results(results)

        assert "APT28" in output
        assert "APT29" in output
        assert "45" in output  # Jaccard percentage

    def test_format_similar_groups(self):
        """Test formatting similar groups results."""
        from attack_query_mcp.tools import format_query_results

        results: dict[str, Any] = {
            "query_type": "similar_groups",
            "group": "APT28",
            "similar_groups": [
                {"name": "APT29", "jaccard": 0.45},
                {"name": "Turla", "jaccard": 0.35},
            ],
        }

        output = format_query_results(results)

        assert "APT28" in output
        assert "APT29" in output
        assert "45" in output

    def test_format_subtechniques(self):
        """Test formatting sub-techniques results."""
        from attack_query_mcp.tools import format_query_results

        results: dict[str, Any] = {
            "query_type": "subtechniques_of",
            "parent": "T1566",
            "subtechniques": [
                {"id": "T1566.001", "name": "Spearphishing Attachment"},
                {"id": "T1566.002", "name": "Spearphishing Link"},
            ],
        }

        output = format_query_results(results)

        assert "T1566" in output
        assert "T1566.001" in output
        assert "Spearphishing" in output

    def test_format_mitigations(self):
        """Test formatting mitigations results."""
        from attack_query_mcp.tools import format_query_results

        results: dict[str, Any] = {
            "query_type": "mitigations_for_technique",
            "mitigations": [
                {"id": "M1017", "name": "User Training"},
                {"id": "M1054", "name": "Software Configuration"},
            ],
        }

        output = format_query_results(results)

        assert "M1017" in output
        assert "User Training" in output

    def test_format_unknown_type(self):
        """Test formatting unknown query type."""
        from attack_query_mcp.tools import format_query_results

        results: dict[str, Any] = {
            "query_type": "unknown_type",
            "some_data": "value",
        }

        output = format_query_results(results)

        # Should return string representation
        assert "unknown_type" in output


class TestToolRegistration:
    """Tests for tool registration."""

    def test_tools_registered(self):
        """Test that tools are registered with the server."""
        from attack_query_mcp.server import app

        # The decorators should have registered handlers
        # We check that the server has the expected tool handler registered
        assert app is not None
        # Tools are registered via decorators, so the app should exist and be configured
        assert app.name == "attack-query-mcp"


# Phase 2 tool tests


class TestCompareGroupsTool:
    """Tests for the compare_groups tool."""

    @pytest.fixture
    def mock_engine(self):
        """Create a mock engine."""
        with patch("attack_query_mcp.server.get_engine") as mock:
            engine = MagicMock()
            mock.return_value = engine
            yield engine

    @pytest.fixture
    def mock_store(self):
        """Create a mock store."""
        with patch("attack_query_mcp.server.get_store") as mock:
            store = MagicMock()
            mock.return_value = store
            yield store

    @pytest.mark.asyncio
    async def test_compare_groups(self, mock_engine: MagicMock, mock_store: MagicMock):
        """Test comparing two groups."""
        from attack_query_mcp.tools import handle_compare_groups

        mock_engine.calculate_group_similarity.return_value = {
            "jaccard": 0.45,
            "overlap": 0.65,
            "cosine": 0.55,
            "group1_count": 40,
            "group2_count": 35,
            "shared_count": 20,
            "unique_to_group1": 20,
            "unique_to_group2": 15,
            "shared_techniques": {"T1566", "T1059"},
        }

        g1 = MagicMock()
        g1.name = "APT28"
        g2 = MagicMock()
        g2.name = "APT29"
        mock_store.get_group.side_effect = lambda g: g1 if "28" in g else g2

        t1 = MagicMock()
        t1.name = "Phishing"
        mock_store.get_technique.return_value = t1

        result = await handle_compare_groups({"group1": "APT28", "group2": "APT29"})

        assert len(result) == 1
        assert "APT28" in result[0].text
        assert "APT29" in result[0].text
        assert "45" in result[0].text  # Jaccard percentage

    @pytest.mark.asyncio
    async def test_compare_groups_missing_args(self):
        """Test missing arguments."""
        from attack_query_mcp.tools import handle_compare_groups

        result = await handle_compare_groups({"group1": "APT28"})
        assert "Error:" in result[0].text

        result = await handle_compare_groups({})
        assert "Error:" in result[0].text

    @pytest.mark.asyncio
    async def test_compare_groups_not_found(self, mock_engine: MagicMock):
        """Test group not found."""
        from attack_query_mcp.tools import handle_compare_groups

        mock_engine.calculate_group_similarity.side_effect = ValueError("Group not found")

        result = await handle_compare_groups({"group1": "APT28", "group2": "APT999"})
        assert "Error:" in result[0].text


class TestFindSimilarGroupsTool:
    """Tests for the find_similar_groups tool."""

    @pytest.fixture
    def mock_engine(self):
        """Create a mock engine."""
        with patch("attack_query_mcp.server.get_engine") as mock:
            engine = MagicMock()
            mock.return_value = engine
            yield engine

    @pytest.mark.asyncio
    async def test_find_similar_groups(self, mock_engine: MagicMock):
        """Test finding similar groups."""
        from attack_query_mcp.tools import handle_find_similar_groups

        mock_engine.find_similar_groups.return_value = [
            {"id": "G0016", "name": "APT29", "jaccard": 0.45, "shared_count": 20},
            {"id": "G0010", "name": "Turla", "jaccard": 0.35, "shared_count": 15},
        ]

        result = await handle_find_similar_groups({"group": "APT28"})

        assert len(result) == 1
        assert "APT28" in result[0].text
        assert "APT29" in result[0].text
        assert "45" in result[0].text

    @pytest.mark.asyncio
    async def test_find_similar_groups_with_options(self, mock_engine: MagicMock):
        """Test with threshold and limit options."""
        from attack_query_mcp.tools import handle_find_similar_groups

        mock_engine.find_similar_groups.return_value = []

        result = await handle_find_similar_groups({"group": "APT28", "threshold": 0.5, "limit": 5})

        mock_engine.find_similar_groups.assert_called_once_with("APT28", threshold=0.5, limit=5)
        assert "No groups found" in result[0].text

    @pytest.mark.asyncio
    async def test_find_similar_groups_missing_arg(self):
        """Test missing group argument."""
        from attack_query_mcp.tools import handle_find_similar_groups

        result = await handle_find_similar_groups({})
        assert "Error:" in result[0].text

    @pytest.mark.asyncio
    async def test_find_similar_groups_not_found(self, mock_engine: MagicMock):
        """Test group not found."""
        from attack_query_mcp.tools import handle_find_similar_groups

        mock_engine.find_similar_groups.side_effect = ValueError("Group not found")

        result = await handle_find_similar_groups({"group": "APT999"})
        assert "Error:" in result[0].text


class TestGetMitigationsTool:
    """Tests for the get_mitigations tool."""

    @pytest.fixture
    def mock_engine(self):
        """Create a mock engine."""
        with patch("attack_query_mcp.server.get_engine") as mock:
            engine = MagicMock()
            mock.return_value = engine
            yield engine

    @pytest.fixture
    def mock_store(self):
        """Create a mock store."""
        with patch("attack_query_mcp.server.get_store") as mock:
            store = MagicMock()
            mock.return_value = store
            yield store

    @pytest.mark.asyncio
    async def test_get_mitigations(self, mock_engine: MagicMock, mock_store: MagicMock):
        """Test getting mitigations for a technique."""
        from attack_query_mcp.tools import handle_get_mitigations

        technique = MagicMock()
        technique.name = "Phishing"
        mock_store.get_technique.return_value = technique

        mock_engine.get_mitigations_for_technique.return_value = [
            {"id": "M1017", "name": "User Training", "description": "Train users."},
            {"id": "M1054", "name": "Software Configuration", "description": "Configure."},
        ]

        result = await handle_get_mitigations({"technique_id": "T1566"})

        assert len(result) == 1
        assert "T1566" in result[0].text
        assert "M1017" in result[0].text
        assert "User Training" in result[0].text

    @pytest.mark.asyncio
    async def test_get_mitigations_none_found(self, mock_engine: MagicMock, mock_store: MagicMock):
        """Test no mitigations found."""
        from attack_query_mcp.tools import handle_get_mitigations

        technique = MagicMock()
        technique.name = "Some Technique"
        mock_store.get_technique.return_value = technique

        mock_engine.get_mitigations_for_technique.return_value = []

        result = await handle_get_mitigations({"technique_id": "T9999"})

        assert "No mitigations found" in result[0].text

    @pytest.mark.asyncio
    async def test_get_mitigations_technique_not_found(self, mock_store: MagicMock):
        """Test technique not found."""
        from attack_query_mcp.tools import handle_get_mitigations

        mock_store.get_technique.return_value = None

        result = await handle_get_mitigations({"technique_id": "T9999"})

        assert "Error:" in result[0].text
        assert "T9999" in result[0].text

    @pytest.mark.asyncio
    async def test_get_mitigations_missing_arg(self):
        """Test missing technique_id argument."""
        from attack_query_mcp.tools import handle_get_mitigations

        result = await handle_get_mitigations({})
        assert "Error:" in result[0].text


class TestExportNavigatorLayerTool:
    """Tests for the export_navigator_layer tool."""

    @pytest.fixture
    def mock_engine(self):
        """Create a mock engine."""
        with patch("attack_query_mcp.server.get_engine") as mock:
            engine = MagicMock()
            mock.return_value = engine
            yield engine

    @pytest.mark.asyncio
    async def test_export_navigator_layer(self, mock_engine: MagicMock):
        """Test exporting Navigator layer."""
        from attack_query_mcp.tools import handle_export_navigator_layer

        mock_engine.export_navigator_layer.return_value = {
            "name": "Test Layer",
            "domain": "enterprise-attack",
            "techniques": [{"techniqueID": "T1566", "color": "#ff6666"}],
        }

        result = await handle_export_navigator_layer(
            {"technique_ids": ["T1566", "T1059"], "name": "Test Layer"}
        )

        assert len(result) == 1
        assert "Test Layer" in result[0].text
        assert "json" in result[0].text
        assert "T1566" in result[0].text

    @pytest.mark.asyncio
    async def test_export_navigator_layer_with_options(self, mock_engine: MagicMock):
        """Test with description and color options."""
        from attack_query_mcp.tools import handle_export_navigator_layer

        mock_engine.export_navigator_layer.return_value = {"name": "Test"}

        await handle_export_navigator_layer(
            {
                "technique_ids": ["T1566"],
                "name": "Test",
                "description": "My description",
                "color": "#00ff00",
            }
        )

        mock_engine.export_navigator_layer.assert_called_once()
        call_args = mock_engine.export_navigator_layer.call_args
        assert call_args.kwargs["description"] == "My description"
        assert call_args.kwargs["color"] == "#00ff00"

    @pytest.mark.asyncio
    async def test_export_navigator_layer_missing_args(self):
        """Test missing required arguments."""
        from attack_query_mcp.tools import handle_export_navigator_layer

        result = await handle_export_navigator_layer({"name": "Test"})
        assert "Error:" in result[0].text
        assert "technique_ids" in result[0].text

        result = await handle_export_navigator_layer({"technique_ids": ["T1566"]})
        assert "Error:" in result[0].text
        assert "name" in result[0].text


class TestGetGroupTechniquesTemporalTool:
    """Tests for the get_group_techniques_temporal tool."""

    @pytest.fixture
    def mock_engine(self):
        """Create a mock engine."""
        with patch("attack_query_mcp.server.get_engine") as mock:
            engine = MagicMock()
            mock.return_value = engine
            yield engine

    @pytest.fixture
    def mock_store(self):
        """Create a mock store."""
        with patch("attack_query_mcp.server.get_store") as mock:
            store = MagicMock()
            mock.return_value = store
            yield store

    @pytest.mark.asyncio
    async def test_single_year_query(self, mock_engine: MagicMock, mock_store: MagicMock):
        """Test querying techniques for a single year."""
        from attack_query_mcp.tools import handle_get_group_techniques_temporal

        mock_engine.get_group_techniques_in_year.return_value = {
            "group": "APT28",
            "group_id": "G0007",
            "year": 2023,
            "techniques": {"T1566", "T1059"},
            "campaigns_used": [
                {
                    "id": "C0027",
                    "name": "Campaign A",
                    "first_seen": "2023-01",
                    "last_seen": "2023-06",
                }
            ],
            "campaign_count": 1,
        }

        t1 = MagicMock()
        t1.name = "Phishing"
        t2 = MagicMock()
        t2.name = "Command and Scripting Interpreter"
        mock_store.get_technique.side_effect = lambda tid: t1 if tid == "T1059" else t2

        result = await handle_get_group_techniques_temporal({"group": "APT28", "year": 2023})

        assert len(result) == 1
        assert "APT28" in result[0].text
        assert "2023" in result[0].text
        assert "T1566" in result[0].text
        assert "campaigns" in result[0].text.lower()
        assert "⚠️" in result[0].text  # Warning note
        mock_engine.get_group_techniques_in_year.assert_called_once_with("APT28", 2023)

    @pytest.mark.asyncio
    async def test_year_range_query(self, mock_engine: MagicMock, mock_store: MagicMock):
        """Test querying techniques for a year range."""
        from attack_query_mcp.tools import handle_get_group_techniques_temporal

        mock_engine.get_group_techniques_in_range.return_value = {
            "group": "APT28",
            "group_id": "G0007",
            "start_year": 2022,
            "end_year": 2024,
            "techniques": {"T1566", "T1059", "T1071"},
            "campaigns_used": [
                {
                    "id": "C0027",
                    "name": "Campaign A",
                    "first_seen": "2022-03",
                    "last_seen": "2022-08",
                },
                {
                    "id": "C0028",
                    "name": "Campaign B",
                    "first_seen": "2023-01",
                    "last_seen": "2024-02",
                },
            ],
            "campaign_count": 2,
        }

        t1 = MagicMock()
        t1.name = "Phishing"
        mock_store.get_technique.return_value = t1

        result = await handle_get_group_techniques_temporal(
            {"group": "APT28", "start_year": 2022, "end_year": 2024}
        )

        assert len(result) == 1
        assert "APT28" in result[0].text
        assert "2022-2024" in result[0].text
        assert "2 campaign" in result[0].text
        mock_engine.get_group_techniques_in_range.assert_called_once_with("APT28", 2022, 2024)

    @pytest.mark.asyncio
    async def test_no_techniques_found(self, mock_engine: MagicMock):
        """Test when no techniques are found in time period."""
        from attack_query_mcp.tools import handle_get_group_techniques_temporal

        mock_engine.get_group_techniques_in_year.return_value = {
            "group": "APT28",
            "group_id": "G0007",
            "year": 2030,
            "techniques": set(),
            "campaigns_used": [],
            "campaign_count": 0,
        }

        result = await handle_get_group_techniques_temporal({"group": "APT28", "year": 2030})

        assert len(result) == 1
        assert "No techniques found" in result[0].text

    @pytest.mark.asyncio
    async def test_missing_group(self):
        """Test missing group returns error."""
        from attack_query_mcp.tools import handle_get_group_techniques_temporal

        result = await handle_get_group_techniques_temporal({"year": 2023})

        assert len(result) == 1
        assert "Error:" in result[0].text
        assert "group is required" in result[0].text

    @pytest.mark.asyncio
    async def test_missing_time_parameters(self):
        """Test missing time parameters returns error."""
        from attack_query_mcp.tools import handle_get_group_techniques_temporal

        result = await handle_get_group_techniques_temporal({"group": "APT28"})

        assert len(result) == 1
        assert "Error:" in result[0].text
        assert "year" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_partial_range_parameters(self):
        """Test partial range parameters (only start_year) returns error."""
        from attack_query_mcp.tools import handle_get_group_techniques_temporal

        result = await handle_get_group_techniques_temporal({"group": "APT28", "start_year": 2022})

        assert len(result) == 1
        assert "Error:" in result[0].text

    @pytest.mark.asyncio
    async def test_group_not_found(self, mock_engine: MagicMock):
        """Test group not found error."""
        from attack_query_mcp.tools import handle_get_group_techniques_temporal

        mock_engine.get_group_techniques_in_year.side_effect = ValueError("Group not found: APT999")

        result = await handle_get_group_techniques_temporal({"group": "APT999", "year": 2023})

        assert len(result) == 1
        assert "Error:" in result[0].text
        assert "APT999" in result[0].text


class TestFormatTemporalQueryResults:
    """Tests for formatting temporal query results."""

    def test_format_group_techniques_in_year(self):
        """Test formatting single year temporal query results."""
        from attack_query_mcp.tools import format_query_results

        results: dict[str, Any] = {
            "query_type": "group_techniques_in_year",
            "group": "APT28",
            "group_id": "G0007",
            "year": 2023,
            "techniques": {"T1566", "T1059"},
            "campaigns_used": [{"id": "C0027", "name": "Campaign A"}],
            "campaign_count": 1,
        }

        output = format_query_results(results)

        assert "APT28" in output
        assert "2023" in output
        assert "T1566" in output
        assert "1 campaign" in output
        assert "Note:" in output  # Warning about campaign-based results

    def test_format_group_techniques_in_range(self):
        """Test formatting year range temporal query results."""
        from attack_query_mcp.tools import format_query_results

        results: dict[str, Any] = {
            "query_type": "group_techniques_in_range",
            "group": "APT28",
            "group_id": "G0007",
            "start_year": 2022,
            "end_year": 2024,
            "techniques": {"T1566", "T1059", "T1071"},
            "campaigns_used": [],
            "campaign_count": 0,
        }

        output = format_query_results(results)

        assert "APT28" in output
        assert "2022-2024" in output
        assert "3 techniques" in output
