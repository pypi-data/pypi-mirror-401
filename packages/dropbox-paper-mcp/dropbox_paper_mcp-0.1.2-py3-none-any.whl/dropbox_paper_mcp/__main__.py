"""CLI entry point for Dropbox Paper MCP Server."""

from dropbox_paper_mcp import mcp


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
