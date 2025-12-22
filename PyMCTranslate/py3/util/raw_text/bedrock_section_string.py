from __future__ import annotations

from typing import overload, Literal, Union

from .data import TextComponent, CompoundTextComponent

from ._section_string import BedrockFormatting, _to_section_string, _from_section_string


@overload
def from_bedrock_section_string(
    section_str: str,
) -> CompoundTextComponent: ...


@overload
def from_bedrock_section_string(
    section_str: str, split_newline: Literal[False]
) -> CompoundTextComponent: ...


@overload
def from_bedrock_section_string(
    section_str: str, split_newline: Literal[True]
) -> list[CompoundTextComponent]: ...


@overload
def from_bedrock_section_string(
    section_str: str, split_newline: bool
) -> Union[CompoundTextComponent, list[CompoundTextComponent]]: ...


def from_bedrock_section_string(
    section_str: str, split_newline: bool = False
) -> Union[CompoundTextComponent, list[CompoundTextComponent]]:
    return _from_section_string(section_str, BedrockFormatting(), split_newline)


def to_bedrock_section_string(
    component: Union[TextComponent, list[TextComponent]],
) -> str:
    if isinstance(component, list):
        return "\n".join(to_bedrock_section_string(line) for line in component)
    else:
        return "".join(
            _to_section_string(component, BedrockFormatting(), BedrockFormatting())
        )
