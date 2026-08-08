# FL-03 — Submission kit (copy-paste blocks)

Fill the ladder doc with your real runs FIRST. Then do the steps below **in this order**:
push to GitHub → add deliverable link + files on the portal card → close the issue → move the board card.

---

## 1. File placement

Put the ladder doc in the repo at:

```
ai-fluency/fl-03/prompt-ladder.md
```

If you saved output screenshots, put them in:

```
ai-fluency/fl-03/outputs/
```

---

## 2. Devlog entry (repo root `devlog.md`)

English, 3–5 lines. This is a near-final draft — confirm the two bracketed spots after your real runs, then paste it. Do NOT touch SafeBump's `build-log.md` (that opens Day 6).

```
2026-08-08 | FL-03 The Prompt Ladder — built a 6-run prompt ladder for code review on one fixed FastAPI/SQLite snippet: naive baseline + 5 cumulative techniques (role, context+motivation, few-shot, output structure, step decomposition), then ran the final prompt in Claude and ChatGPT and compared.
Stuck/learned: [CONFIRM — which rung underdelivered, e.g. "few-shot mostly parroted the example format instead of finding new issues"]; the step-decomposition pass was what finally surfaced the non-security bugs (missing 404, unclosed connection).
Tomorrow: Day 3 — [next task].
```

---

## 3. Git commit (Conventional Commits)

```bash
git add ai-fluency/fl-03/ devlog.md
git commit -m "docs(fl-03): add prompt ladder — baseline + 5 techniques, cross-model compare, reusable template"
git push
```

After pushing, grab the commit hash:

```bash
git rev-parse --short HEAD
```

---

## 4. Portal card (FL-03 "Prompting Fundamentals on Real Tasks")

- **Deliverable links** (one per line):
  ```
  https://github.com/bilgenurpala/flyrank-internship/tree/main/ai-fluency/fl-03
  ```
- **Files:** attach your output screenshots (if any).
- **Notes (optional):** e.g. "Ladder is cumulative; input fixed across all 6 runs. Honest miss recorded on the few-shot rung."
- Then **Save submission**. Test the GitHub link logged out / in a private window.

---

## 5. Issue closing comment (paste into the FL-03 issue, then Close)

Confirm the two bracketed values first.

```
Delivered: 6-run cumulative prompt ladder for code review (baseline + role, context, few-shot, output structure, step decomposition) + cross-model comparison + reusable template.
Deliverable: https://github.com/bilgenurpala/flyrank-internship/tree/main/ai-fluency/fl-03
Portal: submitted ✅
Commit: [short hash from step 3]
```

---

## 6. Board

Move the FL-03 card: **In progress → Done**.
```
