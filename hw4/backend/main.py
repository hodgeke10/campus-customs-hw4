"""FastAPI backend for the Campus Customs shop."""

from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field

import agent
import auth
import chat_store
import db
from models import ChatResponse, ChatTurn

logger = logging.getLogger("campus_customs")

app = FastAPI(title="Campus Customs API")

# The Vite dev server proxies /api and /media, but allow direct calls too.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Product photos live in data/products and are referenced by catalogue.image_file_path,
# so mounting data/ at /media makes those stored paths resolvable as URLs.
app.mount("/media", StaticFiles(directory=db.DATA_DIR), name="media")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/categories")
def categories() -> list[str]:
    return db.list_categories()


@app.get("/api/products")
def products() -> list[dict]:
    return db.list_products()


@app.get("/api/products/{product_id}")
def product(product_id: str) -> dict:
    found = db.get_product(product_id)
    if found is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return found


# ---------- Accounts ----------


class SignupRequest(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


@app.post("/api/signup", status_code=201)
def signup(payload: SignupRequest) -> dict:
    try:
        return auth.create_user(
            payload.first_name, payload.last_name, payload.email, payload.password
        )
    except auth.EmailTaken:
        raise HTTPException(
            status_code=409, detail="An account with that email already exists."
        )


@app.post("/api/login")
def login(payload: LoginRequest) -> dict:
    user = auth.authenticate(payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    return user


# ---------- Chat ----------


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[ChatTurn] = Field(default_factory=list)
    # Optional: present when the shopper is signed in, so the reply can be
    # personalized and the exchange saved to their history.
    user_id: int | None = None
    # Optional: the product the shopper is currently viewing, so "do you have this in
    # pink?" resolves to the right item.
    current_product_id: str | None = None


@app.post("/api/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> dict:
    # Build the shopper context the agent receives as deps: who is chatting and what
    # product page they are on.
    shopper = agent.ShopperContext()
    if payload.user_id is not None:
        user = db.get_user(payload.user_id)
        if user is not None:
            shopper.name = user["first_name"] or user["name"]
            shopper.email = user["email"]
    if payload.current_product_id is not None:
        product = db.get_product(payload.current_product_id)
        if product is not None:
            shopper.current_product_id = product["product_id"]
            shopper.current_product_name = product["name"]

    try:
        reply = await agent.run_chat(
            payload.message, payload.history, shopper=shopper
        )
    except Exception as exc:  # noqa: BLE001
        # Log the real error server-side, but never leak internals to the shopper.
        # Return a friendly fallback as a normal reply so the chat UI stays usable.
        logger.exception("Chat agent failed: %s", exc)
        return {
            "reply": (
                "Sorry — I'm having trouble reaching the shop's systems right now. "
                "Please try again in a moment."
            ),
            "products": [],
        }

    # Hydrate the agent's chosen ids into full products from the database, so prices
    # and stock shown to the shopper are authoritative regardless of what the model said.
    products = [
        product
        for product_id in reply.product_ids
        if (product := db.get_product(product_id)) is not None
    ]

    if payload.user_id is not None:
        chat_store.save_exchange(
            payload.user_id, payload.message, reply.reply, products
        )

    return {"reply": reply.reply, "products": products}


@app.get("/api/chat/history")
def chat_history(user_id: int) -> list[dict]:
    """Prior messages for a signed-in shopper, oldest first."""
    return chat_store.load_history(user_id)
