# Home Assistant Trello Sync

A Home Assistant custom integration for syncing Trello cards with a Home Assistant todo entity in both directions.

## Features

- Bidirectional sync between Home Assistant todo items and Trello cards
- Maps Trello cards to Home Assistant todo items
- Syncs card summaries, descriptions, due dates, and completion state
- Polls Trello on a regular interval and refreshes the Home Assistant entity state
- Includes a configuration flow for entering Trello credentials and board ID

## What this repository includes

This is a working starter implementation for a Home Assistant custom component. It sets up:

- a Trello API client
- a Home Assistant config flow
- a todo entity that surfaces Trello cards as HA tasks
- synchronization logic to create, update, and delete tasks across the two systems

## Installation

1. Copy the `custom_components/trello_sync` directory into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Go to Settings > Devices & Services > Add Integration.
4. Select `Trello Sync`.
5. Enter:
   - Trello API key
   - Trello API token
   - Trello board ID
6. Save the configuration.

## Trello setup

1. Create a Trello app at https://trello.com/app-key
2. Generate an API token with access to the board you want to sync
3. Copy the board ID from the board URL or Trello API output

## Notes

This implementation uses polling to detect Trello changes and refresh Home Assistant state. For a production-grade setup, you can extend it with Trello webhooks or additional list-to-status mapping logic.

## License

MIT
