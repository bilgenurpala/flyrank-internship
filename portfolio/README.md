# Portfolio Technical Walkthrough

This portfolio is a static Astro site deployed on Netlify. Astro was selected because the site needs reusable page structure and components but does not need a runtime backend. The production build is plain HTML, CSS, JavaScript, and image files.

## Commands

- `npm run dev` starts the local development server.
- `npm run build` generates the production site in `dist/`.
- `npm run preview` serves the generated production build locally.

## Configuration

- `package.json` names the project, locks Astro to version 7.2.1, and defines the three commands above.
- `package-lock.json` records the exact dependency versions so local and Netlify builds install the same packages.
- `astro.config.mjs` sets `output: "static"`, which means every route is generated at build time and no server is required after deployment.
- `netlify.toml` tells Netlify to run the build command, publish the generated `dist/` directory, and use Node.js 22.

## Shared Structure

- `src/layouts/BaseLayout.astro` owns the common document structure, metadata, fonts, header, footer, and the small reveal-on-scroll script used across every page.
- `src/components/Header.astro` defines the Home, Work, About, and Contact navigation and marks the current page for screen readers and visual styling.
- `src/components/Footer.astro` keeps the positioning statement and verified external links consistent across the site.
- `src/components/AnimatedPortrait.astro` combines the real portrait with lightweight CSS-driven motion. It has no canvas, animation library, or generated video.
- `src/components/SystemFlow.astro` visualizes the design principle used in the portfolio: request, context, tool call, verification, and a human gate.
- `src/components/ProjectCard.astro` is the reusable summary card that links Home-page project summaries to full Work-page cases.

## Pages

- `src/pages/index.astro` is the Home route. It states the positioning claim, shows selected evidence, presents SafeBump as the completed lead case, and links to every full case.
- `src/pages/work.astro` is the Work route. It contains the full SafeBump, PetAdopt, Local RAG, and backend-foundations cases with evidence, repository links, and known limits.
- `src/pages/about.astro` is the About route. It explains the engineering progression, working method, current focus, portrait, and profile links.
- `src/pages/contact.astro` is the Contact route. Its primary action opens the verified public Cal.com booking page; GitHub, LinkedIn, and CV remain supporting links.

## Styling and Assets

- `src/styles/global.css` contains the identity-kit colors, typography, layout, responsive breakpoints, focus states, evidence galleries, and animations. Its reduced-motion rule disables animation when the visitor requests less motion.
- `public/assets/logo.svg` and the favicon files carry the identity mark into the browser tab, header, and saved mobile shortcut.
- `public/assets/bilgenur-pala-portrait.webp` is the real portrait used on Home and About, resized and encoded for web delivery.
- `public/cv/bilgenur-pala-ai-engineer-resume.pdf` is the verified one-page AI Engineer CV linked from About, Contact, and the footer.
- `public/assets/projects/petadopt-*` came from the PetAdopt repository's recorded application, AI assistant, OpenAPI, and Newman evidence.
- `public/assets/projects/foundry-local-rag-interface.png` is a capture of the real local RAG web interface running at `127.0.0.1:8000`.
- `public/assets/projects/backend-*` came from the BE-02 SQLite and BE-03 authenticated Swagger evidence already stored in this repository.

## Ownership Boundaries

The site has no database, authentication, form handler, analytics, or application backend. External profile, repository, and booking links leave the site. SafeBump's reported results are bounded to its committed Ubuntu 26.04/Python 3.14 evaluation evidence.
