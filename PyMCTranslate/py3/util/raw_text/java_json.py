from __future__ import annotations

from .data import JSON, TextComponent


def from_java_json(json: JSON) -> TextComponent:
    raise NotImplementedError


def to_java_json(component: TextComponent) -> JSON:
    raise NotImplementedError
