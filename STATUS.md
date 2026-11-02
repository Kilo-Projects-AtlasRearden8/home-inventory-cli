# STATUS

## What was built

`home-inventory-cli` — a local-first Python CLI for documenting household belongings (rooms, items, values, photo references) with local JSON storage and CSV export for insurance records.

Files:
- `pyproject.toml` — project metadata, console script entry point `home-inventory = home_inventory.cli:main`
- `home_inventory/__init__.py` — package marker
- `home_inventory/models.py` — `Item`, `Room`, `Inventory` dataclasses with add/remove/find/total-value logic and JSON (de)serialization
- `home_inventory/storage.py` — JSON load/save with `StorageError`; missing file loads as an empty inventory
- `home_inventory/export.py` — CSV export (columns: room, item, value, photo, description)
- `home_inventory/cli.py` — argparse CLI: `init`, `add-room`, `add-item`, `list`, `remove-item`, `export`
- `tests/test_entries.py` — 9 tests covering entry logic (add/remove, duplicates, totals, JSON round-trip, CSV export)
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`
- `README.md` — usage docs crediting Asdale Dynamics, LLC
- `STATUS.md` — this file

## How to run

```bash
pip install .            # or pip install -e . for editable dev install
home-inventory init inventory.json
home-inventory --file inventory.json add-room "Living Room"
home-inventory --file inventory.json add-item "Living Room" TV --value 699.99 --photo photos/tv.jpg
home-inventory --file inventory.json list
home-inventory --file inventory.json export inventory.csv
```

All data stays in a local JSON file you control; no keys, no accounts, no network.

## Verification results

- `python3 -m pytest`: 9 passed in 0.03s
- End-to-end smoke test: init, add-room, add-item, list, and CSV export all worked; CSV rows matched expected values (`room,item,value,photo,description`)
- `home-inventory --help` renders all subcommands correctly
- Git initialized at commit `cd26370` ("Initial commit: home inventory CLI with JSON storage and CSV export"); working tree clean

## Known gaps

- No `remove-room` command (items can be removed, rooms cannot)
- No item editing — to change a value/photo/description, remove and re-add the item
- Value parsing accepts any float; negative values are not rejected
- No `.github/workflows` files (intentionally omitted per project rules)
- Not published to PyPI (intentionally; never pushed, no remote repo)
