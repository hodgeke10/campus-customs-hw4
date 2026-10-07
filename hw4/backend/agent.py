"""PydanticAI shop assistant for Campus Customs, wired through Portkey."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent, RunContext, UsageLimits
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

import audit
import tools
from models import AgentReply, ChatTurn

HERE = Path(__file__).resolve().parent

# Load PORTKEY_API_KEY from a .env, trying the project root next to backend/ first (the
# layout in the GitHub repo), then the workspace root used during development, then any
# .env found walking up from the current directory. load_dotenv does not override values
# already set in the environment.
for candidate in (HERE.parent / ".env", *(p / ".env" for p in HERE.parents[1:3])):
    if candidate.exists():
        load_dotenv(candidate)
load_dotenv(find_dotenv(usecwd=True))

MODEL_NAME = "gpt-5.6-luna"
PROMPT_PATH = HERE / "prompts" / "prompt.md"
USAGE_LIMITS = UsageLimits(request_limit=6, tool_calls_limit=8)


@dataclass
class ShopperContext:
    """Who is chatting and where they are — passed to the agent as run dependencies.

    Lets the agent greet by name, and resolve "this"/"it" to the product the shopper is
    currently viewing. All fields are optional: a signed-out shopper browsing the home
    page has none of them.
    """

    name: str | None = None
    email: str | None = None
    current_product_id: str | None = None
    current_product_name: str | None = None


@lru_cache(maxsize=1)
def build_agent() -> Agent[ShopperContext, AgentReply]:
    """Create the shop assistant agent using the Portkey-backed OpenAI gateway."""
    api_key = os.getenv("PORTKEY_API_KEY")
    if not api_key:
        raise RuntimeError("PORTKEY_API_KEY is missing from the workspace-root .env file.")

    client = AsyncOpenAI(
        api_key=api_key,
        base_url=os.getenv("PORTKEY_BASE_URL", "https://api.portkey.ai/v1"),
        default_headers={"x-portkey-api-key": api_key},
    )
    model = OpenAIChatModel(MODEL_NAME, provider=OpenAIProvider(openai_client=client))
    agent = Agent(
        model,
        deps_type=ShopperContext,
        output_type=AgentReply,
        system_prompt=PROMPT_PATH.read_text(encoding="utf-8"),
    )

    @agent.system_prompt
    def shopper_context(ctx: RunContext[ShopperContext]) -> str:
        """Add who-is-chatting and current-page context to the system prompt."""
        deps = ctx.deps
        lines: list[str] = []
        if deps.name:
            who = deps.name + (f" ({deps.email})" if deps.email else "")
            lines.append(f"The signed-in shopper is {who}. Greet them by name when it fits.")
        else:
            lines.append("The shopper is not signed in; you do not know their name.")
        if deps.current_product_id:
            lines.append(
                "The shopper is currently viewing this product: "
                f'"{deps.current_product_name}" (product_id {deps.current_product_id}). '
                'If they say "this", "it", or "this one", they mean that product — use its '
                "product_id with your tools."
            )
        return "\n".join(lines)

    @agent.tool
    def search_catalogue(
        ctx: RunContext[ShopperContext], query: str, limit: int = 6
    ) -> list[dict]:
        """Search the product catalogue for items matching a shopper's request."""
        del ctx
        matches = tools.search_catalogue(query, limit)
        audit.record_tool(
            "search_catalogue",
            {"query": query, "limit": limit},
            f"{len(matches)} matches",
        )
        return [m.model_dump() for m in matches]

    @agent.tool
    def list_categories(ctx: RunContext[ShopperContext]) -> list[str]:
        """List the product categories the shop carries."""
        del ctx
        result = tools.list_categories()
        audit.record_tool("list_categories", {}, f"{len(result)} categories")
        return result

    @agent.tool
    def get_product_details(
        ctx: RunContext[ShopperContext], product_id: str
    ) -> dict | None:
        """Full details for one product, including price and per-size stock."""
        del ctx
        result = tools.get_product_details(product_id)
        audit.record_tool(
            "get_product_details",
            {"product_id": product_id},
            f"{result.name} ${result.price:.2f}" if result else "not found",
        )
        return result.model_dump() if result else None

    @agent.tool
    def check_size_stock(
        ctx: RunContext[ShopperContext], product_id: str, size: str
    ) -> dict | None:
        """Check whether a specific size of a product is in stock."""
        del ctx
        result = tools.check_size_stock(product_id, size)
        audit.record_tool(
            "check_size_stock",
            {"product_id": product_id, "size": size},
            f"{result.size}: {result.quantity} in stock" if result else "not found",
        )
        return result.model_dump() if result else None

    return agent


def _compose_input(message: str, history: list[ChatTurn]) -> str:
    """Fold recent history into the agent's input so follow-ups keep context."""
    parts: list[str] = []
    recent = history[-8:]
    if recent:
        parts.append("Conversation so far:")
        for turn in recent:
            speaker = "Shopper" if turn.role == "user" else "You"
            parts.append(f"{speaker}: {turn.content}")
    parts.append(f"Shopper: {message}")
    return "\n".join(parts)


async def run_chat(
    message: str,
    history: list[ChatTurn] | None = None,
    shopper: ShopperContext | None = None,
) -> AgentReply:
    """Run one turn of the shop conversation and return the structured reply."""
    agent = build_agent()
    prompt = _compose_input(message, history or [])
    try:
        result = await agent.run(
            prompt, deps=shopper or ShopperContext(), usage_limits=USAGE_LIMITS
        )
    except Exception as exc:  # noqa: BLE001 — record the stop reason, then re-raise
        audit.record_run_end(f"error: {type(exc).__name__}")
        raise

    # Record why the loop stopped and how much work it took. `usage` is an attribute in
    # some pydantic-ai versions and a method in others — handle both.
    usage = result.usage
    usage = usage() if callable(usage) else usage
    audit.record_run_end(
        "completed",
        products_shown=len(result.output.product_ids),
        requests=getattr(usage, "requests", None),
    )
    return result.output
