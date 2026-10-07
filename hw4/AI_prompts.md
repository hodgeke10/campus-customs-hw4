# AI Prompts

Log of the prompts I typed into the vibe coder for Homework 4. Each problem follows the same
shape as Homework 3 — the initial prompt, what was lacking after it, and the follow-up
prompt(s). Everything in quotes is exactly what I wrote; the "what was lacking" notes are the
assistant's analysis.

## Setup

> "unzip data.zip so we have data/campus_customs.db (a SQLite database with tables catalogue, inventory, and users), data/products/ (product images, paths match the catalogue table)"

> "This is the scenario for HW4 (don't create anything yet): campus customs needs a real customer website with a helpful chatbot. we will build a react + Vite typescript front end and a python fastapi backend whose brain is a pydanticAI agent. shoppers should be able to browse products, create an account, chat about merch, see matching items appear on the page, and get honest answers about price and stock from a local database. we are given campus_customs.db with tables for product catalogue, inventory by size, and users with hashed passwords. product image file paths are in the catalogue table. research yalebulldogblue.com to learn the syle of the campus customs page and information for our agent prompt. use the PORTKEY_API_KEY."

## Problem 1 — Vibe coder prompts

### Initial prompt

> "create AI_prompts.md to keep a log of what I type into the vibe coder"

### What was lacking after the first prompt

The prompt didn't define the log's format or how much to capture for each entry. I adopted
the Homework 3 convention — initial prompt, what was lacking, follow-up — and quoted the
actual prompts.

## Problem 2 — Analyze the database

### Initial prompt

> "look at the database data/campus_customs.db and understand the fields of each table"

### What was lacking after the first prompt

Understanding the fields didn't say which tables mattered most, or where to write the
findings down for later problems.

### Follow-up prompts

> "at minimum you should understand catalogue, inventory, and users"

> "start the file output/harness.md. write down each table and its fields and one short line about why each field matters for the shop or the chatbot. we will keep growing this harness file in later problems (models, tools, safety, specs)"

## Problem 3 — Build the Campus Customs website

### Initial prompt

> "scaffold a react + vite + typescript front end for Campus Customs. Put a nav bar at the top that links to the main pages: home, products, about us, log in, create account"

### What was lacking after the first prompt

A scaffold with a nav bar left every page empty — no real copy, no product data, no detail
view, no chat, and no API to read the database.

### Follow-up prompts

> "pull campus customs-style wording from yalebulldogblue.com for Home and About Us, but write these pages in a different voice so its not copying the original site text."

> "on the products page, show product images from the catalogue (use the image paths in the database) with basic product info (name, price, short description)."

> "make each product open a single-item page (large image on one side, full product text on the other, description, price, sizes/stock when you have them). Clicking a card on products should take the shopper there."

> "add a chat interface in the bottom right of the site (a floating chat panel is fine). It does not need to talk to an agent yet, a stub that will call your backend later is enough for this problem."

> "we will need a small API soon to read the database. it's fine to start a simple FastAPI app in backend/main.py just to serve products and images, then grow it into the agent backend in problem 5"

## Problem 4 — Create account and login

### Initial prompt

> "build a normal create -account / login flow. Create account: first name, last name, email, password (and confirm password), Log in: email and password. New accounts go into the users table. make sure to store passwords securely"

### What was lacking after the first prompt

The first prompt didn't give a known account to test against (the seeded passwords are
hashed with an unknown iteration count), or ask to document how auth works.

### Follow-up prompt

> "the seed database has a test user you can use while building. Email test@campuscustoms.yale.edu, password: password , confirm that you can log in as that test user, and that a brand new account you create also works. Update output/harness.md with how auth works (what you store for a user and how passwords are protected)"

## Problem 5 — PydanticAI agent backend

### Initial prompt

> "build the shop chatbot as a PydanticAI agent behind FastAPI, plugged into your front-end chat widget. Put the API app in backend/main.py , thats the file we run with Uvicorn. Keep the agent as these four files next to it (same idea as homework 3)
>
> * backend/prompts/prompt.md - system prompt (grow this same file later)
> * backend/agent.py - agent entry / wiring
> * backend/tools.py - tools the agent can call
> * backend/models.py - Pydantic/PydanticAI structured types
>
> in main.py expose a chat route so a message from the website returns a reply from the agent (and whatever else we need for products/auth)."

### What was lacking after the first prompt

The build didn't address search quality, didn't put voice/safety rules in the system
prompt, didn't type the chat/product structures, and didn't document how to run or wire the
backend.

### Follow-up prompts

> "yeah tighten the search"

> "put campus customs voice and safety basics into prompts/prompt.md (we will expand tools and safety later). start or update types in models.py for chat replies / product cards as needed."

> "in output/harness.md note how the front end talks to FastAPI and how the agent is loaded (prompt file + model). Make sure the backend runs from the backend/ folder like this: uvicorn main:app --reload --port 8000"

## Problem 6 — Tools: product info and stock

### Initial prompt

> "give the agent tools that look up real information from campus_customs.db:
>
> * product description
> * price
> * how many are in stock (by size when the customer asks)
>
> the agent must use the database - it should not invent prices or quantities. if a size is out of stock, say so clearly"

### What was lacking after the first prompt

Adding the tools didn't tell the agent (via its prompt) when to call them, didn't give the
results explicit return types, and didn't document which fields were chosen and why.

### Follow-up prompt

> "expand prompts/prompt.md so the agent knows to call these tools for price and stock questions. Add or update return types in models.py. In output/harness.md list each tool and explain which model fields you chose for lookup results and why"

## Problem 7 — Chat search that updates the page

### Initial prompt

> "now we will add a new feature to the site. When a customer asks about a type of item - for example "what hoodies do you have?" - the agent should search the catalogue and the website should dynamically show those matching items as product cards (image, name, price, short info). The is an API contract: the agent returns structured product matches and then the front end renders them on the webiste."

### What was lacking after the first prompt

The new page behavior didn't confirm that the single-item detail view still opened from the
chat-placed cards, or document how the matches travel from the agent to the page.

### Follow-up prompt

> "After the dynamic product cards are loaded by your new feature, make sure the same single-item page behavior we built in Problem 3 still works: each product card, including the one the chat just put on the page, should still open that detail view (large image + full info) when clicked. Update prompts/prompt.md and output/harness.md so it is clear how search results reach the page."

## Problem 8 — Customer memory

### Initial prompt

> "when a shopped is logged in, save their chat history in the database in an appropriate table and reload it when they return. The agent should know who is chatting (name, email) - put that in agent deps (or an equivalent clear pattern) and/or tools the agent can call. Also pass enough page context that if someone is on a product page and asks "do you have this in pink?", the agent knows which item they mean"

### What was lacking after the first prompt

The first prompt focused on logged-in users and didn't say what should happen for guests,
or ask to document how the memory, customer fields, and page context work.

### Follow-up prompt

> "guests can still chat, but history only needs to persist for logged-in users. Document in output/harness.md : how user chat history is stored, what customer fields the agent sees, and how page context is passed"

## Problem 9 — Usability improvements

### Initial prompt

> "Now that the core shop works, improve it. Choose and implement: 2 front-end usability improvments and 2 agent/backend usability improvements"

### What was lacking after the first prompt

Building the improvements didn't include a write-up explaining them, or a check that each
one actually shows up in the running app for graders.

### Follow-up prompt

> "write output/usability.md before or as you build. for each of the improvements say what you added and why it helps a campus customs shopper or the business. Then make sure all improvements actually show up in the running app. Graders will read the write-up and look for the features so this is an important part."

## Problem 10 — Style the website

### Initial prompt

> "now we're adding more style so it feels more real (fonts, color, hierarchy, motion, product presentation, chat feel). Lets make the website more collegiate, preppy, and youthful"

### What was lacking after the first prompt

The style pass restyled the existing layout but added no imagery, so the pages still felt
text-heavy; it also surfaced smaller gaps (a leftover graphic, a product-name typo) and left
room for deeper usability and a short write-up.

### Follow-up prompts

> "lets add photos of college students hanging out on campus to the home page, and some yale graphics of a bull dog"

> "on the home page, for each of the 3 text sections pair them with an appropriate photo, for example the varisty teams part should be next to a photo of a yale student playing a sport. Are you able to search for liscenced yale photos on the web?"

> "now that we have real photos you can remove graphic next to "Gear that lives where you do.""

> "i noted some of the clothing says "1 4 Zip" please change this to "Quarter-Zip""

> "how else would you improve the look of the website?"

> "lets do 1 and 3 from the highest impact list"

> "on the about us page lets add some photos to make the page more interesting to look at"

> "write output/design.md for what we changed and why it should help customers stick around and buy. keep it concrete and short"

> "i think we can make that even more straightforward"

## Problem 12 — Audit trail, safety, finish harness

### Initial prompt

> "keep an append-only output/audit_trail.json of agent-loop activity (time, tool name, short args/result, stop reason). do not wipe it between runs."

### What was lacking after the first prompt

The audit-trail prompt covered logging but not the safety rules the agent needed, nor a
finished harness; writing to the trail also surfaced three real bugs that were fixed (plural
"hoodies" returning nothing, a wrong usage accessor, and `size="medium"` not mapping to `M`).

### Follow-up prompts

> "what safety rules should we give the agent?"

> "yes put them in prompts/prompt.md"

> "finish output/harness.md so it is clear how the system works.
>
> * model fields in models.py and why you chose them
> * tools and abilities
> * safety rules
> * specs (loop limits, result caps, models, how to run front and back"

## Problem 11 — Site testing (app check)

### Initial prompt

> "test the live site and document it in output/app_check.html (a page you can double-click open). Include clear screenshots and short captions for 1) Chat checking the inventory level of an item (honest stock/price from the DB) 2) the dynamic search-result cards appearing after a category question (ex hoodies) 3) One of the usability features we added in problem 9"

### What was lacking after the first prompt

The first version of this prompt log paraphrased the prompts instead of quoting what I
actually wrote.

### Follow-up prompts

> "in ai_prompts.md quote my actual prompts"

> "still keep your "what was lacking after the first prompt" and "follow-up prompt" framing. Use quotes around what I wrote so its clear to the reader."
