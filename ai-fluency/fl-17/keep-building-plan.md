# The Plan to Keep Building

## Next project

The next bounded extension is an approval-gated draft pull request for SafeBump. After a dependency candidate is kept on a local branch, the maintainer can explicitly approve creation of a draft PR containing the observed test and `pip check` evidence. SafeBump will still never merge automatically.

This is one continuation, not a promise to add major upgrades, npm, multiple repositories, and scheduling at the same time.

## Schedule

- 1–7 September 2026: specify the exact approval input, remote side effects, idempotency rule, and three eval cases before implementation.
- 8–14 September 2026: implement against a disposable repository and verify that missing or repeated approval cannot create unintended remote changes.
- 15–16 September 2026: update the README and add the result to the existing SafeBump case only if the eval evidence supports it.
- First Monday of each month at 10:00: review one concrete next action, evidence gaps, and whether the portfolio needs an update.

## How to add the next case

1. Preserve the original problem, decision, observed outcome, and limitation in the project README or build log.
2. Select only evidence that a visitor can inspect publicly and remove any claim that is not supported by it.
3. Write the case in three beats: the problem, what I did and decided, and what came of it.
4. Add the case to `portfolio/src/pages/work.astro`; add a Home card only if it strengthens the single portfolio claim.
5. Build locally, test every new link and asset, then verify the production deployment on desktop and a physical phone.
6. Recheck the CV, GitHub profile, and portfolio wording so completion status and evidence agree.

## Preserved context

The existing AI workspace remains the source for the proof statement, voice card, stack rationale, identity kit, and case-study structure. Repository artifacts remain the source of technical truth; the workspace does not override test output, raw runs, or build logs.

## Reminder evidence

An active recurring reminder named `SafeBump continuation review` was created in Codex. It runs on the first Monday of each month at 10:00 and asks for one evidence-backed next action rather than a broad roadmap.
