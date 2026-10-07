"""Structured types for the Campus Customs shop assistant agent and chat API."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


# ---------- Conversation ----------


class ChatTurn(BaseModel):
    """One prior message in the conversation, sent by the front end."""

    role: str = Field(description="Either 'user' or 'assistant'.")
    content: str = Field(description="The message text.")


class AgentReply(BaseModel):
    """The agent's structured output.

    The agent chooses which catalogue products to surface by id only; the backend
    hydrates those ids into full product cards from the database, so prices and stock
    shown to the shopper always come from the data, never from the model.
    """

    reply: str = Field(description="The assistant's message to the shopper, in plain text.")
    product_ids: list[str] = Field(
        default_factory=list,
        description="product_id values to display as cards beside the reply, in order. "
        "Empty when no specific products should be shown.",
    )


# ---------- Product cards (API response shape) ----------


class InventoryItem(BaseModel):
    """Stock for one size of a product."""

    size: str
    quantity: int


class ProductCard(BaseModel):
    """A product as shown on the site and in chat replies.

    Built from the database (never the model), so every field is authoritative. Matches
    the shape the front end's product grid, detail page, and chat cards consume.
    """

    model_config = ConfigDict(extra="ignore")

    product_id: str
    name: str
    garment_type: str
    category: str
    description: str
    short_description: str
    colors: list[str]
    search_tags: list[str]
    image_file_path: str
    image_url: str
    price: float
    inventory: list[InventoryItem]
    total_stock: int


class ChatResponse(BaseModel):
    """What `POST /api/chat` returns to the website."""

    reply: str = Field(description="The assistant's message.")
    products: list[ProductCard] = Field(
        default_factory=list,
        description="Products to display as cards beside the reply, in order.",
    )


# ---------- Tool return types ----------
#
# These are what the agent's tools hand back. They are deliberately leaner than
# ProductCard: a card is for display, whereas a lookup result is for the agent to reason
# and answer from, so each carries only the fields a price/stock question needs.


class ProductSummary(BaseModel):
    """A search hit — just enough to name a product and compare on price/availability."""

    product_id: str = Field(description="Handle to look up full details or show a card.")
    name: str
    category: str
    colors: list[str]
    price: float
    total_stock: int = Field(description="Units across all sizes; 0 means fully sold out.")


class ProductDetails(BaseModel):
    """Full lookup for one product: the source of truth for description, price, stock."""

    product_id: str
    name: str
    category: str
    description: str = Field(description="The catalogue description, for 'what is this' questions.")
    colors: list[str]
    price: float = Field(description="Authoritative price; quote exactly.")
    inventory: list[InventoryItem] = Field(description="Quantity for every size.")
    sizes_in_stock: list[str] = Field(description="Sizes with quantity > 0.")
    sizes_out_of_stock: list[str] = Field(description="Sizes at 0, so out-of-stock is stated plainly.")
    total_stock: int


class SizeStock(BaseModel):
    """Answer to 'do you have this in <size>?' for one product and size."""

    product_id: str
    name: str
    size: str
    quantity: int = Field(description="Units of this size; 0 means out of stock.")
    in_stock: bool = Field(description="True only when quantity > 0.")
    note: str | None = Field(
        default=None, description="Set when the size is not one this product comes in."
    )
