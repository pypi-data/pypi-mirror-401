"""TMail API Python wrapper.

This mirrors the JavaScript `tmail.js` API from the original project:
- `domains()`
- `create(email='')`
- `messages(email)`
- `delete_message(msg_id)`

It is a tiny, synchronous wrapper around `requests`.
"""
from urllib.parse import quote_plus
import requests
import re
from html import unescape


class TMail:
    def __init__(self, base: str, key: str):
        self.base = base.rstrip('/')
        self.key = key
        self.session = requests.Session()

    def domains(self):
        """Fetch available domains."""
        resp = self.session.get(f"{self.base}/domains/{self.key}")
        resp.raise_for_status()
        return resp.json()

    def create(self, email: str = ''):
        """Create a random or custom email. If `email` is empty, creates random."""
        email_q = quote_plus(email)
        resp = self.session.get(f"{self.base}/email/{email_q}/{self.key}")
        resp.raise_for_status()
        return resp.json()

    def raw_messages(self, email: str):
        """Get messages for `email`."""
        email_q = quote_plus(email)
        resp = self.session.get(f"{self.base}/messages/{email_q}/{self.key}")
        resp.raise_for_status()
        return resp.json()

    def delete_message(self, msg_id):
        """Delete a message by id."""
        resp = self.session.delete(f"{self.base}/message/{msg_id}/{self.key}")
        resp.raise_for_status()
        return resp.json()

    def _clean_html(self, html_content: str) -> str:
        """Strip HTML, scripts/styles and collapse whitespace."""
        if not html_content:
            return ""
        # remove script/style blocks
        text = re.sub(r'<script.*?</script>', '', html_content, flags=re.S | re.I)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.S | re.I)
        # strip tags
        text = re.sub(r'<[^>]+>', '', text)
        # unescape HTML entities
        text = unescape(text)
        # collapse whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _extract_links(self, html_content: str) -> list:
        """Extract links from HTML content."""
        if not html_content:
            return []
        # find all links, including those with other attributes
        links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', html_content, re.I)
        return links

    def clean_message(self, msg: dict) -> dict:
        """Return a cleaned, normalized message dict from raw API message."""
        html_content = msg.get('content', '')
        subject = msg.get('subject', '')
        sender_name = msg.get('sender_name', '').lower()

        cleaned_msg = {
            'id': msg.get('id'),
            'subject': subject,
            'sender_name': msg.get('sender_name'),
            'sender_email': msg.get('sender_email'),
            'date': msg.get('date'),
            'age': msg.get('datediff'),
            'attachments': msg.get('attachments', []),
            'content': self._clean_html(html_content),
            #'links': self._extract_links(html_content)
            'discord': {}
        }

        is_discord_verification = (
            sender_name == 'discord' and subject == 'Verify Email Address for Discord'
        )

        is_discord_password_reset = (
            sender_name == 'discord' and subject == 'Password Reset Request for Discord'
        )

        if is_discord_verification:
            match = re.search(r'<a[^>]*href="([^"]*)"[^>]*>\s*Verify Email\s*</a>', html_content, re.I)
            if match:
                cleaned_msg['discord']['verification_link'] = match.group(1)

        if is_discord_password_reset:
            match = re.search(r'<a[^>]*href="([^"]*)"[^>]*>\s*Reset Password\s*</a>', html_content, re.I)
            if match:
                cleaned_msg['discord']['password_reset_link'] = match.group(1)

        return cleaned_msg

    def clean_messages(self, email: str):
        """Fetch messages for `email` and return cleaned versions."""
        raw = self.raw_messages(email)
        return [self.clean_message(m) for m in raw]
