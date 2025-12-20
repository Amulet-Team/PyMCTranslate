from __future__ import annotations

from typing import Union
from dataclasses import dataclass, field

from amulet_nbt import (
    CompoundTag,
    AnyNBT,
)

JSONList = list["JSON"]
JSONDict = dict[str, "JSON"]
JSON = Union[bool, int, float, str, JSONList, JSONDict]


class ColourCodes:
    class Java:
        RGBToName = {
            (0x00, 0x00, 0x00): "black",
            (0x00, 0x00, 0xAA): "dark_blue",
            (0x00, 0xAA, 0x00): "dark_green",
            (0x00, 0xAA, 0xAA): "dark_aqua",
            (0xAA, 0x00, 0x00): "dark_red",
            (0xAA, 0x00, 0xAA): "dark_purple",
            (0xFF, 0xAA, 0x00): "gold",
            (0xAA, 0xAA, 0xAA): "gray",
            (0x55, 0x55, 0x55): "dark_gray",
            (0x55, 0x55, 0xFF): "blue",
            (0x55, 0xFF, 0x55): "green",
            (0x55, 0xFF, 0xFF): "aqua",
            (0xFF, 0x55, 0x55): "red",
            (0xFF, 0x55, 0xFF): "light_purple",
            (0xFF, 0xFF, 0x55): "yellow",
            (0xFF, 0xFF, 0xFF): "white",
        }
        NameToRGB = {v: k for k, v in RGBToName.items()}


@dataclass(kw_only=True)
class Colour:
    """
    An RGB colour with an optional name.
    """

    # The name or #RRGGBB value
    name: Union[str, None]

    # The RGB value of the colour [0-255]
    r: int
    g: int
    b: int


@dataclass(kw_only=True)
class RGBAInt:
    # RGBA values in range [0-255]
    r: int
    g: int
    b: int
    a: int


@dataclass(kw_only=True)
class RGBAFloat:
    # RGBA values in range [0.0-1.0]
    r: float
    g: float
    b: float
    a: float


@dataclass(kw_only=True)
class UnhandledCompound:
    format_id: str
    tag: CompoundTag


TextComponent = Union[
    "InvalidTextComponent",
    "PlainTextComponent",
    "RecursiveTextComponent",
    "CompoundTextComponent",
]


@dataclass(kw_only=True)
class InvalidTextComponent:
    tag: AnyNBT


@dataclass(kw_only=True)
class PlainTextComponent:
    """Plain text with no formatting."""

    text: str


@dataclass(kw_only=True)
class RecursiveTextComponent:
    """
    A list of text components, each of which is a child of the previous.

    Section string: components joined
    Java JSON: [{"text": "red", "color": "red"}, "red"]
    Java NBT: [{"text": "red", "color": "red"}, {"": "red"}]
    """

    # The components in the list
    components: list[TextComponent] = field(default_factory=list)


@dataclass(kw_only=True)
class TextContent:
    text: str


@dataclass(kw_only=True)
class TranslatableContent:
    key: str
    fallback: Union[str, None] = None
    args: Union[list[TextComponent], None] = None


@dataclass(kw_only=True)
class ScoreboardContent:
    selector: Union[str, None]
    objective: Union[str, None]
    unhandled: Union[UnhandledCompound, None]


@dataclass(kw_only=True)
class EntityContent:
    selector: Union[str, None]
    separator: Union[TextComponent, None]


@dataclass(kw_only=True)
class KeybindContent:
    key: Union[str, None]


# @dataclass(kw_only=True)
# class NBTContent:
#     class BlockLocation(str):
#         pass
#
#     class EntitySelector(str):
#         pass
#
#     class StorageLocation(str):
#         pass
#
#     source: Union[str, None]
#     path: Union[str, None]
#     interpret: Union[bool, None]
#     separator: Union[CompoundTag, None]
#     content: Union[BlockLocation, EntitySelector, StorageLocation, None]


# @dataclass(kw_only=True)
# class AtlasContent:
#     atlas: Union[str, None]
#     sprite: Union[str, None]
#
#
# @dataclass(kw_only=True)
# class PlayerContent:
#     username: Union[str, None]
#     uuid: Union[str, None]
#     texture_path: Union[str, None]
#     cape_path: Union[str, None]
#     model: Union[str, None]  # "wide" or "slim"
#     properties: Union[list[], None]
#     show_hat: Union[bool, None]
#
#
# @dataclass(kw_only=True)
# class ObjectContent:
#     object_type: Union[str, None]
#     object: Union[AtlasContent, PlayerContent, None]


Content = Union[
    TextContent,
    TranslatableContent,
    ScoreboardContent,
    EntityContent,
    KeybindContent,
    # NBTContent,
    # ObjectContent,
]


@dataclass(kw_only=True)
class CompoundTextComponent:
    # The node in the empty key
    empty_node: Union[TextComponent, None] = None

    content_type: Union[str, None] = None
    content: Union[Content, None] = None

    # Each child inherits this component's formatting but are independent of each other.
    children: Union[list[TextComponent], None] = None

    # Formatting
    colour: Union[Colour, None] = None
    font: Union[str, None] = None
    bold: Union[bool, None] = None
    italic: Union[bool, None] = None
    underlined: Union[bool, None] = None
    strikethrough: Union[bool, None] = None
    obfuscated: Union[bool, None] = None
    shadow_colour: Union[RGBAInt, RGBAFloat, None] = None

    # Interaction
    insertion: Union[str, None] = None
    click_event: None = None
    hover_event: None = None

    unhandled: Union[UnhandledCompound, None] = None
