"""Dropbox Paper MCP Server

Exposes Dropbox Paper capabilities via MCP protocol:
- Paper search
- Paper content viewing (markdown)
- Paper metadata viewing
- Create Paper from markdown
- OAuth 2.0 authorization flow for obtaining refresh tokens
"""

import os
from datetime import datetime

import dropbox
from dropbox.files import SearchOptions, FileCategory, ImportFormat, SearchOrderBy
from dropbox.oauth import DropboxOAuth2FlowNoRedirect
import dropbox.paper
import dropbox.common
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Initialize MCP server
mcp = FastMCP("Dropbox Paper MCP Server")


# Global client cache
_dbx_client_cache = None

# Global OAuth flow cache (for multi-step authorization)
_oauth_flow_cache = None


def get_dropbox_client() -> dropbox.Dropbox:
    """Get authenticated Dropbox client with team root configured if applicable.
    
    Supports two authentication modes:
    1. Refresh token mode (recommended): Uses DROPBOX_REFRESH_TOKEN, DROPBOX_APP_KEY, 
       and DROPBOX_APP_SECRET to automatically refresh access tokens.
    2. Access token mode (legacy): Uses DROPBOX_ACCESS_TOKEN directly.
    """
    global _dbx_client_cache
    if _dbx_client_cache:
        return _dbx_client_cache

    # Try refresh token mode first (recommended)
    refresh_token = os.environ.get("DROPBOX_REFRESH_TOKEN")
    app_key = os.environ.get("DROPBOX_APP_KEY")
    app_secret = os.environ.get("DROPBOX_APP_SECRET")
    
    if refresh_token and app_key:
        # Use refresh token - SDK will automatically handle token refresh
        dbx = dropbox.Dropbox(
            oauth2_refresh_token=refresh_token,
            app_key=app_key,
            app_secret=app_secret,  # Optional if using PKCE
        )
    else:
        # Fall back to access token mode
        token = os.environ.get("DROPBOX_ACCESS_TOKEN")
        if not token:
            raise ValueError(
                "Either DROPBOX_REFRESH_TOKEN + DROPBOX_APP_KEY, "
                "or DROPBOX_ACCESS_TOKEN must be set"
            )
        dbx = dropbox.Dropbox(token)

    # Configure path root to access full team space if applicable
    try:
        account = dbx.users_get_current_account()
        if account.root_info and account.root_info.root_namespace_id:
            dbx = dbx.with_path_root(
                dropbox.common.PathRoot.root(account.root_info.root_namespace_id)
            )
    except Exception:
        # Fallback to default if we can't get account info or set root
        pass

    _dbx_client_cache = dbx
    return dbx


@mcp.tool
def oauth_get_auth_url(app_key: str, app_secret: str | None = None) -> str:
    """
    Start OAuth 2.0 authorization flow and get the authorization URL.
    
    This is the first step to obtain a refresh token. After calling this tool:
    1. Open the returned URL in a browser
    2. Authorize the application
    3. Copy the authorization code
    4. Call oauth_exchange_code with the code to get your refresh token
    
    Args:
        app_key: Your Dropbox app key (from https://www.dropbox.com/developers/apps)
        app_secret: Your Dropbox app secret (optional if using PKCE)
    
    Returns:
        Authorization URL to open in a browser
    """
    global _oauth_flow_cache
    
    # Create OAuth flow with offline access to get refresh token
    _oauth_flow_cache = DropboxOAuth2FlowNoRedirect(
        consumer_key=app_key,
        consumer_secret=app_secret,
        token_access_type='offline',  # This ensures we get a refresh token
    )
    
    authorize_url = _oauth_flow_cache.start()
    
    return f"""## OAuth Authorization Flow Started

**Step 1:** Open this URL in your browser:
{authorize_url}

**Step 2:** Authorize the application and copy the authorization code.

**Step 3:** Call `oauth_exchange_code` with the authorization code to get your refresh token.

> **Note:** The authorization code expires quickly, so complete step 3 promptly.
"""


@mcp.tool
def oauth_exchange_code(authorization_code: str) -> str:
    """
    Exchange an authorization code for a refresh token.
    
    This is the second step of the OAuth flow. You must call oauth_get_auth_url first.
    
    Args:
        authorization_code: The authorization code from Dropbox (copied from browser)
    
    Returns:
        The refresh token and instructions for using it
    """
    global _oauth_flow_cache
    
    if not _oauth_flow_cache:
        return """**Error:** No active OAuth flow found.

Please call `oauth_get_auth_url` first to start the authorization flow.
"""
    
    try:
        oauth_result = _oauth_flow_cache.finish(authorization_code.strip())
        
        # Clear the flow cache
        _oauth_flow_cache = None
        
        # Format the result
        return f"""## OAuth Authorization Successful! 🎉

**Your Refresh Token:**
```
{oauth_result.refresh_token}
```

**Your Access Token** (short-lived, for reference):
```
{oauth_result.access_token}
```

**Account ID:** {oauth_result.account_id}
**Token Expiration:** {oauth_result.expires_at}

---

### How to Use

Add these to your `.env` file:

```bash
DROPBOX_REFRESH_TOKEN={oauth_result.refresh_token}
DROPBOX_APP_KEY=<your_app_key>
DROPBOX_APP_SECRET=<your_app_secret>
```

You can remove the old `DROPBOX_ACCESS_TOKEN` line. The refresh token won't expire and the SDK will automatically refresh access tokens as needed.
"""
    except Exception as e:
        _oauth_flow_cache = None
        return f"""**Error exchanging authorization code:** {e}

Please try again by calling `oauth_get_auth_url` to start a new flow.
"""


@mcp.tool
def paper_search(
    query: str,
    path_scope: str | None = None,
    order_by: str = "relevance",
    modified_after: str | None = None,
    max_results: int = 20,
) -> str:
    """
    Search for Dropbox Paper documents.

    Args:
        query: Search keywords
        path_scope: Optional path to limit search (e.g., "/Teams/Marketing")
        order_by: Sort order: "relevance" (default) or "last_modified_time"
        modified_after: Only return docs modified after this date (YYYY-MM-DD)
        max_results: Maximum number of results (default 20, max 100)

    Returns:
        List of matching documents with paths and names
    """
    dbx = get_dropbox_client()

    # Resolve order_by enum
    if order_by == "last_modified_time":
        order_arg = SearchOrderBy.last_modified_time
    else:
        order_arg = SearchOrderBy.relevance

    # Configure search options
    options = SearchOptions(
        path=path_scope,
        max_results=min(max_results, 100),
        file_categories=[FileCategory.paper],
        order_by=order_arg,
    )

    try:
        # Parse date if provided
        min_date = None
        if modified_after:
            try:
                min_date = datetime.strptime(modified_after, "%Y-%m-%d")
            except ValueError:
                return "Error: modified_after must be in YYYY-MM-DD format"

        result = dbx.files_search_v2(query, options=options)

        if not result.matches:
            return "No matching Paper documents found"

        output = []
        count = 0
        for match in result.matches:
            metadata = match.metadata.get_metadata()
            
            # Apply date filter
            if min_date and hasattr(metadata, "server_modified"):
                # server_modified is usually naive datetime from dropbox sdk, but let's compare safely
                # Dropbox SDK returns datetime objects. We assume they are comparable.
                if metadata.server_modified < min_date:
                    continue

            output.append(
                f"- **{metadata.name}**\n  Path: `{metadata.path_display}`\n  Modified: {metadata.server_modified}"
            )
            count += 1

        if count == 0:
            return f"Found matching docs, but none were modified after {modified_after}"

        return f"Found {count} results:\n\n" + "\n".join(output)
    except dropbox.exceptions.ApiError as e:
        return f"Search failed: {e}"


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
        return result[1].content.decode("utf-8")
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
def paper_list(
    filter_by: str = "docs_accessed",
    sort_by: str = "accessed",
    sort_order: str = "descending",
    limit: int = 50,
) -> str:
    """
    List Paper documents.

    Args:
        filter_by: Filter criteria. "docs_accessed" (default) or "docs_created".
        sort_by: Sort field. "accessed" (default), "modified", or "created".
        sort_order: Sort order. "descending" (default) or "ascending".
        limit: Maximum number of documents to return (default 50)

    Returns:
        List of Paper documents
    """
    dbx = get_dropbox_client()

    # Resolve enums
    filter_arg = (
        dropbox.paper.ListPaperDocsFilterBy.docs_created
        if filter_by == "docs_created"
        else dropbox.paper.ListPaperDocsFilterBy.docs_accessed
    )

    sort_by_arg = getattr(
        dropbox.paper.ListPaperDocsSortBy, sort_by, dropbox.paper.ListPaperDocsSortBy.accessed
    )

    sort_order_arg = (
        dropbox.paper.ListPaperDocsSortOrder.ascending
        if sort_order == "ascending"
        else dropbox.paper.ListPaperDocsSortOrder.descending
    )

    try:
        result = dbx.paper_docs_list(
            filter_by=filter_arg,
            sort_by=sort_by_arg,
            sort_order=sort_order_arg,
            limit=min(limit, 1000),
        )

        if not result.doc_ids:
            return "No Paper documents found"

        output = [
            f"Found {len(result.doc_ids)} Paper documents (Filter: {filter_by}, Sort: {sort_by} {sort_order}):\n"
        ]
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

