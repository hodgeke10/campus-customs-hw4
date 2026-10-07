"""Password hashing and user accounts for Campus Customs.

Stored hashes use the format already present in the seeded database:

    pbkdf2_sha256$<salt>$<hex-digest>

The iteration count is not part of that string, so it is a module constant. New
accounts are hashed with PBKDF2-HMAC-SHA256, a fresh random salt, and this count.
Verification is format-driven: it re-derives the digest from the supplied password
and the stored salt and compares in constant time. Passwords are never stored,
logged, or returned to the client.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import sqlite3
from typing import Any

import db

ALGORITHM = "pbkdf2_sha256"
# Matches the iteration count used to hash the seeded accounts, so one verification path
# works for both the pre-seeded demo users and newly created accounts.
ITERATIONS = 120_000
SALT_BYTES = 16


def hash_password(password: str) -> str:
    """Hash a plaintext password into the stored string format."""
    salt = secrets.token_hex(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), ITERATIONS)
    return f"{ALGORITHM}${salt}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Check a plaintext password against a stored hash string."""
    try:
        algorithm, salt, expected = stored.split("$")
    except ValueError:
        return False
    if algorithm != ALGORITHM:
        return False
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), ITERATIONS)
    return hmac.compare_digest(digest.hex(), expected)


def _public_user(row: sqlite3.Row) -> dict[str, Any]:
    """Shape a user row for the client, omitting the password hash."""
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "first_name": row["first_name"],
        "last_name": row["last_name"],
    }


class EmailTaken(Exception):
    """Raised when a signup email is already registered."""


def create_user(
    first_name: str, last_name: str, email: str, password: str
) -> dict[str, Any]:
    """Insert a new account and return its public fields."""
    email = email.strip().lower()
    first_name = first_name.strip()
    last_name = last_name.strip()
    full_name = f"{first_name} {last_name}".strip()
    password_hash = hash_password(password)

    with db.connect() as conn:
        existing = conn.execute(
            "SELECT 1 FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing:
            raise EmailTaken(email)
        cursor = conn.execute(
            "INSERT INTO users (name, first_name, last_name, email, password_hash) "
            "VALUES (?, ?, ?, ?, ?)",
            (full_name, first_name, last_name, email, password_hash),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM users WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return _public_user(row)


def authenticate(email: str, password: str) -> dict[str, Any] | None:
    """Return the public user if the email/password match, else None."""
    email = email.strip().lower()
    with db.connect() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
    if row is None:
        return None
    if not verify_password(password, row["password_hash"]):
        return None
    return _public_user(row)
