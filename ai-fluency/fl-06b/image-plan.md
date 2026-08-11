# Kill Your Darlings — Curate Your Images

**Bilgenur Pala** · Week 3 · AI Fluency
Deliverable for the portal card *"Kill Your Darlings: Curate Your Images"*

---

## 1. The rule I curated against

**Real work is shown with real captures. Generated imagery is not used to represent anything I built.**

A generated illustration of "an AI agent" tells a technical reader nothing except that I had nothing real to show. Every image below is either a capture of something that actually ran, a photograph of me, or a diagram I drew from the real system. There is no decorative imagery on this site.

The list is derived from the content map — each image exists because a specific section needs it, not because the page looked empty.

---

## 2. The image set

Status key: **Have** = exists · **Crop** = exists, needs cleaning · **Capture** = must be taken · **Blocked** = the thing itself does not exist yet

### Home

| # | Image | Content need (content map §) | Type | Status |
|---|---|---|---|---|
| 1 | SafeBump decision-loop diagram | Home §3 — makes the loop legible in five seconds | Diagram, drawn by me | **Blocked** — drawn from the real loop after 17 Aug |
| 2 | SafeBump report — rollback decision visible | Home §3 — the single strongest piece of evidence on the site | Terminal / Markdown capture | **Blocked** — 17 Aug |
| 3 | Demo video poster frame | Home §3 — thumbnail before play | Frame from the real recording | **Blocked** — 18 Aug |
| 4 | Portrait of me | Home §5 | Real photograph | **Capture** — before 14 Aug |
| 5 | PetAdopt card thumbnail | Home §4 | Crop of image 8 | **Crop** |
| 6 | Foundry Local RAG card thumbnail | Home §4 | Crop of image 11 | **Crop** |

### Work

| # | Image | Content need | Type | Status |
|---|---|---|---|---|
| 7 | SafeBump full run — one complete loop | Work §2 — proves the agent runs end to end | Terminal capture | **Blocked** — 17 Aug |
| 8 | PetAdopt — assistant conversation with the matched record | Work §3 — shows the grounding: request in, real row out | App capture from `docs/screenshots/` | **Crop** |
| 9 | PetAdopt — OpenAPI / Swagger view | Work §3 — the contract, RFC 7807 error shapes visible | Browser capture | **Capture** — needs a clean, cropped shot |
| 10 | PetAdopt — architecture sketch (API ↔ separate AI service ↔ PostgreSQL) | Work §3 — carries the decision the case rests on | Diagram, drawn by me | **Capture** |
| 11 | Foundry Local RAG — ten-question evaluation table | Work §4 — the honest 8/10, shown not asserted | Table capture or rendered Markdown | **Capture** — `[VERIFY: is this committed to the repo, or only in your notes?]` |
| 12 | Foundry Local RAG — running with no network | Work §4 — proves "fully local" instead of claiming it | Terminal capture | **Capture** |
| 13 | BE-02 `docs/database-view.png` | Work §5 — persistence, and the SafeBump target project | Existing capture | **Have** |
| 14 | BE-03 `docs/swagger-ui.png` (lock icons on protected routes) | Work §5 — auth is visible at a glance | Existing capture | **Have** |
| 15 | BE-02 test run — six tests passing | Work §5 — the deterministic suite SafeBump depends on | Terminal capture | **Capture** |

### About

| # | Image | Content need | Type | Status |
|---|---|---|---|---|
| 16 | Portrait — wider crop | About §4 | Same shoot as image 4 | **Capture** |
| 17 | `build-log.md` excerpt showing a real failure | About §2 — evidence for "I write down what breaks" | Capture of the real file | **Blocked** — 15 Aug onward |

### Site-wide

| # | Image | Content need | Type | Status |
|---|---|---|---|---|
| 18 | Favicon (16/32/180 px) | Browser tab | Identity kit asset | **Have** |
| 19 | Social share preview (1200 × 630) | Link previews | Logo + claim, identity kit colours | **Capture** |
| 20 | FlyRank graduate badge | Footer | Issued by FlyRank | **Blocked** — after capstone approval |

**Totals:** 20 images. 3 have · 3 need cropping · 8 need capturing · 6 blocked on work that does not exist yet.

---

## 3. Capture standard

Applied to every screenshot before it goes on the site.

- **Crop to the evidence.** No browser chrome, no desktop, no editor sidebar unless the sidebar *is* the point.
- **Legible at the size it will be displayed**, not at full size. If the text is unreadable in the layout, the crop is wrong — enlarging the image is not the fix.
- **Terminal captures:** light background, increased font size, only the relevant lines. A dark terminal on a near-white page pulls the eye away from the text around it.
- **Nothing sensitive.** No tokens, keys, `.env` contents, real email addresses, or absolute paths containing my machine's user directory.
- **Real output only.** No editing a terminal capture to make results look tidier. If a run was messy, the messy run is the honest capture.
- **Compressed** before upload; PNG for UI and terminal captures, JPEG for photographs.
- **Alt text** written for every image, describing what it shows rather than repeating the caption.

---

## 4. Generated imagery

**None is used.** There is no consistent generated style to define, because no generated image survived the cut.

The two diagrams (images 1 and 10) are drawn by me from the real systems, in the identity kit colours: deep teal on paper, ink labels, Inter at 15 px, one stroke weight, no shadows or gradients. They are documentation, not illustration — and because there are only two, they form a set rather than a pile.

---

## 5. The real photograph

**Image 4 / 16 — portrait of me.** A real photograph, not an avatar, not a generated headshot, not a placeholder silhouette.

Requirements: natural light, plain uncluttered background, shoulders-up, looking at the camera, neutral clothing that does not fight the palette. One tight crop for Home §5, one wider crop for About §4. Taken on a phone is fine; the point is that it is me.

**Why this is not optional:** the entire site asks a stranger to book a conversation with a person. A generated or missing face undermines the one action on every page.

---

## 6. Rejected images

### Rejected — AI-generated hero illustration for the SafeBump section

**What it was:** a generated conceptual image of a robotic arm inspecting stacked blocks, in a flat teal-and-rust technical style matching the palette — intended for Home §3 while the real agent captures do not yet exist.

**Why it was rejected:**

It illustrated the *idea* of an agent checking something, which a technical reader already understands and does not need drawn for them. Worse, it would sit in the most important position on the site — the slot reserved for the one piece of evidence that carries my whole claim — and quietly signal that I had nothing real to put there. A metaphor in the place where proof belongs is weaker than an empty space, because the empty space is at least honest about the gap.

**What I am doing instead:** Home §3 stays without a hero image until 17 August, then takes the real report capture showing an actual rollback decision.

### Also rejected

| Image | Why |
|---|---|
| Stock photo of a laptop with code on the screen | Someone else's code. Says nothing about me and appears on ten thousand other portfolios. |
| Generated abstract "neural network" background for the hero | Decoration competing with the claim. Breaks the identity kit rule that the design must not outshine the evidence. |
| Photographs of pets for the PetAdopt case | Charming and misleading. PetAdopt is a backend and a grounding decision; a photograph of a dog makes it look like a pet-photo gallery and hides the actual work. |
| A full-desktop screenshot of the PetAdopt app | Too much at once. Cropping to the conversation and the matched record (image 8) shows the one thing that matters. |
| A logo wall of technologies used (FastAPI, Docker, PostgreSQL…) | An unverifiable claim dressed as evidence. The screenshots already prove which technologies are in play, and the sitemap deliberately has no Skills page for the same reason. |

---

## 7. Open items

- [ ] Take the portrait (images 4, 16) — before 14 Aug
- [ ] Crop the PetAdopt captures from `docs/screenshots/` (image 8)
- [ ] Clean captures: Swagger view (9), BE-02 test run (15), RAG offline run (12)
- [ ] `[VERIFY: commit the ten-question RAG evaluation to the repo if it is not already there]` (image 11)
- [ ] Draw the PetAdopt architecture sketch (image 10)
- [ ] Build the social share preview (image 19)
- [ ] After 17–18 Aug: SafeBump diagram, report capture, full run capture, video poster frame (1, 2, 3, 7)
- [ ] After 15 Aug: build-log excerpt (17)
