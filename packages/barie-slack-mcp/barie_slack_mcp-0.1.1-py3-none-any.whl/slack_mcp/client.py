"""Slack API client for interacting with Slack Web API."""
import os
import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
import httpx
import traceback


logger = logging.getLogger(__name__)


class SlackClient:
    """Client for interacting with Slack Web API."""

    def __init__(self, api_token: str, workspace_id: Optional[str] = None, file_storage_path: str = None):
        self.api_token = api_token
        self.workspace_id = workspace_id
        self.base_url = "https://slack.com/api"
        self.file_storage_path = file_storage_path

        if not self.api_token:
            raise ValueError("Slack API token is required")

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        form_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the Slack API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., "conversations.list")
            params: Query parameters or form data (for multipart/form-data)
            json_data: JSON body data
            form_data: Form data for multipart/form-data requests
        """
        try:
            url = f"{self.base_url}/{endpoint}"
            headers = {"Authorization": f"Bearer {self.api_token}"}

            async with httpx.AsyncClient() as client:
                # Use form_data for multipart/form-data (file uploads)
                if form_data:
                    response = await client.request(
                        method, url, headers=headers, data=form_data, timeout=60.0
                    )
                # Use json_data for JSON requests
                elif json_data:
                    headers["Content-Type"] = "application/json"
                    response = await client.request(
                        method, url, headers=headers, json=json_data, timeout=30.0
                    )
                # Use params for query parameters (GET requests)
                else:
                    response = await client.request(
                        method, url, headers=headers, params=params, timeout=30.0
                    )

                data = response.json()
                logger.warning(f"Slack API Response: {data}")
                if not data.get("ok", False):
                    error_msg = data.get("error", "Unknown error")
                    raise Exception(f"Slack API error: {error_msg}")

                return data
        
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def list_channels(
        self, types: Optional[List[str]] = None, exclude_archived: bool = True, limit: int = 100
    ) -> Dict[str, Any]:
        """List all channels in the workspace."""
        try:
            params = {"exclude_archived": exclude_archived, "limit": limit}

            if types:
                params["types"] = ",".join(types)

                return await self._make_request("GET", "conversations.list", params=params)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def get_channel_info(self, channel_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific channel."""
        try:
            params = {"channel": channel_id}
            return await self._make_request("GET", "conversations.info", params=params)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def list_users(self, limit: int = 100, include_locale: bool = False) -> Dict[str, Any]:
        """List all users in the workspace."""
        try:
            params = {"limit": limit, "include_locale": include_locale}
            return await self._make_request("GET", "users.list", params=params)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific user."""
        try:
            params = {"user": user_id}
            return await self._make_request("GET", "users.info", params=params)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def send_message(
        self, channel: str, text: str, thread_ts: Optional[str] = None, blocks: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Send a message to a channel."""
        try:
            data = {"channel": channel, "text": text}

            if thread_ts:
                data["thread_ts"] = thread_ts

            if blocks:
                data["blocks"] = blocks

            return await self._make_request("POST", "chat.postMessage", json_data=data)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def update_message(
        self, channel: str, ts: str, text: str, blocks: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Update an existing message."""
        try:
            data = {"channel": channel, "ts": ts, "text": text}

            if blocks:
                data["blocks"] = blocks

            return await self._make_request("POST", "chat.update", json_data=data)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def delete_message(self, channel: str, ts: str) -> Dict[str, Any]:
        """Delete a message from a channel."""
        try:
            data = {"channel": channel, "ts": ts}
            return await self._make_request("POST", "chat.delete", json_data=data)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def get_channel_history(
        self,
        channel: str,
        limit: int = 100,
        oldest: Optional[str] = None,
        latest: Optional[str] = None,
        inclusive: bool = True,
    ) -> Dict[str, Any]:
        """Get message history for a channel."""
        try:
            params = {"channel": channel, "limit": limit, "inclusive": inclusive}

            if oldest:
                params["oldest"] = oldest

            if latest:
                params["latest"] = latest

            return await self._make_request("GET", "conversations.history", params=params)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def search_messages(
        self, query: str, sort: str = "timestamp", sort_dir: str = "desc", count: int = 20
    ) -> Dict[str, Any]:
        """Search for messages across the workspace."""
        try:
            params = {"query": query, "sort": sort, "sort_dir": sort_dir, "count": count}
            return await self._make_request("GET", "search.messages", params=params)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def upload_file(
        self,
        channels: List[str],
        file_name: str,
        title: Optional[str] = None,
        initial_comment: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload a file to one or more channels using the modern 3-step process.
        
        This follows Slack's recommended approach:
        1. Get upload URL from files.getUploadURLExternal
        2. POST file content to the upload URL
        3. Complete upload with files.completeUploadExternal
        
        Args:
            channels: List of channel IDs where the file will be shared
            file_name: Name of the file to upload
            title: Optional title for the file (displayed in Slack)
            initial_comment: Optional message text introducing the file in the channel
        
        Note: Requires files:write scope.
        """
        try:
            if os.path.isabs(file_name):
                file_path = file_name.replace('/home/workspace', self.file_storage_path)
            else:
                file_path = os.path.join(self.file_storage_path, file_name)

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            read_result = open(file_path, 'rb').read()
            if isinstance(read_result, str):
                file_bytes = read_result.encode('utf-8')
            elif isinstance(read_result, bytes):
                file_bytes = read_result
            else:
                raise Exception(f"Unexpected file content type: {type(read_result)}")
            
            file_length = len(file_bytes)
            
            # Get upload URL using multipart/form-data
            upload_form_data = {
                "filename": file_name,
                "length": str(file_length)
            }
            upload_response = await self._make_request("POST", "files.getUploadURLExternal", form_data=upload_form_data)
            
            if not upload_response.get("ok"):
                raise Exception(f"Failed to get upload URL: {upload_response.get('error', 'Unknown error')}")
            
            upload_url = upload_response["upload_url"]
            file_id = upload_response["file_id"]
            
            # Step 2: Upload file content to the URL
            async with httpx.AsyncClient() as client:
                upload_headers = {"Content-Type": "application/octet-stream"}
                upload_response_http = await client.post(
                    upload_url,
                    content=file_bytes,
                    headers=upload_headers,
                    timeout=60.0
                )
                upload_response_http.raise_for_status()
            
            # Step 3: Complete the upload
            files_data = [{"id": file_id}]
            if title:
                files_data[0]["title"] = title
            
            complete_form_data = {
                "files": json.dumps(files_data),
            }
            
            # Handle channel(s) - can be single channel_id or comma-separated channels
            if len(channels) == 1:
                complete_form_data["channel_id"] = channels[0]
            else:
                complete_form_data["channels"] = ",".join(channels)
            
            if initial_comment:
                complete_form_data["initial_comment"] = initial_comment
            
            return await self._make_request("POST", "files.completeUploadExternal", form_data=complete_form_data)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def get_team_info(self) -> Dict[str, Any]:
        """Get information about the Slack workspace/team."""
        try:
            return await self._make_request("GET", "team.info")
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def create_channel(self, name: str, is_private: bool = False) -> Dict[str, Any]:
        """Create a new channel."""
        try:
            data = {"name": name, "is_private": is_private}
            return await self._make_request("POST", "conversations.create", json_data=data)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def archive_channel(self, channel: str) -> Dict[str, Any]:
        """Archive a channel."""
        try:
            data = {"channel": channel}
            return await self._make_request("POST", "conversations.archive", json_data=data)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def unarchive_channel(self, channel: str) -> Dict[str, Any]:
        """Unarchive a channel."""
        try:
            data = {"channel": channel}
            return await self._make_request("POST", "conversations.unarchive", json_data=data)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def invite_to_channel(self, channel: str, users: List[str]) -> Dict[str, Any]:
        """Invite users to a channel."""
        try:
            data = {"channel": channel, "users": ",".join(users)}
            return await self._make_request("POST", "conversations.invite", json_data=data)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def set_channel_topic(self, channel: str, topic: str) -> Dict[str, Any]:
        """Set the topic for a channel."""
        try:
            data = {"channel": channel, "topic": topic}
            return await self._make_request("POST", "conversations.setTopic", json_data=data)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")

    async def set_channel_purpose(self, channel: str, purpose: str) -> Dict[str, Any]:
        """Set the purpose for a channel."""
        try:
            data = {"channel": channel, "purpose": purpose}
            return await self._make_request("POST", "conversations.setPurpose", json_data=data)
        except:
            logger.error(f"Slack API error: {traceback.format_exc()}")
            raise Exception(f"Slack API error: {traceback.format_exc()}")