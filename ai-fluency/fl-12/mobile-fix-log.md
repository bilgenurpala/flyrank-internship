# Open It on Your Phone — Fix Log

Date: 19 August 2026
Live site: <https://bilgenurpala.netlify.app/>

## Scope

The required route is Home → Work → About → Contact. The portfolio has one primary conversion action: opening the public 30-minute Cal.com booking page.

## Pre-device Audit and Fixes

| Finding | Change | Verification status |
| --- | --- | --- |
| Mobile navigation links used padding that produced targets smaller than the recommended 44 px minimum. | Set every primary-navigation link to a minimum height of 44 px and retained a readable 14 px mobile label size. | Passed on the physical phone across all four routes. |
| Inline case links, repository links, and footer links did not guarantee a 44 px touch target. | Converted them to aligned inline-flex targets with a 44 px minimum height. | Passed on the physical phone; Work, About, Contact, CV, and booking links opened. |
| The Contact page visually presented GitHub as the primary action. | Made `Book a conversation` the first and only primary button; kept GitHub, LinkedIn, and CV as secondary evidence links. | Passed; the booking action was visually primary and opened the real scheduler. |
| The About closing CTA routed through Contact instead of opening the intended action. | Changed the primary CTA to open the verified public Cal.com URL directly. | Passed through the physical-phone booking flow. |
| The technical walkthrough claimed the booking URL was unknown and SafeBump had no evidence. | Updated the walkthrough and published the completed SafeBump case with its 5/5 evaluation record and evidence boundaries. | Passed source, build, live HTTP, and physical-phone checks. |
| The 1254 × 1254 portrait PNG was 2.7 MB, dominating the page's image transfer. | Re-encoded a proportionally resized 900 × 900 WebP at 49 KB and updated both portrait consumers. The original remains in the repository as the source asset. | Passed; the portrait remained sharp on the physical phone. |
| The PetAdopt portrait cover first became too narrow, then clipped its left-side title when expanded to the mobile card width. It also foregrounded a decorative cover over real evidence. | Replaced the lead cover with the working landscape application capture, removed its duplicate from the gallery, and kept full-size tap access. | Passed after the second physical-phone correction. |
| iPhone Safari reserved an excessively tall box for the Foundry Local RAG capture and pushed the actual screenshot to the bottom. | Set the image's explicit source ratio and automatic height, expanded it to the card width on mobile, and added a full-size evidence link. | Passed after physical-phone retest. |

## Automated and Desktop-Width Checks

- Astro production build: passed; Home, Work, About, and Contact generated successfully.
- Live Home, Work, About, and Contact routes: HTTP 200.
- Public Cal.com URL: HTTP 200. This proves network reachability, not that the appointment interface works on the physical phone.
- Responsive source audit: single-column layouts are defined below 620 px; images use `max-width: 100%`; buttons use a 48 px minimum height; primary and supporting text retain at least a 16 px body baseline on mobile.
- Placeholder audit: no generic placeholder text remains. SafeBump now presents its completed 5/5 evaluation record, repository evidence, guardrails, and explicit verification limits.

## Required Physical-Phone Retest

Device and browser: physical iPhone, Chrome on iOS

| Check | Result | Evidence |
| --- | --- | --- |
| Home has no horizontal scrolling; text is readable without zoom; images stay inside the viewport. | Pass | [`01-home.jpg`](evidence/01-home.jpg) |
| Home → Work navigation works and Work evidence remains crisp without overflow. | Pass | [`02-work-safebump.jpg`](evidence/02-work-safebump.jpg), [`03-work-footer.jpg`](evidence/03-work-footer.jpg) |
| Work → About navigation works and all About controls are comfortably tappable. | Pass | [`04-about.jpg`](evidence/04-about.jpg), [`05-cv.jpg`](evidence/05-cv.jpg) |
| About → Contact navigation works and the booking CTA is visually primary. | Pass | [`06-contact.jpg`](evidence/06-contact.jpg) |
| Booking CTA opens the real Cal.com appointment screen and exposes selectable scheduling UI. | Pass | [`07-booking.jpg`](evidence/07-booking.jpg); no appointment was completed. |
| Back navigation returns to the portfolio without losing the tested route. | Pass | Confirmed immediately after the booking-screen check. |

## Retest Rule

Every physical-phone row passed after the recorded fixes and redeployments. The screenshots show the actual device and browser state; automated HTTP checks are retained as separate supporting evidence rather than a substitute for the phone test.
