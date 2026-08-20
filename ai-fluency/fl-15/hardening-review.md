# FL-15: Break Your Own Site

## Scope

The hardening review covers the public Home, Work, About, and Contact routes, every internal and external link, mobile layout, image weight, the Netlify contact form, booking, content completeness, and launch metadata.

## Attack checklist

| Check | Finding | Classification | Resolution or boundary |
|---|---|---|---|
| Empty contact form | The production form blocks submission, focuses the first missing input, and shows a clear status message. | Pass | Verified on the deployed site. |
| Invalid email | The production form rejects a malformed address before sending a request. | Pass | Verified with `abc`. |
| Short message | The production form reports the ten-character minimum and current character count. | Pass | Verified with a two-character message. |
| Double submission | The button disables synchronously while the request is pending; a rapid double click produced one verified Netlify record. | Pass | A second browser tab can still submit the same content; Netlify has no application-level idempotency key. |
| Network or Netlify failure | Before form detection was enabled, the real production POST returned 404 while the UI retained the entered values and displayed the retry or booking fallback. | Pass after fix | Form detection was enabled, a static form blueprint was added, and the next real submission succeeded. |
| Spam input | Netlify reports extra spam prevention through the `company` honeypot field. | Known limitation | Honeypots reduce basic bot spam; they do not replace rate limiting or advanced abuse protection. |
| Booking | The public Cal.com page loaded available dates, times, and the confirmation form in a logged-out session. | Pass | No appointment was completed. |
| SafeBump status | The site presents the completed agent, five observed eval outcomes, evidence links, and limitations. | Pass | No “in development” site copy remains. |
| CV consistency | The production CV now describes SafeBump as completed, reports the observed 5/5 outcomes, and keeps the approval and no-auto-merge limits. | Fixed and deployed | Extracted production PDF text contains no “in progress” claim. |
| BE-05 and BE-06 evidence | Both projects were absent from Work. | Fixed | Added separate cases with verified outcomes and honest boundaries. |
| Internal links | Home, About, Work, Contact, and the published CV returned HTTP 200 after deployment. | Pass | Case anchors remain ordinary in-page targets and were included in the source audit. |
| External links | Cal.com, GitHub profile, SafeBump, and internship repositories returned HTTP 200. LinkedIn rejects automated HEAD requests but remained visible in Google and opened in browser testing. | Pass with external boundary | Remote availability can change independently of the site. |
| Mobile layout | Physical-phone checks covered the deployed SafeBump lead case and the complete Contact form, submit button, footer, and booking CTA without horizontal overflow or overlap. | Pass | Evidence was captured on a real phone. |
| Large images | Loaded portfolio assets are each under 100 KB and use lazy loading outside the hero. An unused 2.7 MB portrait PNG remains in the repository but is not requested by the pages. | Known limitation | Remove the unused source in a later asset-cleanup change after confirming no external dependency. |
| SEO, speed, and discovery | Page titles, descriptions, canonicals, Open Graph and X fields are deployed. Mobile PageSpeed scored 93 performance and 100 for accessibility, best practices, and SEO. Search Console ownership is verified and the sitemap was accepted. | Pass with known limitation | Google found the live URL indexable, but the portfolio was not yet present in name-search results and the account's manual indexing quota was exhausted. Indexing timing remains controlled by Google. |

## Hard critique before submission

SafeBump is the strongest case because it shows a real decision boundary and failure evidence, but the page still relies heavily on text. The rollback result is described rather than shown visually, so a skeptical reviewer must leave the portfolio to inspect raw evidence. BE-05, BE-06, and BE-08 remain concise implementation summaries rather than deep case studies; that is acceptable for supporting work, not for lead evidence. The contact form is now operational and verified in the Netlify inbox, and the CV agrees that SafeBump is complete. The remaining launch weakness is discovery latency: Google can crawl the site and has accepted its sitemap, but the portfolio is not yet visible in the tested name search.

## Submission gate

- [x] Production deployment contains SafeBump, BE-05, BE-06, BE-08, and the contact form.
- [x] A real contact submission appears in Netlify Forms.
- [x] Work and Contact pass a fresh physical-phone check.
- [x] Internal routes, CV, booking, and repository links pass deployed checks.
- [x] Booking opens the real scheduler in a logged-out session.
- [x] The published CV describes SafeBump as completed.
- [x] Search metadata and a mobile PageSpeed report are captured.
- [x] Fix-now findings are resolved; remaining limitations are named rather than hidden.

## Private portal evidence

The following screenshots are retained locally for the assignment's Files field and are not committed because they contain account or submission context.

- `empty-form-validation.png`
- `invalid-email-validation.png`
- `short-message-validation.png`
- `double-submit-single-record.png`
- `booking-incognito-availability.png`
- `mobile-work-safebump.jpg`
- `mobile-contact-layout.jpg`
- `mobile-contact-submit-and-footer.jpg`
- `pagespeed-mobile-results.png`
- `google-findability-check.png`
- `search-console-ownership-verified.png`
- `sitemap-submitted.png`
- `google-live-url-indexable.png`
- `search-console-indexing-quota.png`
