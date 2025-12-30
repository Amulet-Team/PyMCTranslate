from amulet_nbt import StringTag, CompoundTag, ListTag, AnyNBT

from PyMCTranslate.py3.util.raw_text.data import PlainTextComponent, TextComponent
from PyMCTranslate.py3.util.raw_text.bedrock_section_string import (
    from_bedrock_section_string,
)
from PyMCTranslate.py3.util.raw_text.java_section_string import from_java_section_string
from PyMCTranslate.py3.util.raw_text.java_json import from_java_json
from PyMCTranslate.py3.util.raw_text.java_nbt import to_java_nbt


EmptyTag = StringTag()


def escape_tags(tags: list[AnyNBT]) -> list[AnyNBT]:
    if not tags:
        return tags
    tag_0 = tags[0]
    if not all(type(tag_0) == type(tag) for tag in tags[1:]):
        for i, tag in enumerate(tags):
            if not isinstance(tag, CompoundTag):
                tags[i] = CompoundTag({"": tag})
    return tags


def pack_components(
    components: list[TextComponent],
) -> tuple[AnyNBT, AnyNBT, AnyNBT, AnyNBT]:
    java_json = [to_java_nbt(component) for component in components[:4]]
    java_json += [EmptyTag] * (4 - len(java_json))
    java_json = escape_tags(java_json)
    return java_json[0], java_json[1], java_json[2], java_json[3]


def bedrock_string_to_java_nbt(
    text: str,
) -> tuple[AnyNBT, AnyNBT, AnyNBT, AnyNBT]:
    return pack_components(from_bedrock_section_string(text, split_newline=True))


def java_string_to_java_nbt(
    lines: ListTag,
) -> tuple[AnyNBT, AnyNBT, AnyNBT, AnyNBT]:
    return pack_components(
        [
            (
                from_java_section_string(line.py_str)
                if isinstance(line, StringTag)
                else PlainTextComponent(text="")
            )
            for line in lines[:4]
        ]
    )


def java_json_to_java_nbt(
    lines: ListTag,
) -> tuple[AnyNBT, AnyNBT, AnyNBT, AnyNBT]:
    return pack_components(
        [
            (
                from_java_json(line.py_str)
                if isinstance(line, StringTag)
                else PlainTextComponent(text="")
            )
            for line in lines[:4]
        ]
    )


def java_nbt_to_java_nbt(
    lines: ListTag,
) -> tuple[AnyNBT, AnyNBT, AnyNBT, AnyNBT]:
    java_nbt = [line if isinstance(line, StringTag) else EmptyTag for line in lines[:4]]
    java_nbt += [EmptyTag] * (4 - len(java_nbt))
    java_nbt = escape_tags(java_nbt)
    return java_nbt[0], java_nbt[1], java_nbt[2], java_nbt[3]


def unpack_text(tag: CompoundTag) -> tuple[AnyNBT, AnyNBT, AnyNBT, AnyNBT]:
    bedrock_string = tag.get("bedrock_string")
    if isinstance(bedrock_string, StringTag):
        return bedrock_string_to_java_nbt(bedrock_string.py_str)

    java_string = tag.get("java_string")
    if isinstance(java_string, ListTag):
        return java_string_to_java_nbt(java_string)

    java_json = tag.get("java_json")
    if isinstance(java_json, ListTag):
        return java_json_to_java_nbt(java_json)

    java_nbt = tag.get("java_nbt")
    if isinstance(java_nbt, ListTag):
        return java_nbt_to_java_nbt(java_nbt)

    return EmptyTag, EmptyTag, EmptyTag, EmptyTag


def main(nbt):
    front_text_1 = front_text_2 = front_text_3 = front_text_4 = back_text_1 = (
        back_text_2
    ) = back_text_3 = back_text_4 = StringTag()

    if isinstance(nbt, CompoundTag):
        utags = nbt.get("utags")
        if isinstance(utags, CompoundTag):
            front_text_tag = utags.get("front_text")
            if isinstance(front_text_tag, CompoundTag):
                front_text_1, front_text_2, front_text_3, front_text_4 = unpack_text(
                    front_text_tag
                )
            back_text_tag = utags.get("back_text")
            if isinstance(back_text_tag, CompoundTag):
                back_text_1, back_text_2, back_text_3, back_text_4 = unpack_text(
                    back_text_tag
                )

    return [
        ["", "compound", [("front_text", "compound")], 0, front_text_1],
        ["", "compound", [("front_text", "compound")], 1, front_text_2],
        ["", "compound", [("front_text", "compound")], 2, front_text_3],
        ["", "compound", [("front_text", "compound")], 3, front_text_4],
        ["", "compound", [("back_text", "compound")], 0, back_text_1],
        ["", "compound", [("back_text", "compound")], 1, back_text_2],
        ["", "compound", [("back_text", "compound")], 2, back_text_3],
        ["", "compound", [("back_text", "compound")], 3, back_text_4],
    ]
