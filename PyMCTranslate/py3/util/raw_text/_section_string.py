from __future__ import annotations

from typing import Union, ClassVar, TypeVar
from dataclasses import dataclass
import copy

from .data import (
    ColourCodes,
    TextComponent,
    PlainTextComponent,
    ListTextComponent,
    CompoundTextComponent,
    TextContent,
)


@dataclass(kw_only=True)
class BedrockFormatting:
    colour_codes: ClassVar = ColourCodes.Bedrock
    colour: str = "0"
    bold: bool = False
    italic: bool = False
    obfuscated: bool = False


@dataclass(kw_only=True)
class JavaFormatting:
    colour_codes: ClassVar = ColourCodes.Java
    colour: str = "0"
    bold: bool = False
    italic: bool = False
    underlined: bool = False
    strikethrough: bool = False
    obfuscated: bool = False


Formatting = Union[BedrockFormatting, JavaFormatting]


FormattingT = TypeVar("FormattingT", BedrockFormatting, JavaFormatting)


def _to_section_string(component: TextComponent, src_formatting: FormattingT, dst_formatting: FormattingT) -> list[str]:
    if isinstance(component, PlainTextComponent):
        return [component.text]
    elif isinstance(component, ListTextComponent):
        out = []
        for i, child in enumerate(component.components):
            if i:
                out.extend(_to_section_string(child, copy.copy(src_formatting), dst_formatting))
            else:
                out.extend(_to_section_string(child, src_formatting, dst_formatting))
        return out
    elif isinstance(component, CompoundTextComponent):
        out = []
        # Technically, if empty_node and other data is defined, nothing renders
        if component.empty_node is not None:
            out.extend(_to_section_string(component.empty_node, copy.copy(src_formatting), dst_formatting))

        # Merge formatting with parent formatting
        if component.bold is not None:
            src_formatting.bold = component.bold
        if component.italic is not None:
            src_formatting.italic = component.italic
        if component.obfuscated is not None:
            src_formatting.obfuscated = component.obfuscated
        reset = (
                (dst_formatting.bold and not src_formatting.bold)
                or (dst_formatting.italic and not src_formatting.italic)
                or (dst_formatting.obfuscated and not src_formatting.obfuscated)
        )

        if isinstance(src_formatting, JavaFormatting):
            if component.underlined is not None:
                src_formatting.underlined = component.underlined
            if component.strikethrough is not None:
                src_formatting.strikethrough = component.strikethrough
            reset = (
                reset
                or (dst_formatting.underlined and not src_formatting.underlined)
                or (dst_formatting.strikethrough and not src_formatting.strikethrough)
            )
        if reset:
            out.append("§r")
            dst_formatting.colour = "0"
            dst_formatting.bold = False
            dst_formatting.italic = False
            dst_formatting.obfuscated = False
            if isinstance(dst_formatting, JavaFormatting):
                dst_formatting.underlined = False
                dst_formatting.strikethrough = False

        if component.colour is not None:
            src_formatting.colour = dst_formatting.colour_codes.find_closest(component.colour.r, component.colour.g, component.colour.b)[1]

        if dst_formatting.colour != src_formatting.colour:
            out.append(f"§{src_formatting.colour}")
            dst_formatting.colour = src_formatting.colour

        if src_formatting.bold and not dst_formatting.bold:
            out.append("§l")
        dst_formatting.bold = src_formatting.bold

        if src_formatting.italic and not dst_formatting.italic:
            out.append("§o")
        dst_formatting.italic = src_formatting.italic

        if isinstance(src_formatting, JavaFormatting):
            if src_formatting.underlined and not dst_formatting.underlined:
                out.append("§n")
            dst_formatting.underlined = src_formatting.underlined

            if src_formatting.strikethrough and not dst_formatting.strikethrough:
                out.append("§m")
            dst_formatting.strikethrough = src_formatting.strikethrough

        if src_formatting.obfuscated and not dst_formatting.obfuscated:
            out.append("§k")
        dst_formatting.obfuscated = src_formatting.obfuscated

        content = component.content
        if isinstance(content, TextContent):
            out.append(content.text)

        if component.children is not None:
            for child in component.children:
                out.extend(_to_section_string(child, copy.copy(src_formatting), dst_formatting))
        return out
    else:
        return [""]
