"""Gmail API client wrapper."""

import base64
from pathlib import Path
from typing import Any

from googleapiclient.discovery import build

from .auth import get_credentials


class GmailClient:
    """Client for interacting with Gmail API."""

    def __init__(self):
        self._service = None

    @property
    def service(self):
        """Lazy initialization of Gmail API service."""
        if self._service is None:
            creds = get_credentials()
            self._service = build("gmail", "v1", credentials=creds)
        return self._service

    def search_emails(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        """
        Search emails using Gmail search syntax.

        Args:
            query: Gmail search query (e.g., "from:example@gmail.com", "has:attachment")
            max_results: Maximum number of results to return (default 10)

        Returns:
            List of email summaries with id, from, subject, date, snippet, has_attachments
        """
        results = self.service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get("messages", [])
        emails = []

        for msg in messages:
            email_data = self._get_email_summary(msg["id"])
            if email_data:
                emails.append(email_data)

        return emails

    def _get_email_summary(self, message_id: str) -> dict[str, Any] | None:
        """Get email summary (headers + snippet) for search results."""
        msg = self.service.users().messages().get(
            userId="me",
            id=message_id,
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}

        # Check for attachments
        has_attachments = self._has_attachments(msg.get("payload", {}))

        return {
            "id": message_id,
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "date": headers.get("Date", ""),
            "snippet": msg.get("snippet", ""),
            "has_attachments": has_attachments
        }

    def _has_attachments(self, payload: dict) -> bool:
        """Check if message has attachments."""
        parts = payload.get("parts", [])
        for part in parts:
            if part.get("filename"):
                return True
            # Check nested parts
            if self._has_attachments(part):
                return True
        return False

    def get_email(self, message_id: str) -> dict[str, Any]:
        """
        Get full email content by message ID.

        Args:
            message_id: Gmail message ID

        Returns:
            Email with id, from, to, subject, date, body, attachments
        """
        msg = self.service.users().messages().get(
            userId="me",
            id=message_id,
            format="full"
        ).execute()

        payload = msg.get("payload", {})
        headers = {h["name"]: h["value"] for h in payload.get("headers", [])}

        # Extract body (prefer text/plain)
        body = self._extract_body(payload)

        # Extract attachments info
        attachments = self._extract_attachments(payload)

        return {
            "id": message_id,
            "from": headers.get("From", ""),
            "to": headers.get("To", ""),
            "subject": headers.get("Subject", ""),
            "date": headers.get("Date", ""),
            "body": body,
            "attachments": attachments
        }

    def _extract_body(self, payload: dict, preferred_mime: str = "text/plain") -> str:
        """Extract email body, preferring text/plain."""
        mime_type = payload.get("mimeType", "")

        # Direct body
        if mime_type == preferred_mime:
            data = payload.get("body", {}).get("data", "")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

        # Check parts
        parts = payload.get("parts", [])

        # First pass: look for preferred mime type
        for part in parts:
            if part.get("mimeType") == preferred_mime:
                data = part.get("body", {}).get("data", "")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
            # Recurse into multipart
            if part.get("mimeType", "").startswith("multipart/"):
                body = self._extract_body(part, preferred_mime)
                if body:
                    return body

        # Second pass: try text/html if text/plain not found
        if preferred_mime == "text/plain":
            return self._extract_body(payload, "text/html")

        # Fallback: any text part
        for part in parts:
            if part.get("mimeType", "").startswith("text/"):
                data = part.get("body", {}).get("data", "")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

        return ""

    def _extract_attachments(self, payload: dict) -> list[dict[str, Any]]:
        """Extract attachment metadata from email."""
        attachments = []
        self._collect_attachments(payload, attachments)
        return attachments

    def _collect_attachments(self, payload: dict, attachments: list):
        """Recursively collect attachment info from message parts."""
        parts = payload.get("parts", [])

        for part in parts:
            filename = part.get("filename")
            if filename:
                body = part.get("body", {})
                attachments.append({
                    "id": body.get("attachmentId", ""),
                    "filename": filename,
                    "mime_type": part.get("mimeType", ""),
                    "size": body.get("size", 0)
                })
            # Recurse into nested parts
            self._collect_attachments(part, attachments)

    def download_attachment(
        self,
        message_id: str,
        attachment_id: str,
        save_path: str
    ) -> str:
        """
        Download email attachment to specified path.

        Args:
            message_id: Gmail message ID
            attachment_id: Attachment ID from get_email() result
            save_path: Path to save the attachment

        Returns:
            Absolute path to saved file
        """
        attachment = self.service.users().messages().attachments().get(
            userId="me",
            messageId=message_id,
            id=attachment_id
        ).execute()

        data = attachment.get("data", "")
        file_data = base64.urlsafe_b64decode(data)

        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(file_data)

        return str(save_path.resolve())
