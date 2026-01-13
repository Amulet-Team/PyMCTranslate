import uuid

from amulet_nbt import CompoundTag, ListTag, IntTag, StringTag


def convert_uuid(tag: CompoundTag):
    id_tag = tag.pop("Id", None)
    if (
        isinstance(id_tag, ListTag)
        and id_tag.list_data_type == IntTag.tag_id
        and len(id_tag) == 4
    ):
        tag["Id"] = StringTag(
            str(
                uuid.UUID(
                    int=((id_tag[0] & 0xFFFFFFFF) << 96)
                    | ((id_tag[1] & 0xFFFFFFFF) << 64)
                    | ((id_tag[2] & 0xFFFFFFFF) << 32)
                    | (id_tag[3] & 0xFFFFFFFF)
                )
            )
        )


def convert_properties(tag: CompoundTag):
    properties_tag = tag.get("properties")
    if isinstance(properties_tag, ListTag):
        new_properties_tag = CompoundTag()
        for prop_tag in properties_tag:
            if isinstance(prop_tag, CompoundTag):
                name = prop_tag.get("name")
                value = prop_tag.get("value")
                signature = prop_tag.get("signature")
                if isinstance(name, StringTag) and isinstance(value, StringTag):
                    new_prop_tag = CompoundTag({"Value": value})
                    if isinstance(signature, StringTag):
                        new_prop_tag["Signature"] = signature
                    new_properties_tag.setdefault(name.py_str, ListTag()).append(
                        new_prop_tag
                    )
        tag["Properties"] = new_properties_tag


def downgrade_name(tag: CompoundTag):
    name_tag = tag.pop("name", None)
    if isinstance(name_tag, StringTag):
        tag["Name"] = name_tag


def main(nbt):
    if isinstance(nbt, CompoundTag):
        utags = nbt.get("utags")
        if isinstance(utags, CompoundTag):
            owner_j19 = utags.get("owner_j19")
            if isinstance(owner_j19, CompoundTag):
                return [
                    [
                        "",
                        "compound",
                        [],
                        "Owner",
                        owner_j19,
                    ]
                ]
            owner_j116 = utags.get("owner_j116")
            if isinstance(owner_j116, CompoundTag):
                # convert list[int, 4] to uuid
                convert_uuid(owner_j116)
                return [
                    [
                        "",
                        "compound",
                        [],
                        "Owner",
                        owner_j116,
                    ]
                ]
            owner_j1205 = utags.get("owner_j1205")
            if isinstance(owner_j1205, CompoundTag):
                convert_uuid(owner_j1205)
                convert_properties(owner_j1205)
                downgrade_name(owner_j1205)
                return [
                    [
                        "",
                        "compound",
                        [],
                        "Owner",
                        owner_j1205,
                    ]
                ]

    return []
