import uuid

from amulet_nbt import CompoundTag, ListTag, IntTag, StringTag


def convert_uuid(tag: CompoundTag):
    id_tag = tag.pop("Id", None)
    if isinstance(id_tag, StringTag):
        try:
            uuid_ = uuid.UUID(id_tag.py_str)
        except ValueError:
            pass
        else:
            uuid_int = uuid_.int
            tag["Id"] = ListTag([
                IntTag((uuid_int >> 96) & 0xFFFFFFFF),
                IntTag((uuid_int >> 64) & 0xFFFFFFFF),
                IntTag((uuid_int >> 32) & 0xFFFFFFFF),
                IntTag(uuid_int & 0xFFFFFFFF),
            ])


def convert_properties(tag: CompoundTag):
    properties_tag = tag.get("Properties")
    if isinstance(properties_tag, CompoundTag):
        new_properties_tag = ListTag()
        for prop_name, prop_tags in properties_tag.items():
            if isinstance(prop_tags, ListTag):
                for prop_tag in prop_tags:
                    if isinstance(prop_tag, CompoundTag):
                        value = prop_tag.get("Value")
                        signature = prop_tag.get("Signature")
                        if isinstance(value, StringTag):
                            new_prop_tag = CompoundTag({
                                "name": prop_name,
                                "value": value
                            })
                            if isinstance(signature, StringTag):
                                new_prop_tag["signature"] = signature
                            new_properties_tag.append(new_prop_tag)
        if new_properties_tag:
            tag["properties"] = new_properties_tag


def main(nbt):
    if isinstance(nbt, CompoundTag):
        utags = nbt.get("utags")
        if isinstance(utags, CompoundTag):
            owner_j19 = utags.get("owner_j19")
            if isinstance(owner_j19, CompoundTag):
                convert_uuid(owner_j19)
                convert_properties(owner_j19)
                return [
                    "",
                    "compound",
                    [],
                    "profile",
                    owner_j19,
                ]
            owner_j116 = utags.get("owner_j116")
            if isinstance(owner_j116, CompoundTag):
                convert_properties(owner_j116)
                return [
                    "",
                    "compound",
                    [],
                    "profile",
                    owner_j116,
                ]
            owner_j1205 = utags.get("owner_j1205")
            if isinstance(owner_j1205, CompoundTag):
                return [
                    "",
                    "compound",
                    [],
                    "profile",
                    owner_j1205,
                ]

    return []
