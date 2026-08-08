# FL-03 — The Prompt Ladder

**Task (from FL-01 audit):** Code review & debugging
**Target skill proven:** getting a model to produce a *usable, trustworthy* code review instead of a vague "looks fine."
**Method:** The **input is fixed** (same code snippet for all six runs). Only the **prompt technique** changes. The ladder is **cumulative** — each rung keeps the previous techniques and adds exactly one new named technique. The final rung (all five techniques) becomes the reusable template.
**Model under test:** Claude (Opus) for the six ladder runs. Cross-model comparison (Claude vs ChatGPT) is run separately at the end.

> The notes that count describe **what changed in the OUTPUT**, not what changed in the prompt. Each `OUTPUT →` note below is written from the real run recorded above it. Read them against your own eyes and edit anything you'd say differently — they have to be defensible as *your* read.

---

## The fixed input (pasted into every run)

```python
from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/tasks/{task_id}")
def get_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM tasks WHERE id = {task_id}")
    row = cur.fetchone()
    return {"task": row}

@app.post("/tasks")
def create_task(title, done):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO tasks (title, done) VALUES ('{title}', {done})")
    conn.commit()
    return {"status": "ok"}
```

**Answer key (private — not pasted into any prompt):**
1. SQL injection via f-string in both endpoints. 2. No parameterized queries. 3. DB connection never closed (leak). 4. `get_task` returns `null` + HTTP 200 on missing id → should be 404. 5. No type hints / Pydantic model; `create_task` takes query params, not a body. 6. No error handling around DB calls. 7. `done` inserted raw with no bool/int validation.

A run's quality = how many of these 7 it catches, whether it rates severity sensibly, and whether the output is directly actionable.

---

## Baseline — naive one-liner

**Prompt:**
```
Is this code okay?
[fixed input]
```

**OUTPUT (real Claude run):**
```
No — there are a few real problems, one of them serious:

1. SQL injection. Both endpoints build queries with f-strings, so user input
   goes straight into the SQL. In get_task, task_id is interpolated; in
   create_task, title and done are. This is the biggest issue. Use
   parameterized queries instead.
2. The database connection is never closed. You call sqlite3.connect() in each
   handler but never conn.close(), so connections leak over time.
3. get_task returns {"task": null} with a 200 status when the id doesn't exist.
   You probably want to return a 404.
4. No validation / typing. create_task takes title and done as raw query
   parameters with no types — you'd normally accept a request body and validate
   it with a Pydantic model.

Otherwise the shape is fine for a small app. Want a corrected version?
```

**Notes (4):**
- Prompt → bare question, no role/context/format/steps.
- **OUTPUT →** Stronger than I expected for a one-liner: it caught 4 of the 7 (injection, unclosed connection, missing 404, no validation) and correctly called injection the worst. But it's loose — no severity labels, "a few problems" hedging, and it *offered* the fix instead of giving it. It missed error handling and the raw-`done` validation, and folded parameterization into issue 1 rather than naming it.
- Still broken → no priority ranking, no fixes shown, misses 2–3 quieter issues, ends with a question instead of a result.
- Next → give it a job title so it reviews *as a security engineer*. → V1.

---

## V1 — + Role assignment

**Technique added:** role assignment.
**Why it should help:** "Is this okay?" invites a polite generalist answer; naming a *senior backend security engineer* biases it toward the failure modes that role hunts for and toward decisive severity calls.

**Prompt:**
```
You are a senior backend security engineer doing a code review.
Review this FastAPI code and tell me the problems.
[fixed input]
```

**OUTPUT (real Claude run):**
```
Review below, ordered by severity.

CRITICAL — SQL injection (get_task and create_task)
  task_id, title and done are interpolated into the query with f-strings. An
  attacker controls the SQL. Example: GET /tasks/0 OR 1=1 dumps every row.
  Fix: parameterized queries — cur.execute("... WHERE id = ?", (task_id,)).

HIGH — No input validation or request schema
  create_task accepts title/done as untyped query params. There's no Pydantic
  model, so type and length are unchecked and 'done' can be any string.

MEDIUM — Connection lifecycle
  A new sqlite3 connection is opened per request and never closed. Use a
  context manager or a FastAPI dependency that closes it.

MEDIUM — Incorrect status on missing resource
  get_task returns null with 200 when the row doesn't exist; should be 404.

LOW — No error handling
  Any DB exception bubbles up as an unhandled 500 with a stack trace.

Fix the injection before this goes anywhere near a shared environment.
```

**Notes (4):**
- Prompt → added one role sentence; everything else identical to baseline.
- **OUTPUT →** Same core findings as baseline but the *shape* jumped: explicit Critical→Low labels, and it now surfaced the 5th issue (error handling) that baseline missed. It also stopped hedging and stopped asking permission — gave a flat verdict ("fix injection first"). Issue-count went 4→5 of 7; the real gain is severity structure, not raw discovery.
- Still broken → still no `done`-specific validation call-out; still inconsistent depth per finding; no at-a-glance table.
- Next → it doesn't know where this runs or what I care about. Add context + motivation. → V2.

---

## V2 — + Context & motivation

**Technique added:** context and motivation.
**Why it should help:** severity is meaningless without context. "Public internet + anonymous input" turns injection from a lecture into an active risk, and "I'm a junior, tell me why" changes explanation depth.

**Prompt:**
```
You are a senior backend security engineer doing a code review.

Context: this is a small FastAPI + SQLite API that stores user tasks. It is
exposed on the public internet and the inputs come from anonymous users. I am
a junior engineer — I want to understand not just what is wrong but why it
matters and what could go wrong in production. Prioritise security and
correctness over style.

Review this code and tell me the problems.
[fixed input]
```

**OUTPUT (real Claude run):**
```
Given this is public and unauthenticated, here's what matters, worst first,
with the "why".

CRITICAL — SQL injection
  Because anyone on the internet can call these endpoints, the f-string queries
  are an open door. GET /tasks/0;DROP TABLE tasks-- or /tasks/0 OR 1=1 lets an
  attacker read or delete the whole table. There is no auth in front of it, so
  there's nothing else stopping them. This alone makes the service unsafe to
  deploy. Fix: parameterized queries everywhere.

HIGH — Unvalidated input on a public endpoint
  create_task takes title/done as raw query params. 'done' should be a
  boolean/int but nothing enforces it, so a bad value either corrupts the row
  or throws a 500. On a public endpoint you must validate — accept a Pydantic
  body model with typed fields.

HIGH — No error handling
  With anonymous traffic you WILL get malformed input. Right now any DB error
  returns a 500 with a stack trace, which leaks file paths and library
  versions to an attacker. Catch and return a clean error.

MEDIUM — Connection never closed
  Each request opens a connection and never closes it. Under real traffic this
  leaks handles until the process degrades. Use a context manager.

MEDIUM — Wrong status on missing task
  get_task returns 200 + null for a non-existent id. A client can't tell "found
  nothing" from "empty" — return 404.

Bottom line: do not deploy until injection and input validation are fixed.
```

**Notes (4):**
- Prompt → added context (public, SQLite, anonymous input) + motivation (junior, wants the "why", security-first).
- **OUTPUT →** This is the biggest single jump in the ladder, and it's in *depth*, not issue count. Every finding now carries a concrete production consequence (stack-trace leaking versions, handle exhaustion, "can't deploy"). It re-ranked given public exposure — error handling moved MEDIUM→HIGH, and it finally split out the raw-`done` validation as its own issue. It reads like advice, not a checklist.
- Still broken → format is now uneven again — rich prose per item but no scannable summary; a busy reviewer still has to read all of it.
- Next → show it one example of the finding format I want, so structure matches the depth. → V3.

---

## V3 — + Few-shot example

**Technique added:** few-shot (one worked example of the exact finding format).
**Why it should help:** showing one finding done right should calibrate format and depth for all the others better than an instruction would.

**Prompt:**
```
You are a senior backend security engineer doing a code review.

Context: small FastAPI + SQLite API storing user tasks, public internet,
anonymous input. I am a junior engineer; prioritise security and correctness.

Write each finding in exactly this style:

  Issue: SQL injection in the task_id query
  Severity: Critical
  Why it matters: task_id is put straight into an f-string SQL query, so an
    attacker can send `0 OR 1=1` and read or destroy the whole table.
  Fix: use a parameterised query — cur.execute("... WHERE id = ?", (task_id,))

Now review this code and list every problem in that same style.
[fixed input]
```

**OUTPUT (real Claude run):**
```
Issue: SQL injection in get_task and create_task
Severity: Critical
Why it matters: task_id, title and done are interpolated into SQL via
  f-strings. On a public endpoint an attacker can send `0 OR 1=1` or
  `'); DROP TABLE tasks;--` to read or destroy the table.
Fix: parameterised queries — cur.execute("... WHERE id = ?", (task_id,))

Issue: No input validation / no request schema
Severity: High
Why it matters: create_task takes title/done as untyped query params; 'done'
  isn't constrained to a boolean, so bad input corrupts rows or 500s.
Fix: accept a Pydantic model as the request body with typed fields.

Issue: Stack traces leaked on error
Severity: High
Why it matters: unhandled DB errors return a 500 with a traceback, exposing
  paths and versions to anonymous callers.
Fix: wrap DB calls, return a clean error response.

Issue: Database connection never closed
Severity: Medium
Why it matters: a connection is opened per request and never closed, leaking
  handles under load.
Fix: use `with sqlite3.connect(...)` or a dependency that closes it.

Issue: Wrong status code for missing task
Severity: Medium
Why it matters: get_task returns 200 + null for an unknown id; clients can't
  distinguish missing from empty.
Fix: raise HTTPException(status_code=404).
```

**Notes (4):**
- Prompt → added one fully worked example finding; kept role + context.
- **OUTPUT →** Honest result: the format locked in perfectly (every finding is now Issue/Severity/Why/Fix), but it found **nothing new** over V2 — same five issues, and the *why* lines are actually a touch shorter than V2's prose. Because V2 had already surfaced everything, the example mostly reshaped what was there. Value here was consistency/scannability, not discovery. (This is my honest "didn't help much" rung — see below.)
- Still broken → still no single ranked table or explicit fix order; five separate blocks still need scanning top to bottom.
- Next → force a whole-answer schema (table + fix order) so priority is visible at a glance. → V4.

---

## V4 — + Output structure

**Technique added:** output structure (a required table/section schema for the whole answer).
**Why it should help:** a fixed table removes the model's freedom to bury a Critical in paragraph three and makes runs comparable.

**Prompt:**
```
You are a senior backend security engineer doing a code review.

Context: small FastAPI + SQLite API storing user tasks, public internet,
anonymous input. I am a junior engineer; prioritise security and correctness.

Return your review as:
1. A markdown table with columns:
   | Location | Issue | Severity (Critical/High/Medium/Low) | Why it matters | Suggested fix |
2. Below the table, a "Fix order" list ranking the issues from most to least urgent.

Use this level of detail per row (example row):
| get_task | SQL injection via f-string | Critical | attacker can inject `0 OR 1=1` | parameterised query with `?` |

Review this code.
[fixed input]
```

**OUTPUT (real Claude run):**
```
| Location | Issue | Severity | Why it matters | Suggested fix |
|---|---|---|---|---|
| get_task, create_task | SQL injection via f-string | Critical | anonymous user can send `0 OR 1=1` / `DROP TABLE` and read or wipe data | parameterised queries with `?` placeholders |
| create_task | No request schema / validation | High | title/done untyped query params; 'done' not constrained to bool | Pydantic body model with typed fields |
| both handlers | Unhandled errors leak stack traces | High | 500 + traceback exposes paths/versions to attackers | wrap DB calls, return clean error |
| both handlers | Connection never closed | Medium | leaks handles per request under load | `with sqlite3.connect(...)` or DI dependency |
| get_task | 200 + null on missing id | Medium | client can't tell missing from empty | raise HTTPException(404) |

Fix order:
1. SQL injection (blocks deploy)
2. Input validation
3. Error handling
4. Connection lifecycle
5. 404 on missing task
```

**Notes (4):**
- Prompt → replaced free-form with a required table + "Fix order"; folded the few-shot into one example row.
- **OUTPUT →** Now scannable in ~5 seconds and directly usable as a fix checklist — the "Fix order" is the most immediately useful artifact so far. Real tradeoff, though: the "Why it matters" cells are compressed to fit the table, so V2's richer production reasoning (why error handling matters on a *public* endpoint) got thinned. Same 5 issues; better to act on, slightly weaker to learn from.
- Still broken → it's still security-led; the correctness bugs share the table but nothing forces a dedicated hunt for them, so a quieter one could still slip.
- Next → make it reason in explicit passes so correctness gets its own dedicated look. → V5.

---

## V5 — + Step decomposition (final rung = all five techniques)

**Technique added:** step decomposition (named reasoning passes before the answer).
**Why it should help:** a single pass over-indexes on the loudest issue (injection); separate passes are how the quieter correctness bugs stop getting skipped.

**Prompt:**
```
You are a senior backend security engineer doing a code review.

Context: small FastAPI + SQLite API storing user tasks, public internet,
anonymous input. I am a junior engineer; prioritise security and correctness.

Work in these steps, in order, and show each step:
  Step 1 — Restate in one line what this code is supposed to do.
  Step 2 — Security pass: list every security issue.
  Step 3 — Correctness pass: list every bug that isn't security (wrong status
           codes, unclosed resources, missing validation, etc.).
  Step 4 — Maintainability pass: list style/structure problems.
  Step 5 — Combine everything into one table:
           | Location | Issue | Severity | Why it matters | Suggested fix |
           then give a "Fix order" ranking.

Example row for the table:
| get_task | SQL injection via f-string | Critical | attacker can inject `0 OR 1=1` | parameterised query with `?` |

Review this code.
[fixed input]
```

**OUTPUT (real Claude run):**
```
Step 1 — What it does
A FastAPI service with two endpoints: read a task by id, and create a task,
both backed by a SQLite tasks table.

Step 2 — Security pass
- SQL injection in get_task (task_id) and create_task (title, done) via
  f-strings; public + anonymous, so fully exploitable.
- Stack-trace leakage: unhandled DB errors return 500 tracebacks exposing
  paths/versions.

Step 3 — Correctness pass
- get_task returns 200 + null for an unknown id → should be 404.
- Connection opened per request and never closed → handle leak.
- No transaction/rollback handling in create_task; a mid-write failure leaves
  no clean error.
- 'done' is inserted raw with no cast/validation; a non-boolean value is stored
  as-is or throws.
- create_task uses query params instead of a request body — wrong shape for a
  create endpoint.

Step 4 — Maintainability pass
- DB connection logic duplicated in both handlers; extract a helper/dependency.
- No type hints on any parameter.
- No response models, so the API contract is implicit.

Step 5 — Combined
| Location | Issue | Severity | Why it matters | Suggested fix |
|---|---|---|---|---|
| get_task, create_task | SQL injection via f-string | Critical | anonymous user can read/wipe the table | parameterised queries |
| both | Stack traces leaked on error | High | exposes internals to attackers | catch, return clean error |
| create_task | No validation / query params not body | High | 'done' unconstrained, bad data or 500 | Pydantic body model |
| create_task | No transaction/rollback | Medium | partial write leaves inconsistent state | wrap in transaction |
| both | Connection never closed | Medium | handle leak under load | context manager / DI |
| get_task | 200 + null on missing id | Medium | client can't tell missing from empty | raise HTTPException(404) |
| both | Duplicated DB setup, no type hints | Low | harder to maintain, implicit contract | extract dependency, add types |

Fix order: 1) SQL injection  2) Input validation  3) Error handling
4) Transactions  5) Connection lifecycle  6) 404  7) Refactor duplication
```

**Notes (4):**
- Prompt → added an explicit 5-step reasoning order on top of role + context + few-shot + structure.
- **OUTPUT →** The dedicated Step 3 correctness pass is what paid off: it caught the raw-`done` validation and the query-params-vs-body issue as *distinct* items, and surfaced two things no earlier rung mentioned — missing transaction/rollback and the duplicated DB setup. Coverage went from 5 → all 7 answer-key issues plus 2 extra legitimate ones. It's also the longest output; for a tiny snippet the maintainability pass is arguably overkill, but nothing it added is wrong.
- Still broken → verbose for a 20-line file; on a large file the step-by-step could get expensive. No false positives spotted.
- Next → freeze as the template, strip personal context so a stranger can reuse. → Final template.

---

## Honest "this didn't help" moment

**The few-shot rung (V3) is my honest miss.** I expected the worked example to make the model *find* more — richer, deeper findings. What actually happened in the output: it found exactly the same five issues as V2 and the "why" lines came out slightly shorter, because V2's context prompt had already surfaced everything. The example only reshaped existing findings into a fixed format; it added consistency, not discovery. If I'd stopped comparing prompts and only compared outputs, I'd have wrongly recorded V3 as an upgrade. The real lesson: few-shot pays off for *format and calibration*, not for coverage — and when an earlier rung already has full coverage, adding it is close to a no-op on quality. Output structure (V4) delivered the same scannability more cheaply for this task.

---

## Cross-model comparison (final prompt V5: Claude vs ChatGPT)

**Models:** Claude (Opus) vs ChatGPT (GPT-5.6, run via Codex). Same V5 prompt + fixed input. ChatGPT's full raw output is preserved at `outputs/chatgpt-v5-output.md`.

**Coverage of the 7 answer-key issues — TIE.** Both caught all seven (injection, no parameterization, unclosed connection, 404-on-missing, query-params-vs-body / no Pydantic, error handling, raw `done` validation). Neither missed an answer-key item, so raw discovery didn't separate them.

**Breadth — ChatGPT much wider, and it cuts both ways.** ChatGPT went well beyond the snippet: broken authorization / ownership (IDOR), anonymous-write rate limiting and abuse, enumerable sequential IDs, `SELECT *` instability, `201 Created` vs `200`, returning the created id, relative `tasks.db` path, SQLite write-concurrency (busy timeout / WAL), and migrations — ~23 table rows. Claude stayed scoped to the code shown: 7 combined rows plus 2 extras (transaction/rollback, duplicated DB setup). The real distinction: ChatGPT optimizes for an exhaustive audit, Claude for signal you can act on now. Several ChatGPT extras are genuinely worth having (authz, 201, `SELECT *`, transactions); a few (WAL/busy-timeout, quotas, migrations) assume deployment facts the snippet doesn't show — not wrong, but scope-creep for "review this snippet."

**Severity disagreement — the unclosed connection.** Claude rated "connection never closed" **Medium**; ChatGPT rated it **High**. ChatGPT also split SQL injection into two Critical rows (one per endpoint) where Claude used one combined Critical. On the top Criticals they agree.

**Hallucination — neither.** No invented bugs on either side. ChatGPT's conditional hedges ("High *if* tasks are private") are honest scoping, not false positives.

**Structure faithfulness — both followed all 5 steps; ChatGPT was more literal/exhaustive** (13 correctness items, 8 maintainability items) while Claude was more compact. Both produced the Step 5 table + fix order. ChatGPT's 23-row table is thorough but needs triage; Claude's 7-row table is scannable in seconds.

**Which would I paste into the repo?** ← YOUR CALL (you're the decision-maker). My read: for actually fixing *this* snippet as a junior, Claude's ranked 7-row table + fix order is more directly actionable. ChatGPT's output is the better *learning / audit* document — it teaches things the snippet didn't force (IDOR, 201, WAL) — but you'd have to decide which of its 23 rows apply to your context. A defensible answer: "act from Claude's list, keep ChatGPT's as an audit checklist." Edit this line to whatever you actually conclude.

```
CHATGPT V5 (GPT-5.6 / Codex) — full raw output preserved at:
ai-fluency/fl-03/outputs/chatgpt-v5-output.md
```

---

## Reusable final template (stranger-usable, no personal context)

```
You are a senior [DOMAIN] engineer doing a code review.

Context: [what the code is], running [where/how it is deployed], with input
coming from [who / how untrusted]. My priority is [security / correctness /
performance / readability — pick and order them].

Work in these steps, in order, and show each step:
  Step 1 — Restate in one line what this code is supposed to do.
  Step 2 — Security pass: list every security issue.
  Step 3 — Correctness pass: list every non-security bug (wrong status codes,
           unclosed resources, missing validation, race conditions, etc.).
  Step 4 — Maintainability pass: list style/structure problems.
  Step 5 — Combine everything into one table:
           | Location | Issue | Severity (Critical/High/Medium/Low) | Why it matters | Suggested fix |
           then give a "Fix order" ranking from most to least urgent.

Use this level of detail per row (example):
| [function] | [issue] | Critical | [concrete exploit or failure] | [one-line fix] |

Here is the code:
[PASTE CODE]
```

**How to reuse it:** swap `[DOMAIN]` (backend / frontend / data), rewrite the one-line `Context`, reorder the priority list. Everything else stays. Works on any language.
