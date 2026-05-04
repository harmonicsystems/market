# Kinderhook Farmers' Market Website

## Project Overview

A modern, community-centered website for the Kinderhook Farmers' Market in Kinderhook, NY. The site serves as both a market resource and a broader village economic development tool — a hub for vendors, KBPA businesses, historic landmarks, seasonal produce, and community recipes.

**Client:** Kinderhook Business and Professional Association / Economic Development Coordinator
**Goal:** Replace the outdated 2015 WordPress site with a fast, beautiful, easily-maintainable modern site that strengthens the local economy, boosts search visibility for Kinderhook, and makes the village a must-visit destination.

**Live site:** https://harmonicsystems.github.io/market/
**Status:** Active development with designer assets integrated. SEO infrastructure and content are production-ready.

---

## What's Built (50 pages)

| Section | Pages | Route | Content Source |
|---------|-------|-------|----------------|
| Homepage | 1 | `/` | `content/weeks/*.md` (auto-selects next upcoming week) |
| Vendors | 12 | `/vendors/`, `/vendors/[slug]` | `content/vendors/*.md` (11 vendors) |
| Business Directory | 18 | `/businesses/`, `/businesses/[slug]` | `content/businesses/*.md` (17 KBPA members) |
| Discover Kinderhook | 9 | `/discover/`, `/discover/[slug]` | `content/landmarks/*.md` (8 landmarks) |
| Recipes | 6 | `/recipes/`, `/recipes/[slug]` | `content/recipes/*.md` (5 recipes) |
| Core pages | 4 | `/about`, `/visit`, `/whats-fresh`, `/contact` | Inline + JSON data |
| Share cards | 27 | `/share/[week]` | `content/weeks/*.md` (one route per Saturday) |
| Dev tools | 1 | `/styleguide` | Inline (noindex) |

---

## Technical Architecture

### Stack

- **Framework:** Astro 5 (static site generation)
- **Styling:** Tailwind CSS 4
- **Content:** Astro Content Collections (Markdown + Zod schemas) + JSON data files
- **SEO:** Custom `SEO.astro` + `StructuredData.astro` components, `@astrojs/sitemap`
- **Hosting:** GitHub Pages via GitHub Actions (auto-deploy on push to `main`)
- **Forms:** Netlify Forms (contact page, will need Netlify hosting to activate)

### Key Files

```
src/
├── components/
│   ├── SEO.astro              # Open Graph, Twitter cards, geo meta tags, canonical URLs
│   ├── StructuredData.astro   # JSON-LD schemas (organization, event, vendor, business, landmark, recipe, breadcrumb)
│   ├── MarketIcon.astro           # Hand-drawn Procreate icon component (13 icons)
│   ├── HeroCore.astro             # Shared market identity block (sunflower/title/divider/schedule/time)
│   ├── ShareableMarketCard.astro  # Canvas-based save-the-date image generator (tone: dark|light)
│   └── ...
├── layouts/
│   └── BaseLayout.astro       # Sitewide layout with nav, footer (share bar + designer signature), SEO, Organization schema
├── lib/
│   └── weeks.ts               # getCurrentMarketWeek(), todayInET(), formatDisplayDate() — ET-aware week selection
├── pages/
│   ├── index.astro            # Homepage — auto-advances to next upcoming week; off-season fallback message
│   ├── vendors/
│   │   ├── index.astro        # Vendor directory (regular + guest)
│   │   └── [slug].astro       # Vendor detail pages with vendor schema + related vendors/recipes
│   ├── businesses/
│   │   ├── index.astro        # KBPA business directory
│   │   └── [slug].astro       # Business detail pages with LocalBusiness schema
│   ├── discover/
│   │   ├── index.astro        # "Discover Kinderhook" attractions page
│   │   └── [slug].astro       # Landmark detail pages with TouristAttraction schema
│   ├── recipes/
│   │   ├── index.astro        # Recipe collection
│   │   └── [slug].astro       # Recipe detail pages with Recipe schema
│   ├── share/
│   │   └── [week].astro       # 1080×1080 share-card route — one path per week from content/weeks/ (noindex)
│   ├── styleguide.astro       # Design reference page (noindex, dev tool)
│   ├── about.astro            # Market story, history, KBPA member listing
│   ├── visit.astro            # Plan your visit + dynamic landmarks from collection
│   ├── whats-fresh.astro      # Seasonal produce guide with tab switching
│   └── contact.astro          # Contact form + vendor applications
├── content/
│   ├── vendors/*.md           # 11 market vendors (regular + guest)
│   ├── businesses/*.md        # 17 KBPA member businesses
│   ├── landmarks/*.md         # 8 Kinderhook landmarks and attractions
│   ├── recipes/*.md           # 5 community recipes
│   ├── events/*.md            # 19 community events (parades, library programs, gallery openings)
│   ├── performers/*.md        # 11 music acts with profile pages
│   └── weeks/*.md             # 27 Saturdays of the season (one file per market day)
├── data/
│   ├── site-config.json       # Market hours, location, season dates, contact info
│   ├── music-schedule.json    # Per-Saturday music lineup for the season
│   ├── weekly-vendors.json    # Default weekly-regular vendor roster (homepage fallback)
│   └── sponsors.json          # Sponsor list with logos and links
└── content.config.ts          # Zod schemas for all content collections
```

### Deployment

- **Hosting:** GitHub Pages (harmonicsystems/market repo)
- **CI/CD:** `.github/workflows/deploy.yml` — builds with Astro on push to `main`
- **Scheduled rebuild:** Every Sunday at 11:00 UTC (7am EDT / 6am EST) via cron — advances "Next Market" to the upcoming Saturday after each market day, no manual edit needed
- **Pages source:** Must be set to "GitHub Actions" in repo Settings > Pages (not "Deploy from branch")
- **Base URL:** `/market` (configured in `astro.config.mjs`)
- **Future domain:** `kinderhookfarmersmarket.com` — update `site` in astro.config.mjs and `robots.txt` when ready

---

## SEO / GEO Architecture

The site is built to rank for "Hudson Valley farmers market", "things to do in Kinderhook", "Columbia County" searches.

### Sitewide (every page)
- `LocalBusiness` JSON-LD with `@id` anchor at `/#organization`
- `areaServed`: Kinderhook, Valatie, Hudson, Columbia County, Hudson Valley, Capital Region
- `sameAs` links to Facebook and Instagram
- Geo meta tags: `geo.region`, `geo.placename`, `geo.position`, `ICBM`
- Open Graph + Twitter card meta tags
- Canonical URLs
- Auto-generated sitemap via `@astrojs/sitemap`

### Per-page schemas
- **Homepage:** `Event` with date, theme, performer (MusicGroup), free Offer (price: 0 + isAccessibleForFree)
- **Vendor pages:** `Organization` with `memberOf` back-reference to parent market `@id`
- **Business pages:** `LocalBusiness` with `containedInPlace` (Kinderhook → Columbia County)
- **Landmark pages:** `TouristAttraction` with geo coordinates and `containedInPlace`
- **Recipe pages:** `Recipe` with prep/cook time, servings, keywords
- **All detail pages:** `BreadcrumbList` for navigation display in search results

### Event schema specifics
- EDT timezone (`-04:00`) for May–October market season
- `performer` array only emitted when a music act exists (no empty arrays)
- `offers` with `price: 0` + `isAccessibleForFree: true` = Google shows "Free" in event results

---

## Content Schemas

All defined in `src/content.config.ts` with Zod validation.

### Vendor (`content/vendors/*.md`)
Fields: `name`, `slug`, `tagline`, `categories[]`, `description`, `image`, `website`, `instagram`, `facebook`, `featured`, `active`, `vendorType` (regular|guest)

### Business (`content/businesses/*.md`)
Fields: `name`, `slug`, `type`, `tagline`, `image`, `address`, `phone`, `website`, `hours`, `description`

### Landmark (`content/landmarks/*.md`)
Fields: `name`, `slug`, `type` (historic-site|museum|gallery|trail|neighborhood), `tagline`, `image`, `address`, `phone`, `website`, `hours`, `admission`, `description`, `featured`, `coordinates` ({lat, lng})

### Recipe (`content/recipes/*.md`)
Fields: `title`, `slug`, `emoji`, `image`, `prepTime`, `cookTime`, `servings`, `season[]`, `produce[]`, `contributor`, `contributorLink`, `difficulty` (easy|medium|hard), `tags[]`

---

## Design System

### Brand Colors

```css
--color-orange: #B8860B;   /* Dark goldenrod — primary accent, CTAs, highlights */
--color-purple: #5D3C54;   /* Deep plum — secondary accent, taglines, category alternatives */
--color-black: #2E1F2F;    /* Deep aubergine — text, headings, dark sections */
--color-cream: #DFA926;    /* Golden amber (yellow) — sitewide background */
--color-white: #FFFFFF;    /* Card surfaces, text on dark */
```

Teal and Lime were removed in favor of this tighter, more accessible palette. Orange and Purple together cover differentiation needs (primary vs secondary CTAs, regular vs guest vendors, easy/medium/hard difficulty, spring/summer vs fall seasons).

### Typography (Google Fonts)

```css
--font-logo: 'Aoboshi One', Georgia, serif;       /* Logo/brand text only */
--font-display: 'DM Serif Display', Georgia, serif; /* Headings throughout site */
--font-body: 'Lora', Georgia, serif;                /* Body text */
--font-accent: 'DM Serif Display', Georgia, serif;  /* Accent text */
```

- **Logo/Brand:** Aoboshi One (`font-logo`) — header wordmark, footer wordmark only
- **Display/Headings:** DM Serif Display (`font-display`) — homepage hero title, all page headings, nav, NEXT MARKET banner
- **Body:** Lora (`font-body`) — paragraphs, descriptions

### Icons

Custom hand-drawn Procreate PNG icons from designer (Susanne Lamb) in `public/icons/`. All are black-on-transparent PNGs.

**Category icons** — rendered via `MarketIcon.astro` with short name props (e.g., `<MarketIcon name="apple" class="w-16 h-16" />`):

| Icon | File | Used for |
|------|------|----------|
| Apple | FM-APPLE-ICON.png | Regular vendors |
| Bike | FM-BIKE-ICON.png | Neighborhoods, visit |
| Bird | FM-BIRD-ICON.png | Trails, nature |
| Brush | FM-BRUSH-ICON.png | Galleries, arts |
| History | FM-HISTORY-ICON.png | Historic sites, museums |
| OK | FM-OK-ICON.png | Businesses, fallback |
| Sunflower | FM-SUNFLOWER-ICON.png | Guest vendors |
| Music | FM-MUSIC-ICON.png | Live music section |
| Star | FM-STAR-ICON.png | Special events |
| Heart | FM-HEART-ICON.png | Follow for Weekly Updates label |

**Social icons** — rendered inline via CSS mask technique (see below):

| Icon | File | Used for |
|------|------|----------|
| Facebook | FM-FACEBOOK-ICON.png | Facebook share/follow links |
| Instagram | FM-INSTAGRAM-ICON.png | Instagram follow links |
| Nextdoor | FM-NEXTDOOR-ICON.png | Nextdoor share links |
| Download | FM-DOWNLOAD-ICON.png | Save share image button |

**Decorative elements:**

| Asset | File | Used for |
|-------|------|----------|
| Sunflower banner (GIF) | FM-SUNFLOWER-TOP_BANNER.gif | Animated hero banner |
| Sunflower banner (static) | FM-SUNFLOWER-TOP_BANNER-STATIC.png | Canvas share card |
| Divider line | FM-DIVIDER_2.png | Hand-drawn underline below title |
| Flourish | FM-DIVIDER_1.png | Curly brackets around time (split via mask-position) |
| Floral divider | FM-DIVIDER_3.png | Available but not yet used |
| Designer signature | DESIGNED-BY-SUSANNE-LAMB.png | Footer credit (linked to susannelamb.com) |

### Icon Rendering Technique

Icons are tinted to brand colors via CSS `mask-image` — the PNG's alpha channel masks a solid `background-color`:

```html
<span class="social-icon-mask block w-12 h-12"
  style="background-color: #5D3C54;
         -webkit-mask-image: url('/icons/FM-MUSIC-ICON.png');
         mask-image: url('/icons/FM-MUSIC-ICON.png');">
</span>
```

The `.social-icon-mask` utility in `global.css` sets `mask-size: contain; mask-repeat: no-repeat; mask-position: center`.

**Color by context:**
- On cream (hero, cards): `#2E1F2F` (aubergine), `#5D3C54` (purple for music), `#B8860B` (orange for stars)
- On aubergine (footer): `#FFFFFF` (white)

**Known limitation:** CSS masks don't survive browser "Full Page" screenshot tools (iOS Safari, etc.) — icons render as solid rectangles. This is cosmetic only and doesn't affect Playwright screenshots (stage 3 of share-card unification).

### Header Behavior
- Gold background (`bg-cream`), blends with page
- Logo text hidden on homepage until user scrolls past hero (IntersectionObserver on `#homepage-hero`)
- Logo always visible on all other pages
- Mobile hamburger menu

### Contrast Notes
- On gold/cream background: use `text-black` or `text-black/90` minimum (7.27:1 ratio)
- Never use `text-orange` or `text-white` directly on cream — insufficient contrast
- On white cards: `text-black`, `text-purple` (~6:1), and large `text-orange` (3.25:1) are fine
- `text-purple` on cream is readable but large sizes only; prefer `text-purple` on white surfaces

---

## Location Data (confirmed)

```
Village Green, Kinderhook, NY 12106
Intersection of U.S. Route 9 (Broad/Chatham Streets) and Albany Avenue
Coordinates: 42.3951, -73.6981 (42°23'42.2"N 73°41'53.3"W)
Schedule: Saturdays 8:30 AM – 12:30 PM, May through October
```

---

## Weekly Schedule + Auto-Advance

The "Next Market" block on the homepage and the footer share card are both driven by the `weeks` content collection (`src/content/weeks/YYYY-MM-DD.md`, one file per Saturday) via `src/lib/weeks.ts`.

**Selection logic** — `getCurrentMarketWeek()` returns the first week where `date >= today` (today computed in `America/New_York` so the UTC build server doesn't drift). On Saturday morning the page still shows today's market; the Sunday-morning cron rebuild advances it to the next Saturday.

**Off-season fallback** — when no future market remains in the collection, `getCurrentMarketWeek()` returns `undefined` and the homepage swaps the "Next Market:" block for a "See you in May:" closed-for-the-season message. The footer share card is hidden across the site. Weather widget is hidden anytime the next market is more than 7 days out (Open-Meteo's forecast window).

**Weather widget** — wired to the actual selected market date via a `data-market-date` attribute, so it can never disagree with the displayed date regardless of the visitor's timezone.

**Per-week info** — each week file's frontmatter can carry `theme`, `note`, `specialEvents[]`, `guestVendors[]`, `communityPartners[]`, and `regularVendors[]` (override). All optional — empty stubs are fine. Music is normally pulled from `music-schedule.json` automatically; a per-week `music: { name, time }` override is supported.

**Share-card route** — `/share/[week].astro` generates one route per entry in the weeks collection (27 paths). All routes have `noindex,nofollow` and are sized for a Playwright snapshot at 1080×1080.

### HeroCore.astro

The shared market identity block (sunflower banner / title / divider / schedule line) used by both the homepage hero and `/share/[week]`. Props: `fluid` (default `true` for homepage, `false` for fixed-size share canvas) and `scheduleText` (homepage uses a generic season line; share page uses the specific market date).

**Remaining share-card stages:**
- **Stage 3:** GitHub Action runs Playwright to screenshot each `/share/<date>` at 1080×1080 and commits PNGs to `public/share/`
- **Stage 4:** Wire hero download button to static PNGs; retire `ShareableMarketCard.astro` canvas code; use PNGs as `og:image`

---

## Key Features Still on Roadmap

### Near-term
- **Share-card unification stages 3–4** — Playwright snapshots of `/share/[week]` to PNG; retire `ShareableMarketCard.astro` canvas code
- **Interactive Leaflet map** on Visit page (placeholder currently shown)
- **Vendor/business photos** — Photo fields exist in schemas but no images yet
- **OG image and logo assets** — `og-image.png` and `logo.png` referenced in schemas but not yet created
- **2027 season prep** — Add `content/weeks/2027-*.md` and update `music-schedule.json` before May 2027; otherwise the homepage falls into off-season mode after Oct 31, 2026

### Future
- **Events calendar** with iCal export
- **Newsletter integration** (Mailchimp or similar)
- **Local currency tie-in** (heritage currency project)
- **QR scavenger hunt** for historical locations
- **Google Search Console** registration + indexing API pings
- **Google Business Profile** integration

---

## Content Update Guide

### Updating an Upcoming Market
Edit (or create) `src/content/weeks/YYYY-MM-DD.md`. Frontmatter fields: `theme`, `note`, `specialEvents[]`, `guestVendors[]`, `communityPartners[]`, `regularVendors[]` (override the season roster), and `music: { name, time }` (override the schedule lookup). All optional. The homepage, footer share card, calendar headlines, and `/share/<week>/` route all update together. The Sunday-morning cron auto-advances the homepage to the next upcoming market — no manual edit needed for the date roll.

### Adding a Vendor
1. Create `src/content/vendors/vendor-name.md` with frontmatter
2. Commit and push — auto-deploys and generates detail page + schema

### Adding a Business
1. Create `src/content/businesses/business-name.md`
2. Business appears on directory page and About page KBPA listing

### Adding a Landmark
1. Create `src/content/landmarks/landmark-name.md`
2. If `featured: true`, it shows on the Visit page and Discover page hero

### Adding a Recipe
1. Create `src/content/recipes/recipe-name.md`
2. If contributor matches a vendor name, it cross-links on the vendor detail page

---

## Coding Standards

- Semantic HTML5, WCAG 2.1 AA accessibility
- Mobile-first responsive design
- All images optimized (WebP with Astro's built-in optimization)
- Conventional commits (feat:, fix:, docs:, content:)
- Content in `/content` or `/data` — never hardcoded in pages
- TypeScript Zod schemas for all content collections

---

## Notes

- **Designer:** Susanne Lamb ([susannelamb.com](https://susannelamb.com)) — hand-drawn Procreate icons, dividers, sunflower banner, signature. Credit in footer links to her site.
- The KBPA website (kinderhookbusiness.com) appears to be down — we now host the most complete KBPA member directory
- Jack Shainman Gallery: The School is open Saturdays, same as the market — natural synergy
- The Dutch Farming Heritage Trail connects Van Alen House to Lindenwald — great day trip content
- Empire State Trail (750 miles) passes through Kinderhook Village
