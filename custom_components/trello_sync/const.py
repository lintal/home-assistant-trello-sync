from __future__ import annotations

import logging
from typing import Any

import requests

_LOGGER = logging.getLogger(__name__)


class TrelloAPI:
    """Minimal Trello API client for board and card access."""

    def __init__(self, api_key: str, api_token: str, board_id: str) -> None:
        self.api_key = api_key
        self.api_token = api_token
        self.board_id = board_id
        self.base_url = "https://api.trello.com/1"

    def _params(self) -> dict[str, str]:
        return {
            "key": self.api_key,
            "token": self.api_token,
        }

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None) -> Any:
        payload = self._params()
        if params:
            payload.update(params)

        response = requests.request(
            method,
            f"{self.base_url}{path}",
            params=payload,
            timeout=30,
        )

        if response.status_code >= 400:
            raise ValueError(
                f"Trello API request failed for {path}: {response.status_code} - {response.text}"
            )

        return response.json()

    def fetch_board(self) -> dict[str, Any]:
        """Fetch board details and all open cards grouped by list."""
        board = self._request(
            "GET",
            f"/boards/{self.board_id}",
            {"fields": "name,shortLink"},
        )
        lists_ = self._request(
            "GET",
            f"/boards/{self.board_id}/lists",
            {"cards": "open", "card_fields": "name,desc,due,closed,idList"},
        )
        return {"board": board, "lists": lists_}

    def create_card(self, name: str, description: str = "", list_id: str | None = None, due: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["desc"] = description
        if list_id:
            payload["idList"] = list_id
        if due:
            payload["due"] = due
        return self._request("POST", "/cards", payload)

    def update_card(self, card_id: str, **kwargs: Any) -> dict[str, Any]:
        return self._request("PUT", f"/cards/{card_id}", kwargs)

    def delete_card(self, card_id: str) -> None:
        self._request("DELETE", f"/cards/{card_id}")

    def get_list(self, list_id: str) -> dict[str, Any]:
        return self._request("GET", f"/lists/{list_id}")
