# Design — „Trasa“

## Concept

24. oktobar works underground: it digs trenches, lays pipes and cables, compacts the backfill and puts the ground back the way it was. The company has no photo archive, but it does have a 20-year record of specific works with places and lengths. The design uses that record.

The visual language is borrowed from **survey and route drawings**: thin rules, a red line that marks the route, small monospaced annotations for years and metres, and one technical illustration (a trench cross-section) that explains the work sequence in the company's own words. Projects are presented as a **ledger**, not as cards. Large condensed headings give the confident, industrial voice the references share, without imitating their photo-led layouts.

## Colour

| Token | Hex | Use |
|---|---|---|
| `--t-red` | `#D34053` | Logo red (sampled from `head.gif`). Large fills, rules, route line, chart bars. |
| `--t-red-ink` | `#A92D3D` | Red for text, links, buttons and the contact band. White on it is 6.7:1. |
| `--t-ink` | `#1C1D1B` | Headings, body text, dark bands |
| `--t-ink-2` | `#4A4741` | Secondary text (7.9:1 on sand) |
| `--t-sand` | `#F2EEE6` | Default page background (soil and paper, not tech white) |
| `--t-paper` | `#FAF8F4` | Alternate section background |
| `--t-line` | `#D8D0C2` | Hairlines and table rules |
| `--t-muted-dark` | `#B5AEA2` | Secondary text on ink |
| `--t-pipe` | `#E5B323` | Gas-pipe yellow, used **only** inside the trench diagram |

There's no blue anywhere. Red is a signal colour and never covers more than one band per page.

## Typography (Google Fonts, Latin Extended for č ć đ š ž, loaded locally by Elementor)

| Role | Face | Desktop / mobile |
|---|---|---|
| H1 | Archivo Narrow 700 | 64 / 40 px, line-height 1.02 |
| H2 | Archivo Narrow 700 | 44 / 32 px, 1.08 |
| H3 | Archivo Narrow 600 | 26 / 22 px, 1.2 |
| Lead | Archivo 400 | 21 / 18 px, 1.5 |
| Body | Archivo 400 | 17 / 16 px, 1.6 |
| Label / data | IBM Plex Mono 500 | 13 px, uppercase, +0.08em tracking (years, metres, eyebrows) |

The page uses one superfamily (Archivo and Archivo Narrow) plus one mono face, at five weights in total.

## Layout and spacing

- Content width 1240 px with 24 px side gutters (20 px on mobile). Running text is capped at about 680 px.
- 8 px base unit. Section padding is 112 px on desktop, 80 on tablet and 56 on mobile.
- Asymmetric splits (5/7, 4/8, 3/9) instead of equal columns. Rows are separated by 1 px rules, not boxes.
- No rounded corners, shadows, gradients or entrance animations.

## Components

- **Eyebrow:** a short red bar followed by an uppercase mono label (`.t-eyebrow`).
- **Buttons:** rectangular, 2 px border, Archivo Narrow 600, with an arrow. Primary is red-ink fill and white text. Secondary is an ink outline. On hover the fill inverts. Every button has a visible focus ring.
- **Ledger rows** (`.t-ledger`): period · title · place · scope on a 12-column grid with a rule between rows. On mobile they stack, period first.
- **Reference lists** (`.t-reflist`): one item per line. Text set in *italics* in the editor (the „I“ button) is rendered as a right-aligned mono figure. This is how lengths like *19.150 m* are entered.
- **Trench diagram:** inline SVG in an HTML widget, numbered 1–6, with an HTML legend underneath so the text stays readable and translatable.
- **Length chart:** CSS bars of kilometres per period, 1998–2012. All values come from `docs/data/references.json`.

## Photography rules (for when the company supplies its own photos)

- Use only genuine site photographs from 24. oktobar. Never use stock or manufacturer images.
- Use 3:2 landscape for project images and 4:5 for details. Crop to the work itself (trench, pipe, machine on site).
- Use square corners and full colour (no filters), with a mono caption giving place and year.
- Recommended slots: the homepage intro (replacing or beside the diagram), one image per ledger row on the References page, and the About page.

## Navigation

Astra header: logo on the left; Delatnosti · Reference · Mehanizacija · O nama · Kontakt; a red phone button on the right. On mobile the header shows the logo and a menu toggle that opens a dropdown, with the phone number repeated in the mobile header. The current page is underlined with a 2 px red rule.

## Mobile

Splits collapse to one column in reading order. The diagram scales to full width with its legend below. Ledger rows stack. Headings drop to the mobile scale, and phone and e-mail stay large tap targets (at least 44 px).
