"""Zi MCP Server - Expose Zi chat as MCP tools."""

import asyncio
import os
import uuid
from typing import Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from zi_mcp.client import ZiClient


# Create MCP server
app = Server("zi")

# Global client instance (initialized in main)
client: Optional[ZiClient] = None


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Zi tools."""
    return [
        Tool(
            name="zi_chat",
            description="Send a message to Zi and receive a response. Zi is an AI companion for life guidance, offering insights on career, relationships, and personal growth. Optionally continue a conversation by providing thread_id.",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to send to Zi",
                    },
                    "thread_id": {
                        "type": "string",
                        "description": "Optional thread ID to continue an existing conversation",
                    },
                    "language": {
                        "type": "string",
                        "enum": ["EN", "VN"],
                        "default": "EN",
                        "description": "Response language: EN (English) or VN (Vietnamese)",
                    },
                },
                "required": ["message"],
            },
        ),
        Tool(
            name="zi_list_threads",
            description="List all conversation threads with Zi",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="zi_get_thread",
            description="Get the conversation history for a specific thread",
            inputSchema={
                "type": "object",
                "properties": {
                    "thread_id": {
                        "type": "string",
                        "description": "The thread ID to retrieve",
                    },
                },
                "required": ["thread_id"],
            },
        ),
        Tool(
            name="zi_create_thread",
            description="Create a new conversation thread (returns a new thread ID)",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="zi_delete_thread",
            description="Delete a conversation thread",
            inputSchema={
                "type": "object",
                "properties": {
                    "thread_id": {
                        "type": "string",
                        "description": "The thread ID to delete",
                    },
                },
                "required": ["thread_id"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    global client

    if client is None:
        return [TextContent(type="text", text="Error: Zi client not initialized. Check ZI_API_KEY.")]

    try:
        if name == "zi_chat":
            result = await client.chat(
                message=arguments["message"],
                thread_id=arguments.get("thread_id"),
                language=arguments.get("language", "EN"),
            )
            response_text = f"**Zi's response:**\n\n{result['response']}\n\n---\n*Thread ID: {result['thread_id']}*"
            return [TextContent(type="text", text=response_text)]

        elif name == "zi_list_threads":
            threads = await client.list_threads()
            if not threads:
                return [TextContent(type="text", text="No conversation threads found.")]

            lines = ["**Conversation Threads:**\n"]
            for t in threads:
                lines.append(f"- **{t.get('title', 'Untitled')}**")
                lines.append(f"  - ID: `{t['id']}`")
                lines.append(f"  - Updated: {t.get('updated_at', 'Unknown')}")
                lines.append("")
            return [TextContent(type="text", text="\n".join(lines))]

        elif name == "zi_get_thread":
            thread_id = arguments["thread_id"]
            result = await client.get_thread(thread_id)
            messages = result.get("messages", [])

            if not messages:
                return [TextContent(type="text", text=f"No messages in thread {thread_id}")]

            lines = [f"**Thread {thread_id}:**\n"]
            for msg in messages:
                role = msg.get("role", "unknown").capitalize()
                content = msg.get("content", "")
                if isinstance(content, dict):
                    content = str(content)
                lines.append(f"**{role}:** {content[:500]}{'...' if len(str(content)) > 500 else ''}")
                lines.append("")
            return [TextContent(type="text", text="\n".join(lines))]

        elif name == "zi_create_thread":
            thread_id = str(uuid.uuid4())
            return [TextContent(type="text", text=f"Created new thread: `{thread_id}`\n\nUse this thread_id with zi_chat to start a conversation.")]

        elif name == "zi_delete_thread":
            thread_id = arguments["thread_id"]
            success = await client.delete_thread(thread_id)
            if success:
                return [TextContent(type="text", text=f"Thread `{thread_id}` deleted successfully.")]
            else:
                return [TextContent(type="text", text=f"Failed to delete thread `{thread_id}`. It may not exist.")]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def run_server():
    """Run the MCP server."""
    global client

    # Get API key from environment
    api_key = os.environ.get("ZI_API_KEY")
    if not api_key:
        print("Error: ZI_API_KEY environment variable is required", flush=True)
        print("Get your API key from https://ziai.chat/settings", flush=True)
        return

    # Optional: custom base URL for development
    base_url = os.environ.get("ZI_API_URL", "https://api.ziai.chat")

    # Initialize client
    client = ZiClient(api_key=api_key, base_url=base_url)

    # Run server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main():
    """Entry point for the MCP server."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
