# Asset inventory

## Assets used on the site

| Asset | Original source | Use | Local file | Media Library |
|---|---|---|---|---|
| Logo (colour) | Redrawn from `https://www.24oktobar.co.rs/head.gif` and `https://www.24oktobar.co.rs/contact-us.jpg`. The only originals are rasters about 55 px tall. | Header logo | `build/assets/24-oktobar-logo.png` (880×240, transparent). The redraw source is `build/assets/logo-source.html`. | ID 6, "24. Oktobar — logo" |
| Logo (white) | Same redraw | Spare, for dark backgrounds | `build/assets/24-oktobar-logo-beli.png` | ID 7 |
| Site icon | "24." from the logo on logo red | Browser tab and favicon | `build/assets/24-oktobar-ikonica.png` (512×512). The source is `build/assets/icon-source.html`. | ID 8 |
| Trench cross-section | Drawn for this site. The steps quote the Petrovaradin description in old `index.html`. | Home, Delatnosti | `build/parts.py` → `trench_svg()` (inline SVG) | — |
| Length chart | Data from old `ref1999…ref2012.html` | Home | `build/parts.py` → `length_chart()` | — |

**About the logo redraw:** the redraw uses the free Google font *Stardos Stencil* (SIL OFL) for the lettering. The roof, chimney and colour #D34053 were traced from `head.gif`. It is a faithful reconstruction, not the original artwork. Replace it if the company has the original vector file.

## Text and data reused

| Content | Source URL |
|---|---|
| Company description, activities, Novi Sad Gas, Petrovaradin, Greping, water networks | https://www.24oktobar.co.rs/index.html (identical on https://web.24oktobar.co.rs/about/) |
| Reference lists 1998–2018 → `docs/data/references.json` | https://www.24oktobar.co.rs/ref1999.html … ref2018.html |
| Excavators and mini excavators | https://www.24oktobar.co.rs/bageri.html (labels in `bageri-novi-2019.jpg`, `mini-51-novi-2019.jpg`) |
| Tools | https://www.24oktobar.co.rs/alati.html (labels in `alati-2019.jpg`) |
| Vehicles | https://www.24oktobar.co.rs/vozila.html (labels in `kamioni-2019.jpg`) |
| Address, phones, fax, mobile, e-mail, PIB, MBR | https://www.24oktobar.co.rs/kontakt.html |
| Working hours | https://web.24oktobar.co.rs/ (contact block) |

## Images reviewed and not used

| Files | Source | Reason |
|---|---|---|
| `4cx-bag, 4cx-blato, 4cx-down, 8032sun, bager, bager-gro, jcb8018noc` | old site | Manufacturer promotional photos (JCB, Volvo), about 220 px wide |
| `ing, ekipa, majstori, pocetak, slem, majstor-mob, contact-us, udarna-bosch` | old site | Stock or product imagery, about 220 px wide |
| `kanal, kanal-ploce, vodovod-kolektor, polaganje-cevi, pipeline` | old site | Provenance unclear and about 220 px wide. Usable only if the company confirms they are its own photos, and even then too small. |
| `bageri-novi-2019, mini-51-novi-2019, alati-2019, kamioni-2019` | old site | Collages of manufacturer product photos. Only the labels were used. |
| `baer, header, cropped-header, CM20190926-66cab-33d2a, Dc5qyBaXkAUNmHG, Finning-Branch-Location-Placeholder-727x420-1, unnamed` | web.24oktobar.co.rs `/wp-content/uploads/2020/07/` | Caterpillar / Finning dealer marketing images |
| `coffee, sandwich, espresso` | web.24oktobar.co.rs | WordPress theme demo images |

No image on the site is hotlinked from the old domains.
