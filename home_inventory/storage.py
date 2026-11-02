"""JSON storage for home inventories."""

import json
import os
from typing import Optional

from home_inventory.models import Inventory


class StorageError(Exception):
    """Raised when reading or writing the inventory file fails."""


def default_path() -> str:
    return os.path.join(os.getcwd(), "inventory.json")


def load(path: str) -> Inventory:
    """Load an Inventory from a JSON file. Missing file yields an empty inventory."""

    if not os.path.exists(path):
        return Inventory()
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise StorageError(f"Failed to read inventory file '{path}': {exc}") from exc
    if not isinstance(data, dict):
        raise StorageError(f"Inventory file '{path}' does not contain a JSON object")
    return Inventory.from_dict(data)


def save(inventory: Inventory, path: str) -> None:
    """Persist an Inventory to a JSON file."""

    directory = os.path.dirname(os.path.abspath(path))
    if directory and not os.path.isdir(directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as exc:
            raise StorageError(f"Failed to create directory '{directory}': {exc}") from exc
    try:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(inventory.to_dict(), handle, indent=2, sort_keys=True)
            handle.write("\n")
    except OSError as exc:
        raise StorageError(f"Failed to write inventory file '{path}': {exc}") from exc
