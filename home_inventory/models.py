"""Home inventory data models."""

from dataclasses import dataclass, field, asdict
from typing import List, Optional


@dataclass
class Item:
    """A single belonging with a value and optional photo reference."""

    name: str
    value: float = 0.0
    photo: Optional[str] = None
    description: str = ""

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError(f"Item '{self.name}' value cannot be negative")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        return cls(
            name=str(data.get("name", "")),
            value=float(data.get("value", 0.0) or 0.0),
            photo=data.get("photo"),
            description=str(data.get("description", "")),
        )


@dataclass
class Room:
    """A room containing a list of items."""

    name: str
    items: List[Item] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"name": self.name, "items": [item.to_dict() for item in self.items]}

    @classmethod
    def from_dict(cls, data: dict) -> "Room":
        return cls(
            name=str(data.get("name", "")),
            items=[Item.from_dict(item) for item in data.get("items", [])],
        )

    def item_names(self) -> List[str]:
        return [item.name for item in self.items]

    def find_item(self, name: str) -> Optional[Item]:
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None

    def add_item(self, item: Item) -> None:
        if self.find_item(item.name) is not None:
            raise ValueError(f"Item '{item.name}' already exists in room '{self.name}'")
        self.items.append(item)

    def remove_item(self, name: str) -> Item:
        item = self.find_item(name)
        if item is None:
            raise KeyError(f"Item '{name}' not found in room '{self.name}'")
        self.items = [i for i in self.items if i.name.lower() != name.lower()]
        return item

    def total_value(self) -> float:
        return sum(item.value for item in self.items)


@dataclass
class Inventory:
    """Top-level inventory: a collection of rooms persisted to JSON."""

    rooms: List[Room] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"rooms": [room.to_dict() for room in self.rooms]}

    @classmethod
    def from_dict(cls, data: dict) -> "Inventory":
        return cls(rooms=[Room.from_dict(room) for room in data.get("rooms", [])])

    def room_names(self) -> List[str]:
        return [room.name for room in self.rooms]

    def find_room(self, name: str) -> Optional[Room]:
        for room in self.rooms:
            if room.name.lower() == name.lower():
                return room
        return None

    def add_room(self, room: Room) -> None:
        if self.find_room(room.name) is not None:
            raise ValueError(f"Room '{room.name}' already exists")
        self.rooms.append(room)

    def remove_room(self, name: str) -> Room:
        room = self.find_room(name)
        if room is None:
            raise KeyError(f"Room '{name}' not found")
        self.rooms = [r for r in self.rooms if r.name.lower() != name.lower()]
        return room

    def total_value(self) -> float:
        return sum(room.total_value() for room in self.rooms)
