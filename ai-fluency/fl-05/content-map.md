# The Through-Line — Map Content & CTAs

**Bilgenur Pala** · Week 3 · AI Fluency
Deliverable for the portal card *"The Through-Line: Map Content & CTAs"*

---

## 1. The one-line claim

> **I build AI agents that run real tools, test their own work, and know when to ask a human.**

**Why this sentence and not another:**

It describes behaviour, not a category. "AI engineer" or "backend developer" tells a reader what box I go in; this tells them what my software does when it runs. The three verbs map to the three things I actually have to prove — tool use, self-verification, and escalation — and each one is demonstrated by a specific artefact in the SafeBump case.

The last clause is deliberate. Most junior portfolios claim more autonomy than they have built. Claiming that the agent knows when to stop is a smaller claim and a harder one, and it is the one my work actually supports.

**Alternatives considered and rejected:**

| Candidate | Why rejected |
|---|---|
| "Backend that lets AI agents act on real systems — and verify their own work" | Accurate but abstract. "Verify their own work" does not create a picture. |
| "Backend behind agents that act, verify, and roll back — not just chat" | Defines itself against something else. Negative framing ages badly and makes the reader think about chatbots instead of about me. |
| "I build production-ready AI agents" | Inflated, and false. Nothing I have built is in production. |

**Supporting line (used directly beneath the claim on Home):**

> Not chat wrappers — agents that open a branch, run the tests, and roll back when they break something.

---

## 2. The one action

**Every CTA on the site ladders to one action: book a conversation.**

There is no newsletter, no download, no "follow me". A second call to action would split the reader's attention and lower the one that matters. Repository and demo links exist throughout, but they are evidence, not calls to action — they support the booking decision rather than competing with it.

---

## 3. Content map

Sitemap: **Home → Work → About → Contact.**
No Skills page and no Blog. Both were removed during the Week 1 pressure test: a skills list is an unverifiable claim, and a blog I will not maintain is a liability that dates the site.

**Case hierarchy:** SafeBump is the unmistakable lead case. Everything else is supporting evidence. This is a featured-case architecture, not a flat gallery — a grid of four equal-weight projects would make the reader rank them, and they would rank them wrong.

---

### Home

The whole page has one job: make the claim believable in under sixty seconds, then ask for the conversation.

| # | Section | Content | Case shown | CTA |
|---|---|---|---|---|
| 1 | Hero | The one-line claim, the supporting line, name and role | — | **Book a conversation** (primary) · *See how the agent decides* (secondary, anchors to §3) |
| 2 | Proof strip | Three short statements of what I can show: an agent that decides and rolls back · an AI service grounded in a real database · a local RAG assistant with a published eval score | — | none — links to §3, §4, §5 |
| 3 | **Featured case: SafeBump** | The strongest section on the site. The problem in two sentences, the decision loop as a small diagram, the rollback moment, the honesty layer, and the demo video embedded | SafeBump | **Book a conversation** · *Read the full case* → Work |
| 4 | Supporting work | Two compact cards, three lines each — no grid of four | PetAdopt · Foundry Local RAG | *See all work* → Work |
| 5 | Who I am | Two sentences from the short bio, photo, link onward | — | *More about how I work* → About |
| 6 | Footer | Booking link, GitHub, LinkedIn, CV, email. FlyRank graduate badge once issued | — | **Book a conversation** |

**Note on §3:** the booking CTA must be reachable from inside the SafeBump case, not only from the footer. That is the point of highest interest on the page — a reader who has just watched an agent roll back a broken upgrade is the reader most likely to book.

---

### Work

Ordered by strength, not by date. The reader should never have to choose between four equal-looking things.

| # | Section | Content | Case shown | CTA |
|---|---|---|---|---|
| 1 | Page intro | One line: what these cases are meant to prove, tied back to the claim | — | none |
| 2 | **SafeBump — full case** | The three beats in full: the problem · what I did and decided (loop, code vs model reasoning, guardrails) · what came of it (eval results, limitations, next step). Demo video, repository link, report screenshot, the honest build story with one real limitation | SafeBump | **Book a conversation** |
| 3 | PetAdopt — full case | Three beats. Emphasis on the grounding decision: the model interprets, the database decides what is real | PetAdopt | **Book a conversation** |
| 4 | Foundry Local RAG — full case | Three beats. Leads with the honest eval number: eight of ten | Foundry Local RAG | **Book a conversation** |
| 5 | Backend Foundations | One combined case covering BE-01…BE-04 as a progression, with the BE-04 unpinned-dependencies debt stated openly | Backend Foundations | *Repositories on GitHub* |
| 6 | Footer | Standard | — | **Book a conversation** |

**Decision recorded:** BE-01…BE-04 appear as **one** case, not four. Four thin entries would outnumber the lead case three to one on the page and flatten the hierarchy the whole site depends on.

---

### About

Trajectory and working philosophy — not a biography, and not a CV in prose.

| # | Section | Content | Case shown | CTA |
|---|---|---|---|---|
| 1 | Intro | The long bio: where I came from (PHP/MySQL → Python/FastAPI), where I am going (agent engineering), and why that order shapes how I build | — | none |
| 2 | How I work | Three short paragraphs: I use AI as a mentor, not as a tool that takes over — decisions, implementation, and verification stay mine, because I have to defend all three. What I do when something breaks. What I write down and why | referenced: SafeBump build log | none |
| 3 | What I am learning now | Current, specific, and dated — not a skills list. What I am working through and what I do not know yet | — | none |
| 4 | Photo + credentials | Real photo. FlyRank internship, links to GitHub, LinkedIn, CV | — | none |
| 5 | Close | "If you are hiring for this kind of work" | — | **Book a conversation** |

**Guard against:** this page defaulting to autobiography. Every paragraph has to answer "why does this make her more credible on the claim", or it comes out.

---

### Contact

One field of focus. Nothing on this page competes with the booking.

| # | Section | Content | Case shown | CTA |
|---|---|---|---|---|
| 1 | Heading | What the conversation is for and what it is not — plain and specific | — | — |
| 2 | Booking | Booking link, prominent. 30 minutes, online or in person | — | **Book a conversation** |
| 3 | Fallback | Email address, plainly written, for people who will not use a booking tool | — | email link |
| 4 | Elsewhere | GitHub, LinkedIn, CV | — | — |

**Later:** if the working contact form built in Week 8 ("Make It Do Something") lands here, it sits **beneath** the booking link, never above it. The form is a fallback, not the goal.

---

## 4. CTA ladder — every call to action, checked

| Page | CTA | Ladders to the one action? |
|---|---|---|
| Home hero | Book a conversation | Yes — direct |
| Home hero secondary | See how the agent decides | Yes — on-page anchor to the strongest evidence, then the CTA |
| Home §3 | Book a conversation | Yes — direct, at peak interest |
| Home §4 | See all work | Yes — routes to more evidence, every branch ends at booking |
| Home §5 | More about how I work | Yes — same |
| Every footer | Book a conversation | Yes — direct |
| Work §2, §3, §4 | Book a conversation | Yes — direct, after each case |
| Work §5 | Repositories on GitHub | Evidence link, not a competing CTA |
| About §5 | Book a conversation | Yes — direct |
| Contact | Book a conversation | Yes — direct |

**No CTA anywhere on the site points at anything other than booking, more evidence, or a credibility link.** Nothing asks the reader to subscribe, download, or follow.

---

## 5. Still need to gather

Honest list. Nothing here is written as if it already exists.

### Blocking — the site cannot go live without these

| Item | For | Status | When |
|---|---|---|---|
| SafeBump — the agent itself | Home §3, Work §2 | Not built | 15–17 Aug |
| SafeBump demo video (3–5 min) | Home §3, Work §2 | Not recorded | 18 Aug |
| SafeBump eval results | Work §2 | Not run | 17 Aug |
| SafeBump report screenshot | Home §3, Work §2 | Does not exist | 17 Aug |
| SafeBump repository (public) | Work §2 | Repo not created | 15 Aug |
| Booking link (live URL) | Every page | **Not set up** | Needed before Week 4 |
| Real photo of me | Home §5, About §4 | Not taken | Before 14 Aug |
| CV (public link) | Footer, About | `[VERIFY: does a current version exist and is it publicly linkable?]` | Before 14 Aug |

### Non-blocking — improves the case but does not stop launch

| Item | For | Status |
|---|---|---|
| PetAdopt screenshots, cropped and legible | Work §3 | Exist in `docs/screenshots/` — need selection and cropping |
| PetAdopt OpenAPI / Swagger capture | Work §3 | Needs a clean capture |
| Foundry Local RAG ten-question eval table | Work §4 | `[VERIFY: committed to the repo, or only in your notes?]` |
| BE-02 `docs/database-view.png` | Work §5 | Exists |
| BE-03 `docs/swagger-ui.png` | Work §5 | Exists |
| SafeBump decision-loop diagram | Home §3 | To be drawn after the build, from the real loop |
| FlyRank graduate badge | Footer | Issued after capstone approval — not available yet |

### Deliberately not gathering

- **Testimonials.** I have none, and a testimonial from a friend is worse than no testimonial.
- **Metrics on PetAdopt match quality.** Never measured. The case says so.
- **User or traffic numbers.** None exist for any project.
- **Client logos.** No clients.

---

## 6. Risks I am carrying

1. **The lead case does not exist yet.** The entire architecture rests on SafeBump, and it is built between 15 and 17 August. If it fails, PetAdopt moves up and the claim narrows to grounding rather than agent decision-making. That fallback is a real cost, and I would rather name it now than discover it on the 18th.
2. **The booking link is not set up and appears on every page.** It is the single highest-frequency element on the site and currently does not exist. It needs doing before the build week, not during it.
3. **The About page will drift toward biography** unless section 2 is written first and section 1 written last.
