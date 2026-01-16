"""Dropbox Paper MCP Server

Exposes Dropbox Paper capabilities via MCP protocol:
- Paper search
- Paper content viewing (markdown)
- Paper metadata viewing
- Create Paper from markdown
"""

import os

import dropbox
from dropbox.files import SearchOptions, FileCategory, ImportFormat
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Initialize MCP server
mcp = FastMCP("Dropbox Paper MCP Server")


def get_dropbox_client() -> dropbox.Dropbox:
    """Get authenticated Dropbox client."""
    token = os.environ.get("DROPBOX_ACCESS_TOKEN")
    if not token:
        raise ValueError("DROPBOX_ACCESS_TOKEN environment variable is not set")
    return dropbox.Dropbox(token)


@mcp.tool
def paper_search(query: str, max_results: int = 20) -> str:
    """
    Search for Dropbox Paper documents.

    Args:
        query: Search keywords
        max_results: Maximum number of results (default 20, max 100)

    Returns:
        List of matching documents with paths and names
    """
    dbx = get_dropbox_client()

    # Configure search options to filter for Paper documents
    options = SearchOptions(
        max_results=min(max_results, 100),
        file_categories=[FileCategory.paper],
    )

    result = dbx.files_search_v2(query, options=options)

    if not result.matches:
        return "No matching Paper documents found"

    output = []
    for match in result.matches:
        metadata = match.metadata.get_metadata()
        output.append(f"- **{metadata.name}**\n  Path: `{metadata.path_display}`")

    return f"Found {len(result.matches)} results:\n\n" + "\n".join(output)


@mcp.tool
def paper_get_content(path: str) -> str:
    """
    Get Paper document content in Markdown format.

    Args:
        path: Path to the Paper document, e.g. "/Documents/my_paper.paper"

    Returns:
        Paper document content in Markdown format
    """
    dbx = get_dropbox_client()

    try:
        # Use files_export with markdown format
        result = dbx.files_export(path, export_format="markdown")
        return result[1].text
    except dropbox.exceptions.ApiError as e:
        return f"Failed to get document content: {e}"


@mcp.tool
def paper_get_metadata(path: str) -> str:
    """
    Get Paper document metadata.

    Args:
        path: Path to the Paper document, e.g. "/Documents/my_paper.paper"

    Returns:
        Document metadata including name, size, modification time, etc.
    """
    dbx = get_dropbox_client()

    try:
        metadata = dbx.files_get_metadata(path)

        info = [
            f"**Name**: {metadata.name}",
            f"**Path**: {metadata.path_display}",
            f"**ID**: {metadata.id}",
        ]

        # FileMetadata specific fields
        if hasattr(metadata, "size"):
            info.append(f"**Size**: {metadata.size} bytes")
        if hasattr(metadata, "client_modified"):
            info.append(f"**Client Modified**: {metadata.client_modified}")
        if hasattr(metadata, "server_modified"):
            info.append(f"**Server Modified**: {metadata.server_modified}")
        if hasattr(metadata, "content_hash"):
            info.append(f"**Content Hash**: {metadata.content_hash}")

        return "\n".join(info)

    except dropbox.exceptions.ApiError as e:
        return f"Failed to get metadata: {e}"


@mcp.tool
def paper_create(path: str, content: str) -> str:
    """
    Create a new Paper document from Markdown content.

    Args:
        path: Full path for the new document, must end with .paper, e.g. "/Documents/new_doc.paper"
        content: Document content in Markdown format

    Returns:
        Creation result information
    """
    dbx = get_dropbox_client()

    # Ensure path ends with .paper
    if not path.endswith(".paper"):
        path = path + ".paper"

    try:
        result = dbx.files_paper_create(
            content.encode("utf-8"),
            path,
            ImportFormat.markdown,
        )

        return f"Paper document created successfully!\n\n**Path**: {result.url}\n**File ID**: {result.result_path}"

    except dropbox.exceptions.ApiError as e:
        return f"Creation failed: {e}"


@mcp.tool
def paper_list(limit: int = 50) -> str:
    """
    List all Paper documents.

    Args:
        limit: Maximum number of documents to return (default 50)

    Returns:
        List of Paper documents
    """
    dbx = get_dropbox_client()

    try:
        result = dbx.paper_docs_list(limit=min(limit, 1000))

        if not result.doc_ids:
            return "No Paper documents found"

        output = [f"Found {len(result.doc_ids)} Paper documents:\n"]
        for doc_id in result.doc_ids[:limit]:
            output.append(f"- `{doc_id}`")

        return "\n".join(output)

    except dropbox.exceptions.ApiError as e:
        return f"Failed to list documents: {e}"


@mcp.tool
def list_folder(path: str = "") -> str:
    """
    List files and folders in a directory.

    Args:
        path: Path to the folder, e.g. "/Documents". Use "" for root.

    Returns:
        List of files and folders in the directory
    """
    dbx = get_dropbox_client()

    try:
        result = dbx.files_list_folder(path)

        if not result.entries:
            return "Folder is empty"

        output = [f"Contents of `{path or '/'}`:\n"]
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                output.append(f"📁 **{entry.name}/**")
            elif isinstance(entry, dropbox.files.FileMetadata):
                size = f" ({entry.size} bytes)" if entry.size else ""
                paper = " 📄" if entry.name.endswith(".paper") else ""
                output.append(f"📄 {entry.name}{paper}{size}")

        return "\n".join(output)

    except dropbox.exceptions.ApiError as e:
        return f"Failed to list folder: {e}"

