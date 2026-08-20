# Open It on Your Phone — Fix Log

Date: 19 August 2026
Live site: <https://bilgenurpala.netlify.app/>

## Scope

The required route is Home → Work → About → Contact. The portfolio has one primary conversion action: opening the public 30-minute Cal.com booking page.

## Pre-device Audit and Fixes

| Finding | Change | Verification status |
| --- | --- | --- |
| Mobile navigation links used padding that produced targets smaller than the recommended 44 px minimum. | Set every primary-navigation link to a minimum height of 44 px and retained a readable 14 px mobile label size. | Production build passed; real-phone touch check pending. |
| Inline case links, repository links, and footer links did not guarantee a 44 px touch target. | Converted them to aligned inline-flex targets with a 44 px minimum height. | Production build passed; real-phone touch check pending. |
| The Contact page visually presented GitHub as the primary action. | Made `Book a conversation` the first and only primary button; kept GitHub, LinkedIn, and CV as secondary evidence links. | Source and rendered HTML checked; real-phone booking check pending. |
| The About closing CTA routed through Contact instead of opening the intended action. | Changed the primary CTA to open the verified public Cal.com URL directly. | URL returned HTTP 200; real appointment-screen check pending. |
| The technical walkthrough claimed the booking URL was unknown and SafeBump had no evidence. | Updated the walkthrough to match the current booking link and the intentionally delayed SafeBump case-study publication. | Documentation checked against current source. |

## Automated and Desktop-Width Checks

- Astro production build: passed; Home, Work, About, and Contact generated successfully.
- Live Home, Work, About, and Contact routes: HTTP 200.
- Public Cal.com URL: HTTP 200. This proves network reachability, not that the appointment interface works on the physical phone.
- Responsive source audit: single-column layouts are defined below 620 px; images use `max-width: 100%`; buttons use a 48 px minimum height; primary and supporting text retain at least a 16 px body baseline on mobile.
- Placeholder audit: no generic placeholder text was found. SafeBump remains visibly marked as planned/in development by design and is disclosed in the submission notes.

## Required Physical-Phone Retest

Device and browser: `pending user entry`

| Check | Result | Evidence |
| --- | --- | --- |
| Home has no horizontal scrolling; text is readable without zoom; images stay inside the viewport. | Pending | Home screenshot required. |
| Home → Work navigation works and Work evidence remains crisp without overflow. | Pending | Work screenshot required. |
| Work → About navigation works and all About controls are comfortably tappable. | Pending | About screenshot required. |
| About → Contact navigation works and the booking CTA is visually primary. | Pending | Contact screenshot required. |
| Booking CTA opens the real Cal.com appointment screen and exposes selectable scheduling UI. | Pending | Booking-screen screenshot required; do not complete a booking. |
| Back navigation returns to the portfolio without losing the tested route. | Pending | Record pass or failure. |

## Retest Rule

FL-12 is not complete while any physical-phone row is pending. Record every failure here, fix it, deploy it, and repeat the same check before portal submission.
