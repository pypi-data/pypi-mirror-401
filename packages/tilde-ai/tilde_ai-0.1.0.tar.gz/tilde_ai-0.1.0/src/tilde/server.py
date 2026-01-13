"""MCP server implementation for tilde."""

import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, Tool

from tilde.schema import TildeProfile
from tilde.storage import get_storage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tilde")

# Create the MCP server
server = Server("tilde")


def _get_profile() -> TildeProfile:
    """Load the current profile from storage."""
    storage = get_storage()
    return storage.load()


def _profile_to_text(profile: TildeProfile, section: str | None = None) -> str:
    """Convert profile or section to readable text."""
    if section is None:
        return profile.model_dump_json(indent=2, exclude_none=True)

    # Get specific section
    if section == "identity":
        return profile.user_profile.identity.model_dump_json(indent=2, exclude_none=True)
    elif section == "tech_stack":
        return profile.user_profile.tech_stack.model_dump_json(indent=2, exclude_none=True)
    elif section == "domains":
        return profile.user_profile.domain_knowledge.model_dump_json(indent=2, exclude_none=True)
    elif section == "team":
        if profile.team_context:
            return profile.team_context.model_dump_json(indent=2, exclude_none=True)
        return "{}"
    else:
        return profile.model_dump_json(indent=2, exclude_none=True)


# =============================================================================
# MCP Resources
# =============================================================================


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available tilde resources."""
    return [
        Resource(
            uri="tilde://user/profile",
            name="Full User Profile",
            description="Complete user profile including identity, tech stack, and domain knowledge",
            mimeType="application/json",
        ),
        Resource(
            uri="tilde://user/identity",
            name="User Identity",
            description="User's name, role, and experience level",
            mimeType="application/json",
        ),
        Resource(
            uri="tilde://user/tech_stack",
            name="Tech Stack",
            description="Programming languages, preferences, and environment",
            mimeType="application/json",
        ),
        Resource(
            uri="tilde://user/domains",
            name="Domain Knowledge",
            description="Domain expertise, books learned, papers written, and projects created",
            mimeType="application/json",
        ),
        Resource(
            uri="tilde://team/context",
            name="Team Context",
            description="Team coding standards, architecture patterns, and constraints",
            mimeType="application/json",
        ),
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a tilde resource by URI."""
    profile = _get_profile()

    uri_to_section = {
        "tilde://user/profile": None,  # Full profile
        "tilde://user/identity": "identity",
        "tilde://user/tech_stack": "tech_stack",
        "tilde://user/domains": "domains",
        "tilde://team/context": "team",
    }

    section = uri_to_section.get(uri)
    if uri not in uri_to_section:
        raise ValueError(f"Unknown resource URI: {uri}")

    return _profile_to_text(profile, section)


# =============================================================================
# MCP Tools
# =============================================================================


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tilde tools."""
    return [
        Tool(
            name="get_profile",
            description="Get the user's profile. Optionally specify a section: 'identity', 'tech_stack', 'domains', or 'team'.",
            inputSchema={
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string",
                        "description": "Optional section to retrieve. One of: identity, tech_stack, domains, team. If omitted, returns full profile.",
                        "enum": ["identity", "tech_stack", "domains", "team"],
                    }
                },
            },
        ),
        Tool(
            name="get_team_context",
            description="Get the team's coding standards, architecture patterns, and constraints.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="propose_update",
            description="Propose an update to the user's profile. The update will be queued for user approval - it will NOT be applied immediately. Use this when you learn something new about the user that should be remembered.",
            inputSchema={
                "type": "object",
                "properties": {
                    "field_path": {
                        "type": "string",
                        "description": "Dot-separated path to the field to update. Examples: 'user_profile.tech_stack.preferences', 'user_profile.identity.role', 'user_profile.domain_knowledge.domains.finance'",
                    },
                    "proposed_value": {
                        "description": "The value to set, append, or remove. Can be any JSON-serializable value.",
                    },
                    "action": {
                        "type": "string",
                        "description": "The type of update: 'set' to replace the value, 'append' to add to a list, 'remove' to remove from a list.",
                        "enum": ["set", "append", "remove"],
                        "default": "set",
                    },
                    "reason": {
                        "type": "string",
                        "description": "Explain why you're proposing this update. This helps the user decide whether to approve it.",
                    },
                    "confidence": {
                        "type": "number",
                        "description": "How confident you are in this update (0-1). Higher values indicate stronger evidence from the conversation.",
                        "minimum": 0,
                        "maximum": 1,
                        "default": 0.5,
                    },
                },
                "required": ["field_path", "proposed_value", "reason"],
            },
        ),
        Tool(
            name="list_pending_updates",
            description="List all pending profile updates that are awaiting user approval.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    from tilde.updates import get_update_queue

    profile = _get_profile()

    if name == "get_profile":
        section = arguments.get("section")
        text = _profile_to_text(profile, section)
        return [TextContent(type="text", text=text)]

    elif name == "get_team_context":
        text = _profile_to_text(profile, "team")
        return [TextContent(type="text", text=text)]

    elif name == "propose_update":
        queue = get_update_queue()
        update_id = queue.propose(
            field_path=arguments["field_path"],
            proposed_value=arguments["proposed_value"],
            action=arguments.get("action", "set"),
            reason=arguments.get("reason"),
            source_agent=server.name,
            confidence=arguments.get("confidence", 0.5),
        )
        return [TextContent(
            type="text",
            text=f"Update proposed (ID: {update_id}). The user will be notified and can approve or reject this update using `tilde pending` and `tilde approve {update_id}`.",
        )]

    elif name == "list_pending_updates":
        queue = get_update_queue()
        pending = queue.list_pending()
        if not pending:
            return [TextContent(type="text", text="No pending updates.")]
        
        updates_text = json.dumps(
            [u.to_display_dict() for u in pending],
            indent=2,
        )
        return [TextContent(type="text", text=f"Pending updates:\n{updates_text}")]

    else:
        raise ValueError(f"Unknown tool: {name}")


# =============================================================================
# Server Entry Point
# =============================================================================


async def run_server() -> None:
    """Run the tilde MCP server."""
    logger.info("Starting tilde MCP server...")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> None:
    """Main entry point for the MCP server."""
    import asyncio

    asyncio.run(run_server())


if __name__ == "__main__":
    main()
