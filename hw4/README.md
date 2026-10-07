# Campus Customs — Yale Bulldog Blue (HW4)

A customer website for Campus Customs with a helpful shop chatbot. React + Vite + TypeScript
front end, Python FastAPI backend, and a PydanticAI agent that answers from a local SQLite
database (honest price and stock) and surfaces matching products on the page.

## The agent (four files under `backend/`)

- `backend/prompts/prompt.md` — system prompt: voice + safety rules.
- `backend/agent.py` — agent wiring (Portkey/`gpt-5.6-luna`), deps, `run_chat()`.
- `backend/tools.py` — the tools the agent can call (search, details, stock, categories).
- `backend/models.py` — structured types (chat reply, product card, tool results).

Supporting backend files: `main.py` (FastAPI app/routes), `db.py`, `auth.py`,
`chat_store.py`, `audit.py`. Design notes are in `output/harness.md`.

## Prerequisites

- Python 3.11+
- Node.js 18+
- A Portkey API key

## 1. Add the data pack

The database and product images are **not** included in this repo. Place the provided data
pack so you have:

```
hw4/data/campus_customs.db
hw4/data/products/<product images>.jpg
```

(The catalogue's `image_file_path` values are relative, e.g. `products/basic-hoodie-big-yale.jpg`,
and the backend serves `hw4/data/` at `/media/`.)

## 2. Set your environment variable

From the `hw4/` folder:

```bash
cp .env.example .env
# then edit .env and set PORTKEY_API_KEY=...
```

## 3. Run the backend (port 8000)

From the `hw4/` folder:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd backend
uvicorn main:app --reload --port 8000
```

The backend serves the JSON API under `/api/...` and the product images under `/media/...`.

## 4. Run the front end (port 5173)

In a second terminal, from the `hw4/frontend/` folder:

```bash
npm install
npm run dev
```

Open the URL Vite prints (http://localhost:5173). In development, Vite proxies `/api` and
`/media` to the backend on port 8000, so both run side by side.

## Using it

- Browse products, open a product for its full detail + per-size stock, create an account or
  log in, and add items to the bag.
- Click **Ask the shop** (bottom-right) to chat. Ask things like "what hoodies do you have?"
  (matching products appear on the page), "how many of these in medium?", or "cheapest
  fleece". The assistant answers price and stock only from the database.

## Notes

- A test account ships in the seed database: `test@campuscustoms.yale.edu` / `password`.
- Agent activity is logged, append-only, to `output/audit_trail.json`.
- Full system documentation: `output/harness.md`.
