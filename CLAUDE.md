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
| Homepage | 1 | `/` | `this-week.json` |
| Vendors | 12 | `/vendors/`, `/vendors/[slug]` | `content/vendors/*.md` (11 vendors) |
| Business Directory | 18 | `/businesses/`, `/businesses/[slug]` | `content/businesses/*.md` (17 KBPA members) |
| Discover Kinderhook | 9 | `/discover/`, `/discover/[slug]` | `content/landmarks/*.md` (8 landmarks) |
| Recipes | 6 | `/recipes/`, `/recipes/[slug]` | `content/recipes/*.md` (5 recipes) |
| Core pages | 4 | `/about`, `/visit`, `/whats-fresh`, `/contact` | Inline + JSON data |

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
│   ├── MarketIcon.astro           # Hand-drawn Procreate icon component (7 icons)
│   ├── ShareableMarketCard.astro  # Canvas-based save-the-date image generator
│   └── ...
├── layouts/
│   └── BaseLayout.astro       # Sitewide layout with nav, footer, SEO component, Organization schema
├── pages/
│   ├── index.astro            # Homepage with weekly lineup from this-week.json
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
│   ├── about.astro            # Market story, history, KBPA member listing
│   ├── visit.astro            # Plan your visit + dynamic landmarks from collection
│   ├── whats-fresh.astro      # Seasonal produce guide with tab switching
│   └── contact.astro          # Contact form + vendor applications
├── content/
│   ├── vendors/*.md           # 11 market vendors (regular + guest)
│   ├── businesses/*.md        # 17 KBPA member businesses
│   ├── landmarks/*.md         # 8 Kinderhook landmarks and attractions
│   └── recipes/*.md           # 5 community recipes
├── data/
│   ├── site-config.json       # Market hours, location, season dates, contact info
│   └── this-week.json         # This week's lineup (music, vendors, events)
└── content.config.ts          # Zod schemas for all content collections
```

### Deployment

- **Hosting:** GitHub Pages (harmonicsystems/market repo)
- **CI/CD:** `.github/workflows/deploy.yml` — builds with Astro on push to `main`
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
--color-orange: #B8860B;   /* Dark goldenrod — primary accent, CTAs */
--color-teal: #5A7247;     /* Deep sage green — secondary, links, nature */
--color-lime: #C49A02;     /* Warm gold — tertiary highlights */
--color-black: #2E1F2F;    /* Deep aubergine — text, headers, dark sections */
--color-cream: #DFA926;    /* Golden amber — sitewide background */
```

Designer accent colors (for future use):
- Yellow: `#DFA926` (warm golden amber — currently the background)
- Purple: `#5D3C54` (deep plum)

### Typography (Google Fonts)

```css
--font-logo: 'Aoboshi One', Georgia, serif;       /* Logo/brand text only */
--font-display: 'DM Serif Display', Georgia, serif; /* Headings throughout site */
--font-body: 'Lora', Georgia, serif;                /* Body text */
--font-accent: 'DM Serif Display', Georgia, serif;  /* Accent text */
```

- **Logo/Brand:** Aoboshi One (`font-logo`) — header, footer, homepage hero only
- **Display/Headings:** DM Serif Display (`font-display`) — all page headings, nav
- **Body:** Lora (`font-body`) — paragraphs, descriptions

### Icons

Custom hand-drawn Procreate PNG icons from designer in `public/icons/`:

| Icon | File | Used for |
|------|------|----------|
| Apple | FM-APPLE-ICON.png | Regular vendors |
| Bike | FM-BIKE-ICON.png | Neighborhoods, visit |
| Bird | FM-BIRD-ICON.png | Trails, nature |
| Brush | FM-BRUSH-ICON.png | Galleries, arts |
| History | FM-HISTORY-ICON.png | Historic sites, museums |
| OK | FM-OK-ICON.png | Businesses, fallback |
| Sunflower | FM-SUNFLOWER-ICON.png | Guest vendors, homepage hero |

Rendered via `MarketIcon.astro` component with short name props (e.g., `<MarketIcon name="apple" class="w-16 h-16" />`).

### Header Behavior
- Gold background (`bg-cream`), blends with page
- Logo text hidden on homepage until user scrolls past hero (IntersectionObserver on `#homepage-hero`)
- Logo always visible on all other pages
- Mobile hamburger menu

### Contrast Notes
- On gold background: use `text-black` or `text-black/90` minimum (7.27:1 ratio)
- Never use `text-orange`, `text-teal`, or `text-white` directly on gold — insufficient contrast
- On white cards: `text-black`, `text-teal` (5.34:1), and large `text-orange` (3.25:1) are fine

---

## Location Data (confirmed)

```
Village Green, Kinderhook, NY 12106
Intersection of U.S. Route 9 (Broad/Chatham Streets) and Albany Avenue
Coordinates: 42.3951, -73.6981 (42°23'42.2"N 73°41'53.3"W)
Schedule: Saturdays 8:30 AM – 12:30 PM, May through October
```

---

## Key Features Still on Roadmap

### Near-term
- **Multi-week schedule system** — Replace single `this-week.json` with a full season schedule, generating per-week Event schemas
- **Interactive Leaflet map** on Visit page (placeholder currently shown)
- **Vendor/business photos** — Photo fields exist in schemas but no images yet
- **OG image and logo assets** — `og-image.png` and `logo.png` referenced in schemas but not yet created

### Future
- **Events calendar** with iCal export
- **Newsletter integration** (Mailchimp or similar)
- **Local currency tie-in** (heritage currency project)
- **QR scavenger hunt** for historical locations
- **GitHub Actions cron builds** — Auto-rebuild on schedule during market season
- **Google Search Console** registration + indexing API pings
- **Google Business Profile** integration

---

## Content Update Guide

### Updating This Week's Market
Edit `src/data/this-week.json` — update date, theme, music, vendors, events.

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

- The "It's OK!" tagline comes from Martin Van Buren's nickname "Old Kinderhook" — possibly the origin of the word "okay"
- The KBPA website (kinderhookbusiness.com) appears to be down — we now host the most complete KBPA member directory
- Jack Shainman Gallery: The School is open Saturdays, same as the market — natural synergy
- The Dutch Farming Heritage Trail connects Van Alen House to Lindenwald — great day trip content
- Empire State Trail (750 miles) passes through Kinderhook Village
