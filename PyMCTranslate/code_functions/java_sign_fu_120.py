from amulet_nbt import StringTag, CompoundTag, ListTag

from PyMCTranslate.py3.util.raw_text.data import PlainTextComponent, TextComponent
from PyMCTranslate.py3.util.raw_text.bedrock_section_string import (
    from_bedrock_section_string,
)
from PyMCTranslate.py3.util.raw_text.java_section_string import from_java_section_string
from PyMCTranslate.py3.util.raw_text.java_json import to_java_json
from PyMCTranslate.py3.util.raw_text.java_nbt import from_java_nbt


EmptyJSON = StringTag(r"\"\"")


def pack_components(
    components: list[TextComponent],
) -> tuple[StringTag, StringTag, StringTag, StringTag]:
    java_json = [StringTag(to_java_json(component)) for component in components[:4]]
    java_json += [EmptyJSON] * (4 - len(java_json))
    return java_json[0], java_json[1], java_json[2], java_json[3]


def bedrock_string_to_java_json(
    text: str,
) -> tuple[StringTag, StringTag, StringTag, StringTag]:
    return pack_components(from_bedrock_section_string(text, split_newline=True))


def java_string_to_java_json(
    lines: ListTag,
) -> tuple[StringTag, StringTag, StringTag, StringTag]:
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


def java_json_to_java_json(
    lines: ListTag,
) -> tuple[StringTag, StringTag, StringTag, StringTag]:
    java_json = [
        line if isinstance(line, StringTag) else EmptyJSON for line in lines[:4]
    ]
    java_json += [EmptyJSON] * (4 - len(java_json))
    return java_json[0], java_json[1], java_json[2], java_json[3]


def java_nbt_to_java_json(
    lines: ListTag,
) -> tuple[StringTag, StringTag, StringTag, StringTag]:
    return pack_components([from_java_nbt(line) for line in lines[:4]])


def unpack_text(tag: CompoundTag) -> tuple[StringTag, StringTag, StringTag, StringTag]:
    bedrock_string = tag.get("bedrock_string")
    if isinstance(bedrock_string, StringTag):
        return bedrock_string_to_java_json(bedrock_string.py_str)

    java_string = tag.get("java_string")
    if isinstance(java_string, ListTag):
        return java_string_to_java_json(java_string)

    java_json = tag.get("java_json")
    if isinstance(java_json, ListTag):
        return java_json_to_java_json(java_json)

    java_nbt = tag.get("java_nbt")
    if isinstance(java_nbt, ListTag):
        return java_nbt_to_java_json(java_nbt)

    return EmptyJSON, EmptyJSON, EmptyJSON, EmptyJSON


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
        [
            "",
            "compound",
            [("front_text", "compound"), ("messages", "list")],
            0,
            front_text_1,
        ],
        [
            "",
            "compound",
            [("front_text", "compound"), ("messages", "list")],
            1,
            front_text_2,
        ],
        [
            "",
            "compound",
            [("front_text", "compound"), ("messages", "list")],
            2,
            front_text_3,
        ],
        [
            "",
            "compound",
            [("front_text", "compound"), ("messages", "list")],
            3,
            front_text_4,
        ],
        [
            "",
            "compound",
            [("back_text", "compound"), ("messages", "list")],
            0,
            back_text_1,
        ],
        [
            "",
            "compound",
            [("back_text", "compound"), ("messages", "list")],
            1,
            back_text_2,
        ],
        [
            "",
            "compound",
            [("back_text", "compound"), ("messages", "list")],
            2,
            back_text_3,
        ],
        [
            "",
            "compound",
            [("back_text", "compound"), ("messages", "list")],
            3,
            back_text_4,
        ],
    ]
