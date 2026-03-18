"""Pagination helpers for Trix SDK."""

import json
import logging
from typing import Any, AsyncIterator, Callable, Dict, Iterator, Optional, TypeVar

T = TypeVar("T")

logger = logging.getLogger(__name__)

# Maximum size for duplicate detection set to prevent memory issues
MAX_SEEN_IDS_SIZE = 100_000

# Number of consecutive all-duplicate pages before stopping
MAX_DUPLICATE_PAGES = 3


def _get_item_id(item: Any) -> str:
    """Extract a unique ID from an item for duplicate detection."""
    if isinstance(item, dict):
        if "id" in item and isinstance(item["id"], str):
            return item["id"]
        if "_id" in item and isinstance(item["_id"], str):
            return item["_id"]
    elif hasattr(item, "id") and isinstance(item.id, str):
        return item.id
    elif hasattr(item, "_id") and isinstance(item._id, str):
        return item._id
    return json.dumps(item, sort_keys=True, default=str)


class SyncPaginator:
    """Iterator for paginated list endpoints (sync)."""

    def __init__(
        self,
        fetch_func: Callable[..., Any],
        initial_params: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        max_items: Optional[int] = None,
    ) -> None:
        """
        Initialize paginator.

        Args:
            fetch_func: Function to call for fetching pages
            initial_params: Initial parameters for the request
            limit: Number of items per page
            max_items: Maximum total items to fetch (None for unlimited)
        """
        self._fetch_func = fetch_func
        self._params = initial_params or {}
        self._params["limit"] = limit
        self._limit = limit
        self._max_items = max_items
        self._items_fetched = 0

    def __iter__(self) -> Iterator[Any]:
        """Iterate through all pages."""
        offset = self._params.get("offset", 0)
        cursor = self._params.get("cursor")
        seen_ids: set[str] = set()
        consecutive_dup_pages = 0

        while True:
            # Check if we've reached max items
            if self._max_items and self._items_fetched >= self._max_items:
                break

            # Adjust limit if we're near max_items
            if self._max_items:
                remaining = self._max_items - self._items_fetched
                current_limit = min(self._limit, remaining)
                self._params["limit"] = current_limit

            # Fetch page
            if cursor is not None:
                self._params["cursor"] = cursor
            else:
                self._params["offset"] = offset

            response = self._fetch_func(**self._params)

            # Convert pydantic model to dict if needed
            if hasattr(response, "model_dump"):
                response = response.model_dump()

            # Handle different response formats
            if isinstance(response, dict) and "data" in response:
                items = response["data"]
            else:
                items = response

            if not items:
                break

            # Yield items, skipping duplicates
            duplicates_in_page = 0
            for item in items:
                item_id = _get_item_id(item)
                if item_id in seen_ids:
                    duplicates_in_page += 1
                    continue
                if len(seen_ids) < MAX_SEEN_IDS_SIZE:
                    seen_ids.add(item_id)
                yield item
                self._items_fetched += 1
                if self._max_items and self._items_fetched >= self._max_items:
                    return

            # Detect infinite loop: entire page was duplicates
            if len(items) > 0 and duplicates_in_page == len(items):
                consecutive_dup_pages += 1
                if consecutive_dup_pages >= MAX_DUPLICATE_PAGES:
                    logger.warning(
                        "Pagination stopped: detected %d consecutive pages of "
                        "duplicate items. This may indicate an API pagination issue.",
                        MAX_DUPLICATE_PAGES,
                    )
                    break
            else:
                consecutive_dup_pages = 0

            # Check for next page
            if isinstance(response, dict) and "cursor" in response and response["cursor"]:
                cursor = response["cursor"]
            elif len(items) < self._limit:
                # No more pages
                break
            else:
                offset += len(items)


class AsyncPaginator:
    """Async iterator for paginated list endpoints."""

    def __init__(
        self,
        fetch_func: Callable[..., Any],
        initial_params: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        max_items: Optional[int] = None,
    ) -> None:
        """
        Initialize async paginator.

        Args:
            fetch_func: Async function to call for fetching pages
            initial_params: Initial parameters for the request
            limit: Number of items per page
            max_items: Maximum total items to fetch (None for unlimited)
        """
        self._fetch_func = fetch_func
        self._params = initial_params or {}
        self._params["limit"] = limit
        self._limit = limit
        self._max_items = max_items
        self._items_fetched = 0

    async def __aiter__(self) -> AsyncIterator[Any]:
        """Async iterate through all pages."""
        offset = self._params.get("offset", 0)
        cursor = self._params.get("cursor")
        seen_ids: set[str] = set()
        consecutive_dup_pages = 0

        while True:
            # Check if we've reached max items
            if self._max_items and self._items_fetched >= self._max_items:
                break

            # Adjust limit if we're near max_items
            if self._max_items:
                remaining = self._max_items - self._items_fetched
                current_limit = min(self._limit, remaining)
                self._params["limit"] = current_limit

            # Fetch page
            if cursor is not None:
                self._params["cursor"] = cursor
            else:
                self._params["offset"] = offset

            response = await self._fetch_func(**self._params)

            # Convert pydantic model to dict if needed
            if hasattr(response, "model_dump"):
                response = response.model_dump()

            # Handle different response formats
            if isinstance(response, dict) and "data" in response:
                items = response["data"]
            else:
                items = response

            if not items:
                break

            # Yield items, skipping duplicates
            duplicates_in_page = 0
            for item in items:
                item_id = _get_item_id(item)
                if item_id in seen_ids:
                    duplicates_in_page += 1
                    continue
                if len(seen_ids) < MAX_SEEN_IDS_SIZE:
                    seen_ids.add(item_id)
                yield item
                self._items_fetched += 1
                if self._max_items and self._items_fetched >= self._max_items:
                    return

            # Detect infinite loop: entire page was duplicates
            if len(items) > 0 and duplicates_in_page == len(items):
                consecutive_dup_pages += 1
                if consecutive_dup_pages >= MAX_DUPLICATE_PAGES:
                    logger.warning(
                        "Pagination stopped: detected %d consecutive pages of "
                        "duplicate items. This may indicate an API pagination issue.",
                        MAX_DUPLICATE_PAGES,
                    )
                    break
            else:
                consecutive_dup_pages = 0

            # Check for next page
            if isinstance(response, dict) and "cursor" in response and response["cursor"]:
                cursor = response["cursor"]
            elif len(items) < self._limit:
                # No more pages
                break
            else:
                offset += len(items)
