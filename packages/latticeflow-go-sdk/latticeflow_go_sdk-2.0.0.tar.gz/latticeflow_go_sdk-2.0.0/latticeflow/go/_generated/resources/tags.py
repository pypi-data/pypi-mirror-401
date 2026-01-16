from __future__ import annotations

from latticeflow.go._generated.api.tags.create_tag import asyncio as create_tag_asyncio
from latticeflow.go._generated.api.tags.create_tag import sync as create_tag_sync
from latticeflow.go._generated.api.tags.delete_tag import asyncio as delete_tag_asyncio
from latticeflow.go._generated.api.tags.delete_tag import sync as delete_tag_sync
from latticeflow.go._generated.api.tags.get_tags import asyncio as get_tags_asyncio
from latticeflow.go._generated.api.tags.get_tags import sync as get_tags_sync
from latticeflow.go._generated.api.tags.update_tag import asyncio as update_tag_asyncio
from latticeflow.go._generated.api.tags.update_tag import sync as update_tag_sync
from latticeflow.go._generated.models.model import Error
from latticeflow.go._generated.models.model import StoredTag
from latticeflow.go._generated.models.model import StoredTags
from latticeflow.go._generated.models.model import Success
from latticeflow.go._generated.models.model import Tag
from latticeflow.go.base import BaseClient
from latticeflow.go.types import ApiError


class TagsResource:
    def __init__(self, base_client: BaseClient) -> None:
        self._base = base_client

    def delete_tag(self, tag_id: str) -> Success:
        """Delete a tag

        Args:
            tag_id (str):
        """
        with self._base.get_client() as client:
            response = delete_tag_sync(tag_id=tag_id, client=client)
            if isinstance(response, Error):
                raise ApiError(response)
            return response

    def create_tag(self, body: Tag) -> StoredTag:
        """Create a new tag.

        Args:
            body (Tag):
        """
        with self._base.get_client() as client:
            response = create_tag_sync(body=body, client=client)
            if isinstance(response, Error):
                raise ApiError(response)
            return response

    def get_tags(self) -> StoredTags:
        """Get all tags."""
        with self._base.get_client() as client:
            response = get_tags_sync(client=client)
            if isinstance(response, Error):
                raise ApiError(response)
            return response

    def update_tag(self, tag_id: str, body: Tag) -> StoredTag:
        """Update a tag by its ID.

        Args:
            tag_id (str):
            body (Tag):
        """
        with self._base.get_client() as client:
            response = update_tag_sync(tag_id=tag_id, body=body, client=client)
            if isinstance(response, Error):
                raise ApiError(response)
            return response


class AsyncTagsResource:
    def __init__(self, base_client: BaseClient) -> None:
        self._base = base_client

    async def delete_tag(self, tag_id: str) -> Success:
        """Delete a tag

        Args:
            tag_id (str):
        """
        with self._base.get_client() as client:
            response = await delete_tag_asyncio(tag_id=tag_id, client=client)
            if isinstance(response, Error):
                raise ApiError(response)
            return response

    async def create_tag(self, body: Tag) -> StoredTag:
        """Create a new tag.

        Args:
            body (Tag):
        """
        with self._base.get_client() as client:
            response = await create_tag_asyncio(body=body, client=client)
            if isinstance(response, Error):
                raise ApiError(response)
            return response

    async def get_tags(self) -> StoredTags:
        """Get all tags."""
        with self._base.get_client() as client:
            response = await get_tags_asyncio(client=client)
            if isinstance(response, Error):
                raise ApiError(response)
            return response

    async def update_tag(self, tag_id: str, body: Tag) -> StoredTag:
        """Update a tag by its ID.

        Args:
            tag_id (str):
            body (Tag):
        """
        with self._base.get_client() as client:
            response = await update_tag_asyncio(tag_id=tag_id, body=body, client=client)
            if isinstance(response, Error):
                raise ApiError(response)
            return response
