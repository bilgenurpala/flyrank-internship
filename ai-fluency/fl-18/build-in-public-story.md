# Build-in-Public Story Draft

## Recommended channel

LinkedIn is the best first channel because the portfolio is aimed at technical hiring decision-makers and the story can link directly to both the live case and public evidence. Publish only after the final site deployment and replace the links below with the final `main` URLs.

## Draft

I built SafeBump to answer a narrower question than “can an agent update a package?”

The harder question was: what should it do when the available evidence disagrees?

In one evaluation, SafeBump installed HTTPX `1.0.dev3`. `pip check` reported a clean dependency environment, but pytest could not even collect the target tests because an application API had disappeared. The agent treated the failed test gate as decisive, restored `httpx==0.28.1`, reran the baseline checks, and recorded the concrete failure instead of keeping the upgrade.

That rollback is the real win for me. The useful part is not changing a version number. It is making the next action depend on observable evidence and keeping the action reversible.

The limitation matters just as much: six passing tests and a clean `pip check` do not prove that an upgrade is completely safe. The tests cover only the paths they execute, while `pip check` validates declared package metadata rather than runtime API compatibility. Production traffic, concurrency, performance, and untested behavior remain outside that evidence.

SafeBump therefore keeps successful changes only on a local branch and stops before major upgrades, pushes, pull requests, or merges without explicit approval.

Project: https://github.com/bilgenurpala/safebump
Case study: https://bilgenurpala.netlify.app/work#safebump

I am treating the limitation as part of the result, not as a footnote to remove before publishing.

## Before publishing

- Read it aloud and replace any sentence that does not sound natural.
- Confirm both links resolve while logged out.
- Attach one real rollback/report image, not a decorative illustration.
- Do not add claims about time saved, adoption, reliability, or production safety.
