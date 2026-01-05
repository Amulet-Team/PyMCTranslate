from __future__ import annotations

from typing import Union
import json
import re

from .data import (
    ColourCodes,
    Colour,
    RGBAInt,
    RGBAFloat,
    JSON,
    JSONDict,
    UnhandledDict,
    TextComponent,
    PlainTextComponent,
    ListTextComponent,
    CompoundTextComponent,
    InvalidJSONTextComponent,
    TextContent,
    TranslatableContent,
    ScoreboardContent,
    EntityContent,
    KeybindContent,
)

RGBHexPattern = re.compile(r"#([0-9a-fA-F]{6})")


def _from_java_json(obj: JSON) -> TextComponent:
    if isinstance(obj, str):
        return PlainTextComponent(text=obj)
    elif isinstance(obj, list):
        return ListTextComponent(components=[_from_java_json(o) for o in obj])
    elif isinstance(obj, dict):
        # Get content type
        content_type_tag = obj.get("type", None)
        if isinstance(content_type_tag, str):
            content_type = content_type_tag
            del obj["type"]
        else:
            content_type = None

        def get_text_content(d: JSONDict) -> Union[TextContent, None]:
            text_tag = d.get("text", None)
            if isinstance(text_tag, str):
                del d["text"]
                return TextContent(text=text_tag)
            return None

        def get_translatable_content(
            d: JSONDict,
        ) -> Union[TranslatableContent, None]:
            translate_tag = d.get("translate", None)
            if isinstance(translate_tag, str):
                del d["translate"]
                fallback_tag = d.get("fallback", None)

                # Get fallback tag
                if isinstance(fallback_tag, str):
                    del d["fallback"]
                    fallback = fallback_tag
                else:
                    fallback = None

                # Get with tag
                with_tag = d.get("with", None)
                if isinstance(with_tag, list):
                    del d["with"]
                    args = [_from_java_json(tag) for tag in with_tag]
                else:
                    args = None

                return TranslatableContent(
                    key=translate_tag,
                    fallback=fallback,
                    args=args,
                )
            return None

        def get_scoreboard_content(
            d: JSONDict,
        ) -> Union[ScoreboardContent, None]:
            score_tag = d.get("score", None)
            if isinstance(score_tag, dict):
                name_tag = score_tag.get("name", None)
                objective_tag = score_tag.get("objective", None)
                if isinstance(name_tag, str) and isinstance(objective_tag, str):
                    del d["score"]
                    del score_tag["name"]
                    del score_tag["objective"]
                    return ScoreboardContent(
                        selector=name_tag,
                        objective=objective_tag,
                        unhandled=(
                            UnhandledDict(format_id="java", tag=score_tag)
                            if score_tag
                            else None
                        ),
                    )
            return None

        def get_entity_content(d: JSONDict) -> Union[EntityContent, None]:
            selector_tag = d.get("selector", None)
            if isinstance(selector_tag, str):
                del d["selector"]
                separator_tag = d.pop("separator", None)
                if separator_tag is None:
                    separator = None
                else:
                    separator = _from_java_json(separator_tag)
                return EntityContent(
                    selector=selector_tag,
                    separator=separator,
                )
            return None

        def get_keybind_content(d: JSONDict) -> Union[KeybindContent, None]:
            keybind_tag = d.get("keybind", None)
            if isinstance(keybind_tag, str):
                del d["keybind"]
                return KeybindContent(key=keybind_tag)
            return None

        content = None
        if content_type == "text":
            content = get_text_content(obj)
        elif content_type == "translatable":
            content = get_translatable_content(obj)
        elif content_type == "score":
            content = get_scoreboard_content(obj)
        elif content_type == "selector":
            content = get_entity_content(obj)
        elif content_type == "keybind":
            content = get_keybind_content(obj)
        # TODO: other content types
        # elif content_type == "nbt":
        #     raise NotImplementedError

        if content is None:
            # content-type is undefined, invalid or does not match the content
            content = (
                get_text_content(obj)
                or get_translatable_content(obj)
                or get_scoreboard_content(obj)
                or get_entity_content(obj)
                or get_keybind_content(obj)
            )

        children_tag = obj.get("extra", None)
        if isinstance(children_tag, list):
            children = [_from_java_json(tag) for tag in children_tag]
        else:
            children = None

        # Get colour code
        colour_tag = obj.get("color", None)
        if isinstance(colour_tag, str):
            del obj["color"]
            colour_code = colour_tag
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
        font_tag = obj.get("font", None)
        if isinstance(font_tag, str):
            del obj["font"]
            font = font_tag
        else:
            font = None

        # Get bold
        bold_tag = obj.get("bold", None)
        if isinstance(bold_tag, bool):
            del obj["bold"]
            bold = bold_tag
        else:
            bold = None

        # Get italic
        italic_tag = obj.get("italic", None)
        if isinstance(italic_tag, bool):
            del obj["italic"]
            italic = italic_tag
        else:
            italic = None

        # Get underlined
        underlined_tag = obj.get("underlined", None)
        if isinstance(underlined_tag, bool):
            del obj["underlined"]
            underlined = underlined_tag
        else:
            underlined = None

        # Get strikethrough
        strikethrough_tag = obj.get("strikethrough", None)
        if isinstance(strikethrough_tag, bool):
            del obj["strikethrough"]
            strikethrough = strikethrough_tag
        else:
            strikethrough = None

        # Get obfuscated
        obfuscated_tag = obj.get("obfuscated", None)
        if isinstance(obfuscated_tag, bool):
            del obj["obfuscated"]
            obfuscated = obfuscated_tag
        else:
            obfuscated = None

        # Get shadow colour
        shadow_colour_tag = obj.get("shadow_color", None)
        if isinstance(shadow_colour_tag, int):
            del obj["shadow_color"]
            shadow_colour = RGBAInt(
                a=(shadow_colour_tag >> 24) & 0xFF,
                r=(shadow_colour_tag >> 16) & 0xFF,
                g=(shadow_colour_tag >> 8) & 0xFF,
                b=shadow_colour_tag & 0xFF,
            )
        elif (
            isinstance(shadow_colour_tag, list)
            and len(shadow_colour_tag) == 4
            and all(isinstance(v, (float, int)) for v in shadow_colour_tag)
        ):
            del obj["shadow_color"]
            shadow_colour = RGBAFloat(
                r=float(shadow_colour_tag[0]),
                g=float(shadow_colour_tag[1]),
                b=float(shadow_colour_tag[2]),
                a=float(shadow_colour_tag[3]),
            )
        else:
            shadow_colour = None

        # TODO: Interaction

        return CompoundTextComponent(
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
            unhandled=UnhandledDict(format_id="java", tag=obj) if obj else None,
        )
    else:
        return InvalidJSONTextComponent(tag=obj)


def from_java_json(s: str) -> TextComponent:
    return _from_java_json(json.loads(s))


def _to_java_json(component: TextComponent) -> JSON:
    if isinstance(component, InvalidJSONTextComponent):
        return component.tag
    elif isinstance(component, PlainTextComponent):
        return component.text
    elif isinstance(component, ListTextComponent):
        return [_to_java_json(child) for child in component.components]

    elif isinstance(component, CompoundTextComponent):
        if (
            isinstance(component.unhandled, UnhandledDict)
            and component.unhandled.format_id == "java"
        ):
            d = component.unhandled.tag
        else:
            d = {}

        if component.empty_node is not None:
            d[""] = _to_java_json(component.empty_node)

        if component.content_type is not None:
            d["type"] = component.content_type

        content = component.content
        if isinstance(content, TextContent):
            d["text"] = content.text
        elif isinstance(content, TranslatableContent):
            d["translate"] = content.key
            if content.fallback is not None:
                d["fallback"] = content.fallback
            if content.args is not None:
                d["with"] = [_to_java_json(tag) for tag in content.args]
        elif isinstance(content, ScoreboardContent):
            if (
                isinstance(content.unhandled, UnhandledDict)
                and content.unhandled.format_id == "java"
            ):
                score = content.unhandled.tag
            else:
                score = {}
            score["name"] = content.selector
            score["objective"] = content.objective
            d["score"] = score
        elif isinstance(content, EntityContent):
            d["selector"] = content.selector
            if content.separator is not None:
                d["separator"] = _to_java_json(content.separator)
        elif isinstance(content, KeybindContent):
            d["keybind"] = content.key
        else:
            d["text"] = ""
        # TODO: other content types

        if component.children is not None:
            d["extra"] = [_to_java_json(child) for child in component.children]

        if component.colour is not None:
            colour = component.colour
            r = max(0, min(colour.r, 255))
            g = max(0, min(colour.g, 255))
            b = max(0, min(colour.b, 255))
            if colour.name is None:
                mc_colour = ColourCodes.Java.RGBToColour.get((r, g, b))
                if mc_colour is None:
                    colour_code = f"#{r:02X}{g:02X}{b:02X}"
                else:
                    colour_code = mc_colour.name
            elif RGBHexPattern.fullmatch(colour.name) is not None:
                colour_code = colour.name
            else:
                mc_colour = ColourCodes.Java.NameToColour.get(colour.name)
                if mc_colour is not None and mc_colour.rgb == (r, g, b):
                    colour_code = mc_colour.name
                else:
                    colour_code = f"#{r:02X}{g:02X}{b:02X}"
            d["color"] = colour_code

        if component.font is not None:
            d["font"] = component.font

        if component.bold is not None:
            d["bold"] = component.bold

        if component.italic is not None:
            d["italic"] = component.italic

        if component.underlined is not None:
            d["underlined"] = component.underlined

        if component.strikethrough is not None:
            d["strikethrough"] = component.strikethrough

        if component.obfuscated is not None:
            d["obfuscated"] = component.obfuscated

        if component.shadow_colour is not None:
            if isinstance(component.shadow_colour, RGBAInt):
                d["shadow_color"] = (
                    (component.shadow_colour.a & 0xFF) << 24
                    | (component.shadow_colour.r & 0xFF) << 16
                    | (component.shadow_colour.g & 0xFF) << 8
                    | (component.shadow_colour.b & 0xFF)
                )
            elif isinstance(component.shadow_colour, RGBAFloat):
                d["shadow_color"] = [
                    component.shadow_colour.r,
                    component.shadow_colour.g,
                    component.shadow_colour.b,
                    component.shadow_colour.a,
                ]

        return d
    else:
        return ""


def to_java_json(component: TextComponent) -> str:
    return json.dumps(_to_java_json(component))
