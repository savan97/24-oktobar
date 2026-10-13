# Project status — 2026-10-13

## Done
- [x] Phase 1: research of both company sites, the 3 design references and the local WP install → `docs/RESEARCH.md`
- [x] Phase 2: "Trasa" design system → `DESIGN.md`
- [x] Phase 3: DB backup; Astra, Elementor (free) and The SEO Framework installed; Serbian-Latin mu-plugin; logo redrawn; Media Library set up
- [x] Phase 4: 6 pages built in Elementor (Početna, Delatnosti, Reference, Mehanizacija, O nama, Kontakt), plus header, menu and footer
- [x] Phase 5 QA:
  - [x] Desktop (1440) and mobile (390) visual checks for all pages
  - [x] 30 internal links return 200; unknown URLs return 404
  - [x] Each page has one H1, a logical heading order, a custom title and a meta description
  - [x] No images without alt text
  - [x] Clickable `tel:` and `mailto:` links on every page
  - [x] Focus outlines and 44 px tap targets
  - [x] `prefers-reduced-motion` respected
  - [x] Fonts self-hosted
- [x] Phase 6: `README.md`, `docs/ASSETS.md`, this file

## Current state
The site is complete and running locally at http://24-oktobar.local. Nothing is published.

## Needs the client (blocking accuracy, not function)
1. **Own photographs** of sites, crews and machines. None of the old images are usable (stock or manufacturer images, about 220 px wide).
2. **Confirm e-mail**: the site shows `24oktobar.ns@gmail.com`; the old site's link pointed to `okt24@nscable.net`.
3. **References 2019–2026**: the site currently says 1998–2018.
4. **Current equipment and vehicles**: the lists are from 2019, and the old vehicle text contradicted the 2019 photo labels.
5. **Original logo file** (vector), to replace the redraw.
6. Is cooperation with Novi Sad Gas ongoing? The copy currently uses the past tense ("ostvarili smo dugogodišnju saradnju").
7. Confirm "Liparija" (source: "Liparijea"), the Adice 2006 length (source: "1.3350m"), and the "≈ 1.086 km" total on the homepage, which is computed from the reference list.

## Optional next steps
- Add photos per `DESIGN.md` once supplied (homepage intro, ledger rows, O nama).
- Decide whether a contact form is wanted. It needs SMTP on the hosting; WPForms Lite or Contact Form 7 would cover it.
- Migration and 301 redirects from the old `.html` URLs (see README). This needs the client's authorisation.
- Delete the inactive Twenty Twenty-* themes before going live.
