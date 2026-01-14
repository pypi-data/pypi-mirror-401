"""Block Kit builder utilities for creating Slack message blocks."""

from typing import Optional, List, Dict, Any


class BlockKitBuilder:
    """Utility class for building Block Kit elements."""

    @staticmethod
    def header(text: str) -> Dict[str, Any]:
        """Create a header block."""
        return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": text
            }
        }

    @staticmethod
    def section(text: str, text_type: str = "mrkdwn") -> Dict[str, Any]:
        """Create a section block with text."""
        return {
            "type": "section",
            "text": {
                "type": text_type,
                "text": text
            }
        }

    @staticmethod
    def divider() -> Dict[str, Any]:
        """Create a divider block."""
        return {"type": "divider"}

    @staticmethod
    def fields_section(fields: List[str]) -> Dict[str, Any]:
        """Create a section block with multiple fields."""
        return {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": field
                }
                for field in fields
            ]
        }

    @staticmethod
    def context(elements: List[str]) -> Dict[str, Any]:
        """Create a context block with multiple text elements."""
        return {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": element
                }
                for element in elements
            ]
        }

    @staticmethod
    def image(image_url: str, alt_text: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Create an image block."""
        block = {
            "type": "image",
            "image_url": image_url,
            "alt_text": alt_text
        }
        if title:
            block["title"] = {
                "type": "plain_text",
                "text": title
            }
        return block

    @staticmethod
    def button(text: str, action_id: str, value: Optional[str] = None, url: Optional[str] = None, style: Optional[str] = None) -> Dict[str, Any]:
        """Create a button element."""
        element = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": text
            },
            "action_id": action_id
        }
        if value:
            element["value"] = value
        if url:
            element["url"] = url
        if style in ["primary", "danger"]:
            element["style"] = style
        return element

    @staticmethod
    def actions(*elements) -> Dict[str, Any]:
        """Create an actions block with interactive elements."""
        return {
            "type": "actions",
            "elements": list(elements)
        }

    @staticmethod
    def select_menu(placeholder: str, action_id: str, options: List[Dict[str, str]]) -> Dict[str, Any]:
        """Create a static select menu element."""
        return {
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "text": placeholder
            },
            "action_id": action_id,
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": option["text"]
                    },
                    "value": option["value"]
                }
                for option in options
            ]
        }

    @staticmethod
    def section_with_accessory(text: str, accessory: Dict[str, Any], text_type: str = "mrkdwn") -> Dict[str, Any]:
        """Create a section block with an accessory element."""
        return {
            "type": "section",
            "text": {
                "type": text_type,
                "text": text
            },
            "accessory": accessory
        }

    @staticmethod
    def code_block(code: str, language: Optional[str] = None) -> Dict[str, Any]:
        """Create a formatted code block."""
        formatted_code = f"```{language + chr(10) if language else ''}{code}```"
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": formatted_code
            }
        }

    @staticmethod
    def quote_block(text: str) -> Dict[str, Any]:
        """Create a quote block."""
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f">{text}"
            }
        }

    @staticmethod
    def rich_text_block(elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a rich text block with various formatting elements."""
        return {
            "type": "rich_text",
            "elements": elements
        }

    @staticmethod
    def rich_text_section(*elements) -> Dict[str, Any]:
        """Create a rich text section with inline elements."""
        return {
            "type": "rich_text_section",
            "elements": list(elements)
        }

    @staticmethod
    def rich_text_list(items: List[str], style: str = "bullet") -> Dict[str, Any]:
        """Create a rich text list (bullet or ordered)."""
        return {
            "type": "rich_text_list",
            "style": style,
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [{"type": "text", "text": item}]
                }
                for item in items
            ]
        }