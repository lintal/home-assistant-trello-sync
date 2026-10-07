from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import TrelloAPI
from .const import DEFAULT_POLL_INTERVAL

_LOGGER = logging.getLogger(__name__)


class TrelloSyncCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Poll Trello and keep the Home Assistant todo entity synced."""

    def __init__(self, hass: HomeAssistant, api: TrelloAPI) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="trello_sync",
            update_interval=DEFAULT_POLL_INTERVAL,
        )
        self.api = api
        self.board_id = api.board_id

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.hass.async_add_executor_job(self.api.fetch_board)
        except Exception as err:
            raise UpdateFailed(f"Error fetching Trello board: {err}") from err

    def list_cards(self) -> list[dict[str, Any]]:
        data = self.data or {"lists": []}
        cards: list[dict[str, Any]] = []
        for list_entry in data.get("lists", []):
            for card in list_entry.get("cards", []):
                if not isinstance(card, dict):
                    continue
                cards.append(
                    {
                        "id": card.get("id"),
                        "name": card.get("name", ""),
                        "description": card.get("desc", ""),
                        "status": "completed" if card.get("closed") else "needs_action",
                        "due": card.get("due"),
                        "list_id": card.get("idList"),
                        "list_name": list_entry.get("name"),
                    }
                )
        return cards

    def get_list_id_for_name(self, list_name: str) -> str | None:
        data = self.data or {"lists": []}
        for list_entry in data.get("lists", []):
            if list_entry.get("name") == list_name:
                return list_entry.get("id")
        return None

    def parse_due(self, due_value: str | None):
        if not due_value:
            return None
        try:
            return datetime.fromisoformat(due_value.replace("Z", "+00:00"))
        except ValueError:
            return None
