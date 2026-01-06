from __future__ import annotations

from typing import Union, ClassVar, TypeVar, overload, Literal
from dataclasses import dataclass
import copy

from .data import (
    Colour,
    ColourCodes,
    TextComponent,
    PlainTextComponent,
    ListTextComponent,
    CompoundTextComponent,
    TextContent,
)


@dataclass(kw_only=True, slots=True)
class BedrockFormatting:
    colour_codes: ClassVar = ColourCodes.Bedrock
    colour: str = "0"
    bold: bool = False
    italic: bool = False
    obfuscated: bool = False


@dataclass(kw_only=True, slots=True)
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


@overload
def _from_section_string(
    section_str: str, formatting: Formatting, split_newline: Literal[False]
) -> CompoundTextComponent: ...


@overload
def _from_section_string(
    section_str: str, formatting: Formatting, split_newline: Literal[True]
) -> list[CompoundTextComponent]: ...


@overload
def _from_section_string(
    section_str: str, formatting: Formatting, split_newline: bool
) -> Union[list[CompoundTextComponent], CompoundTextComponent]: ...


def _from_section_string(
    section_str: str, formatting: Formatting, split_newline: bool
) -> Union[TextComponent, list[TextComponent]]:
    lines: list[CompoundTextComponent] = []
    line = CompoundTextComponent()

    def get_simplifid_line() -> TextComponent:
        if line.children:
            if len(line.children) == 1:
                return line.children[0]
            else:
                return line
        else:
            return PlainTextComponent(text="")

    def reset_formatting() -> None:
        formatting.colour = "0"
        formatting.bold = False
        formatting.italic = False
        formatting.obfuscated = False
        if isinstance(formatting, JavaFormatting):
            formatting.underlined = False
            formatting.strikethrough = False

    reset_formatting()

    buffer: list[str] = []

    def append_to_line() -> None:
        if not buffer:
            return
        if (
            formatting.colour != "0"
            or formatting.bold
            or formatting.italic
            or formatting.obfuscated
            or (
                isinstance(formatting, JavaFormatting)
                and (formatting.underlined or formatting.strikethrough)
            )
        ):
            component = CompoundTextComponent()
            component.content = TextContent(text="".join(buffer))
            if formatting.colour != "0":
                colour = formatting.colour_codes.SectionCodeToColour.get(
                    formatting.colour
                )
                if colour is not None:
                    r, g, b = colour.rgb
                    component.colour = Colour(name=None, r=r, g=g, b=b)
            if formatting.bold:
                component.bold = True
            if formatting.italic:
                component.italic = True
            if formatting.obfuscated:
                component.obfuscated = True
            if isinstance(formatting, JavaFormatting):
                if formatting.underlined:
                    component.underlined = True
                if formatting.strikethrough:
                    component.strikethrough = True
        else:
            component = PlainTextComponent(text="".join(buffer))
        if line.children is None:
            line.children = []
        line.children.append(component)
        buffer.clear()

    index = 0
    section_str_len = len(section_str)
    while index < section_str_len:
        char = section_str[index]
        index += 1
        if char == "§":
            append_to_line()
            if index < section_str_len:
                char = section_str[index]
                index += 1
                if char in formatting.colour_codes.SectionCodeToColour:
                    formatting.colour = char
                elif char == "k":  # obfuscated
                    formatting.obfuscated = True
                elif char == "l":  # bold
                    formatting.bold = True
                elif char == "o":  # italic
                    formatting.italic = True
                elif char == "r":  # reset
                    reset_formatting()
                elif isinstance(formatting, JavaFormatting):
                    if char == "m":  # strikethrough
                        formatting.strikethrough = True
                    elif char == "n":  # underlined
                        formatting.underlined = True
        elif split_newline and char == "\n":
            append_to_line()
            lines.append(get_simplifid_line())
            line = CompoundTextComponent()
        else:
            buffer.append(char)

    # There may still be data in the buffer
    append_to_line()

    if split_newline:
        if line.children:
            lines.append(get_simplifid_line())
        return lines
    else:
        return get_simplifid_line()


def _to_section_string(
    component: TextComponent, src_formatting: FormattingT, dst_formatting: FormattingT
) -> list[str]:
    if isinstance(component, PlainTextComponent):
        return [component.text]
    elif isinstance(component, ListTextComponent):
        out = []
        for i, child in enumerate(component.components):
            if i:
                out.extend(
                    _to_section_string(child, copy.copy(src_formatting), dst_formatting)
                )
            else:
                out.extend(_to_section_string(child, src_formatting, dst_formatting))
        return out
    elif isinstance(component, CompoundTextComponent):
        out = []
        # Technically, if empty_node and other data is defined, nothing renders
        if component.empty_node is not None:
            out.extend(
                _to_section_string(
                    component.empty_node, copy.copy(src_formatting), dst_formatting
                )
            )

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
            src_formatting.colour = dst_formatting.colour_codes.find_closest(
                component.colour.r, component.colour.g, component.colour.b
            ).section_code

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
                out.extend(
                    _to_section_string(child, copy.copy(src_formatting), dst_formatting)
                )
        return out
    else:
        return [""]
