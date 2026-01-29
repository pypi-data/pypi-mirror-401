"""MCP server entry point."""

from fastmcp import FastMCP

from youtube_mcp.transcript import get_transcript
from youtube_mcp.video_info import get_video_info

mcp = FastMCP("youtube")

mcp.tool()(get_transcript)
mcp.tool()(get_video_info)


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
