# Home Inventory CLI

A friendly, local-first command-line tool for documenting your household belongings — rooms, items, values, and photo references — with JSON storage and CSV export for insurance records. Built with care by **Asdale Dynamics, LLC**.

No accounts, no cloud, no API keys, no personal data collected. Everything stays on your computer in a plain JSON file you control.

## Who this is for

Anyone who wants a simple, no-frills way to keep track of what they own and roughly what it's worth — handy for insurance paperwork, moving, or just peace of mind. It's part of Asdale Dynamics, LLC's line of small-business and life-admin helpers: practical, tested, local-first tools you can run without signing up for anything. Indiana, formed October 2026.

## What it does

- Create and manage a home inventory stored in a local JSON file
- Add rooms and belongings, each with a dollar value, optional photo reference, and optional description
- List all your rooms with per-room and total values
- Remove items or whole rooms
- Edit an item's value, photo reference, or description
- Export the full inventory to CSV (one row per item: room, item, value, photo, description) for insurance paperwork

## Install

You need Python 3.8 or newer. From this folder:

```bash
pip install .
```

That installs the `home-inventory` command. Or run it straight from the folder without installing:

```bash
python3 -m home_inventory.cli --help
```

## Step by step: your first inventory

**1. Create a new inventory file.**

```bash
home-inventory init inventory.json
```

This creates an empty `inventory.json` in your current folder. You can name it whatever you like and keep it anywhere on your computer.

**2. Add a room.**

```bash
home-inventory --file inventory.json add-room "Living Room"
```

**3. Add an item to that room.**

```bash
home-inventory --file inventory.json add-item "Living Room" "Television" --value 699.99 --photo photos/tv.jpg --description "55-inch OLED"
```

- `--value` is the dollar amount (must be zero or more).
- `--photo` is just a path to a photo you already have — the tool never touches your photos.
- `--description` is free-form notes.

**4. See everything.**

```bash
home-inventory --file inventory.json list
```

You'll see each room, how many items it has, the room's total value, and the grand total.

**5. Edit an item.**

Made a mistake or want to update a value? Edit it without re-adding:

```bash
home-inventory --file inventory.json edit-item "Living Room" "Television" --value 599.99
```

**6. Remove an item or room.**

```bash
home-inventory --file inventory.json remove-item "Living Room" "Television"
home-inventory --file inventory.json remove-room "Attic"
```

**7. Export to CSV for insurance.**

```bash
home-inventory --file inventory.json export home_inventory.csv
```

The CSV has these columns: `room, item, value, photo, description`. Open it in any spreadsheet app.

## Storage

All data lives on your machine in a plain JSON file you control. There are no servers, no accounts, and no keys. Photo references are stored as file paths only — the tool never reads, moves, or collects your photos, and Asdale Dynamics, LLC collects no personal data from you.

## Tests

```bash
python3 -m pytest
```

The test suite covers adding rooms and items, duplicate rejection, removals, total values, JSON save/load, CSV export, negative-value rejection, and item editing.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

## About Asdale Dynamics, LLC

Asdale Dynamics, LLC is an Indiana company founded by Dylan Asdale, a registered nurse turned AI author. The LLC publishes beginner-friendly AI education, books and guides, practical tools, and templates — AI tools, agents/MCP, local AI, free AI coding, GitHub, automation, privacy, small-business and author tools, life-admin helpers, and healthcare-worker AI aids (education only, never medical advice). Dylan's book *The Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a friend would": plain English, step by step, never condescending.
