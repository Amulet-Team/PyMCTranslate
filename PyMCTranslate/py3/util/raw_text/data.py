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
    class ABC:
        Colours: list[tuple[tuple[int, int, int], str, str]] = []
        RGBToName: dict[tuple[int, int, int], str] = {}
        NameToRGB: dict[str, tuple[int, int, int]] = {}

        @classmethod
        def find_closest(
            cls, r: int, g: int, b: int
        ) -> tuple[tuple[int, int, int], str, str]:
            return min(
                cls.Colours,
                key=lambda c: abs(c[0][0] - r) + abs(c[0][1] - g) + abs(c[0][2] - b),
            )

    class Java(ABC):
        Colours = [
            ((0x00, 0x00, 0x00), "0", "black"),
            ((0x00, 0x00, 0xAA), "1", "dark_blue"),
            ((0x00, 0xAA, 0x00), "2", "dark_green"),
            ((0x00, 0xAA, 0xAA), "3", "dark_aqua"),
            ((0xAA, 0x00, 0x00), "4", "dark_red"),
            ((0xAA, 0x00, 0xAA), "5", "dark_purple"),
            ((0xFF, 0xAA, 0x00), "6", "gold"),
            ((0xAA, 0xAA, 0xAA), "7", "gray"),
            ((0x55, 0x55, 0x55), "8", "dark_gray"),
            ((0x55, 0x55, 0xFF), "9", "blue"),
            ((0x55, 0xFF, 0x55), "a", "green"),
            ((0x55, 0xFF, 0xFF), "b", "aqua"),
            ((0xFF, 0x55, 0x55), "c", "red"),
            ((0xFF, 0x55, 0xFF), "d", "light_purple"),
            ((0xFF, 0xFF, 0x55), "e", "yellow"),
            ((0xFF, 0xFF, 0xFF), "f", "white"),
        ]
        RGBToName = {rgb: name for rgb, _, name in Colours}
        NameToRGB = {name: rgb for rgb, _, name in Colours}

    class Bedrock(ABC):
        Colours = [
            ((0x00, 0x00, 0x00), "0", "black"),
            ((0x00, 0x00, 0xAA), "1", "dark_blue"),
            ((0x00, 0xAA, 0x00), "2", "dark_green"),
            ((0x00, 0xAA, 0xAA), "3", "dark_aqua"),
            ((0xAA, 0x00, 0x00), "4", "dark_red"),
            ((0xAA, 0x00, 0xAA), "5", "dark_purple"),
            ((0xFF, 0xAA, 0x00), "6", "gold"),
            ((0xAA, 0xAA, 0xAA), "7", "gray"),
            ((0x55, 0x55, 0x55), "8", "dark_gray"),
            ((0x55, 0x55, 0xFF), "9", "blue"),
            ((0x55, 0xFF, 0x55), "a", "green"),
            ((0x55, 0xFF, 0xFF), "b", "aqua"),
            ((0xFF, 0x55, 0x55), "c", "red"),
            ((0xFF, 0x55, 0xFF), "d", "light_purple"),
            ((0xFF, 0xFF, 0x55), "e", "yellow"),
            ((0xFF, 0xFF, 0xFF), "f", "white"),
            ((0xDD, 0xD6, 0x05), "g", "minecoin_gold"),
            ((0xE3, 0xD4, 0xD1), "h", "material_quartz"),
            ((0xCE, 0xCA, 0xCA), "i", "material_iron"),
            ((0x44, 0x3A, 0x3B), "j", "material_netherite"),
            ((0x97, 0x16, 0x07), "m", "material_redstone"),
            ((0xB4, 0x68, 0x4D), "n", "material_copper"),
            ((0xDE, 0xB1, 0x2D), "p", "material_gold"),
            ((0x47, 0xA0, 0x36), "q", "material_emerald"),
            ((0x2C, 0xBA, 0xA8), "s", "material_diamond"),
            ((0x21, 0x49, 0x7B), "t", "material_lapis"),
            ((0x9A, 0x5C, 0xC6), "u", "material_amethyst"),
            ((0xEB, 0x71, 0x14), "v", "material_resin"),
        ]
        RGBToName = {rgb: name for rgb, _, name in Colours}
        NameToRGB = {name: rgb for rgb, _, name in Colours}


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
    "ListTextComponent",
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
class ListTextComponent:
    """
    A list of text components.
    All components after the first inherit formatting from the first.

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
    selector: str
    objective: str
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

    # Formatting
    colour: Union[Colour, None] = None
    font: Union[str, None] = None
    bold: Union[bool, None] = None
    italic: Union[bool, None] = None
    underlined: Union[bool, None] = None
    strikethrough: Union[bool, None] = None
    obfuscated: Union[bool, None] = None
    shadow_colour: Union[RGBAInt, RGBAFloat, None] = None

    content_type: Union[str, None] = None
    content: Union[Content, None] = None

    # Each child inherits this component's formatting but are independent of each other.
    children: Union[list[TextComponent], None] = None

    # Interaction
    insertion: Union[str, None] = None
    click_event: None = None
    hover_event: None = None

    unhandled: Union[UnhandledCompound, None] = None
