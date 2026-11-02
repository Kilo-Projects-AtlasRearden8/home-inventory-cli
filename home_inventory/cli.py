"""Command-line interface for the home inventory tool."""

import argparse
import sys
from typing import List, Optional

from home_inventory.models import Inventory, Item, Room
from home_inventory.storage import load, save, default_path, StorageError
from home_inventory.export import export_csv


def _money(value: float) -> str:
    return f"${value:,.2f}"


def _print_rooms(inventory: Inventory, show_items: bool = True) -> None:
    if not inventory.rooms:
        print("No rooms yet. Add one with: home-inventory add-room \"Living Room\"")
        return
    for room in inventory.rooms:
        print(f"- {room.name} ({len(room.items)} item(s), {_money(room.total_value())})")
        if show_items and room.items:
            for item in room.items:
                photo = f" photo={item.photo}" if item.photo else ""
                print(f"    * {item.name} — {_money(item.value)}{photo}")


def cmd_init(args: argparse.Namespace) -> int:
    path = args.file or default_path()
    try:
        save(Inventory(), path)
    except StorageError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Initialized empty inventory at {path}")
    return 0


def cmd_add_room(args: argparse.Namespace) -> int:
    path = args.file or default_path()
    try:
        inventory = load(path)
        inventory.add_room(Room(name=args.name))
        save(inventory, path)
    except StorageError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Added room '{args.name}'")
    return 0


def cmd_add_item(args: argparse.Namespace) -> int:
    path = args.file or default_path()
    try:
        inventory = load(path)
        room = inventory.find_room(args.room)
        if room is None:
            print(f"Error: room '{args.room}' not found", file=sys.stderr)
            return 1
        item = Item(
            name=args.name,
            value=args.value,
            photo=args.photo,
            description=args.description,
        )
        room.add_item(item)
        save(inventory, path)
    except StorageError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except (ValueError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Added item '{args.name}' to room '{args.room}' ({_money(args.value)})")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    path = args.file or default_path()
    try:
        inventory = load(path)
    except StorageError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    _print_rooms(inventory)
    print(f"\nTotal value: {_money(inventory.total_value())}")
    return 0


def cmd_remove_room(args: argparse.Namespace) -> int:
    path = args.file or default_path()
    try:
        inventory = load(path)
        removed = inventory.remove_room(args.name)
        save(inventory, path)
    except StorageError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Removed room '{removed.name}' and all its items")
    return 0


def cmd_edit_item(args: argparse.Namespace) -> int:
    path = args.file or default_path()
    if args.value is None and args.photo is None and args.description is None:
        print("Error: specify at least one of --value, --photo, or --description to edit", file=sys.stderr)
        return 1
    try:
        inventory = load(path)
        room = inventory.find_room(args.room)
        if room is None:
            print(f"Error: room '{args.room}' not found", file=sys.stderr)
            return 1
        item = room.find_item(args.name)
        if item is None:
            print(f"Error: item '{args.name}' not found in room '{args.room}'", file=sys.stderr)
            return 1
        if args.value is not None:
            if args.value < 0:
                print(f"Error: value cannot be negative", file=sys.stderr)
                return 1
            item.value = args.value
        if args.photo is not None:
            item.photo = args.photo
        if args.description is not None:
            item.description = args.description
        save(inventory, path)
    except StorageError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Edited item '{args.name}' in room '{args.room}'")
    return 0


def cmd_remove_item(args: argparse.Namespace) -> int:
    path = args.file or default_path()
    try:
        inventory = load(path)
        room = inventory.find_room(args.room)
        if room is None:
            print(f"Error: room '{args.room}' not found", file=sys.stderr)
            return 1
        removed = room.remove_item(args.name)
        save(inventory, path)
    except StorageError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Removed item '{removed.name}' from room '{args.room}'")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    path = args.file or default_path()
    try:
        inventory = load(path)
        header = export_csv(inventory, args.output)
    except StorageError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Exported {len(inventory.rooms)} room(s) to {args.output} ({', '.join(header)})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="home-inventory",
        description="Document household belongings with local JSON storage and CSV export.",
    )
    parser.add_argument(
        "--file",
        default=None,
        help="Inventory JSON file path (default: inventory.json in current directory)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create a new empty inventory file")
    p_init.add_argument("file", nargs="?", default=None, help="Inventory JSON file path")
    p_init.set_defaults(func=cmd_init)

    p_room = sub.add_parser("add-room", help="Add a room")
    p_room.add_argument("name", help="Room name")
    p_room.set_defaults(func=cmd_add_room)

    p_item = sub.add_parser("add-item", help="Add an item to a room")
    p_item.add_argument("room", help="Room name")
    p_item.add_argument("name", help="Item name")
    p_item.add_argument("--value", type=float, default=0.0, help="Item value in dollars")
    p_item.add_argument("--photo", default=None, help="Photo reference path")
    p_item.add_argument("--description", default="", help="Item description")
    p_item.set_defaults(func=cmd_add_item)

    p_list = sub.add_parser("list", help="List rooms, items, and total value")
    p_list.set_defaults(func=cmd_list)

    p_remove = sub.add_parser("remove-item", help="Remove an item from a room")
    p_remove.add_argument("room", help="Room name")
    p_remove.add_argument("name", help="Item name")
    p_remove.set_defaults(func=cmd_remove_item)

    p_remove_room = sub.add_parser("remove-room", help="Remove a room and all its items")
    p_remove_room.add_argument("name", help="Room name")
    p_remove_room.set_defaults(func=cmd_remove_room)

    p_edit = sub.add_parser("edit-item", help="Edit an item's value, photo, or description")
    p_edit.add_argument("room", help="Room name")
    p_edit.add_argument("name", help="Item name")
    p_edit.add_argument("--value", type=float, default=None, help="New item value in dollars")
    p_edit.add_argument("--photo", default=None, help="New photo reference path")
    p_edit.add_argument("--description", default=None, help="New item description")
    p_edit.set_defaults(func=cmd_edit_item)

    p_export = sub.add_parser("export", help="Export inventory to CSV")
    p_export.add_argument("output", help="Output CSV file path")
    p_export.set_defaults(func=cmd_export)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
