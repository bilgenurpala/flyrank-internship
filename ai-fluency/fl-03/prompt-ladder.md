# FL-03 — The Prompt Ladder

**Task (from FL-01 audit):** Code review & debugging
**Target skill proven:** getting a model to produce a *usable, trustworthy* code review instead of a vague "looks fine."
**Method:** The **input is fixed** (same code snippet for all six runs). Only the **prompt technique** changes. The ladder is **cumulative** — each rung keeps the previous techniques and adds exactly one new named technique. The final rung (all five techniques) becomes the reusable template.

> Grading note to self: the notes that count describe **what changed in the OUTPUT**, not what changed in the prompt. Fill the `OUTPUT →` line in your own words after each real run. Do not skip the honest "this didn't help" moment.

---

## The fixed input (paste this same block into every run)

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

**Known real problems in this snippet** (your private answer key — use it to judge each run, do NOT paste it into the prompt):

1. SQL injection via f-string in both endpoints (the main one).
2. No parameterized queries.
3. DB connection is never closed → resource leak.
4. `get_task` returns `{"task": null}` with HTTP 200 when the id doesn't exist → should be 404.
5. No type hints / no Pydantic model → `title`, `done`, `task_id` are unvalidated; `create_task` takes query params instead of a request body.
6. No error handling around the DB calls.
7. `done` is inserted raw with no boolean/int validation.

A run's quality = how many of these it catches, how correctly it rates their severity, and whether the output is something you could act on directly.

---

## Baseline — naive one-liner (no technique)

**Prompt:**
```
Is this code okay?
[paste the fixed input]
```

**Run it. Save the raw output below.**

```
BASELINE OUTPUT ↓ (paste real output)


```

**Notes (4):**
- Prompt → nothing but the question. No role, no context, no format, no steps.
- **OUTPUT → ← YOU WRITE THIS. What did the answer actually look like? (e.g. how many of the 7 issues did it find? Did it miss SQL injection? Was it a wall of prose or actionable? Did it invent problems that aren't there?)**
- Still broken → ← what's missing / wrong in this output?
- Next → give the model a job title, so it reviews *as a security engineer* rather than a generic assistant. → V1.

---

## V1 — + Role assignment

**Technique added:** role assignment (one sentence giving the model an identity + a lens).
**Why it should help:** "Is this okay?" lets the model answer as a polite generalist. Naming a *senior backend security engineer* biases it toward the failure modes that role looks for (injection, resource handling, error paths) instead of surface style.

**Prompt:**
```
You are a senior backend security engineer doing a code review.
Review this FastAPI code and tell me the problems.
[paste the fixed input]
```

```
V1 OUTPUT ↓ (paste real output)


```

**Notes (4):**
- Prompt → added one role sentence. Everything else identical to baseline.
- **OUTPUT → ← YOU WRITE THIS. Compared to baseline: did security issues move up? Did it now catch the SQL injection if baseline missed it? Did the tone/depth change? Be specific — "it found 2 more issues and led with injection" beats "it was better".**
- Still broken → ← e.g. does it still explain nothing about *why*, or ramble without priorities?
- Next → the model doesn't know where this code runs or what you care about. Add context + motivation. → V2.

---

## V2 — + Context & motivation

**Technique added:** context and motivation (what the code is, where it runs, who you are, what you want).
**Why it should help:** severity is meaningless without context. "Public internet + stores user input" turns SQL injection from a style nit into a Critical. Telling it you're a junior who wants the *why* changes the explanation depth.

**Prompt:**
```
You are a senior backend security engineer doing a code review.

Context: this is a small FastAPI + SQLite API that stores user tasks. It is
exposed on the public internet and the inputs come from anonymous users. I am
a junior engineer — I want to understand not just what is wrong but why it
matters and what could go wrong in production. Prioritise security and
correctness over style.

Review this code and tell me the problems.
[paste the fixed input]
```

```
V2 OUTPUT ↓ (paste real output)


```

**Notes (4):**
- Prompt → added context (public internet, SQLite, user input) + motivation (junior, wants the "why", security first).
- **OUTPUT → ← YOU WRITE THIS. Did severities re-rank now that it knows it's public-facing? Did the explanations get deeper / more concrete ("an attacker could send `1 OR 1=1`...")? Did it drop or keep the minor style notes?**
- Still broken → ← e.g. is the output shape still inconsistent — some issues detailed, some one-liners?
- Next → the model doesn't know what a *good* finding looks like to you. Show it one example. → V3.

---

## V3 — + Few-shot example

**Technique added:** few-shot (one worked example of the exact finding format + level of detail you want).
**Why it should help:** telling a model "be detailed" is weaker than *showing* it one finding done right. One example calibrates format, severity labels, and depth for every remaining finding.

**Prompt:**
```
You are a senior backend security engineer doing a code review.

Context: this is a small FastAPI + SQLite API that stores user tasks. It is
exposed on the public internet and the inputs come from anonymous users. I am
a junior engineer — I want to understand not just what is wrong but why it
matters. Prioritise security and correctness over style.

Write each finding in exactly this style:

  Issue: SQL injection in the task_id query
  Severity: Critical
  Why it matters: task_id is put straight into an f-string SQL query, so an
    attacker can send `0 OR 1=1` and read or destroy the whole table.
  Fix: use a parameterised query — cur.execute("... WHERE id = ?", (task_id,))

Now review this code and list every problem in that same style.
[paste the fixed input]
```

**Heads-up (possible honest-fail rung):** the example already hands the model the SQL-injection finding. Watch whether V3 genuinely *adds* value on the other 6 issues, or whether it mostly just parrots the format while finding the same things V2 already found. If it's the latter, this is a legitimate "the technique cost tokens and gave me little" moment — record it honestly instead of pretending every rung was a win.

```
V3 OUTPUT ↓ (paste real output)


```

**Notes (4):**
- Prompt → added one fully-worked example finding (Issue / Severity / Why / Fix). Kept role + context.
- **OUTPUT → ← YOU WRITE THIS. Did every finding now follow the format? Did detail improve on the findings you did NOT hand it — or did giving it the injection example make it lazy/repetitive elsewhere? This is a strong candidate for your honest "this didn't help as much as I expected" note.**
- Still broken → ← e.g. format is consistent but there's still no at-a-glance priority ranking?
- Next → force a machine-like structure so you can scan severities at a glance. → V4.

---

## V4 — + Output structure

**Technique added:** output structure (an explicit table/section schema for the whole answer).
**Why it should help:** a fixed schema (table + summary) removes the model's freedom to bury a Critical in paragraph three. It makes runs comparable and the result directly usable as a checklist.

**Prompt:**
```
You are a senior backend security engineer doing a code review.

Context: small FastAPI + SQLite API storing user tasks, exposed on the public
internet with anonymous input. I am a junior engineer; prioritise security and
correctness over style.

Return your review as:

1. A markdown table with columns:
   | Location | Issue | Severity (Critical/High/Medium/Low) | Why it matters | Suggested fix |
2. Below the table, a "Fix order" list ranking the issues from most to least urgent.

Use this level of detail per row (example row):
| get_task | SQL injection via f-string | Critical | attacker can inject `0 OR 1=1` | use parameterised query with `?` |

Review this code.
[paste the fixed input]
```

```
V4 OUTPUT ↓ (paste real output)


```

**Notes (4):**
- Prompt → replaced free-form with a required table schema + "Fix order" ranking. (Folded the few-shot into one example row.)
- **OUTPUT → ← YOU WRITE THIS. Is it now scannable? Did forcing a table make it DROP any nuance/explanation that the prose version had (structure can cost depth)? Did the "Fix order" match how you'd actually prioritise?**
- Still broken → ← e.g. does it still miss the 404-on-missing-id correctness bug because it's hunting security only?
- Next → make it reason in explicit passes so correctness bugs (not just security) get their own dedicated look. → V5.

---

## V5 — + Step decomposition (final rung = all five techniques)

**Technique added:** step decomposition (make the model work in named passes before answering).
**Why it should help:** a single pass over-indexes on the loudest issue (here, injection). Forcing separate passes — restate → security → correctness → maintainability → rank — is how the quieter bugs (missing 404, unclosed connection, no validation) stop getting skipped.

**Prompt:**
```
You are a senior backend security engineer doing a code review.

Context: small FastAPI + SQLite API storing user tasks, exposed on the public
internet with anonymous input. I am a junior engineer; prioritise security and
correctness over style.

Work in these steps, in order, and show each step:
  Step 1 — Restate in one line what this code is supposed to do.
  Step 2 — Security pass: list every security issue.
  Step 3 — Correctness pass: list every bug that isn't security (wrong status
           codes, unclosed resources, missing validation, etc.).
  Step 4 — Maintainability pass: list style/structure problems.
  Step 5 — Combine everything into one table:
           | Location | Issue | Severity (Critical/High/Medium/Low) | Why it matters | Suggested fix |
           then give a "Fix order" ranking.

Example row for the table:
| get_task | SQL injection via f-string | Critical | attacker can inject `0 OR 1=1` | parameterised query with `?` |

Review this code.
[paste the fixed input]
```

```
V5 OUTPUT ↓ (paste real output)


```

**Notes (4):**
- Prompt → added an explicit 5-step reasoning order on top of role + context + few-shot + structure.
- **OUTPUT → ← YOU WRITE THIS. Did the dedicated "correctness pass" finally catch the non-security bugs V4 skipped (404, unclosed connection, no body model)? How many of the 7 answer-key issues did it get vs baseline? Did the extra steps add real value or just length?**
- Still broken → ← anything from the answer key still missing, or any false positive?
- Next → freeze this as the template and strip the personal context so a stranger can reuse it. → Final template.

---

## Honest "this didn't help" moment

> Pick the ONE rung where the added technique gave you little or nothing (strong candidate: **V3 few-shot**, or possibly **V4 structure** if it cost you explanation depth). Write 2–3 real sentences: what you expected, what actually happened in the output, and why you think it underdelivered. One honest miss here is worth more to the reviewer than five "it got better" notes.

```
← YOU WRITE THIS (2-3 sentences, about a real run)


```

---

## Cross-model comparison (final prompt V5: Claude vs ChatGPT)

Run the **exact same V5 prompt + fixed input** in both. Then write a *specific* difference — "both were good" fails this criterion.

Prompts that force specificity (answer these, don't just vibe-check):
- Which model found **more** of the 7 answer-key issues? Which one did each **miss**?
- Did they **disagree on severity** for any issue (e.g. one rated the missing-404 High, the other Low)?
- Did either **hallucinate** a problem that isn't in the code?
- Which followed the **5-step structure** more faithfully?
- Which corrected-code / fix would you actually **paste into your repo**, and why?

```
CLAUDE vs CHATGPT — specific differences ↓ (YOU WRITE THIS)


```

---

## Reusable final template (stranger-usable, no personal context)

This is the deliverable a stranger could apply to *their* code. All five techniques, personal details replaced by fill-in slots.

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

**How to reuse it:** swap `[DOMAIN]` (backend / frontend / data), rewrite the one-line `Context`, and reorder the priority list. Everything else stays. Works on any language, not just Python.
