# Usability Improvements

Four improvements on top of the working Campus Customs shop — two front-end, two
agent/backend. For each: what was added, and why it helps a shopper or the business.

## Front-end

### 1. Starter suggestion chips in the chat

**What:** Before the shopper has said anything, the chat panel shows one-click starter
questions — "What hoodies do you have?", "Cheapest fleece", "Show me crewnecks". Clicking
one sends it immediately; the chips disappear once the conversation begins. The old plain
"Looking…" label was also replaced with an animated typing indicator.

**Why it helps:** The assistant's best trick — ask a question and watch matching products
fill the page — is invisible to a shopper staring at an empty text box. The chips advertise
that capability and remove the blank-page hesitation, so a first-time visitor gets to a
useful result in one click. For the business, that means more shoppers actually engage the
assistant instead of bouncing, and they immediately see real merchandise.

**Where to see it:** Open the "Ask the shop" panel (bottom-right) on a fresh visit — the
three chips sit just above the input.

### 2. Skeleton loading cards on the product grid

**What:** While the catalogue loads, the Products page shows eight shimmering placeholder
cards instead of a single "Loading…" line.

**Why it helps:** The product grid is the most-visited screen. Placeholder cards keep the
page's layout stable and make the load feel faster, which reduces the sense of waiting and
the chance a shopper leaves before products appear. A steadier, more polished first
impression reflects well on the store.

**Where to see it:** Load or refresh the Products page — the shimmer cards show for the
moment before the 102 products arrive (briefly on a fast connection).

## Agent / backend

### 3. Graceful chat error handling

**What:** If the agent or the Portkey gateway fails, the chat API logs the real error on the
server and returns a friendly fallback message — "Sorry — I'm having trouble reaching the
shop's systems right now. Please try again in a moment." — as a normal reply. It never sends
a raw error or internal detail to the browser.

**Why it helps:** When something breaks, the shopper sees a calm, human message in the chat
rather than a broken panel or a technical error, so the site still feels trustworthy and they
know to try again. For the business, it prevents leaking internal details (a safety and
professionalism win) and keeps a transient outage from looking like a dead site.

**Where to see it:** It only appears on a backend/model failure. Verified by forcing the
agent to fail: the chat shows the friendly line, the server log records the real error, and
no internals reach the client.

### 4. Price-aware search

**What:** The catalogue search understands price intent. "cheapest" / "least expensive"
sorts results by price ascending, "most expensive" descending, and "under $N" / "below $N"
caps the price. Price words don't interfere with matching, so "cheapest fleece" still finds
fleece and "something under $40" still returns items.

**Why it helps:** Shoppers really do ask "what's your cheapest hoodie?" or "anything under
$75?". Before, the search ignored the price part and ranked only by keyword, so the cheapest
item wasn't necessarily shown first — the assistant quietly failed at a basic job. Now a
budget shopper gets the right items, in the right order, drawn straight from the database.
That is a more honest, more helpful assistant, and it nudges price-sensitive shoppers toward
items they can actually afford.

**Where to see it:** Ask the assistant "cheapest hoodie under $70" — the page fills with
hoodies priced $70 or less, lowest first.
