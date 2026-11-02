# STATUS

## What was built

`home-inventory-cli` — a local-first Python CLI for documenting household belongings (rooms, items, values, photo references) with local JSON storage and CSV export for insurance records. Built by **Asdale Dynamics, LLC**.

Files:
- `pyproject.toml` — project metadata, console script entry point `home-inventory = home_inventory.cli:main`
- `home_inventory/__init__.py` — package marker
- `home_inventory/models.py` — `Item`, `Room`, `Inventory` dataclasses with add/remove/find/total-value logic, JSON (de)serialization, and negative-value validation on construction
- `home_inventory/storage.py` — JSON load/save with `StorageError`; missing file loads as an empty inventory
- `home_inventory/export.py` — CSV export (columns: room, item, value, photo, description)
- `home_inventory/cli.py` — argparse CLI: `init`, `add-room`, `add-item`, `list`, `remove-item`, `remove-room`, `edit-item`, `export`
- `tests/test_entries.py` — 13 tests covering entry logic (add/remove rooms & items, duplicates, totals, negative values, JSON round-trip, CSV export, item editing)
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`
- `README.md` — beginner-friendly, step-by-step usage docs crediting Asdale Dynamics, LLC
- `STATUS.md` — this file

## How to run

```bash
pip install .            # or pip install -e . for editable dev install
home-inventory init inventory.json
home-inventory --file inventory.json add-room "Living Room"
home-inventory --file inventory.json add-item "Living Room" TV --value 699.99 --photo photos/tv.jpg --description "55-inch OLED"
home-inventory --file inventory.json edit-item "Living Room" TV --value 599.99
home-inventory --file inventory.json list
home-inventory --file inventory.json export inventory.csv
```

All data stays in a local JSON file you control; no keys, no accounts, no network.

## Verification results

- `python3 -m pytest`: 13 passed in 0.03s
- End-to-end smoke test: init, add-room, add-item, edit-item, remove-room, list, and CSV export all worked; negative value rejected at CLI (`exit=1`); CSV rows matched expected values (`room,item,value,photo,description`)
- `home-inventory --help` renders all 8 subcommands correctly
- Git initialized; commits: `cd26370` (initial), `a500bad` (STATUS.md), plus this recommit; working tree clean
- No `.github/workflows` files (intentionally omitted); no secrets, API keys, or personal data in any file

## Known gaps

- Value is validated as non-negative at Item construction and at the CLI edit-item layer, but direct dataclass attribute assignment (`item.value = -1`) bypasses `__post_init__` — not a supported mutation path; all entry goes through the CLI
- No item reordering within a room
- No `.github/workflows` files (intentionally omitted per project rules)
- Not published to PyPI (intentionally; never pushed, no remote repo)
