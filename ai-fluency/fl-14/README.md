# FL-14: Make It Do Something

## The one feature

The portfolio adds exactly one dynamic feature: a contact form handled by Netlify Forms on the existing free deployment. Booking remains the primary action. The form is a secondary route for visitors who need to send context before scheduling.

## Backend, feature, and data flow

A backend is the part of a system that receives requests, applies server-side behavior, and stores or forwards data outside the visitor's browser. Here, Netlify provides the managed backend. The visitor completes the form, the browser validates required fields and email format, JavaScript sends URL-encoded form data to Netlify, its honeypot filters basic bot submissions, and the submission appears in the site owner's Netlify Forms inbox. The page shows success only after Netlify returns a successful response.

Empty, malformed, and too-short input is blocked with native browser validation and a visible guidance message. During submission, the button is disabled and reports progress. A successful response clears the form and shows confirmation. A network or Netlify failure keeps the form values available and shows a retry or booking fallback without displaying false success.

## Production verification

- The committed form markup and static Netlify form blueprint are deployed.
- Netlify detects the `contact` form and reports the honeypot as active.
- A real message submitted from the public URL returned the inline success state.
- The same message appeared in the Netlify Forms verified-submissions inbox.
- `contact-form-success.png` and `netlify-verified-submission.png` preserve the two sides of the end-to-end check.
