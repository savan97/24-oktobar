# Phase 1 — Research and audit

Date of research: 2026-10-13. Everything below was read directly from the sources listed; nothing is assumed.

## 1. Sources inspected

| Source | What it is | Pages inspected |
|---|---|---|
| `https://www.24oktobar.co.rs/` (old site) | Static XHTML site, 1024 px fixed layout, last content update 2018–2019 | `index.html` (O nama), `bageri.html`, `alati.html`, `vozila.html` (Oprema), `ref1999…ref2018.html` (19 reference pages; `ref2002`/`ref2000`/`ref1998` link to the combined pages), `kontakt.html` |
| `https://web.24oktobar.co.rs/` (newer site) | WordPress 6.0 one-page theme from July 2020, never finished | `/`, `/about/`, `/contact/`, `/blog/` (empty), REST API `pages`, `posts` (0), `media` (10 files) |

The newer site repeats the old site's "O nama" and contact text word for word. The only new facts it adds are the **working hours**: Monday–Friday 08:00–15:00.

## 2. Verified company facts

| Fact | Value | Source |
|---|---|---|
| Legal name as written by company | Građevinsko preduzeće „24. Oktobar“ d.o.o. | old `index.html`, `kontakt.html` |
| Founded | 1997, Novi Sad | old `index.html` |
| Address | Temerinska 50, 21000 Novi Sad, Srbija | old `kontakt.html`, new `/contact/` |
| Phones | +381 21 47 41 048 · +381 21 551 044 · +381 21 6413 900 / lok. 116 | old `kontakt.html` |
| Fax | +381 21 47 41 048 | old `kontakt.html` |
| Mobile | +381 63 503 333 | old `kontakt.html` |
| E-mail (displayed) | 24oktobar.ns@gmail.com | old `kontakt.html`, new site |
| PIB / MBR | 101 699 336 / 0866 4102 | old `kontakt.html` |
| Working hours | Pon–pet 08:00–15:00 | new site homepage |
| Tagline in logo header | „Preduzeće za izvođenje grubih građevinskih radova“ | old `head.gif` |

### Business activities (old `index.html`)
1. **Grubi građevinski radovi** — raščišćavanje terena, iskop i zatrpavanje rovova, odvoz i dovoz zemlje i građevinskog materijala, razbijanje i sečenje betona i asfalta, podbušivanje, mašinsko nabijanje zemlje i peska u rov.
2. **Specifični radovi niskogradnje** — magistralni gasovodi, distributivne gasne mreže, kućni gasni priključci, vodovodna i toplovodna mreža, mreža za odvod atmosferskih voda, PTT mreža.

Additional work types evidenced only in the reference lists: gasovodi visokog i srednjeg pritiska, GMRS (glavne merno-regulacione stanice), otpremno-čistačko mesto, HD podbušivanje reka (Janja, Dašnica, Pilica), telekomunikaciona mreža (optički kabl), zidana trafo stanica, proizvodno-klanička hala, centralni magacin opreme (JVP „Vode Vojvodine“), sanacija deponije (Ada).

### Key client and narrative facts
- Long-term cooperation with investor DP „Novi Sad Gas“ as main contractor of construction works (municipalities: Novi Sad, Bački Petrovac, Bačka Palanka, Beočin, Sremski Karlovci, Bukovac).
- Petrovaradin fortress „podgrađe“: complete gas network, with the work sequence described in detail.
- Investor „Greping“: toplovod for residential buildings in Danila Kiša (1999) and Kornelija Stankovića (2000).
- Water networks Bečej and Susek; atmospheric drainage Bački Petrovac, Maglić, Gložan.

### References
135 listed entries, 1998–2018 (parsed into `docs/data/references.json`). Lengths are given for 1998–2012 entries; the sum of the given lengths of completed works is ≈ 1,086 km (1,085,573 m) (excluding the ambiguous „1.3350m“ Adice 2006 entry and the Silbaš network that was still in progress in 2012). Work in Republika Srpska / BiH (Bijeljina, Šepak) from 2009 to 2018.

### Equipment (old `bageri.html`, `alati.html`, `vozila.html`, collages dated 2019)
- Bageri rovokopači-utovarivači: 2× JCB 4CX, 2× JCB 3CX, Takeuchi TB1140
- Mini bageri: JCB 8018, 3× Takeuchi TB 235, plus one unlabelled Takeuchi (omitted)
- Alati: Bomag BT 60/4, Bosch GSH27 (2), Hitachi H90, Hycon HPP13, Norton Clipper C99, Gölz FS170, Wacker Neuson vibronabijač, Kärcher HD 7/18, mešalica za malter, mašina za podbušivanje sa spiralom
- Vozni park (2019 collage): GAZ Cab 112, GAZ 3302, Opel Combo-C, TAM 80T 5BK, Mercedes 1117 L, Iveco Daily 35S, Daimler Chrysler 970 – Atego 1015, Renault Kangoo, Iveco Daily 50C, VW Transporter T5, VW Caddy, Dacia Duster

## 3. Missing, outdated or conflicting information (needs client confirmation)

| # | Issue | Decision in the new site |
|---|---|---|
| 1 | E-mail: link target is `okt24@nscable.net`, displayed text is `24oktobar.ns@gmail.com` | Published the displayed Gmail address (also on the newer site). **Confirm.** |
| 2 | „11-godišnje iskustvo“, „preko 10 godina saradnje“ — written ≈ 2008 | Not repeated. Replaced with „od 1997.“ |
| 3 | No references after 2018 | Site says „1998–2018“. **Ask for 2019–2026 work.** |
| 4 | Vehicle text („4 kamiona Iveco, Zastava, GAZ“) contradicts the 2019 vehicle collage | Used the 2019 collage. **Confirm current fleet.** |
| 5 | Equipment lists are from 2019 | Published as listed. **Confirm still current.** |
| 6 | „DP Novi Sad Gas“ — company's current legal form not verified | Written as „Novi Sad Gas“ in historical context. |
| 7 | Adice 2006 length „1.3350m“ is ambiguous | Shown without length. |
| 8 | Typos in source lists (Lig → Lug, Svilos → Sviloš, Liparijea) | Corrected obvious ones; „Liparijea“ shown as „Liparija“ — **confirm.** |
| 9 | Fax shares the number of the first phone line | Shown as „tel./faks“. |
| 10 | No original logo vector | Logo redrawn from the 2 raster sources — **request original file.** |

## 4. Image audit — the main constraint

All 34 images were downloaded and inspected (`scratchpad`, not committed).

| Group | Files | Finding | Decision |
|---|---|---|---|
| Old site small photos | `4cx-bag, 4cx-blato, 4cx-down, 8032sun, bager, bager-gro, jcb8018noc, ing, ekipa, majstori, pocetak, kanal, kanal-ploce, vodovod-kolektor, polaganje-cevi, pipeline, slem, udarna-bosch, majstor-mob, contact-us` | 194–228 px wide. Many are recognisable manufacturer or stock images (JCB/Volvo promo shots, call-centre headset model, engineers in ties, Bosch product shot). None can be confirmed as the company's own site photography. | **Not reused.** Too small for any modern layout, and provenance can't be verified. |
| Equipment collages | `bageri-novi-2019, mini-51-novi-2019, alati-2019, kamioni-2019` | Manufacturer product images assembled into collages; the **labels** are company data. | Data reused as text; images not reused (manufacturer copyright). |
| Newer site media | `baer, header, cropped-header, CM20190926…, Dc5qy…, Finning-Branch-Location-Placeholder…, unnamed` | CAT marketing / dealer (Finning) images, HDR stock loader | **Not reused** — third-party. |
| Newer site media | `coffee, sandwich, espresso` | WordPress theme demo images | **Not reused.** |
| Logo | `head.gif` (1024×145), `contact-us.jpg` | Only raster sources, ≈ 55 px tall | Redrawn at high resolution (see `docs/ASSETS.md`). |

**Consequence for design:** the brief requires real company photographs and forbids stock substitutes. No verifiable company photos exist online, so the design must be credible without photography. It also needs clear places where the client's own photos can be added later (see `README.md`). This is the most important open request to the client.

## 5. Design references — what makes them work

- **Skender** — confident black/white editorial type, very large project imagery, short declarative statements, market-led navigation. Lesson: *hierarchy through scale and restraint, not decoration.*
- **McCarthy** — dense but disciplined; condensed sans for headings (Roboto Condensed), warm dark neutrals (#221f1b) with a single signal colour; project names as the main content; heritage stated once, plainly. Lesson: *a narrow, industrial typeface and one signal colour read as "builder".*
- **DAVIS** — calm navy palette, plain-language promises, project spotlight with name and location as the primary metadata. Lesson: *project name and location are the essential project data.*

Shared principles: real work is the hero; little ornament; one accent colour; clear navigation of 5–6 items; contact always reachable. All three depend on large professional photography, which 24. oktobar doesn't have. Copying their photo-led layouts would therefore fail here.

## 6. Three design directions

1. **„Trasa“ (the route) — chosen.** Visual language of an engineering survey: thin rules, a trench cross-section diagram that explains the actual work sequence (iskop → posteljica → cev → nabijanje → zatrpavanje → vraćanje terena), monospaced annotations for years and metres, and the logo red used like a marked pipeline route. The 20-year reference list becomes the main proof, set as a ledger. Works without photography and is specific to a low-construction / pipeline contractor.
2. **„Arhiva“** — editorial company archive: serif headlines, chronological story 1997–2018, large photo plates. Rejected because its impact depends on archival photos that don't exist.
3. **„Teren“** — dark, full-bleed field photography with large type over images (closest to the references). Rejected: requires high-resolution genuine photos. With stock images it would be exactly the generic template the brief forbids.

## 7. Sitemap

```
Početna            /
Delatnosti         /delatnosti/
Reference          /reference/        (complete ledger 1998–2018)
Mehanizacija       /mehanizacija/     (was "Oprema" on the old site)
O nama             /o-nama/
Kontakt            /kontakt/
```
No individual project pages: the sources give only name, place, year and length per project, which the ledger presents completely. Separate pages would be empty.
