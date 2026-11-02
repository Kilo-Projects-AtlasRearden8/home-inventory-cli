"""CSV export for home inventories."""

import csv
from typing import List

from home_inventory.models import Inventory, Item


def export_csv(inventory: Inventory, path: str) -> List[str]:
    """Export every item to a CSV file with one row per item.

    Columns: room, item, value, photo, description.
    Returns the list of header names written.
    """

    header = ["room", "item", "value", "photo", "description"]
    try:
        with open(path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=header)
            writer.writeheader()
            for room in inventory.rooms:
                for item in room.items:
                    writer.writerow(
                        {
                            "room": room.name,
                            "item": item.name,
                            "value": f"{item.value:.2f}",
                            "photo": item.photo or "",
                            "description": item.description,
                        }
                    )
    except OSError as exc:
        raise OSError(f"Failed to write CSV file '{path}': {exc}") from exc
    return header
