# Decide Once — Identity Kit

**Bilgenur Pala** · Week 3 · AI Fluency
Deliverable for the portal card *"Decide Once: Build Your Identity Kit"*

> **The rule this kit exists to enforce:** the design frames the work; it must never be more
> memorable than the evidence. Every decision below is made once, written down, and not revisited
> during the build week.

---

## 1. Style note (two lines)

> Space Grotesk headings on Inter body text, set on near-white with a single deep teal doing the structural work. One rust accent, reserved exclusively for the booking action.
>
> The mood is a clean technical document, not a marketing page: quiet, legible, and confident enough not to decorate itself.

*Added to the AI workspace as a standing instruction alongside the voice card.*

---

## 2. Typography

Two fonts. Both free, both under the SIL Open Font License, both available on Google Fonts and self-hostable.

| Role | Font | Weights used | Why |
|---|---|---|---|
| **Headings** | **Space Grotesk** | 500, 700 | A grotesque with slightly mechanical letterforms — technical character without novelty. Distinctive enough that headings do work; restrained enough that they do not shout. |
| **Body** | **Inter** | 400, 500, 600 | Designed specifically for screen UI. Tall x-height and open apertures make it hold up at small sizes on a phone, which is where most of the site will actually be read. |
| **Code** | *system monospace stack* | 400 | For `pip check`, file names, and command output. No third font is loaded — the OS stack is free and already present. |

**Why two and not one:** Space Grotesk is excellent for headings and tiring in long paragraphs; Inter is excellent for paragraphs and slightly anonymous as a heading. Each covers the other's weakness. A third font would be decoration.

**Type scale** (1.25 ratio, base 17px):

| Use | Size | Font | Weight |
|---|---|---|---|
| Hero claim | 44 / 34 px mobile | Space Grotesk | 700 |
| Page heading (h1) | 34 px | Space Grotesk | 700 |
| Section heading (h2) | 26 px | Space Grotesk | 500 |
| Sub-heading (h3) | 21 px | Space Grotesk | 500 |
| Body | 17 px | Inter | 400 |
| Small / caption | 15 px | Inter | 400 |

Body line height 1.6. Measure capped at roughly 68 characters.

**Loading:**

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

Only the six weights listed are loaded. `display=swap` so text is readable before the fonts arrive.

---

## 3. Palette

Four controlled colours plus one support grey. Every combination below was checked programmatically against the WCAG 2.1 relative-luminance formula — the ratios are computed, not estimated.

| Name | Hex | Role |
|---|---|---|
| **Deep Teal** | `#14524A` | Main colour. Headings, logo, links, section rules, primary button fill. |
| **Ink** | `#14161A` | Body text. Near-black, not pure black — pure black on a bright background is harsh. |
| **Paper** | `#FAFAF8` | Page background. Near-white with a trace of warmth, not pure white. |
| **Rust** | `#B4462C` | The single accent. |
| **Muted Ink** | `#5A6068` | Support grey. Captions, metadata, table labels. Never body text. |

### Verified contrast ratios

| Combination | Ratio | WCAG (normal text) |
|---|---|---|
| Ink on Paper | **17.33 : 1** | AAA |
| Deep Teal on Paper | **8.60 : 1** | AAA |
| Paper on Deep Teal | **8.60 : 1** | AAA |
| Rust on Paper | **5.22 : 1** | AA |
| Paper on Rust | **5.22 : 1** | AA |
| Muted Ink on Paper | **6.07 : 1** | AA |

**Known limitation, recorded honestly:** Deep Teal on Ink is **2.01 : 1** and fails. Teal is a light-background colour only. If a dark section is ever introduced, it needs a separate lighter tint — which would mean adding a colour, so the simpler answer is not to build a dark section.

### Accent rule

**Rust appears in exactly one place: the booking call to action.** Not on headings, not on links, not on hover states, not on decorative rules. The moment it appears twice it stops meaning "this is the thing to click".

This is the rule most likely to erode during the build week. It is written here so that breaking it is a visible decision rather than a drift.

### CSS variables

```css
:root {
  --teal:  #14524A;
  --ink:   #14161A;
  --paper: #FAFAF8;
  --rust:  #B4462C;
  --muted: #5A6068;
  --rule:  #E2E2DE;

  --font-head: "Space Grotesk", system-ui, sans-serif;
  --font-body: "Inter", system-ui, -apple-system, sans-serif;
}
```

`--rule` (`#E2E2DE`) is a hairline border tint for table and card edges, not a sixth palette colour — it is never used for text.

---

## 4. Logo and favicon

A **BP monogram**: geometric letterforms built from a single stroke weight, set in a rounded square tile.

**Why a monogram and not a wordmark or a symbol:** a symbol would need explaining, and an abstract mark from a junior portfolio reads as decoration. Initials are honest and legible at 16 pixels, which is the size that actually matters — the browser tab.

**Design decisions:**

- One consistent stroke weight throughout, matching the mechanical feel of Space Grotesk without imitating it.
- No custom font dependency — the letterforms are vector paths, so the mark renders identically everywhere and never waits on a webfont.
- Tile radius is 22% of the width, matching the site's card corners.
- Tested down to 16 px: both letters remain distinguishable.

**Files:**

| File | Use |
|---|---|
| `assets/logo.svg` | Primary — teal tile, paper letterforms. Header, social preview. |
| `assets/logo-mark.svg` | Teal letterforms, no tile. For use on the paper background. |
| `assets/favicon-32.png`, `favicon-16.png` | Browser tab |
| `assets/favicon-180.png` | Apple touch icon |
| `assets/logo-tile-512.png`, `logo-mark-teal-512.png` | Raster fallbacks |
| `assets/logo-preview.png` | Size test: 200 px down to 16 px |
| `assets/palette.png` | Palette sheet with the computed contrast ratios |

```html
<link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/favicon-180.png">
```

---

## 5. Layout and spacing

Not required by the card, but recorded here so it is also decided once.

- **Spacing scale:** 4 / 8 / 16 / 24 / 40 / 64 / 96 px. Nothing off-scale.
- **Content width:** 720 px maximum for text; 1040 px for full-width sections.
- **Corner radius:** 10 px on cards and buttons; 22% on the logo tile.
- **Borders:** 1 px `--rule`. No drop shadows anywhere — shadows are the fastest way to make a restrained page look like a template.
- **Images:** 10 px radius, 1 px `--rule` border, so a light screenshot does not bleed into the paper background.

---

## 6. Phone readability check

| Check | Result |
|---|---|
| Body text at 17 px on a phone | To be verified on a real device |
| Ink on Paper contrast | 17.33 : 1 — passes with a wide margin |
| Rust CTA on Paper | 5.22 : 1 — passes AA at 17 px |
| Favicon legibility at 16 px | Verified in `logo-preview.png` |
| Hero claim reflow at 34 px mobile | To be verified once the page exists |

**Honest status:** contrast is verified by computation; **on-device readability is not yet verified**, because there is no page to open. That check belongs to *Open It on Your Phone* in Week 7 and is not claimed here.

---

## 7. What this kit deliberately does not include

- **No dark mode.** Two themes means every contrast decision made twice, for a site a reader will visit once.
- **No third font, no icon set, no illustration style.** Nothing that competes with the screenshots.
- **No gradients, shadows, or animation.** The work is the interesting part.
- **No second accent colour.** One accent with one job is what makes the CTA visible at all.
