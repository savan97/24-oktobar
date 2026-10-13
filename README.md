# 24. oktobar — company website (WordPress + Elementor)

A website for Građevinsko preduzeće „24. Oktobar“ d.o.o., Novi Sad: a contractor for gas pipelines, utility networks and earthworks. It runs on Local (by Flywheel) at **http://24-oktobar.local**.

## What's built

| Page | URL | Content |
|---|---|---|
| Početna | `/` | Intro with trench cross-section, activities, selected works ledger, documented-length chart, Novi Sad Gas / Petrovaradin case, machinery summary, contact band |
| Delatnosti | `/delatnosti/` | 8 activity groups, each with examples from the reference list, plus the work-sequence diagram |
| Reference | `/reference/` | All 135 references 1998–2018 by year, with a year jump index |
| Mehanizacija | `/mehanizacija/` | Excavators, mini excavators, tools, vehicles |
| O nama | `/o-nama/` | Company story, chronology, company data |
| Kontakt | `/kontakt/` | Clickable phones and e-mail, address with map link, working hours, PIB/MB |

All copy is Serbian Latin and drawn only from the company's own two websites (see `docs/RESEARCH.md`). Design rationale is in `DESIGN.md`, and asset sources are in `docs/ASSETS.md`.

## Stack

- **WordPress** 7.1.3 (existing Local install, preserved)
- **Theme:** Astra 4.14 (free). Twenty Twenty-Five, Four and Three are still installed but inactive.
- **Plugins:** Elementor 4.3.4 (free) and The SEO Framework 5.1.4 (free, for titles and descriptions)
- **Must-use plugin:** `wp-content/mu-plugins/24oktobar-site.php` (see below)
- No paid themes, plugins or templates. No contact form: there is no verified mail setup, so contact is by phone and e-mail links.

## Where things are managed

| What | Where in WP admin |
|---|---|
| Page content | Pages → *page* → **Edit with Elementor** |
| Global colours and fonts | Elementor editor → ☰ → Site Settings → Global Colors / Global Fonts |
| Logo, site icon | Appearance → Customize → Header Builder → Logo, and Site Identity |
| Header phone button | Appearance → Customize → Header Builder → Button 1 (desktop) and HTML 1 ("Pozovite", mobile) |
| Menu | Appearance → Menus → "Glavni meni" (locations: Primary, Mobile) |
| Footer columns | Appearance → Widgets → Footer Widget 1–3 (Custom HTML blocks) |
| Footer copyright | Appearance → Customize → Footer Builder → Copyright |
| Site CSS | Appearance → Customize → Additional CSS. Source: `wp-custom/site.css` |
| SEO title / description | Edit page (WordPress editor) → The SEO Framework box. Homepage: SEO Settings → Homepage |
| Images | Media Library |

## Editing pages in Elementor (for the company representative)

1. Log in → **Pages** → hover a page → **Edit with Elementor**.
2. Click any text on the page and type. Headings, paragraphs and lists edit directly.
3. **Reference and machinery lists:** each line is one list item. The grey number on the right (for example *19.150 m* or *2 kom.*) is text set in *italic*. Select it and press the **I** button in the text toolbar. Without italics it shows as normal text on the left.
4. **Buttons:** click the button, then change *Text* and *Link* in the left panel.
5. **Adding a new year to Reference:** right-click the row for the newest year (for example 2018) → **Duplicate**, then drag the copy above it. Change the year heading and the list. On the Advanced tab, set **CSS ID** to `g` followed by the year (for example `g2019`). Then add a link for the year at the top of the page by editing the HTML widget with the year buttons.
6. Click **Publish / Update** (bottom left).

Two blocks are **HTML widgets** because they're drawings: the trench diagram (Home, Delatnosti) and the length chart (Home). Their numbers can be edited in the HTML, but they're best left to a developer.

**Styles come from CSS classes.** Each element's look is set by a class under *Advanced → CSS Classes* (for example `t-h2`, `t-eyebrow`, `t-reflist`). Keep these classes when duplicating elements. Changing colours or fonts directly in a widget's *Style* tab also works, but it breaks consistency with the rest of the site.

### Adding photographs (recommended once the company provides its own)

Use only the company's own site photographs; see `DESIGN.md` → Photography rules. In Elementor, drag an **Image** widget into a section, choose the photo from the Media Library, set *Image Size* to "Large" and write the **Alt text** in the Media Library (place, year and type of work). Upload JPGs about 2000 px wide. WordPress creates the smaller sizes and lazy-loads them.

## Custom code (all of it)

| File | What it does |
|---|---|
| `wp-content/mu-plugins/24oktobar-site.php` | Sets `<html lang="sr-Latn">` and the OG locale. Translates the few English front-end strings Astra prints ("Skip to content", menu labels, 404 text). WordPress has no Serbian Latin locale, so the admin stays in English. |
| `wp-custom/site.css` → Additional CSS | The design system: tokens, `t-*` component classes, and header/footer styling for Astra. |
| `build/` | Developer tooling that generated the pages. **The site doesn't depend on it at runtime.** |

### Developer rebuild (optional)

The pages were generated from code so the layout stays consistent. The generator is idempotent: it matches pages by slug and doesn't delete anything.

```bash
python build/pages.py                       # writes build/out/*.json (needs docs/data/references.json)
wp eval-file build/import.php               # creates/updates pages, kit, Astra settings, menu, footer, CSS, SEO
wp elementor flush-css
```

⚠️ Re-running the import **overwrites changes made in Elementor** on those six pages. After the client starts editing, treat WordPress as the source of truth and stop using the generator.

With Local the DB host isn't the default. Run WP-CLI from Local's "Open site shell", or add `--exec="define('DB_HOST','127.0.0.1:10017');"`.

## Backups and reverting

- `backups/db-before-build-2026-10-13.sql` is the database before any of this work, taken right after the initial commit.
- The default "Hello world!" post and "Sample Page" were moved to **Trash** (restorable), not deleted.

## Known limitations

- **No company photographs.** None of the images on the old sites could be verified as the company's own, and they're about 220 px wide. The design works without photos, but real site photos would strengthen it. See `PROJECT_STATUS.md`.
- The logo is a high-resolution **redraw** (see `docs/ASSETS.md`). Replace it if the original vector exists.
- References stop at 2018 and equipment lists are from 2019. Both need the company to confirm or update them.
- Astra Free has no sticky header, which is acceptable for this site.
- Fonts are self-hosted by Elementor (Settings → Advanced → *Load Google Fonts Locally* is on). Pages not built with Elementor (404, search) fall back to system fonts.

## Migration to hosting (when authorised)

Nothing has been published, and no DNS or hosting settings were touched.

1. Export with Local (*Export site*) or use a migration plugin such as All-in-One WP Migration or Duplicator (free). Alternatively, copy `app/public` and import a `mysqldump`.
2. Search and replace the URL: `wp search-replace 'http://24-oktobar.local' 'https://www.24oktobar.co.rs' --all-tables`.
3. Elementor → Tools → **Regenerate CSS & Data**, then Settings → Permalinks → Save.
4. Check *Settings → Reading → Search engine visibility*, enable HTTPS, and set up SMTP if a contact form is ever added.
5. Redirect old URLs (301): `index.html` → `/o-nama/`, `bageri.html`, `alati.html`, `vozila.html` → `/mehanizacija/`, `ref*.html` → `/reference/`, `kontakt.html` → `/kontakt/`. Decide what happens to `web.24oktobar.co.rs`.
