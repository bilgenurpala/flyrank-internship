# FL-15: Break Your Own Site

## Scope

The hardening review covers the public Home, Work, About, and Contact routes, every internal and external link, mobile layout, image weight, the Netlify contact form, booking, content completeness, and launch metadata.

## Attack checklist

| Check | Finding | Classification | Resolution or boundary |
|---|---|---|---|
| Empty contact form | Required inputs prevent submission and expose native field errors. | Pass | Keep native validation as the first layer. |
| Invalid email | The browser rejects malformed email input before a request is sent. | Pass | Retest on the deployed form. |
| Short message | Messages shorter than ten characters are rejected. | Pass | Retest on the deployed form. |
| Double submission | The submit button is disabled while the request is pending. | Pass | A second browser tab can still submit the same content; Netlify has no application-level idempotency key. |
| Network or Netlify failure | The form keeps entered values and shows a retry or booking fallback. | Pass | Confirm by blocking the request in browser tools after deployment. |
| Spam input | A hidden `company` honeypot is submitted to Netlify. | Known limitation | Honeypots reduce basic bot spam; they do not replace rate limiting or advanced abuse protection. |
| Booking | Every primary booking CTA uses the same public Cal.com URL. | Pass | Physical-phone evidence already confirms the scheduler opens; no appointment was completed. |
| SafeBump status | The site presents the completed agent, five observed eval outcomes, evidence links, and limitations. | Pass | No “in development” site copy remains. |
| CV consistency | A local resume-generation source still says “SafeBump (in progress).” | Fix now | Regenerate the published CV from the completed-project wording before Checkpoint 2 submission. |
| BE-05 and BE-06 evidence | Both projects were absent from Work. | Fixed | Added separate cases with verified outcomes and honest boundaries. |
| Internal links | Source audit finds valid Home, Work, About, Contact, case anchors, image assets, and CV paths. | Pending deployed retest | Click every route and anchor after production deployment. |
| External links | GitHub, LinkedIn, Cal.com, and repository links are explicitly listed. | Pending deployed retest | Test logged out; remote availability can change independently of the site. |
| Mobile layout | Existing phone QA passed the four-route flow before the two new cases and form were added. | Fix now | Repeat physical-phone QA on the deployed Work and Contact pages. |
| Large images | Loaded portfolio assets are each under 100 KB and use lazy loading outside the hero. An unused 2.7 MB portrait PNG remains in the repository but is not requested by the pages. | Known limitation | Remove the unused source in a later asset-cleanup change after confirming no external dependency. |
| SEO and sharing | Page titles, descriptions, favicons, canonical URLs, Open Graph fields, and X card fields are emitted. | Fixed; deployed preview pending | Verify the public share preview after production deployment. The current portrait is functional but less informative than a dedicated landscape share card. |

## Hard critique before submission

SafeBump is the strongest case because it shows a real decision boundary and failure evidence, but the page still relies heavily on text. The rollback result is described rather than shown visually, so a skeptical reviewer must leave the portfolio to inspect raw evidence. BE-05 and BE-06 are honest but currently read as implementation summaries rather than deep case studies; that is acceptable for supporting work, not for lead evidence. The contact form cannot be called complete until a production submission appears in the Netlify inbox. The published CV and site must also stop disagreeing about whether SafeBump is finished.

## Submission gate

- Production deployment contains SafeBump, BE-05, BE-06, and the contact form.
- A real contact submission appears in Netlify Forms.
- Work and Contact pass a fresh physical-phone check.
- All links are clicked from the deployed site while logged out.
- Booking opens the real scheduler.
- The published CV describes SafeBump as completed.
- Share metadata and a speed report are captured.
- Fix-now findings are resolved; remaining limitations are submitted unchanged.
