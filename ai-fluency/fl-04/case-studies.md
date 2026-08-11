# Frame It as Cases — Work That Speaks for Itself

**Bilgenur Pala** · Backend AI Engineering Intern, FlyRank AI
Week 2 · AI Fluency · Deliverable for the portal card *"Frame It as Cases"*

---

## 1. Voice card

> **Direct, technical, honest, no inflated claims.**

This is a standing instruction in my AI workspace. Every piece of portfolio copy — case studies, bio, CTAs — is written and edited against it.

**What it means in practice:**

| Rule | Applied |
|---|---|
| Direct | Lead with the thing itself. No warm-up sentences. |
| Technical | Name the actual tool, protocol, or failure mode. "JWT verification" not "secure login". |
| Honest | If a result is small, say the small number. If something is unverified, say so. |
| No inflated claims | No "production-grade", "seamless", "cutting-edge", "revolutionizing". No metric I cannot point to. |

**Test before publishing:** read the line aloud. If I could not defend it to my mentor with a file, a test run, or a screenshot, it does not ship.

---

## 2. Cases

Each case follows three beats: **the problem → what I did and decided → what came of it.**

Cases are ordered by how strongly they support the claim, not chronologically.

---

### Case 1 — SafeBump: a dependency-upgrade agent that decides for itself

> **Status: not built yet.** Design starts 15 August, build 16–17 August, demo 18 August.
> This section is a reserved slot with the scope agreed in the design phase. Every sentence below
> describes intent, not achievement, and is marked as such. It will be rewritten in the same
> three-beat structure once the agent runs, with real eval results replacing the placeholders.

**The problem**

Upgrading dependencies is work developers keep postponing. Updating a library can quietly break a project, so security debt accumulates instead of getting paid down. The hard part is not performing the upgrade — `pip install -U` does that. The hard part is deciding what to do when the tests go red: keep it, roll it back, or ask a human. A fixed script cannot reason about whether a given breakage is acceptable.

**What I did and decided** *(planned — to be rewritten after the build)*

- Target: a copy of my own BE-02 project, placed under `safebump/target/`. Chosen because it has four pinned packages, six deterministic tests, and no network or API-key dependency — so a failing test means the upgrade broke something, not that the environment flaked.
- Planned loop: scan (`pip list --outdated`, `pip-audit`) → prioritise (security > patch > minor; major never automatic) → open a git branch, upgrade, run `pytest` → keep if tests pass **and** `pip check` is clean, otherwise roll back and record why → write a Markdown report and stop at an approval gate before any push.
- Design decisions taken before writing code: which part of the loop is deterministic code and which part genuinely needs model reasoning; five eval cases written before the build so they are not shaped around the implementation.
- Guardrails: never operates on the main branch, no push or merge without approval, attempt and time limits, and an honesty layer that states "tests passed, but I could not verify this area".

**What came of it**

*To be filled in with real eval results, the raw unedited run capture, and the honest limitations list. No outcome is claimed until the agent has run.*

**Evidence to attach:** repository link, demo video, `evals.md` results, `build-log.md`.

---

### Case 2 — PetAdopt: an AI assistant grounded in a real database

**The problem**

Adoption matching normally happens through filter dropdowns: species, age, size. That fails the people who do not know what to filter for. Someone can describe their living situation and what they can handle in plain language, but a filter form has nowhere to put that. The interesting question was whether a language model could handle the conversation *without* being allowed to invent animals — a model left to itself will happily describe a perfect dog that does not exist in the database.

**What I did and decided**

- Built a FastAPI backend and kept the AI service **separate** from it, rather than calling the model from inside the API layer. That boundary meant the model could be swapped or removed without touching the core CRUD and auth code.
- The assistant asks the user questions, evaluates both text and image input, and matches against the real animal records held in PostgreSQL. The model interprets; the database decides what exists. Recommendations come from actual rows.
- Chose RFC 7807 for error responses and OpenAPI 3.1 for the contract, so failures are machine-readable rather than free-text strings.
- Auth with JWT; the whole stack runs under Docker Compose.
- QA on two levels: `pytest` for the code, and a Newman collection to exercise the endpoints from the outside.

**What came of it**

A working backend where the AI layer is grounded in real application data rather than generating plausible answers. The separation of the AI service from the API is the decision I would defend hardest — it is what makes the system debuggable, because when a recommendation is wrong I can tell whether the model misread the request or the query returned the wrong rows.

*Honest limit:* matching quality was checked by hand against the seeded records. There is no user-facing evaluation set and no adoption outcome data, so I make no claim about match quality at scale.

**Evidence to attach:** repository link, screenshots from `docs/screenshots/`, OpenAPI schema view.
`[VERIFY: confirm the test count and whether the Newman collection is committed before publishing.]`

---

### Case 3 — Foundry Local RAG Assistant: retrieval with no internet at all

**The problem**

Most RAG tutorials assume a hosted model and an API key. That assumption breaks the moment the material is something you cannot send to a third party, or the moment the budget is zero. I wanted to find out what a retrieval assistant actually costs in capability when nothing leaves the machine.

**What I did and decided**

- Built the assistant on Microsoft Foundry Local, running fully offline. No hosted API, no key, no outbound request.
- Decided to evaluate it rather than demo it. Wrote a fixed set of ten questions with known answers and ran them against the assistant.

**What came of it**

**Eight of ten questions answered correctly.** Two were not. That is the honest number, and the two failures were more instructive than the eight successes — they showed me that retrieval quality, not model size, was the binding constraint.

The wider result: I now have a first-hand sense of what local inference gives up and what it does not, which is the kind of judgement you cannot get from reading a comparison table.

**Evidence to attach:** repository link, the ten-question evaluation table.
`[VERIFY: is the ten-question evaluation written down in the repo? If it only exists in your notes, commit it — it is the strongest part of this case.]`

---

### Case 4 — Backend Foundations: four assignments, one progression

> Presented as **one case, not four.** The individual assignments are not portfolio-worthy on their
> own; the progression is. Splitting them into four thin entries would dilute the claim and push
> the lead case down the page.

**The problem**

An agent is only as trustworthy as the system it acts on. Before building anything that upgrades, tests, or rolls back a real project, I needed a backend I actually understood end to end — including how it persists, how it authenticates, and how it is reproduced on a different machine. These four assignments are that groundwork.

**What I did and decided**

Four steps, each one fixing a specific weakness in the previous one:

| Step | What it added | The decision behind it |
|---|---|---|
| **BE-01** — first API endpoints | Three JSON endpoints served with FastAPI over Uvicorn | Started with the HTTP contract itself — methods, status codes, and what the generated Swagger UI reveals about the code |
| **BE-02** — database-backed CRUD | SQLite persistence, full CRUD, six tests | Moved off in-memory state so data survives a restart; used parameterised SQL against injection; wrote tests against endpoint *behaviour*, not implementation |
| **BE-03** — auth | Supabase Auth, verified JWTs, ten tests | Built protection as a **reusable HTTPBearer dependency** rather than repeating a check in every route — one place to get right, one place to break |
| **BE-04** — containerised stack | PostgreSQL + Docker Compose, health checks, named volume | Split the code into route / service / repository layers so storage is interchangeable; the point was orchestration and separation of concerns, not Docker for its own sake |

**What came of it**

BE-02 became the target project for SafeBump. That was not the plan when I built it — it earned the role because it has pinned dependencies, six deterministic tests, and no external services, which makes a red test a real signal instead of a flaky one. The groundwork turned into the test bed.

**Honest technical debt:** BE-04's `requirements.txt` is **not pinned** — versions are not fixed. I know it, it is written down, and if I extend that project it needs a `pip freeze` baseline first. I am leaving it visible rather than quietly fixing it before anyone looks, because it is exactly the class of problem SafeBump exists to deal with.

**Evidence to attach:** repository links, `docs/database-view.png` (BE-02), `docs/swagger-ui.png` (BE-03, lock icons on protected routes).

---

## 3. Bio

**Short version (site header / About intro):**

> I am Bilgenur Pala, a Backend AI Engineering intern at FlyRank AI. I build the backend that lets AI agents act on real systems — run tools, check their own work against tests, and stop when they should not proceed alone.

**Longer version (About page):**

> I am Bilgenur Pala, a Backend AI Engineering intern at FlyRank AI, working in Python and FastAPI. I came to AI work from ordinary backend engineering — PHP and MySQL first, then Python, REST APIs, SQLite and PostgreSQL, auth, and Docker — and that order matters to how I build. An agent is only as reliable as the system underneath it, so I care about the unglamorous parts: what happens when the call fails, what gets rolled back, what the code should decide on its own and what it should hand to a person.
>
> My current work is SafeBump, an agent that upgrades a project's dependencies and proves each upgrade against the project's own test suite, deciding for itself whether to keep it, roll it back, or escalate. I use AI as a mentor rather than as a tool that takes over the work — the decisions, the implementation, and the verification are mine, because I have to be able to defend all three.

`[VERIFY: adjust "intern" if your title or status changes before the site goes live.]`

---

## 4. CTA copy

Every call to action ladders to **one action: book a conversation.**

| Placement | Copy | Note |
|---|---|---|
| Home hero (primary) | **Book a conversation** | The only primary button on the page |
| Home hero (secondary) | See how the agent decides | Anchors to the SafeBump case, not a separate destination |
| End of each case | **Book a conversation** | Repeated at the point of highest interest — right after the evidence |
| Work page footer | Want the reasoning behind any of these? **Book a conversation** | |
| About page close | If you are hiring for this kind of work, **book a conversation** | Names the reader plainly |
| Contact page | **Book a conversation** — 30 minutes, online or in person | Single field of focus; email listed underneath as the fallback |
| Site footer | **Book a conversation** | Present on every page |

**Rejected CTA copy and why:**

- ~~"Let's connect!"~~ — says nothing, asks for nothing specific.
- ~~"Get in touch"~~ — passive, and does not name what happens next.
- ~~"Hire me"~~ — asks for a decision before the reader has had the conversation that would inform it.

---

## 5. Before / after — generic AI copy vs my edited version

One example, kept in full. The generic version is a first-pass AI draft of the PetAdopt opening; the edited version is what I published against the voice card.

### Before — generic AI draft

> PetAdopt is an innovative, AI-powered pet adoption platform that leverages cutting-edge machine learning to seamlessly connect loving families with their perfect furry companions. Built with a robust, production-grade FastAPI backend and powered by state-of-the-art AI, PetAdopt revolutionises the adoption experience by delivering highly personalised, intelligent recommendations that dramatically improve match quality and user satisfaction.

### After — my edited version

> PetAdopt lets someone describe their living situation in plain language instead of guessing at filter dropdowns. A separate AI service interprets the request — text and images — and matches it against the real animal records in PostgreSQL, so every recommendation points at a row that exists. The model interprets; the database decides what is real.

### What I changed and why

| Problem in the draft | Voice card rule it broke | Fix |
|---|---|---|
| "innovative", "cutting-edge", "state-of-the-art", "revolutionises" | No inflated claims | Deleted. None of them carry information. |
| "production-grade" | No inflated claims | Deleted — it is a student project and nothing is in production. |
| "dramatically improve match quality and user satisfaction" | Honest | Deleted outright. **I have no measurement of either.** This was the worst line: an invented result stated as fact. |
| "seamlessly", "perfect furry companions" | Direct | Deleted. Marketing warmth, no substance. |
| "powered by AI" with no mechanism | Technical | Replaced with the actual architecture: a separate AI service, PostgreSQL records, and the grounding boundary between them. |
| Nothing describing an actual decision | Technical | Added the one sentence that carries the case: *the model interprets; the database decides what is real.* |

**The pattern:** the AI draft was longer, warmer, and empty. Its confidence came from adjectives. Everything that made the project worth showing — the grounding boundary, the separated service, the reason it matters — was missing, because the model did not know those things and filled the gap with enthusiasm. Editing was mostly deletion, plus one sentence of substance the draft could never have produced.

---

## 6. Read-aloud check

Every case, the bio, and all CTA copy were read aloud. Lines removed at this stage:

- Any sentence describing a result I cannot point to with a file, a test run, or a screenshot.
- Every superlative not attached to a number.
- Any claim about SafeBump written in the past tense before it exists — the whole case is now explicitly marked as a reserved slot.

**Standing rule:** if I cannot defend a line to my mentor, it does not go on the site.

---

## Open items

- [ ] SafeBump case rewritten with real results after 18 August
- [ ] `[VERIFY]` markers in cases 2 and 3 resolved against the actual repositories
- [ ] Voice card added to the AI workspace as a standing instruction
