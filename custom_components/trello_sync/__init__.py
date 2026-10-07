from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import TrelloSyncCoordinator
from .api import TrelloAPI

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.TODO]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Trello Sync from a config entry."""
    api = TrelloAPI(
        api_key=entry.data["api_key"],
        api_token=entry.data["api_token"],
        board_id=entry.data["board_id"],
    )

    coordinator = TrelloSyncCoordinator(hass, api)
    hass.data.setdefault("trello_sync", {})
    hass.data["trello_sync"][entry.entry_id] = {"coordinator": coordinator}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data["trello_sync"].pop(entry.entry_id, None)
    return unload_ok
