"""Tests for home inventory entry logic."""

import csv
import os
import tempfile

from home_inventory.models import Inventory, Item, Room
from home_inventory.storage import load, save
from home_inventory.export import export_csv


def test_add_room_and_item():
    inventory = Inventory()
    inventory.add_room(Room(name="Kitchen"))
    room = inventory.find_room("Kitchen")
    assert room is not None
    room.add_item(Item(name="Toaster", value=29.99, photo="photos/toaster.jpg"))
    assert len(room.items) == 1
    assert room.items[0].name == "Toaster"
    assert room.items[0].value == 29.99


def test_duplicate_room_rejected():
    inventory = Inventory()
    inventory.add_room(Room(name="Bedroom"))
    try:
        inventory.add_room(Room(name="bedroom"))
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for duplicate room")


def test_duplicate_item_rejected():
    room = Room(name="Office")
    room.add_item(Item(name="Desk", value=150.0))
    try:
        room.add_item(Item(name="DESK", value=10.0))
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for duplicate item")


def test_remove_item():
    room = Room(name="Living Room")
    room.add_item(Item(name="Sofa", value=500.0))
    removed = room.remove_item("Sofa")
    assert removed.name == "Sofa"
    assert room.find_item("Sofa") is None


def test_remove_missing_item_raises():
    room = Room(name="Bathroom")
    try:
        room.remove_item("Missing")
    except KeyError:
        pass
    else:
        raise AssertionError("Expected KeyError for missing item")


def test_total_value():
    room = Room(name="Garage")
    room.add_item(Item(name="Bike", value=300.0))
    room.add_item(Item(name="Tools", value=120.50))
    assert room.total_value() == 420.50
    inventory = Inventory()
    inventory.add_room(room)
    assert inventory.total_value() == 420.50


def test_json_round_trip():
    inventory = Inventory()
    inventory.add_room(Room(name="Hall"))
    inventory.find_room("Hall").add_item(Item(name="Mirror", value=45.0, photo="hall/mirror.jpg"))
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "inventory.json")
        save(inventory, path)
        loaded = load(path)
    assert len(loaded.rooms) == 1
    assert loaded.find_room("Hall") is not None
    item = loaded.find_room("Hall").find_item("Mirror")
    assert item is not None
    assert item.value == 45.0
    assert item.photo == "hall/mirror.jpg"


def test_missing_file_loads_empty():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "does-not-exist.json")
        loaded = load(path)
    assert isinstance(loaded, Inventory)
    assert loaded.rooms == []


def test_csv_export():
    inventory = Inventory()
    room = Room(name="Kitchen")
    room.add_item(Item(name="Toaster", value=29.99, photo="photos/toaster.jpg", description="2-slice"))
    room.add_item(Item(name="Mixer", value=120.0))
    inventory.add_room(room)
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "export.csv")
        header = export_csv(inventory, path)
        assert header == ["room", "item", "value", "photo", "description"]
        with open(path, newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    assert len(rows) == 2
    assert rows[0]["room"] == "Kitchen"
    assert rows[0]["item"] == "Toaster"
    assert rows[0]["value"] == "29.99"
    assert rows[0]["photo"] == "photos/toaster.jpg"
    assert rows[1]["item"] == "Mixer"
    assert rows[1]["photo"] == ""
