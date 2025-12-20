from __future__ import annotations

from typing import overload, Literal, Union
from dataclasses import dataclass, field

from amulet_nbt import (
    CompoundTag,
    ListTag,
    StringTag,
    ByteTag,
    IntTag,
    FloatTag,
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
    unhandled: Union[CompoundTag, None]


@dataclass(kw_only=True)
class EntityContent:
    selector: Union[str, None]
    separator: Union[TextComponent, None]


@dataclass(kw_only=True)
class KeybindContent:
    key: Union[str, None]


Content = Union[
    TextContent,
    TranslatableContent,
    ScoreboardContent,
    EntityContent,
    KeybindContent,
]


@dataclass(kw_only=True)
class Formatting:
    colour: Union[Colour, None] = None
    font: Union[str, None] = None
    bold: Union[bool, None] = None
    italic: Union[bool, None] = None
    underlined: Union[bool, None] = None
    strikethrough: Union[bool, None] = None
    obfuscated: Union[bool, None] = None
    shadow_colour: Union[RGBAInt, RGBAFloat, None] = None


@dataclass(kw_only=True)
class CompoundTextComponent:
    # The node in the empty key
    empty_node: Union[TextComponent, None] = None

    content_type: Union[str, None] = None
    content: Union[Content, None] = None

    # Each child inherits this component's formatting but are independent of each other.
    children: Union[list[TextComponent], None] = None

    formatting: Formatting = field(default_factory=Formatting)

    insertion: Union[str, None] = None
    click_event: None = None
    hover_event: None = None
    unhandled: Union[CompoundTag, None] = None


@overload
def from_bedrock_section_string(
    section_str: str, split_newline: Literal[True]
) -> list[str]: ...


@overload
def from_bedrock_section_string(
    section_str: str, split_newline: Literal[False]
) -> str: ...


def from_bedrock_section_string(
    section_str: str, split_newline: bool
) -> Union[str, list[str]]:
    raise NotImplementedError


@overload
def from_java_section_string(
    section_str: str, split_newline: Literal[True]
) -> list[str]: ...


@overload
def from_java_section_string(
    section_str: str, split_newline: Literal[False]
) -> str: ...


def from_java_section_string(
    section_str: str, split_newline: bool
) -> Union[str, list[str]]:
    raise NotImplementedError


def from_java_json(json: JSON) -> TextComponent:
    raise NotImplementedError


def from_java_nbt(nbt: AnyNBT) -> TextComponent:
    if isinstance(nbt, StringTag):
        return PlainTextComponent(text=nbt.py_str)
    elif isinstance(nbt, ListTag):
        return RecursiveTextComponent(components=[from_java_nbt(tag) for tag in nbt])
    elif isinstance(nbt, CompoundTag):
        # Unpack the node in key ""
        empty_node_tag = nbt.pop("", None)
        if empty_node_tag is None:
            empty_node = None
        else:
            empty_node = from_java_nbt(empty_node_tag)

        # Get content type
        content_type_tag = nbt.get("type", None)
        if isinstance(content_type_tag, StringTag):
            content_type = content_type_tag.py_str
            del nbt["type"]
        else:
            content_type = None

        def get_text_content(compound: CompoundTag) -> Union[TextContent, None]:
            text_tag = compound.get("text", None)
            if isinstance(text_tag, StringTag):
                del compound["text"]
                return TextContent(text=text_tag.py_str)
            return None

        def get_translatable_content(
            compound: CompoundTag,
        ) -> Union[TranslatableContent, None]:
            translate_tag = compound.get("translate", None)
            if isinstance(translate_tag, StringTag):
                del compound["translate"]
                fallback_tag = compound.get("fallback", None)

                # Get fallback tag
                if isinstance(fallback_tag, StringTag):
                    del compound["fallback"]
                    fallback = fallback_tag.py_str
                else:
                    fallback = None

                # Get with tag
                with_tag = compound.get("with", None)
                if isinstance(with_tag, ListTag):
                    del compound["with"]
                    args = [from_java_nbt(tag) for tag in with_tag]
                else:
                    args = None

                return TranslatableContent(
                    key=translate_tag.py_str,
                    fallback=fallback,
                    args=args,
                )
            return None

        def get_scoreboard_content(
            compound: CompoundTag,
        ) -> Union[ScoreboardContent, None]:
            score_tag = compound.get("score", None)
            if isinstance(score_tag, CompoundTag):
                name_tag = score_tag.get("name", None)
                objective_tag = score_tag.get("objective", None)
                if isinstance(name_tag, StringTag) and isinstance(
                    objective_tag, StringTag
                ):
                    del compound["score"]
                    del score_tag["name"]
                    del score_tag["objective"]
                    return ScoreboardContent(
                        selector=name_tag.py_str,
                        objective=objective_tag.py_str,
                        unhandled=score_tag if score_tag else None,
                    )
            return None

        def get_entity_content(compound: CompoundTag) -> Union[EntityContent, None]:
            selector_tag = compound.get("selector", None)
            if isinstance(selector_tag, StringTag):
                del compound["selector"]
                separator_tag = compound.pop("separator", None)
                if separator_tag is None:
                    separator = None
                else:
                    separator = from_java_nbt(separator_tag)
                return EntityContent(
                    selector=selector_tag.py_str,
                    separator=separator,
                )
            return None

        def get_keybind_content(compound: CompoundTag) -> Union[KeybindContent, None]:
            keybind_tag = compound.get("keybind", None)
            if isinstance(keybind_tag, StringTag):
                del compound["keybind"]
                return KeybindContent(key=keybind_tag.py_str)
            return None

        content = None
        if content_type == "text":
            content = get_text_content(nbt)
        elif content_type == "translatable":
            content = get_translatable_content(nbt)
        elif content_type == "score":
            content = get_scoreboard_content(nbt)
        elif content_type == "selector":
            content = get_entity_content(nbt)
        elif content_type == "keybind":
            content = get_keybind_content(nbt)

        if content is None:
            # content-type is undefined, invalid or does not match the content
            content = (
                get_text_content(nbt)
                or get_translatable_content(nbt)
                or get_scoreboard_content(nbt)
                or get_entity_content(nbt)
                or get_keybind_content(nbt)
            )

        children_tag = nbt.get("extra", None)
        if isinstance(children_tag, ListTag):
            children = [from_java_nbt(tag) for tag in children_tag]
        else:
            children = None

        formatting = Formatting()

        # Get colour code
        colour_tag = nbt.get("color", None)
        if isinstance(colour_tag, StringTag):
            del nbt["color"]
            colour_code = colour_tag.py_str
            if colour_code.startswith("#") and len(colour_code) == 7:
                try:
                    r = int(colour_code[1:3], 16)
                    g = int(colour_code[3:5], 16)
                    b = int(colour_code[5:7], 16)
                except ValueError:
                    r = g = b = 0
            elif colour_code in ColourCodes.Java.NameToRGB:
                r, g, b = ColourCodes.Java.NameToRGB[colour_code]
            else:
                # Unknown colour code
                r = g = b = 0
            formatting.colour = Colour(name=colour_code, r=r, g=g, b=b)

        # Get font
        font_tag = nbt.get("font", None)
        if isinstance(font_tag, StringTag):
            del nbt["font"]
            formatting.font = font_tag.py_str

        # Get bold
        bold_tag = nbt.get("bold", None)
        if isinstance(bold_tag, ByteTag):
            del nbt["bold"]
            formatting.bold = bool(bold_tag)

        # Get italic
        italic_tag = nbt.get("italic", None)
        if isinstance(italic_tag, ByteTag):
            del nbt["italic"]
            formatting.italic = bool(italic_tag)

        # Get underlined
        underlined_tag = nbt.get("underlined", None)
        if isinstance(underlined_tag, ByteTag):
            del nbt["underlined"]
            formatting.underlined = bool(underlined_tag)

        # Get strikethrough
        strikethrough_tag = nbt.get("strikethrough", None)
        if isinstance(strikethrough_tag, ByteTag):
            del nbt["strikethrough"]
            formatting.strikethrough = bool(strikethrough_tag)

        # Get obfuscated
        obfuscated_tag = nbt.get("obfuscated", None)
        if isinstance(obfuscated_tag, ByteTag):
            del nbt["obfuscated"]
            formatting.obfuscated = bool(obfuscated_tag)

        # Get shadow colour
        shadow_colour_tag = nbt.get("shadow_color", None)
        if isinstance(shadow_colour_tag, IntTag):
            del nbt["shadow_color"]
            shadow_colour = shadow_colour_tag.py_int
            formatting.shadow_colour = RGBAInt(
                a=(shadow_colour >> 24) & 0xFF,
                r=(shadow_colour >> 16) & 0xFF,
                g=(shadow_colour >> 8) & 0xFF,
                b=shadow_colour & 0xFF,
            )
        elif (
            isinstance(shadow_colour_tag, ListTag)
            and len(shadow_colour_tag) == 4
            and shadow_colour_tag.list_data_type == FloatTag.tag_id
        ):
            del nbt["shadow_color"]
            formatting.shadow_colour = RGBAFloat(
                r=shadow_colour_tag[0].py_float,
                g=shadow_colour_tag[1].py_float,
                b=shadow_colour_tag[2].py_float,
                a=shadow_colour_tag[3].py_float,
            )

        # TODO: Interaction

        return CompoundTextComponent(
            empty_node=empty_node,
            content_type=content_type,
            content=content,
            children=children,
            formatting=formatting,
            unhandled=nbt if nbt else None,
        )
    else:
        return InvalidTextComponent(tag=nbt)


def to_java_nbt(component: TextComponent) -> Union[CompoundTag, ListTag, StringTag]:
    raise NotImplementedError
