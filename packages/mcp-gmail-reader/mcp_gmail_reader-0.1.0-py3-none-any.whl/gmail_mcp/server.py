"""Gmail MCP Server - FastMCP server with Gmail tools."""

from mcp.server.fastmcp import FastMCP

from .gmail_client import GmailClient

# Create MCP server
mcp = FastMCP("gmail")

# Lazy-initialized client
_client: GmailClient | None = None


def get_client() -> GmailClient:
    """Get or create Gmail client instance."""
    global _client
    if _client is None:
        _client = GmailClient()
    return _client


@mcp.tool()
def search_emails(query: str, max_results: int = 10) -> list[dict]:
    """
    Search Gmail using Gmail search syntax.

    Args:
        query: Gmail search query. Examples:
            - "from:example@gmail.com" - emails from specific sender
            - "subject:invoice" - emails with subject containing "invoice"
            - "has:attachment" - emails with attachments
            - "after:2024/01/01" - emails after date
            - "is:unread" - unread emails
            - "label:important" - emails with specific label
        max_results: Maximum number of results (default 10, max 100)

    Returns:
        List of email summaries with: id, from, subject, date, snippet, has_attachments
    """
    client = get_client()
    return client.search_emails(query, min(max_results, 100))


@mcp.tool()
def get_email(message_id: str) -> dict:
    """
    Get full email content by message ID.

    Args:
        message_id: Gmail message ID (from search_emails results)

    Returns:
        Email with: id, from, to, subject, date, body, attachments
        Attachments include: id, filename, mime_type, size
    """
    client = get_client()
    return client.get_email(message_id)


@mcp.tool()
def download_attachment(message_id: str, attachment_id: str, save_path: str) -> str:
    """
    Download email attachment to specified path.

    Args:
        message_id: Gmail message ID
        attachment_id: Attachment ID (from get_email attachments list)
        save_path: Full path where to save the attachment

    Returns:
        Absolute path to the saved file
    """
    client = get_client()
    return client.download_attachment(message_id, attachment_id, save_path)
