# Dev Log

2026-08-18
- Completed SB-12 by turning the SafeBump README into a stranger-reproducible guide with Linux setup, real report examples, Mermaid decision diagrams, guardrails, eval results, limitations, and MIT licensing.
- Wrote Explain It Like You Built It around the SB-08 keep/rollback boundary and distinguished deterministic tool-driven decisions from open-ended model judgment.
- The README audit exposed missing Git identity setup, branch-lifecycle guidance, and a clearly stated intended user; all three were added instead of assuming prior project context.
- Next: run Open It on Your Phone and Survive the Crit while keeping the live SafeBump case marked in development until the planned 2026-08-21 site update.

2026-08-17
- Completed SB-09 through SB-11: generated per-run Markdown reports, enforced branch/remote/time/attempt guardrails, and executed all five Linux evaluations without mid-run hand editing.
- The first main-guard report falsely listed tests as verified even though pytest never ran; the first rollback reason reduced the concrete `BaseTransport` exception to a generic error count.
- Fixed both honesty defects, preserved the before/after raw records, and verified restoration after a pytest failure and after a real `pip check` conflict with six green tests.
- Submitted Build the Agent with the public SafeBump repository, generated reports, build log, and unedited terminal evidence.

2026-08-16
- SB-06: Built the read-only observation slice, parsed `pip list --outdated` and `pip-audit` JSON, merged direct dependency evidence, and prioritized the vulnerable pytest major upgrade before minor updates.
- SB-07: Built a fixed one-package workflow that created a FastAPI upgrade branch, installed the candidate, captured pytest exit code `0`, reported no decision, and restored the baseline afterward.
- SB-08: Added deterministic keep, rollback, skip, and human-approval decisions; kept verified FastAPI and Uvicorn upgrades on separate branches while leaving the pytest major upgrade for approval.
- Rollback demo: Explicitly tested HTTPX `1.0.dev3`; `pip check` remained clean but pytest collection failed, so SafeBump restored HTTPX `0.28.1` and revalidated the baseline with six passing tests.
- Learned that dependency metadata alone cannot prove runtime compatibility; next, add reporting and honesty guardrails, run all five evals, and capture the unedited Build the Agent evidence.

2026-08-15
- SB-01: Created the separate public SafeBump repository, copied BE-02 into `target/` as a disclosed fixture, and verified the Ubuntu 26.04/Python 3.14 baseline with six passing tests and one existing warning.
- SB-02: Ran every planned tool manually; `pip check` was clean, while `pip-audit` found `PYSEC-2026-1845` in pytest 8.4.2 and listed the major release 9.0.3 as the fix.
- SB-03: Defined security-first prioritization, two mandatory keep gates, complete rollback, default-branch protection, time/attempt limits, remote-action approvals, and bounded-success reporting.
- SB-04: Published five measurable eval cases before implementation, covering patch keep, test rollback, major approval, dependency conflict, and blocked push/PR behavior.
- SB-05: Chose a scripted Python agent over n8n and a Claude Project, submitted Design Your Personal Agent, and closed issues #31–#35; next, build and test the narrowest end-to-end loop against the pre-written evals.

2026-08-14
- Audited the live Home, Work, About, and Contact routes and confirmed that BE-01 through BE-04 are visible on the Work page.
- Prepared the PF-04 DNS walkthrough and kept SafeBump labelled as in development without claiming build results.
- Found that the deployed footer initially failed the four-link requirement, then configured and privately tested a real 30-minute Cal.com booking flow before adding its verified URL to the local site update.
- Tomorrow: start the SafeBump repository and build log after today's site evidence, portal submissions, and issue updates are complete.

2026-08-13
- Completed the no-code study-note workflow and classified it as a manually orchestrated workflow rather than an agent.
- Connected GitHub, documented three live tool calls, and proposed a bounded revision-loop agent upgrade with human review preserved.
- Pressure-tested three portfolio stacks, chose Astro with Netlify, deployed the four-page site, and verified the public URL on a phone.
- Learned that tool access is not agency and that a professional static portfolio still does not need a backend; no matching GitHub issue existed for Agent Concepts and MCP Basics.
- Tomorrow: continue the same deployed project with Ship the Ugly One and replace placeholders only with evidence I can defend.

| Date | What I did | AI-free work |
|------|------------|--------------|
| 2026-08-07 | Closed AI Fluency Week 1: locked the sitemap (Home → Work → About → Contact), set up the Claude Project workspace, prepped FL-01/FL-02/Draw the Path for submission. Found the proof statement read like a generic tagline and reworked it to name what I can actually prove. Real FL-01 blocker is the Anthropic Academy "Framework & Foundations" module, not screenshots. | I wrote the proof-statement rewrite and made the submit/no-submit calls myself; AI reviewed and pointed at the weak spots. |
| 2026-08-08 | FL-03 "The Prompt Ladder". Picked code review & debugging as the FL-01 target and fixed one FastAPI/SQLite snippet (7 planted bugs) as the constant input so only the prompt changes. Ran a naive baseline + five cumulative technique rungs (role, context+motivation, few-shot, output structure, step decomposition) in Claude and drafted the output-difference notes. Clearest finding: the context+motivation rung (V2) gave the biggest jump — in depth, not issue count — and the step-decomposition rung (V5) was what finally caught the quiet non-security bugs. Honest miss: the few-shot rung (V3) fixed format but found nothing new over V2. Cross-model done: ran V5 in ChatGPT (GPT-5.6 via Codex) too — both models caught all 7 answer-key issues (a tie on coverage); ChatGPT was far broader (~23 findings incl. IDOR/rate-limiting/WAL) but noisier, and rated the unclosed connection High where Claude said Medium. | Chose the target task and the cumulative-vs-isolated call myself, and I ran the ChatGPT side. Integrity note: the six Claude runs and the first-pass notes were AI-generated on a tired day — before submitting I still need to re-read every OUTPUT note against the runs, rewrite in my own words so I can defend it, and make the "which output would I paste into the repo" call myself. |
| 2026-08-11 | Four Week 2–3 portfolio cards in one session: Frame It as Cases, The Through-Line, Identity Kit, Curate Your Images. Set the voice card (*direct, technical, honest, no inflated claims*), the one-line claim, three-beat cases for PetAdopt / Foundry Local RAG / Backend Foundations, the Home→Work→About→Contact content map, and the 20-image plan. Hardest part was the before/after edit: the generic AI draft claimed PetAdopt "dramatically improved match quality and user satisfaction" — I have never measured either, so editing was almost entirely deletion. Rejected a generated hero illustration for the SafeBump slot; a metaphor sitting where the proof belongs is weaker than an empty space, because the empty space is honest about the gap. Blocked and recorded: SafeBump does not exist yet so the lead case is a reserved placeholder, and the booking link is not set up despite appearing on all ten CTAs. Next: Ship an Automation Workflow v2. | Made the three structural calls myself: the voice card wording, the one-line claim, and collapsing BE-01…BE-04 into one combined case instead of four so the lead case is not outnumbered on the Work page. Integrity note: the case drafts were AI-assisted from my own handoff notes rather than from a one-question-at-a-time interview, so before submitting I still need to read every case against the actual repos, resolve the `[VERIFY]` markers (PetAdopt test count, Newman collection, whether the RAG 10-question eval is committed), and add the decisions only I know about. Photo for FL-06b not taken yet. |
