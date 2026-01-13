"""MCP server for UX Lens."""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .browser import capture_browser_session
from .gemini import analyze_video


app = Server("ux-lens")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="analyze_ui",
            description=(
                "Launch a browser, capture user interaction with the website, "
                "and get a comprehensive UX/frontend critique from Gemini. "
                "Use mode='manual' for human browsing, mode='auto' for automated exploration."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the website to analyze",
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["manual", "auto"],
                        "default": "manual",
                        "description": (
                            "manual: You browse the site interactively. "
                            "auto: Automated exploration (scroll, click links)."
                        ),
                    },
                    "timeout_seconds": {
                        "type": "integer",
                        "default": 180,
                        "description": "Timeout for manual mode (seconds)",
                    },
                },
                "required": ["url"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "analyze_ui":
        url = arguments["url"]
        mode = arguments.get("mode", "manual")
        timeout = arguments.get("timeout_seconds", 180)

        # Capture browser session
        video_path = await capture_browser_session(
            url=url,
            mode=mode,
            timeout_seconds=timeout,
        )

        # Analyze with Gemini
        critique = analyze_video(video_path)

        return [TextContent(type="text", text=critique)]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def run():
    """Entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
