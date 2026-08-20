# Send the Link: Build Write-Up

## What I set out to prove

The portfolio has one claim: I build AI agents that use real tools and data, verify what they change, and stop for human judgment at the boundary of their evidence. SafeBump is the lead case because its keep, rollback, and approval actions are visible in committed reports and raw runs. The backend and grounded-AI cases support that claim without competing with it.

## Stack decision

I chose Astro with Netlify for the portfolio. The site is mostly structured evidence, so a custom application backend would add deployment, persistence, and security work without strengthening the claim. A no-code builder would publish quickly but make the case structure, metadata, and evidence presentation harder to keep under version control. Astro keeps the pages small and maintainable; Netlify supplies HTTPS deployment and the single managed form backend the site actually needs.

## Hardest real break

SafeBump's first default-branch guard report listed all six target tests as verified even though the guard stopped before pytest ran. The mutation guard worked, but the report overstated the evidence. I changed coverage reporting so it depends on an observed successful pytest exit code, retained the inaccurate report as before-evidence, and reran the case. A second reporting pass also replaced a generic pytest error count with the concrete missing `httpx.BaseTransport` exception.

This was harder than a visible crash because the program appeared cautious while its explanation was still wrong. It changed how I think about agent evaluation: the final state and the account of how it was reached both need checking.

## What AI contributed

I used AI to pressure-test architecture alternatives, challenge the keep-or-rollback policy, critique reporting language, and turn vague limitations into testable questions. The implementation decisions, command execution, evidence review, and final claims remained mine. The most useful contribution was not generating more code; it was exposing where a plausible explanation was stronger than the observed run supported.

## Real win and limitation

The clearest win was the HTTPX rollback: dependency metadata stayed clean while the application tests failed during collection, and SafeBump restored and reverified the baseline automatically. The limitation is that six tests and `pip check` remain bounded signals. They do not cover production traffic, concurrency, performance, every runtime path, or complete security behavior.

## Next step

The next bounded extension is an approval-gated draft PR. It will require action-specific approval and idempotency tests in a disposable repository. SafeBump will continue to leave merge to a human. Major-version automation, npm, and multi-repository orchestration are not part of this next step.

## Final gate status

The capstone must not be submitted until Checkpoint 1 and Checkpoint 2 pass, the production contact form succeeds on a fresh attempt, analytics evidence exists, the public story and portfolio video are published, the badge is installed if issued, and the site is submitted to the FlyRank showcase.
