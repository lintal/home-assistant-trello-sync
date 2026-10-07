from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries

from .api import TrelloAPI
from .const import CONF_API_KEY, CONF_API_TOKEN, CONF_BOARD_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)


def validate_input(data: dict[str, Any]) -> dict[str, Any]:
    client = TrelloAPI(
        api_key=data[CONF_API_KEY],
        api_token=data[CONF_API_TOKEN],
        board_id=data[CONF_BOARD_ID],
    )
    board = client.fetch_board()
    if not board.get("board"):
        raise ValueError("invalid_board")
    return {"title": board["board"].get("name", data[CONF_BOARD_ID])}


class TrelloSyncConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                result = await self.hass.async_add_executor_job(validate_input, user_input)
            except Exception:  # noqa: BLE001
                errors["base"] = "invalid_auth"
            else:
                return self.async_create_entry(
                    title=result["title"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_API_TOKEN): str,
                    vol.Required(CONF_BOARD_ID): str,
                }
            ),
            errors=errors,
        )

