"""Tools the shop assistant agent can call.

Every tool reads from the SQLite database via `db`. The agent has no other source of
product facts, so it cannot invent products, prices, or stock. Tools return the typed
lookup models from `models`, so the shapes are explicit and validated.
"""

from __future__ import annotations

import db
from models import ProductDetails, ProductSummary, SizeStock


def search_catalogue(query: str, limit: int = 6) -> list[ProductSummary]:
    """Search the product catalogue for items matching a shopper's request.

    `query` is free text such as "navy hoodie" or "cheapest fleece". Returns the
    best-matching products as summaries (id, name, category, colors, price,
    total_stock). An empty list means nothing matches — tell the shopper we do not carry
    it rather than guessing. To answer a price or stock question, follow up with
    `get_product_details` or `check_size_stock` using a returned product_id.
    """
    return [
        ProductSummary(
            product_id=p["product_id"],
            name=p["name"],
            category=p["category"],
            colors=p["colors"],
            price=p["price"],
            total_stock=p["total_stock"],
        )
        for p in db.search_products(query, limit)
    ]


def list_categories() -> list[str]:
    """List the product categories the shop carries (all apparel)."""
    return db.list_categories()


def get_product_details(product_id: str) -> ProductDetails | None:
    """Look up one product's description, price, and per-size stock.

    Use this for "what is this / how much" questions and for stock across all sizes.
    Includes `sizes_in_stock` and `sizes_out_of_stock` so availability by size can be
    stated directly. Returns None if the product_id is not in the catalogue.
    """
    product = db.get_product(product_id)
    if product is None:
        return None
    return ProductDetails(
        product_id=product["product_id"],
        name=product["name"],
        category=product["category"],
        description=product["description"],
        colors=product["colors"],
        price=product["price"],
        inventory=product["inventory"],
        sizes_in_stock=[i["size"] for i in product["inventory"] if i["quantity"] > 0],
        sizes_out_of_stock=[i["size"] for i in product["inventory"] if i["quantity"] == 0],
        total_stock=product["total_stock"],
    )


def check_size_stock(product_id: str, size: str) -> SizeStock | None:
    """Check how many of a specific size of a product are in stock.

    Use this for "do you have this in <size>?" `size` is one of XS, S, M, L, XL, XXL.
    Returns the quantity and an in_stock flag (with a note if the size is not carried),
    or None if the product_id is unknown.
    """
    result = db.size_stock(product_id, size)
    if result is None:
        return None
    return SizeStock(**result)
