from __future__ import annotations

from typing import overload, Literal, Union


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
