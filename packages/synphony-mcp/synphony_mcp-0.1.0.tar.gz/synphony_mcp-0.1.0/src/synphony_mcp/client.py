"""HTTP client for Synphony API"""

import httpx
from typing import Optional, Any


class SynphonyClient:
    """Client for making authenticated requests to Synphony API"""

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json"
            }
        )

    async def request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make an authenticated request to the API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = await self.client.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    async def get(self, endpoint: str, **kwargs) -> dict:
        """GET request"""
        return await self.request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> dict:
        """POST request"""
        return await self.request("POST", endpoint, **kwargs)

    # Auth methods
    async def validate_api_key(self) -> dict:
        """Validate API key and get user info"""
        return await self.post("/auth")

    # Dataset methods
    async def list_datasets(self, limit: int = 20, cursor: Optional[str] = None) -> dict:
        """List user's datasets"""
        # TODO: Implement pagination when backend supports it
        return await self.post("/list")

    async def get_dataset(self, dataset_id: str) -> dict:
        """Get dataset details"""
        return await self.post("/status", json={"dataset_id": dataset_id})

    # Video methods
    async def search_videos(
        self,
        dataset_id: str,
        stage: Optional[str] = None,
        status: Optional[str] = None,
        name: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        limit: int = 20,
        cursor: Optional[str] = None
    ) -> dict:
        """Search videos with filters"""
        payload = {"dataset_id": dataset_id, "limit": limit}

        if stage:
            payload["stage"] = stage
        if status:
            payload["status"] = status
        if name:
            payload["name"] = name
        if created_after:
            payload["created_after"] = created_after
        if created_before:
            payload["created_before"] = created_before
        if cursor:
            payload["cursor"] = cursor

        return await self.post("/videos/search", json=payload)

    async def get_video(self, video_id: str) -> dict:
        """Get video details"""
        return await self.post("/videos/get", json={"video_id": video_id})

    # Processing methods
    async def multiply(
        self,
        dataset_id: str,
        input_video_ids: list[str],
        prompts: list[str],
        output_name_prefix: Optional[str] = None
    ) -> dict:
        """Generate video variations with prompts"""
        return await self.post("/multiply", json={
            "dataset_id": dataset_id,
            "file_ids": input_video_ids,
            "prompts": prompts
        })

    async def augment(
        self,
        dataset_id: str,
        input_video_ids: list[str],
        transforms: list[dict],
        output_name_prefix: Optional[str] = None
    ) -> dict:
        """Apply augmentations to videos"""
        return await self.post("/augment", json={
            "dataset_id": dataset_id,
            "file_ids": input_video_ids,
            "aug_list": transforms
        })

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
