"""Sample data generation for demos and tests."""

from __future__ import annotations


def generate_sample_users() -> list[dict[str, object]]:
    return [
        {"user_id": "u1", "name": "Ava", "age": 24, "preferences": ["tech", "design"]},
        {"user_id": "u2", "name": "Noah", "age": 31, "preferences": ["science", "history"]},
    ]


def generate_sample_catalog() -> list[dict[str, object]]:
    return [
        {"content_id": "c1", "title": "Design Systems 101", "category": "design", "tags": ["ui", "ux"]},
        {"content_id": "c2", "title": "Intro to AI", "category": "tech", "tags": ["ml", "data"]},
    ]
