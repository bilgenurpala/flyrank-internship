# Survive the Crit

## Proof statement

I build the backend that makes AI agents act on real systems: agents that run tools, verify their own work against tests, and roll back or ask a human when something breaks. I am proving this to a technical decision-maker in an AI product team, and I want that person to book a conversation with me.

Live portfolio: https://bilgenurpala.netlify.app/

## Review questions

1. In ten seconds, what do you think I do?
2. Based on this portfolio, do you believe I can build reliable backend AI systems? Why or why not?

## Reviewer feedback

The reviewer understood the architecture claim: the model interprets, the database decides, and the portfolio reports evidence honestly. The reviewer identified a credibility gap: the work did not visibly establish behavior under load or concurrency, and the portfolio did not clearly show production logging or tracing.

## Triage

### Must-fix

- Make the boundary between tested reliability and untested production reliability visible before a reader can overgeneralize the claim.
- State clearly that the evidence includes functional checks and controlled failure paths, but not sustained load, multi-process concurrency, or production telemetry.

### Nice-to-have

- Add structured run-level logging and trace correlation to a future production-oriented case.
- Add load and concurrency tests with explicit acceptance thresholds instead of implying them from functional test results.

## Changes made

- Added an evidence boundary directly below the homepage proof metrics.
- Added a concise limitation beside the SafeBump lead case.
- Expanded the SafeBump case-study boundary to name load, concurrency, logging, and tracing as untested areas.
- Kept existing failure evidence visible without claiming that controlled rollback tests prove production resilience.

## Response to the reviewer

That gap is fair. The current evidence covers functional checks and controlled failure paths, not sustained load, multi-process concurrency, or production telemetry. I updated the live portfolio so that boundary is visible, and I have kept load testing plus structured logs and traces as named next steps rather than claiming evidence I do not have.
