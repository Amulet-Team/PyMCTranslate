from amulet_nbt import CompoundTag, StringTag, ListTag

from PyMCTranslate.py3.util.raw_text.bedrock_section_string import (
    to_bedrock_section_string,
)
from PyMCTranslate.py3.util.raw_text.java_section_string import from_java_section_string
from PyMCTranslate.py3.util.raw_text.java_json import from_java_json
from PyMCTranslate.py3.util.raw_text.java_nbt import from_java_nbt


def java_string_to_bedrock_string(lines: ListTag) -> StringTag:
    return StringTag(
        "\n§r".join(
            (
                to_bedrock_section_string(from_java_section_string(line.py_str))
                if isinstance(line, StringTag)
                else ""
            )
            for line in lines[:4]
        )
    )


def java_json_to_bedrock_string(lines: ListTag) -> StringTag:
    return StringTag(
        "\n§r".join(
            (
                to_bedrock_section_string(from_java_json(line.py_str))
                if isinstance(line, StringTag)
                else ""
            )
            for line in lines[:4]
        )
    )


def java_nbt_to_bedrock_string(lines: ListTag) -> StringTag:
    return StringTag(
        "\n§r".join(
            to_bedrock_section_string(from_java_nbt(line)) for line in lines[:4]
        )
    )


def unpack_text(tag: CompoundTag) -> StringTag:
    bedrock_string = tag.get("bedrock_string")
    if isinstance(bedrock_string, StringTag):
        return bedrock_string

    java_string = tag.get("java_string")
    if isinstance(java_string, ListTag):
        return java_string_to_bedrock_string(java_string)

    java_json = tag.get("java_json")
    if isinstance(java_json, ListTag):
        return java_json_to_bedrock_string(java_json)

    java_nbt = tag.get("java_nbt")
    if isinstance(java_nbt, ListTag):
        return java_nbt_to_bedrock_string(java_nbt)

    return StringTag()


def main(nbt):
    front_text = back_text = StringTag()

    if isinstance(nbt, CompoundTag):
        utags = nbt.get("utags")
        if isinstance(utags, CompoundTag):
            front_text_tag = utags.get("front_text")
            if isinstance(front_text_tag, CompoundTag):
                front_text = unpack_text(front_text_tag)
            back_text_tag = utags.get("back_text")
            if isinstance(back_text_tag, CompoundTag):
                back_text = unpack_text(back_text_tag)

    return [
        ["", "compound", [("FrontText", "compound")], "Text", front_text],
        ["", "compound", [("BackText", "compound")], "Text", back_text],
    ]
