"""
MCP Resource implementations for attack-query.

Phase 3 resources:
- attack://groups - List all threat groups
- attack://techniques - List all techniques
- attack://tactics - List all tactics
- attack://software - List all software (malware and tools)
- attack://mitigations - List all mitigations
- attack://campaigns - List all campaigns

Phase 4 resource templates:
- attack://groups/{id} - Single group details (by ID, name, or alias)
- attack://techniques/{id} - Single technique details (by ID)
"""

from __future__ import annotations

import re
from typing import Any

from mcp.server import Server
from mcp.types import Resource, ResourceTemplate, TextContent
from pydantic import AnyUrl


def get_resource_list() -> list[Resource]:
    """Return the list of available resources."""
    return [
        Resource(
            uri=AnyUrl("attack://groups"),
            name="ATT&CK Groups",
            description="List of all MITRE ATT&CK threat groups with IDs, names, and aliases",
            mimeType="text/plain",
        ),
        Resource(
            uri=AnyUrl("attack://techniques"),
            name="ATT&CK Techniques",
            description="List of all MITRE ATT&CK techniques with IDs, names, and tactics",
            mimeType="text/plain",
        ),
        Resource(
            uri=AnyUrl("attack://tactics"),
            name="ATT&CK Tactics",
            description="List of all MITRE ATT&CK tactics in kill chain order",
            mimeType="text/plain",
        ),
        Resource(
            uri=AnyUrl("attack://software"),
            name="ATT&CK Software",
            description="List of all MITRE ATT&CK software (malware and tools)",
            mimeType="text/plain",
        ),
        Resource(
            uri=AnyUrl("attack://mitigations"),
            name="ATT&CK Mitigations",
            description="List of all MITRE ATT&CK mitigations",
            mimeType="text/plain",
        ),
        Resource(
            uri=AnyUrl("attack://campaigns"),
            name="ATT&CK Campaigns",
            description="List of all MITRE ATT&CK campaigns",
            mimeType="text/plain",
        ),
    ]


def get_resource_template_list() -> list[ResourceTemplate]:
    """Return the list of available resource templates."""
    return [
        ResourceTemplate(
            uriTemplate="attack://groups/{id}",
            name="ATT&CK Group Details",
            description="Detailed information about a specific threat group (by ID, name, or alias)",
            mimeType="text/plain",
        ),
        ResourceTemplate(
            uriTemplate="attack://techniques/{id}",
            name="ATT&CK Technique Details",
            description="Detailed information about a specific technique (by ID like T1566 or T1566.001)",
            mimeType="text/plain",
        ),
    ]


# Regex patterns for matching templated URIs
GROUP_URI_PATTERN = re.compile(r"^attack://groups/(.+)$")
TECHNIQUE_URI_PATTERN = re.compile(r"^attack://techniques/(.+)$")


async def read_resource(uri: str) -> list[TextContent]:
    """Read a resource by URI."""
    # Normalize URI (handle both AnyUrl objects and strings)
    uri_str = str(uri)

    # Static resources
    if uri_str == "attack://groups":
        return await read_groups_resource()
    elif uri_str == "attack://techniques":
        return await read_techniques_resource()
    elif uri_str == "attack://tactics":
        return await read_tactics_resource()
    elif uri_str == "attack://software":
        return await read_software_resource()
    elif uri_str == "attack://mitigations":
        return await read_mitigations_resource()
    elif uri_str == "attack://campaigns":
        return await read_campaigns_resource()

    # Templated resources
    group_match = GROUP_URI_PATTERN.match(uri_str)
    if group_match:
        return await read_group_detail_resource(group_match.group(1))

    technique_match = TECHNIQUE_URI_PATTERN.match(uri_str)
    if technique_match:
        return await read_technique_detail_resource(technique_match.group(1))

    return [TextContent(type="text", text=f"Unknown resource: {uri_str}")]


def register_resources(app: Server) -> None:
    """Register all MCP resources with the server."""

    @app.list_resources()  # type: ignore[no-untyped-call, untyped-decorator]
    async def list_resources() -> list[Resource]:
        return get_resource_list()

    @app.list_resource_templates()  # type: ignore[no-untyped-call, untyped-decorator]
    async def list_resource_templates() -> list[ResourceTemplate]:
        return get_resource_template_list()

    @app.read_resource()  # type: ignore[no-untyped-call, untyped-decorator]
    async def handle_read_resource(uri: Any) -> list[TextContent]:
        return await read_resource(str(uri))


async def read_groups_resource() -> list[TextContent]:
    """Read the groups resource - list all threat groups."""
    from attack_query_mcp.server import get_store

    store = get_store()
    groups = sorted(store.groups.values(), key=lambda g: g.name)

    lines = [
        "# MITRE ATT&CK Threat Groups",
        f"*{len(groups)} groups in database*",
        "",
        "| ID | Name | Aliases |",
        "|-----|------|---------|",
    ]

    for group in groups:
        aliases = ", ".join(group.aliases[:5]) if group.aliases else "-"
        if len(group.aliases) > 5:
            aliases += f" (+{len(group.aliases) - 5} more)"
        lines.append(f"| {group.id} | {group.name} | {aliases} |")

    return [TextContent(type="text", text="\n".join(lines))]


async def read_techniques_resource() -> list[TextContent]:
    """Read the techniques resource - list all techniques."""
    from attack_query_mcp.server import get_store

    store = get_store()

    # Separate parent techniques and sub-techniques
    parents = []
    subs = []
    for tech in store.techniques.values():
        if "." in tech.id:
            subs.append(tech)
        else:
            parents.append(tech)

    parents.sort(key=lambda t: t.id)
    subs.sort(key=lambda t: t.id)

    lines = [
        "# MITRE ATT&CK Techniques",
        f"*{len(parents)} techniques, {len(subs)} sub-techniques*",
        "",
        "## Techniques",
        "",
        "| ID | Name | Tactics |",
        "|----|------|---------|",
    ]

    for tech in parents:
        tactics = ", ".join(tech.tactics) if tech.tactics else "-"
        lines.append(f"| {tech.id} | {tech.name} | {tactics} |")

    # Add sub-techniques summary
    lines.extend(
        [
            "",
            "## Sub-techniques",
            "",
            f"*{len(subs)} sub-techniques available. Query with `get_technique` for details.*",
            "",
            "Example sub-techniques:",
        ]
    )

    # Show first 20 sub-techniques as examples
    for tech in subs[:20]:
        lines.append(f"- {tech.id}: {tech.name}")
    if len(subs) > 20:
        lines.append(f"... and {len(subs) - 20} more")

    return [TextContent(type="text", text="\n".join(lines))]


async def read_tactics_resource() -> list[TextContent]:
    """Read the tactics resource - list all tactics in kill chain order."""
    from attack_query_mcp.server import get_store

    store = get_store()

    # Sort by x_mitre_shortname (TA ID)
    tactics = sorted(store.tactics.values(), key=lambda t: t.shortname)

    lines = [
        "# MITRE ATT&CK Tactics",
        f"*{len(tactics)} tactics (Enterprise ATT&CK kill chain)*",
        "",
        "| ID | Name | Description |",
        "|----|------|-------------|",
    ]

    for tactic in tactics:
        # Truncate description for table
        desc = tactic.description[:100] if tactic.description else "-"
        if tactic.description and len(tactic.description) > 100:
            desc += "..."
        # Escape pipes in description
        desc = desc.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {tactic.shortname} | {tactic.name} | {desc} |")

    return [TextContent(type="text", text="\n".join(lines))]


async def read_software_resource() -> list[TextContent]:
    """Read the software resource - list all malware and tools."""
    from attack_query_mcp.server import get_store

    store = get_store()

    # Separate malware and tools
    malware = []
    tools = []
    for sw in store.software.values():
        if sw.software_type == "malware":
            malware.append(sw)
        else:
            tools.append(sw)

    malware.sort(key=lambda s: s.name)
    tools.sort(key=lambda s: s.name)

    lines = [
        "# MITRE ATT&CK Software",
        f"*{len(malware)} malware, {len(tools)} tools*",
        "",
        "## Malware",
        "",
        "| ID | Name | Platforms |",
        "|----|------|-----------|",
    ]

    for sw in malware[:100]:  # Limit for context window
        platforms = ", ".join(sw.platforms[:3]) if sw.platforms else "-"
        if len(sw.platforms) > 3:
            platforms += "..."
        lines.append(f"| {sw.id} | {sw.name} | {platforms} |")

    if len(malware) > 100:
        lines.append(f"| ... | *{len(malware) - 100} more malware* | |")

    lines.extend(
        [
            "",
            "## Tools",
            "",
            "| ID | Name | Platforms |",
            "|----|------|-----------|",
        ]
    )

    for sw in tools[:50]:  # Limit for context window
        platforms = ", ".join(sw.platforms[:3]) if sw.platforms else "-"
        if len(sw.platforms) > 3:
            platforms += "..."
        lines.append(f"| {sw.id} | {sw.name} | {platforms} |")

    if len(tools) > 50:
        lines.append(f"| ... | *{len(tools) - 50} more tools* | |")

    return [TextContent(type="text", text="\n".join(lines))]


async def read_mitigations_resource() -> list[TextContent]:
    """Read the mitigations resource - list all mitigations."""
    from attack_query_mcp.server import get_store

    store = get_store()
    mitigations = sorted(store.mitigations.values(), key=lambda m: m.id)

    lines = [
        "# MITRE ATT&CK Mitigations",
        f"*{len(mitigations)} mitigations*",
        "",
        "| ID | Name | Techniques Mitigated |",
        "|----|------|---------------------|",
    ]

    for m in mitigations:
        tech_count = len(m.techniques) if m.techniques else 0
        lines.append(f"| {m.id} | {m.name} | {tech_count} |")

    return [TextContent(type="text", text="\n".join(lines))]


async def read_campaigns_resource() -> list[TextContent]:
    """Read the campaigns resource - list all campaigns."""
    from attack_query_mcp.server import get_store

    store = get_store()
    campaigns = sorted(store.campaigns.values(), key=lambda c: c.id)

    lines = [
        "# MITRE ATT&CK Campaigns",
        f"*{len(campaigns)} campaigns*",
        "",
        "| ID | Name | First Seen | Last Seen | Groups |",
        "|----|------|------------|-----------|--------|",
    ]

    for c in campaigns:
        # first_seen/last_seen are ISO date strings like "2022-06-01T04:00:00.000Z"
        first_seen = c.first_seen[:7] if c.first_seen else "-"  # Extract YYYY-MM
        last_seen = c.last_seen[:7] if c.last_seen else "-"  # Extract YYYY-MM
        # Get group names (convert set to list for slicing)
        group_names = []
        groups_list = list(c.groups)[:3]
        for gid in groups_list:
            g = store.get_group(gid)
            if g:
                group_names.append(g.name)
        groups_str = ", ".join(group_names) if group_names else "-"
        if len(c.groups) > 3:
            groups_str += f" (+{len(c.groups) - 3})"
        lines.append(f"| {c.id} | {c.name} | {first_seen} | {last_seen} | {groups_str} |")

    return [TextContent(type="text", text="\n".join(lines))]


# Phase 4: Resource template handlers


async def read_group_detail_resource(group_id: str) -> list[TextContent]:
    """Read details for a specific group by ID, name, or alias."""
    from urllib.parse import unquote

    from attack_query_mcp.server import get_engine, get_store

    # URL-decode the group_id (handles spaces and special chars)
    group_id = unquote(group_id)

    store = get_store()
    engine = get_engine()

    # Try to get group info (handles ID, name, and alias resolution)
    try:
        group_info = engine.get_group_info(group_id)
    except ValueError:
        return [TextContent(type="text", text=f"Group not found: {group_id}")]

    group = store.get_group(group_id)
    if not group:
        return [TextContent(type="text", text=f"Group not found: {group_id}")]

    # Build detailed response
    lines = [f"# {group_info['name']} ({group_info['id']})"]

    # Show alias resolution if applicable
    if group_info.get("resolved_from"):
        lines.append(f"\n*Resolved from alias: {group_info['resolved_from']}*")

    # Aliases
    if group.aliases:
        lines.extend(["", f"**Aliases:** {', '.join(group.aliases)}"])

    # Technique count
    lines.append(f"\n**Techniques used:** {len(group.techniques)}")

    # Description
    if group_info.get("description"):
        desc = group_info["description"]
        if len(desc) > 1000:
            desc = desc[:1000] + "... (truncated)"
        lines.extend(["", "## Description", "", desc])

    # Techniques list (limited)
    if group.techniques:
        lines.extend(["", "## Techniques Used", ""])
        sorted_techniques = sorted(group.techniques)[:30]
        for tech_id in sorted_techniques:
            tech = store.get_technique(tech_id)
            if tech:
                lines.append(f"- **{tech_id}**: {tech.name}")
        if len(group.techniques) > 30:
            lines.append(f"\n*... and {len(group.techniques) - 30} more techniques*")

    # Software used
    software_ids = list(store.group_to_software.get(group.stix_id, set()))
    if software_ids:
        lines.extend(["", "## Software Used", ""])
        for sw_id in sorted(software_ids)[:20]:
            sw = store.software.get(sw_id)
            if sw:
                lines.append(f"- **{sw.id}**: {sw.name} ({sw.software_type})")
        if len(software_ids) > 20:
            lines.append(f"\n*... and {len(software_ids) - 20} more*")

    return [TextContent(type="text", text="\n".join(lines))]


async def read_technique_detail_resource(technique_id: str) -> list[TextContent]:
    """Read details for a specific technique by ID."""
    from urllib.parse import unquote

    from attack_query_mcp.server import get_engine, get_store

    # URL-decode the technique_id
    technique_id = unquote(technique_id).upper()  # Normalize to uppercase

    store = get_store()
    engine = get_engine()

    technique = store.get_technique(technique_id)
    if not technique:
        return [TextContent(type="text", text=f"Technique not found: {technique_id}")]

    # Build detailed response
    lines = [
        f"# {technique.id}: {technique.name}",
        "",
        f"**Tactics:** {', '.join(technique.tactics) if technique.tactics else 'None'}",
    ]

    # Check if this is a sub-technique
    if "." in technique.id:
        parent_id = technique.id.split(".")[0]
        parent = store.get_technique(parent_id)
        if parent:
            lines.append(f"**Parent technique:** {parent_id} ({parent.name})")

    # Description
    if technique.description:
        desc = technique.description
        if len(desc) > 1500:
            desc = desc[:1500] + "... (truncated)"
        lines.extend(["", "## Description", "", desc])

    # Sub-techniques (if this is a parent technique)
    if "." not in technique.id:
        subtechnique_ids = engine.get_subtechniques_of(technique.id)
        if subtechnique_ids:
            lines.extend(["", "## Sub-techniques", ""])
            for sub_id in sorted(subtechnique_ids):
                sub_tech = store.get_technique(sub_id)
                if sub_tech:
                    lines.append(f"- **{sub_id}**: {sub_tech.name}")

    # Groups using this technique
    groups_using = engine.groups_using_technique(technique.id)
    if groups_using:
        lines.extend(["", "## Groups Using This Technique", ""])
        for group_name in groups_using[:20]:
            group = store.get_group(group_name)
            if group:
                lines.append(f"- **{group.id}**: {group.name}")
            else:
                lines.append(f"- {group_name}")
        if len(groups_using) > 20:
            lines.append(f"\n*... and {len(groups_using) - 20} more groups*")

    # Mitigations
    mitigations = engine.get_mitigations_for_technique(technique.id)
    if mitigations:
        lines.extend(["", "## Mitigations", ""])
        for m in mitigations[:10]:
            lines.append(f"- **{m['id']}**: {m['name']}")
        if len(mitigations) > 10:
            lines.append(f"\n*... and {len(mitigations) - 10} more mitigations*")

    return [TextContent(type="text", text="\n".join(lines))]
