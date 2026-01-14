"""
MCP Tool implementations for attack-query.

Phase 1 tools:
- query_attack: Natural language queries against ATT&CK data
- get_technique: Get detailed technique information
- get_group: Get detailed group information

Phase 2 tools:
- compare_groups: Compare technique overlap between two groups
- find_similar_groups: Find groups with similar technique profiles
- get_mitigations: Get mitigations for a technique
- export_navigator_layer: Export techniques as Navigator layer JSON

See resources.py for Phase 3 MCP resources.
"""

from __future__ import annotations

from typing import Any

from mcp.server import Server
from mcp.types import TextContent, Tool


def register_tools(app: Server) -> None:
    """Register all MCP tools with the server."""

    @app.list_tools()  # type: ignore[no-untyped-call, untyped-decorator]
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="query_attack",
                description=(
                    "Query MITRE ATT&CK data using natural language. "
                    "Supports queries about techniques, groups, software, mitigations, "
                    "campaigns, and more. Examples: 'techniques used by APT28', "
                    "'groups using T1566', 'mitigations for T1566'."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": (
                                "Natural language query (e.g., 'techniques used by APT28 or APT29')"
                            ),
                        },
                        "matrix": {
                            "type": "string",
                            "enum": ["enterprise", "mobile", "ics"],
                            "default": "enterprise",
                            "description": "ATT&CK matrix to query",
                        },
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="get_technique",
                description=(
                    "Get detailed information about a MITRE ATT&CK technique by ID. "
                    "Returns name, description, tactics, and optionally sub-techniques."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "technique_id": {
                            "type": "string",
                            "description": "Technique ID (e.g., 'T1566' or 'T1566.001')",
                        },
                        "include_subtechniques": {
                            "type": "boolean",
                            "default": False,
                            "description": "Include sub-techniques in response",
                        },
                    },
                    "required": ["technique_id"],
                },
            ),
            Tool(
                name="get_group",
                description=(
                    "Get detailed information about a MITRE ATT&CK threat group. "
                    "Supports lookup by name, ID, or alias (e.g., 'APT28', 'G0007', 'Fancy Bear')."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "group": {
                            "type": "string",
                            "description": (
                                "Group name, ID, or alias (e.g., 'APT28', 'G0007', 'Fancy Bear')"
                            ),
                        },
                        "include_techniques": {
                            "type": "boolean",
                            "default": False,
                            "description": "Include list of techniques used",
                        },
                    },
                    "required": ["group"],
                },
            ),
            # Phase 2 tools
            Tool(
                name="compare_groups",
                description=(
                    "Compare techniques between two threat groups. Shows shared and unique "
                    "techniques, plus similarity metrics (Jaccard, Overlap, Cosine)."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "group1": {
                            "type": "string",
                            "description": "First group name, ID, or alias",
                        },
                        "group2": {
                            "type": "string",
                            "description": "Second group name, ID, or alias",
                        },
                    },
                    "required": ["group1", "group2"],
                },
            ),
            Tool(
                name="find_similar_groups",
                description=(
                    "Find threat groups with similar technique profiles to a given group. "
                    "Returns groups ranked by similarity score."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "group": {
                            "type": "string",
                            "description": "Group to find similar groups for",
                        },
                        "threshold": {
                            "type": "number",
                            "default": 0.3,
                            "description": "Minimum similarity score (0-1)",
                        },
                        "limit": {
                            "type": "integer",
                            "default": 10,
                            "description": "Maximum number of results",
                        },
                    },
                    "required": ["group"],
                },
            ),
            Tool(
                name="get_mitigations",
                description=(
                    "Get mitigations that address a specific technique. "
                    "Returns mitigation IDs, names, and descriptions."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "technique_id": {
                            "type": "string",
                            "description": "Technique ID to get mitigations for (e.g., 'T1566')",
                        },
                    },
                    "required": ["technique_id"],
                },
            ),
            Tool(
                name="export_navigator_layer",
                description=(
                    "Export a list of techniques as an ATT&CK Navigator layer JSON. "
                    "Can be imported into ATT&CK Navigator for visualization."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "technique_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of technique IDs to include",
                        },
                        "name": {
                            "type": "string",
                            "description": "Layer name",
                        },
                        "description": {
                            "type": "string",
                            "default": "",
                            "description": "Layer description",
                        },
                        "color": {
                            "type": "string",
                            "default": "#ff6666",
                            "description": "Highlight color for techniques (hex)",
                        },
                    },
                    "required": ["technique_ids", "name"],
                },
            ),
            Tool(
                name="get_group_techniques_temporal",
                description=(
                    "Get techniques used by a group during a specific time period. "
                    "Approximates temporal activity by cross-referencing campaigns "
                    "attributed to the group. Provide either 'year' for a single year "
                    "or 'start_year' and 'end_year' for a range."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "group": {
                            "type": "string",
                            "description": (
                                "Group name, ID, or alias (e.g., 'APT28', 'G0007', 'Fancy Bear')"
                            ),
                        },
                        "year": {
                            "type": "integer",
                            "description": "Single year to query (e.g., 2024)",
                        },
                        "start_year": {
                            "type": "integer",
                            "description": "Start year for range query (inclusive)",
                        },
                        "end_year": {
                            "type": "integer",
                            "description": "End year for range query (inclusive)",
                        },
                    },
                    "required": ["group"],
                },
            ),
        ]

    @app.call_tool()  # type: ignore[untyped-decorator]
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        if name == "query_attack":
            return await handle_query_attack(arguments)
        elif name == "get_technique":
            return await handle_get_technique(arguments)
        elif name == "get_group":
            return await handle_get_group(arguments)
        # Phase 2 tools
        elif name == "compare_groups":
            return await handle_compare_groups(arguments)
        elif name == "find_similar_groups":
            return await handle_find_similar_groups(arguments)
        elif name == "get_mitigations":
            return await handle_get_mitigations(arguments)
        elif name == "export_navigator_layer":
            return await handle_export_navigator_layer(arguments)
        elif name == "get_group_techniques_temporal":
            return await handle_get_group_techniques_temporal(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def handle_query_attack(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle query_attack tool calls."""
    from attack_query_mcp.server import get_parser

    query = arguments.get("query", "")
    if not query:
        return [TextContent(type="text", text="Error: query is required")]

    # matrix = arguments.get("matrix", "enterprise")  # TODO: support matrix switching

    parser = get_parser()
    results = parser.parse_and_execute(query)

    # Format results for AI consumption
    if "error" in results:
        return [TextContent(type="text", text=f"Error: {results['error']}")]

    return [TextContent(type="text", text=format_query_results(results))]


async def handle_get_technique(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle get_technique tool calls."""
    from attack_query_mcp.server import get_engine, get_store

    technique_id = arguments.get("technique_id", "")
    if not technique_id:
        return [TextContent(type="text", text="Error: technique_id is required")]

    include_subtechniques = arguments.get("include_subtechniques", False)

    store = get_store()
    technique = store.get_technique(technique_id)

    if not technique:
        return [TextContent(type="text", text=f"Error: Technique not found: {technique_id}")]

    # Build response
    lines = [
        f"# {technique.id}: {technique.name}",
        "",
        f"**Tactics:** {', '.join(technique.tactics) if technique.tactics else 'None'}",
        "",
        "## Description",
        technique.description[:1000] if technique.description else "No description available.",
    ]

    if technique.description and len(technique.description) > 1000:
        lines.append("... (truncated)")

    # Add sub-techniques if requested and this is a parent technique
    if include_subtechniques and "." not in technique.id:
        engine = get_engine()
        subtechnique_ids = engine.get_subtechniques_of(technique.id)
        if subtechnique_ids:
            lines.extend(["", "## Sub-techniques"])
            for sub_id in sorted(subtechnique_ids):
                sub_tech = store.get_technique(sub_id)
                if sub_tech:
                    lines.append(f"- **{sub_id}**: {sub_tech.name}")

    return [TextContent(type="text", text="\n".join(lines))]


async def handle_get_group(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle get_group tool calls."""
    from attack_query_mcp.server import get_engine, get_store

    group_identifier = arguments.get("group", "")
    if not group_identifier:
        return [TextContent(type="text", text="Error: group is required")]

    include_techniques = arguments.get("include_techniques", False)

    engine = get_engine()
    store = get_store()

    try:
        group_info = engine.get_group_info(group_identifier)
    except ValueError as e:
        return [TextContent(type="text", text=f"Error: {e}")]

    # Build response
    lines = [f"# {group_info['name']} ({group_info['id']})"]

    # Show alias resolution if applicable
    if group_info.get("resolved_from"):
        lines.append(f"\n*Resolved from alias: {group_info['resolved_from']}*")

    # Aliases
    if group_info.get("aliases"):
        lines.extend(["", f"**Aliases:** {', '.join(group_info['aliases'])}"])

    # Technique count
    lines.append(f"\n**Techniques used:** {group_info['technique_count']}")

    # Description (truncated)
    if group_info.get("description"):
        desc = group_info["description"]
        if len(desc) > 500:
            desc = desc[:500] + "... (truncated)"
        lines.extend(["", "## Description", desc])

    # Techniques list if requested
    if include_techniques:
        group = store.get_group(group_identifier)
        if group and group.techniques:
            lines.extend(["", "## Techniques"])
            sorted_techniques = sorted(group.techniques)[:50]  # Limit for context window
            for tech_id in sorted_techniques:
                tech = store.get_technique(tech_id)
                if tech:
                    lines.append(f"- **{tech_id}**: {tech.name}")
            if len(group.techniques) > 50:
                lines.append(f"... and {len(group.techniques) - 50} more")

    return [TextContent(type="text", text="\n".join(lines))]


# Phase 2 tool handlers


async def handle_compare_groups(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle compare_groups tool calls."""
    from attack_query_mcp.server import get_engine, get_store

    group1 = arguments.get("group1", "")
    group2 = arguments.get("group2", "")

    if not group1 or not group2:
        return [TextContent(type="text", text="Error: Both group1 and group2 are required")]

    engine = get_engine()
    store = get_store()

    try:
        similarity = engine.calculate_group_similarity(group1, group2)
    except ValueError as e:
        return [TextContent(type="text", text=f"Error: {e}")]

    # Get group names for display
    g1 = store.get_group(group1)
    g2 = store.get_group(group2)
    g1_name = g1.name if g1 else group1
    g2_name = g2.name if g2 else group2

    lines = [
        f"# Comparing {g1_name} vs {g2_name}",
        "",
        "## Similarity Metrics",
        f"- **Jaccard similarity:** {similarity['jaccard']:.1%}",
        f"- **Overlap coefficient:** {similarity['overlap']:.1%}",
        f"- **Cosine similarity:** {similarity['cosine']:.1%}",
        "",
        "## Technique Counts",
        f"- **{g1_name}:** {similarity['group1_count']} techniques",
        f"- **{g2_name}:** {similarity['group2_count']} techniques",
        f"- **Shared:** {similarity['shared_count']} techniques",
        f"- **Unique to {g1_name}:** {similarity['unique_to_group1']}",
        f"- **Unique to {g2_name}:** {similarity['unique_to_group2']}",
    ]

    # List shared techniques (limited)
    shared = similarity.get("shared_techniques", [])
    if shared:
        lines.extend(["", "## Shared Techniques"])
        for tech_id in list(shared)[:20]:
            tech = store.get_technique(tech_id)
            if tech:
                lines.append(f"- **{tech_id}**: {tech.name}")
        if len(shared) > 20:
            lines.append(f"... and {len(shared) - 20} more")

    return [TextContent(type="text", text="\n".join(lines))]


async def handle_find_similar_groups(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle find_similar_groups tool calls."""
    from attack_query_mcp.server import get_engine

    group = arguments.get("group", "")
    if not group:
        return [TextContent(type="text", text="Error: group is required")]

    threshold = arguments.get("threshold", 0.3)
    limit = arguments.get("limit", 10)

    engine = get_engine()

    try:
        similar = engine.find_similar_groups(group, threshold=threshold, limit=limit)
    except ValueError as e:
        return [TextContent(type="text", text=f"Error: {e}")]

    if not similar:
        return [
            TextContent(
                type="text",
                text=f"No groups found with similarity >= {threshold:.0%} to {group}",
            )
        ]

    lines = [
        f"# Groups Similar to {group}",
        f"*Threshold: {threshold:.0%}, showing top {limit}*",
        "",
    ]

    for i, s in enumerate(similar, 1):
        lines.append(
            f"{i}. **{s['name']}** ({s['id']}): "
            f"{s['jaccard']:.1%} Jaccard, "
            f"{s['shared_count']} shared techniques"
        )

    return [TextContent(type="text", text="\n".join(lines))]


async def handle_get_mitigations(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle get_mitigations tool calls."""
    from attack_query_mcp.server import get_engine, get_store

    technique_id = arguments.get("technique_id", "")
    if not technique_id:
        return [TextContent(type="text", text="Error: technique_id is required")]

    engine = get_engine()
    store = get_store()

    # Verify technique exists
    technique = store.get_technique(technique_id)
    if not technique:
        return [TextContent(type="text", text=f"Error: Technique not found: {technique_id}")]

    mitigations = engine.get_mitigations_for_technique(technique_id)

    if not mitigations:
        return [
            TextContent(
                type="text",
                text=f"No mitigations found for {technique_id}: {technique.name}",
            )
        ]

    lines = [
        f"# Mitigations for {technique_id}: {technique.name}",
        f"*{len(mitigations)} mitigations found*",
        "",
    ]

    for m in mitigations:
        lines.append(f"## {m['id']}: {m['name']}")
        desc = m.get("description", "No description available.")
        if len(desc) > 300:
            desc = desc[:300] + "..."
        lines.append(desc)
        lines.append("")

    return [TextContent(type="text", text="\n".join(lines))]


async def handle_export_navigator_layer(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle export_navigator_layer tool calls."""
    import json

    from attack_query_mcp.server import get_engine

    technique_ids = arguments.get("technique_ids", [])
    name = arguments.get("name", "")

    if not technique_ids:
        return [TextContent(type="text", text="Error: technique_ids is required")]
    if not name:
        return [TextContent(type="text", text="Error: name is required")]

    description = arguments.get("description", "")
    color = arguments.get("color", "#ff6666")

    engine = get_engine()

    # Convert list to set for the engine
    technique_set = set(technique_ids)

    layer = engine.export_navigator_layer(
        technique_ids=technique_set,
        name=name,
        description=description,
        color=color,
    )

    # Return as formatted JSON
    layer_json = json.dumps(layer, indent=2)

    return [
        TextContent(
            type="text",
            text=f"# ATT&CK Navigator Layer: {name}\n\n"
            f"*{len(technique_ids)} techniques included*\n\n"
            f"```json\n{layer_json}\n```\n\n"
            "Save this JSON to a file and import it into "
            "[ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/).",
        )
    ]


async def handle_get_group_techniques_temporal(
    arguments: dict[str, Any],
) -> list[TextContent]:
    """Handle get_group_techniques_temporal tool calls."""
    from attack_query_mcp.server import get_engine, get_store

    group = arguments.get("group", "")
    if not group:
        return [TextContent(type="text", text="Error: group is required")]

    year = arguments.get("year")
    start_year = arguments.get("start_year")
    end_year = arguments.get("end_year")

    # Validate arguments: need either year OR both start_year and end_year
    if year is None and (start_year is None or end_year is None):
        return [
            TextContent(
                type="text",
                text="Error: Provide either 'year' for single year or both 'start_year' and 'end_year' for range",
            )
        ]

    engine = get_engine()
    store = get_store()

    try:
        if year is not None:
            result = engine.get_group_techniques_in_year(group, year)
        else:
            # We've validated both are not None above
            assert start_year is not None and end_year is not None
            result = engine.get_group_techniques_in_range(group, start_year, end_year)
    except ValueError as e:
        return [TextContent(type="text", text=f"Error: {e}")]

    # Build response
    group_name = result["group"]
    group_id = result["group_id"]
    techniques = result["techniques"]
    campaigns_used = result["campaigns_used"]
    campaign_count = result["campaign_count"]

    # Format time period
    time_period = str(year) if year is not None else f"{start_year}-{end_year}"

    lines = [
        f"# Techniques used by {group_name} ({group_id}) in {time_period}",
        "",
        f"*Based on {campaign_count} campaign(s) attributed to this group*",
        "",
        "⚠️ **Note:** This only includes techniques documented in campaigns, "
        "not all techniques attributed to this group.",
        "",
    ]

    if not techniques:
        lines.append("No techniques found in campaigns during this time period.")
    else:
        lines.append(f"## Techniques ({len(techniques)} found)")
        lines.append("")
        for tech_id in sorted(techniques)[:50]:
            tech = store.get_technique(tech_id)
            if tech:
                lines.append(f"- **{tech_id}**: {tech.name}")
            else:
                lines.append(f"- **{tech_id}**")
        if len(techniques) > 50:
            lines.append(f"... and {len(techniques) - 50} more")

    # List campaigns used
    if campaigns_used:
        lines.extend(["", "## Campaigns"])
        for c in campaigns_used[:10]:
            date_range = ""
            if c.get("first_seen") or c.get("last_seen"):
                start = c.get("first_seen", "?")
                end = c.get("last_seen", "?")
                date_range = f" ({start} - {end})"
            lines.append(f"- **{c['id']}**: {c['name']}{date_range}")
        if len(campaigns_used) > 10:
            lines.append(f"... and {len(campaigns_used) - 10} more")

    return [TextContent(type="text", text="\n".join(lines))]


def format_query_results(results: dict[str, Any]) -> str:
    """Format query results for AI-friendly output."""
    query_type = results.get("query_type", "unknown")

    # Techniques by groups (union, intersection, exclusive)
    if query_type in (
        "techniques_by_groups",
        "techniques_intersection",
        "techniques_exclusive",
        "techniques_complement",
        "techniques_not_used_by",
    ):
        techniques = results.get("techniques", [])
        groups = results.get("groups", [])

        lines = []
        if groups:
            lines.append(f"**Groups queried:** {', '.join(groups)}")
        lines.append(f"**Found {len(techniques)} techniques:**")

        # Limit output for context window
        for t in techniques[:50]:
            if isinstance(t, dict):
                lines.append(f"- {t.get('id', 'Unknown')}: {t.get('name', 'Unknown')}")
            else:
                lines.append(f"- {t}")

        if len(techniques) > 50:
            lines.append(f"... and {len(techniques) - 50} more")

        return "\n".join(lines)

    # Groups using technique
    elif query_type == "groups_using_technique":
        groups = results.get("groups", [])
        technique = results.get("technique", "Unknown")
        lines = [f"**Groups using {technique}:** {len(groups)} found"]
        for g in groups[:30]:
            if isinstance(g, dict):
                lines.append(f"- {g.get('name', g.get('id', 'Unknown'))}")
            else:
                lines.append(f"- {g}")
        if len(groups) > 30:
            lines.append(f"... and {len(groups) - 30} more")
        return "\n".join(lines)

    # Group info
    elif query_type == "group_info":
        info = results.get("info", {})
        lines = [
            f"# {info.get('name', 'Unknown')} ({info.get('id', 'Unknown')})",
            f"**Aliases:** {', '.join(info.get('aliases', []))}",
            f"**Techniques:** {info.get('technique_count', 0)}",
        ]
        return "\n".join(lines)

    # Mitigations
    elif query_type in ("mitigations_for_technique", "mitigation_info"):
        mitigations = results.get("mitigations", [])
        if mitigations:
            lines = [f"**Found {len(mitigations)} mitigations:**"]
            for m in mitigations[:20]:
                if isinstance(m, dict):
                    lines.append(f"- {m.get('id', 'Unknown')}: {m.get('name', 'Unknown')}")
                else:
                    lines.append(f"- {m}")
            return "\n".join(lines)

        # Single mitigation info
        info = results.get("info", {})
        if info:
            return f"# {info.get('name', 'Unknown')} ({info.get('id', 'Unknown')})"

    # Similar groups
    elif query_type == "similar_groups":
        similar = results.get("similar_groups", [])
        group = results.get("group", "Unknown")
        lines = [f"**Groups similar to {group}:**"]
        for s in similar[:20]:
            if isinstance(s, dict):
                score = s.get("jaccard", s.get("score", 0))
                lines.append(f"- {s.get('name', 'Unknown')}: {score:.2%} similarity")
            else:
                lines.append(f"- {s}")
        return "\n".join(lines)

    # Group similarity comparison
    elif query_type == "group_similarity":
        lines = [
            f"**Comparing {results.get('group1', 'Unknown')} vs {results.get('group2', 'Unknown')}**",
            f"- Jaccard similarity: {results.get('jaccard', 0):.2%}",
            f"- Overlap coefficient: {results.get('overlap', 0):.2%}",
            f"- Shared techniques: {results.get('shared_count', 0)}",
        ]
        return "\n".join(lines)

    # Sub-techniques
    elif query_type == "subtechniques_of":
        subtechniques = results.get("subtechniques", [])
        parent = results.get("parent", "Unknown")
        lines = [f"**Sub-techniques of {parent}:** {len(subtechniques)} found"]
        for st in subtechniques:
            if isinstance(st, dict):
                lines.append(f"- {st.get('id', 'Unknown')}: {st.get('name', 'Unknown')}")
            else:
                lines.append(f"- {st}")
        return "\n".join(lines)

    # Temporal group queries (via query_attack natural language)
    elif query_type in ("group_techniques_in_year", "group_techniques_in_range"):
        group = results.get("group", "Unknown")
        group_id = results.get("group_id", "")
        techniques = results.get("techniques", [])
        campaign_count = results.get("campaign_count", 0)

        # Determine time period from results
        year = results.get("year")
        start_year = results.get("start_year")
        end_year = results.get("end_year")
        if year is not None:
            time_period = str(year)
        elif start_year is not None and end_year is not None:
            time_period = f"{start_year}-{end_year}"
        else:
            time_period = "unknown period"

        lines = [
            f"**Techniques used by {group} ({group_id}) in {time_period}**",
            f"*Based on {campaign_count} campaign(s)*",
            "",
            "⚠️ Note: Only includes techniques documented in campaigns.",
            "",
            f"**Found {len(techniques)} techniques:**",
        ]

        # Handle both dict format (from parser) and string format
        # Convert to list if it's a set
        tech_list = list(techniques) if isinstance(techniques, set) else techniques
        for t in tech_list[:50]:
            if isinstance(t, dict):
                lines.append(f"- {t.get('id', 'Unknown')}: {t.get('name', 'Unknown')}")
            else:
                lines.append(f"- {t}")
        if len(tech_list) > 50:
            lines.append(f"... and {len(tech_list) - 50} more")

        return "\n".join(lines)

    # Default: return as string
    return str(results)
