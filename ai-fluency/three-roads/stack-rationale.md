# Portfolio Stack Decision

## Constraints

- Cost: free only
- Current skill profile: stronger in Python and backend engineering; weaker in frontend development
- Required sitemap: Home → Work → About → Contact
- Required evidence: screenshots, repository links, demo video, and a future live SafeBump demonstration
- Delivery window: a continuing portfolio that must be completed by 2026-08-22
- Ownership requirement: every deployed file must be understandable and explainable

## Does Launch Need a Dynamic Feature?

No. The launch scope is static content, images, navigation, and external links. The program schedules one real dynamic feature for Week 8, so adding a backend at launch would introduce complexity before a demonstrated requirement exists.

## Three Options

| Option | Build approach | Free host | Backend now? | Fit for the work | Maintenance burden | Main trade-off |
|---|---|---|---|---|---|---|
| Vanilla HTML/CSS/JS | Hand-written pages and shared CSS; JavaScript only where interaction requires it | Netlify Free | No | Fully supports screenshots, repository links, video, case pages, and a later SafeBump link or embed | Low technical overhead, but repeated page structure must be maintained manually | Maximum transparency and minimum tooling in exchange for duplication as the site grows |
| Astro | Static-first pages and reusable `.astro` components with a Node build step | Netlify Free | No for the current scope | Strong fit for repeated case-study layouts and content-heavy pages | Dependencies, framework concepts, and build configuration must be maintained | Better reuse and content structure in exchange for learning and build overhead |
| Next.js | React components, file-based routing, and optional server rendering or functions | Vercel Hobby | No for the current scope | Can support every current and future feature | Largest concept and dependency surface; React, Next.js, rendering modes, and deployment behavior all require ownership | Most capability, but most of it is not required for a static four-page launch |

Netlify's current Free plan is $0 and includes framework or static deployment, a global CDN, custom domains, and SSL within a monthly credit limit. Vercel's Hobby plan is free for personal, non-commercial projects and includes Git deployment and automatic HTTPS within its usage limits.

## Front-Runner Pressure Test

### What breaks if I choose the simplest option?

Nothing required for the first launch breaks with vanilla HTML/CSS/JS. The weakness appears as the portfolio grows: shared navigation, footer markup, project cards, and case-study structure must either be copied across pages or recreated with custom JavaScript. One structural change can require several edits and allow pages to drift apart.

### What must I maintain if I choose the most powerful option?

Next.js adds React's component model, framework routing and rendering behavior, npm dependencies, build output, and platform-specific deployment concepts. That maintenance would exist even while the site only serves text, images, and links.

### Can I finish and understand it within the available window?

Yes. Astro adds a build step and component syntax, but the surface is still small enough to explain: layouts define shared page structure, components hold repeated interface patterns, pages define routes, and Astro produces static HTML for Netlify. This is no longer only an estimate: the four-page site has been built successfully and deployed within the available window. Next.js could also be deployed quickly, but deployment speed is not the same as understanding and maintaining its larger runtime and rendering model.

### Does it present the work correctly?

Yes. The portfolio's proof comes from the quality of its cases, screenshots, repositories, demos, and explanations. A frontend framework does not make backend or agent work more credible. The chosen stack must keep that evidence clear and reachable.

## Final Decision

I am going with Astro on Netlify.

The site still has nothing to compute at launch. It serves content, images, repository and demo links, and four pages of navigation, so it remains a static site with no backend. Astro fits that constraint: it gives me reusable components during development and produces static pages for deployment.

I can maintain this. The extra responsibility is real: I need to understand the npm dependency, Astro's file-based routing, component props, and the build command. In return, the header, footer, project cards, animated portrait, and future case-study structure have one source of truth instead of being copied across pages. That trade is worthwhile because this is a portfolio I intend to keep extending, not a disposable landing page.

I did not choose Astro because a framework automatically makes a site professional. The content, evidence, accessibility, and visual decisions still do that work. I chose it because the site moved beyond a near-blank page into a reusable multi-page structure, and Astro solves that specific maintenance problem without introducing a backend.

I rejected vanilla HTML/CSS/JS as the final stack because its simplicity would be paid back as duplication once case studies grow. I rejected Next.js because React, multiple rendering modes, and platform-specific server features create a larger surface than this static portfolio needs. The Astro site is already live on Netlify, which proves that it fits both the ten-day constraint and the requirement to present my work accurately.

## What Changed From the Initial Front-Runner

Vanilla HTML/CSS/JS was my initial front-runner because it was the lowest-risk way to publish an almost empty site. I changed the decision when the implementation scope became a professional four-page portfolio with reusable project cards, shared navigation, animation, and future case-study growth. The requirement did not force this change; the maintenance trade-off did. I kept Netlify and the static architecture, but adopted Astro for structure and reuse.

## Current Hosting References

- [Netlify pricing](https://www.netlify.com/pricing/)
- [Astro deployment guide](https://docs.astro.build/en/guides/deploy/)
- [Astro on Netlify](https://v5.docs.astro.build/en/guides/deploy/netlify/)
- [Vercel plans](https://vercel.com/docs/plans)
- [Next.js on Vercel](https://vercel.com/docs/frameworks/full-stack/nextjs)
