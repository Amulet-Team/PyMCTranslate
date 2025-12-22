from __future__ import annotations

from typing import Union
import re

from amulet_nbt import (
    CompoundTag,
    ListTag,
    StringTag,
    ByteTag,
    IntTag,
    FloatTag,
    AnyNBT,
)

from .data import (
    ColourCodes,
    Colour,
    RGBAInt,
    RGBAFloat,
    UnhandledCompound,
    TextComponent,
    InvalidTextComponent,
    PlainTextComponent,
    ListTextComponent,
    CompoundTextComponent,
    TextContent,
    TranslatableContent,
    ScoreboardContent,
    EntityContent,
    KeybindContent,
)

RGBHexPattern = re.compile(r"#([0-9a-fA-F]{6})")


def from_java_nbt(nbt: AnyNBT) -> TextComponent:
    if isinstance(nbt, StringTag):
        return PlainTextComponent(text=nbt.py_str)
    elif isinstance(nbt, ListTag):
        return ListTextComponent(components=[from_java_nbt(tag) for tag in nbt])
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
                        unhandled=(
                            UnhandledCompound(format_id="java", tag=score_tag)
                            if score_tag
                            else None
                        ),
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
        # TODO: other content types
        # elif content_type == "nbt":
        #     raise NotImplementedError
        # elif content_type == "object":
        #     raise NotImplementedError

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
            elif colour_code in ColourCodes.Java.NameToColour:
                r, g, b = ColourCodes.Java.NameToColour[colour_code].rgb
            else:
                # Unknown colour code
                r = g = b = 0
            colour = Colour(name=colour_code, r=r, g=g, b=b)
        else:
            colour = None

        # Get font
        font_tag = nbt.get("font", None)
        if isinstance(font_tag, StringTag):
            del nbt["font"]
            font = font_tag.py_str
        else:
            font = None

        # Get bold
        bold_tag = nbt.get("bold", None)
        if isinstance(bold_tag, ByteTag):
            del nbt["bold"]
            bold = bool(bold_tag)
        else:
            bold = None

        # Get italic
        italic_tag = nbt.get("italic", None)
        if isinstance(italic_tag, ByteTag):
            del nbt["italic"]
            italic = bool(italic_tag)
        else:
            italic = None

        # Get underlined
        underlined_tag = nbt.get("underlined", None)
        if isinstance(underlined_tag, ByteTag):
            del nbt["underlined"]
            underlined = bool(underlined_tag)
        else:
            underlined = None

        # Get strikethrough
        strikethrough_tag = nbt.get("strikethrough", None)
        if isinstance(strikethrough_tag, ByteTag):
            del nbt["strikethrough"]
            strikethrough = bool(strikethrough_tag)
        else:
            strikethrough = None

        # Get obfuscated
        obfuscated_tag = nbt.get("obfuscated", None)
        if isinstance(obfuscated_tag, ByteTag):
            del nbt["obfuscated"]
            obfuscated = bool(obfuscated_tag)
        else:
            obfuscated = None

        # Get shadow colour
        shadow_colour_tag = nbt.get("shadow_color", None)
        if isinstance(shadow_colour_tag, IntTag):
            del nbt["shadow_color"]
            shadow_colour_int = shadow_colour_tag.py_int
            shadow_colour = RGBAInt(
                a=(shadow_colour_int >> 24) & 0xFF,
                r=(shadow_colour_int >> 16) & 0xFF,
                g=(shadow_colour_int >> 8) & 0xFF,
                b=shadow_colour_int & 0xFF,
            )
        elif (
            isinstance(shadow_colour_tag, ListTag)
            and len(shadow_colour_tag) == 4
            and shadow_colour_tag.list_data_type == FloatTag.tag_id
        ):
            del nbt["shadow_color"]
            shadow_colour = RGBAFloat(
                r=shadow_colour_tag[0].py_float,
                g=shadow_colour_tag[1].py_float,
                b=shadow_colour_tag[2].py_float,
                a=shadow_colour_tag[3].py_float,
            )
        else:
            shadow_colour = None

        # TODO: Interaction

        return CompoundTextComponent(
            empty_node=empty_node,
            content_type=content_type,
            content=content,
            children=children,
            colour=colour,
            font=font,
            bold=bold,
            italic=italic,
            underlined=underlined,
            strikethrough=strikethrough,
            obfuscated=obfuscated,
            shadow_colour=shadow_colour,
            unhandled=UnhandledCompound(format_id="java", tag=nbt) if nbt else None,
        )
    else:
        return InvalidTextComponent(tag=nbt)


def to_java_nbt(component: TextComponent) -> Union[CompoundTag, ListTag, StringTag]:
    def escape_list_tags(list_tag: list[AnyNBT]) -> list[AnyNBT]:
        if list_tag and next(
            (True for tag in list_tag[1:] if type(tag) != type(list_tag[0])), False
        ):
            # Escape tags
            for i in range(len(list_tag)):
                tag = list_tag[i]
                if not isinstance(tag, CompoundTag):
                    list_tag[i] = CompoundTag({"": tag})
        return list_tag

    if isinstance(component, InvalidTextComponent):
        return component.tag
    elif isinstance(component, PlainTextComponent):
        return StringTag(component.text)
    elif isinstance(component, ListTextComponent):
        return ListTag(
            escape_list_tags([to_java_nbt(child) for child in component.components])
        )

    elif isinstance(component, CompoundTextComponent):
        if component.unhandled is not None and component.unhandled.format_id == "java":
            compound = component.unhandled.tag
        else:
            compound = CompoundTag()

        if component.empty_node is not None:
            compound[""] = to_java_nbt(component.empty_node)

        if component.content_type is not None:
            compound["type"] = StringTag(component.content_type)

        content = component.content
        if isinstance(content, TextContent):
            compound["text"] = StringTag(content.text)
        elif isinstance(content, TranslatableContent):
            compound["translate"] = StringTag(content.key)
            if content.fallback is not None:
                compound["fallback"] = StringTag(content.fallback)
            if content.args is not None:
                compound["with"] = ListTag(
                    escape_list_tags([to_java_nbt(tag) for tag in content.args])
                )
        elif isinstance(content, ScoreboardContent):
            if content.unhandled is not None and content.unhandled.format_id == "java":
                score = content.unhandled.tag
            else:
                score = CompoundTag()
            score["name"] = StringTag(content.selector)
            score["objective"] = StringTag(content.objective)
            compound["score"] = score
        elif isinstance(content, EntityContent):
            compound["selector"] = StringTag(content.selector)
            if content.separator is not None:
                compound["separator"] = to_java_nbt(content.separator)
        elif isinstance(content, KeybindContent):
            compound["keybind"] = StringTag(content.key)
        # TODO: other content types

        if component.children is not None:
            compound["extra"] = ListTag(
                escape_list_tags([to_java_nbt(child) for child in component.children])
            )

        if component.colour is not None:
            colour = component.colour
            r = max(0, min(colour.r, 255))
            g = max(0, min(colour.g, 255))
            b = max(0, min(colour.b, 255))
            if colour.name is None:
                colour_code = f"#{r:02X}{g:02X}{b:02X}"
            elif RGBHexPattern.fullmatch(colour.name) is not None:
                colour_code = colour.name
            else:
                colour = ColourCodes.Java.NameToColour.get(colour.name, None)
                if colour is not None and colour.rgb == (r, g, b):
                    colour_code = colour.name
                else:
                    colour_code = f"#{r:02X}{g:02X}{b:02X}"
            compound["color"] = StringTag(colour_code)

        if component.font is not None:
            compound["font"] = StringTag(component.font)

        if component.bold is not None:
            compound["bold"] = ByteTag(component.bold)

        if component.italic is not None:
            compound["italic"] = ByteTag(component.italic)

        if component.underlined is not None:
            compound["underlined"] = ByteTag(component.underlined)

        if component.strikethrough is not None:
            compound["strikethrough"] = ByteTag(component.strikethrough)

        if component.obfuscated is not None:
            compound["obfuscated"] = ByteTag(component.obfuscated)

        if component.shadow_colour is not None:
            if isinstance(component.shadow_colour, RGBAInt):
                compound["shadow_color"] = IntTag(
                    (component.shadow_colour.a & 0xFF) << 24
                    | (component.shadow_colour.r & 0xFF) << 16
                    | (component.shadow_colour.g & 0xFF) << 8
                    | (component.shadow_colour.b & 0xFF)
                )
            elif isinstance(component.shadow_colour, RGBAFloat):
                compound["shadow_color"] = ListTag(
                    [
                        FloatTag(component.shadow_colour.r),
                        FloatTag(component.shadow_colour.g),
                        FloatTag(component.shadow_colour.b),
                        FloatTag(component.shadow_colour.a),
                    ]
                )

        return compound
    else:
        raise TypeError(f"Unexpected component type: {type(component)}")
