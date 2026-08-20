# Capstone Portfolio Video Runbook

Target duration: 4 minutes. This is a portfolio walkthrough, not the SafeBump agent demo.

## 0:00–0:35 — One claim

Open the live Home page and state the claim in plain language: you build AI agents that run real tools, verify their own work, and know when to ask a human. Show that booking remains the single primary action.

## 0:35–1:40 — Lead proof: SafeBump

Open the SafeBump Work case. Explain that the agent changes one pinned dependency on an isolated branch and uses pytest, `pip check`, version boundaries, and approval state to choose keep, rollback, or ask. Point to the five eval outcomes and the HTTPX rollback. Do not rerun the full SafeBump demo here.

## 1:40–2:25 — Supporting work

Show BE-05 and BE-06 briefly: responsible collection and a trackable job lifecycle. Then show PetAdopt and Local RAG as evidence that model behavior is grounded in real application data or local source material. Avoid reading every metric.

## 2:25–2:55 — Stack decision

Explain that Astro and Netlify were chosen over a custom backend and a heavier application stack because the portfolio was primarily content and evidence. Netlify Forms added the one required dynamic action without turning the site into an authentication or database project.

## 2:55–3:30 — Hardest real break and AI contribution

Show the SafeBump report before and after the honesty fix: a guard-stopped run initially claimed test coverage even though pytest never ran. Explain that AI-assisted critique and the build log helped surface the reporting inconsistency, while you verified the execution path and changed the implementation so coverage is reported only after an observed successful test exit code.

## 3:30–4:00 — Limitation and next step

State that passing tests and clean dependency metadata remain bounded evidence. Name the next project: an explicitly approved draft-PR extension tested against a disposable repository. End with the booking action.

## Recording gate

- Public site is the production version, not a branch preview.
- Contact form succeeds on a fresh submission before recording.
- Every shown repository and report opens while logged out.
- The video is between three and five minutes.
- No notification, token, email address, or unrelated browser tab is exposed.
- The SafeBump demo video and this portfolio walkthrough remain separate uploads.
