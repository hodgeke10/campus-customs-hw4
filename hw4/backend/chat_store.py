"""Persistence for shop-assistant conversations in the chat_messages table."""

from __future__ import annotations

import json
from typing import Any

import db


def save_exchange(
    user_id: int, user_message: str, assistant_message: str, products: list[dict[str, Any]]
) -> None:
    """Store one user turn and the assistant's reply, with the products shown.

    Mirrors the seeded chat_messages format: the assistant row carries the full
    product objects it displayed in products_json, so reloading restores the cards.
    """
    with db.connect() as conn:
        conn.execute(
            "INSERT INTO chat_messages (user_id, role, content, products_json) "
            "VALUES (?, 'user', ?, NULL)",
            (user_id, user_message),
        )
        conn.execute(
            "INSERT INTO chat_messages (user_id, role, content, products_json) "
            "VALUES (?, 'assistant', ?, ?)",
            (user_id, assistant_message, json.dumps(products)),
        )
        conn.commit()


def load_history(user_id: int) -> list[dict[str, Any]]:
    """Return a shopper's messages oldest-first, with any shown products parsed."""
    with db.connect() as conn:
        rows = conn.execute(
            "SELECT role, content, products_json FROM chat_messages "
            "WHERE user_id = ? ORDER BY id",
            (user_id,),
        ).fetchall()
    history = []
    for row in rows:
        products = json.loads(row["products_json"]) if row["products_json"] else []
        history.append(
            {"role": row["role"], "content": row["content"], "products": products}
        )
    return history
