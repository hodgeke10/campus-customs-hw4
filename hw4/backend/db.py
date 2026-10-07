"""SQLite access for the Campus Customs shop."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "campus_customs.db"
PRODUCT_IMAGE_DIR = DATA_DIR / "products"

# `garment_type` is entered inconsistently in the catalogue (22 raw values for about six
# real categories), so browsing filters run off this normalized label instead.
# Order matters: the first matching rule wins. Crewneck is tested before T-Shirt so that
# "crewneck sweatshirt" is not caught by a t-shirt keyword, and the t-shirt keyword stays
# hyphenated because a bare "tshirt" also matches inside the word "sweatshirt".
CATEGORY_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("Quarter-Zip", ("quarter-zip",)),
    ("Hoodie", ("hood",)),
    ("Jacket & Fleece", ("jacket", "fleece")),
    ("Performance", ("performance",)),
    ("Crewneck", ("crewneck", "mockneck", "sweater", "sweatshirt")),
    ("T-Shirt", ("t-shirt", "tee")),
]


def normalize_category(garment_type: str) -> str:
    """Collapse a raw garment_type into one browsable category."""
    lowered = garment_type.lower()
    for label, keywords in CATEGORY_RULES:
        if any(keyword in lowered for keyword in keywords):
            return label
    return "Other"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _loads(raw: str) -> list[str]:
    """colors and search_tags are stored as JSON array strings."""
    try:
        value = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return []
    return value if isinstance(value, list) else []


def _short_description(description: str, limit: int = 120) -> str:
    """Trim the catalogue sentence to card length without cutting mid-word."""
    if len(description) <= limit:
        return description
    return description[:limit].rsplit(" ", 1)[0].rstrip(",;") + "…"


def _row_to_product(row: sqlite3.Row, inventory: list[dict[str, Any]]) -> dict[str, Any]:
    image_file_path = row["image_file_path"]
    return {
        "product_id": row["product_id"],
        "name": row["name"],
        "garment_type": row["garment_type"],
        "category": normalize_category(row["garment_type"]),
        "description": row["description"],
        "short_description": _short_description(row["description"]),
        "colors": _loads(row["colors"]),
        "search_tags": _loads(row["search_tags"]),
        "image_file_path": image_file_path,
        # The backend mounts data/products at /media/products.
        "image_url": f"/media/{image_file_path}",
        "price": row["price"],
        "inventory": inventory,
        "total_stock": sum(item["quantity"] for item in inventory),
    }


# Sizes sort alphabetically by default, which would show L before S. Order them the way a
# shopper expects to read them.
SIZE_ORDER_SQL = (
    "CASE size WHEN 'XS' THEN 1 WHEN 'S' THEN 2 WHEN 'M' THEN 3 "
    "WHEN 'L' THEN 4 WHEN 'XL' THEN 5 WHEN 'XXL' THEN 6 ELSE 7 END"
)


def _inventory_by_product(conn: sqlite3.Connection) -> dict[str, list[dict[str, Any]]]:
    rows = conn.execute(
        "SELECT product_id, size, quantity FROM inventory "
        f"ORDER BY product_id, {SIZE_ORDER_SQL}"
    ).fetchall()

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row["product_id"], []).append(
            {"size": row["size"], "quantity": row["quantity"]}
        )
    return grouped


def list_products() -> list[dict[str, Any]]:
    """Every catalogue product with its per-size stock."""
    with connect() as conn:
        inventory = _inventory_by_product(conn)
        rows = conn.execute("SELECT * FROM catalogue ORDER BY name").fetchall()
    return [_row_to_product(row, inventory.get(row["product_id"], [])) for row in rows]


def get_product(product_id: str) -> dict[str, Any] | None:
    """One product with its per-size stock, or None if the id is unknown."""
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM catalogue WHERE product_id = ?", (product_id,)
        ).fetchone()
        if row is None:
            return None
        inventory = [
            {"size": item["size"], "quantity": item["quantity"]}
            for item in conn.execute(
                "SELECT size, quantity FROM inventory WHERE product_id = ? "
                f"ORDER BY {SIZE_ORDER_SQL}",
                (product_id,),
            ).fetchall()
        ]
    return _row_to_product(row, inventory)


def list_categories() -> list[str]:
    """Normalized categories present in the catalogue, in display order."""
    with connect() as conn:
        rows = conn.execute("SELECT DISTINCT garment_type FROM catalogue").fetchall()
    found = {normalize_category(row["garment_type"]) for row in rows}
    ordered = [label for label, _ in CATEGORY_RULES if label in found]
    return ordered + sorted(found - set(ordered))


def get_user_first_name(user_id: int) -> str | None:
    """First name (or full name) for a user id, for personalizing chat replies."""
    with connect() as conn:
        row = conn.execute(
            "SELECT first_name, name FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    if row is None:
        return None
    return row["first_name"] or row["name"]


def get_user(user_id: int) -> dict[str, Any] | None:
    """Public identity for a user id (no password), for the agent's shopper context."""
    with connect() as conn:
        row = conn.execute(
            "SELECT id, name, email, first_name, last_name FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    if row is None:
        return None
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "first_name": row["first_name"],
        "last_name": row["last_name"],
    }


def _score(product: dict[str, Any], terms: list[str]) -> int:
    """Rank a product against query terms across its searchable text fields."""
    name = product["name"].lower()
    category = product["category"].lower()
    garment = product["garment_type"].lower()
    colors = " ".join(product["colors"]).lower()
    tags = " ".join(product["search_tags"]).lower()
    description = product["description"].lower()

    score = 0
    for term in terms:
        if term in name:
            score += 5
        if term in category or term in garment:
            score += 4
        if term in colors:
            score += 3
        if term in tags:
            score += 2
        if term in description:
            score += 1
    return score


def categories_in_query(query: str) -> set[str]:
    """Categories the query explicitly names, via the same keyword rules as filtering.

    Lets a request like "navy quarter-zip" be restricted to quarter-zips rather than
    any navy item.
    """
    lowered = query.lower()
    found = set()
    for label, keywords in CATEGORY_RULES:
        if any(keyword in lowered for keyword in keywords):
            found.add(label)
    return found


# Words that express price intent rather than product content, so they should not count
# toward keyword matching.
_PRICE_WORDS = {
    "cheap", "cheapest", "cheaper", "affordable", "budget", "inexpensive", "lowest",
    "least", "expensive", "priciest", "premium", "high-end", "costly", "under", "below",
    "less", "than", "over", "above", "most",
}
_ASC_WORDS = {"cheap", "cheapest", "cheaper", "affordable", "budget", "inexpensive", "lowest"}
_DESC_WORDS = {"expensive", "priciest", "premium", "high-end", "costly"}


def _price_intent(query: str) -> tuple[str | None, float | None]:
    """Detect price sort direction and a budget cap from the query.

    Returns (sort, cap) where sort is 'asc' | 'desc' | None and cap is an upper price
    bound from phrases like "under $75" / "below 60".
    """
    import re

    lowered = query.lower()
    words = set(lowered.split())

    sort = None
    if words & _ASC_WORDS or "least expensive" in lowered:
        sort = "asc"
    elif words & _DESC_WORDS or "most expensive" in lowered:
        sort = "desc"

    cap = None
    match = re.search(r"(?:under|below|less than|<)\s*\$?\s*(\d+(?:\.\d+)?)", lowered)
    if match:
        cap = float(match.group(1))
        sort = sort or "asc"  # a budget query implies cheapest-first
    return sort, cap


def search_products(query: str, limit: int = 6) -> list[dict[str, Any]]:
    """Keyword-rank catalogue products for a shopper query.

    Matches only the real catalogue, so the agent can never surface a product that
    does not exist. Returns an empty list when nothing scores, which lets the agent
    say plainly that we do not carry the item.

    When the query names one or more categories (e.g. "quarter-zip", "hoodie"), results
    are restricted to those categories. Price intent is also honored: "cheapest" / "least
    expensive" sorts by price ascending, "most expensive" descending, and "under $N" caps
    the price.
    """
    raw_terms = [t for t in query.lower().split() if t]
    if not raw_terms:
        return []

    sort, cap = _price_intent(query)
    # Content terms exclude price words and bare numbers, so "cheapest fleece" matches on
    # "fleece" and a budget-only query like "under $50" still has candidates.
    terms = [t for t in raw_terms if t not in _PRICE_WORDS and not t.lstrip("$").replace(".", "").isdigit()]

    products = list_products()

    target = categories_in_query(query)
    candidates = [p for p in products if p["category"] in target] if target else products

    if target:
        # The shopper named a category, so category membership is enough — rank the whole
        # category by any extra terms (color, etc.). This keeps "hoodies" (plural) or
        # "what hoodies do you have?" returning the hoodies even though the word itself
        # doesn't lexically match a product field.
        ranked = sorted(candidates, key=lambda p: _score(p, terms), reverse=True)
    elif terms:
        scored = [p for p in candidates if _score(p, terms) > 0]
        # If nothing matched by keyword but there is a price intent, fall back to the
        # candidate set so "something under $50" still returns items.
        ranked = (
            sorted(scored, key=lambda p: _score(p, terms), reverse=True)
            if scored
            else (list(candidates) if (sort or cap) else [])
        )
    else:
        ranked = list(candidates) if (sort or cap) else []

    if cap is not None:
        ranked = [p for p in ranked if p["price"] <= cap]

    if sort == "asc":
        ranked = sorted(ranked, key=lambda p: p["price"])
    elif sort == "desc":
        ranked = sorted(ranked, key=lambda p: p["price"], reverse=True)
    else:
        ranked = sorted(ranked, key=lambda p: _score(p, terms), reverse=True)

    return ranked[:limit]


# Shoppers (and the model) say "medium"; the inventory uses "M".
SIZE_ALIASES = {
    "EXTRA SMALL": "XS",
    "SMALL": "S",
    "MEDIUM": "M",
    "MED": "M",
    "LARGE": "L",
    "EXTRA LARGE": "XL",
    "XLARGE": "XL",
    "EXTRA EXTRA LARGE": "XXL",
    "DOUBLE XL": "XXL",
    "2XL": "XXL",
}


def size_stock(product_id: str, size: str) -> dict[str, Any] | None:
    """Stock for one product and size, or None if the product id is unknown."""
    product = get_product(product_id)
    if product is None:
        return None
    wanted = size.strip().upper()
    wanted = SIZE_ALIASES.get(wanted, wanted)
    for item in product["inventory"]:
        if item["size"].upper() == wanted:
            return {
                "product_id": product_id,
                "name": product["name"],
                "size": item["size"],
                "quantity": item["quantity"],
                "in_stock": item["quantity"] > 0,
            }
    return {
        "product_id": product_id,
        "name": product["name"],
        "size": wanted,
        "quantity": 0,
        "in_stock": False,
        "note": f"{wanted} is not a size we carry for this item.",
    }
