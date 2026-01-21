# Kinderhook Farmers' Market Website

## Project Overview

A modern, community-centered website for the Kinderhook Farmers' Market in Kinderhook, NY. This site serves as both a market resource and a broader village economic development tool, showcasing local vendors, permanent businesses, seasonal produce, and community recipes.

**Client:** Kinderhook Business and Professional Association / Economic Development Coordinator
**Goal:** Replace the outdated 2015 WordPress site with a fast, beautiful, easily-maintainable modern site that strengthens the local economy and community connections.

---

## Design System

### Brand Colors (from official style guide)

```css
:root {
  /* Primary */
  --kinderhook-orange: #F26A2A;      /* Warm orange - primary accent, CTAs, badges */
  --kinderhook-teal: #2AAFCE;        /* Teal/turquoise - headers, links, highlights */

  /* Secondary */
  --kinderhook-lime: #B8BF3D;        /* Lime green - botanical accents, fresh/seasonal */
  --kinderhook-black: #1A1A1A;       /* Rich black - text, contrast elements */

  /* Neutrals */
  --kinderhook-cream: #FFF9F0;       /* Warm cream - backgrounds */
  --kinderhook-white: #FFFFFF;       /* Pure white - cards, content areas */

  /* Semantic */
  --color-primary: var(--kinderhook-orange);
  --color-secondary: var(--kinderhook-teal);
  --color-accent: var(--kinderhook-lime);
  --color-text: var(--kinderhook-black);
  --color-background: var(--kinderhook-cream);
}
```

### Typography

- **Headings:** Rounded, friendly sans-serif (consider: Nunito, Quicksand, or Poppins)
- **Body:** Clean, readable sans-serif (consider: Inter, Source Sans Pro)
- **Accent/Display:** Hand-drawn feel for special callouts (consider: Caveat, Patrick Hand)

### Visual Motifs

- Hand-drawn botanical illustrations (tulips, leaves, sprouts)
- Organic oval/pill shapes for badges and containers
- Scattered dots as decorative elements
- Warm, approachable, farm-fresh aesthetic
- The "It's OK!" badge references Martin Van Buren's "Old Kinderhook" nickname

---

## Technical Architecture

### Stack

- **Framework:** Astro (static site generation, fast, great DX)
- **Styling:** Tailwind CSS with custom design tokens
- **Content:** Markdown files + JSON data files for easy updates
- **Hosting:** Netlify or Vercel (free tier sufficient)
- **Forms:** Netlify Forms or Formspree for contact

### Why This Stack?

1. **Zero runtime cost** - static HTML, blazing fast
2. **Easy content updates** - edit markdown/JSON, no database
3. **Free hosting** - perfect for community budget
4. **Simple handoff** - coordinator can edit text files or we add a simple CMS later

### Directory Structure

```
kinderhook-farmers-market/
├── src/
│   ├── components/
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   ├── VendorCard.astro
│   │   ├── BusinessCard.astro
│   │   ├── RecipeCard.astro
│   │   ├── SeasonalWheel.astro
│   │   ├── EventBanner.astro
│   │   ├── MarketCountdown.astro
│   │   └── ui/
│   │       ├── Button.astro
│   │       ├── Badge.astro
│   │       └── Card.astro
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   └── ContentLayout.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── vendors/
│   │   │   ├── index.astro
│   │   │   └── [slug].astro
│   │   ├── businesses/
│   │   │   ├── index.astro
│   │   │   └── [slug].astro
│   │   ├── recipes/
│   │   │   ├── index.astro
│   │   │   └── [slug].astro
│   │   ├── whats-fresh.astro
│   │   ├── events.astro
│   │   ├── about.astro
│   │   ├── history.astro
│   │   ├── visit.astro
│   │   └── contact.astro
│   ├── content/
│   │   ├── vendors/
│   │   │   └── *.md
│   │   ├── businesses/
│   │   │   └── *.md
│   │   └── recipes/
│   │       └── *.md
│   ├── data/
│   │   ├── vendors.json          # Quick vendor list for filtering
│   │   ├── businesses.json       # Village business directory
│   │   ├── seasonal-produce.json # What's in season when
│   │   ├── events.json           # Upcoming events
│   │   └── site-config.json      # Market hours, dates, contact info
│   ├── styles/
│   │   └── global.css
│   └── assets/
│       ├── images/
│       │   ├── vendors/
│       │   ├── businesses/
│       │   ├── recipes/
│       │   └── decorative/       # Botanical illustrations, etc.
│       └── fonts/
├── public/
│   ├── favicon.svg
│   └── og-image.png
├── astro.config.mjs
├── tailwind.config.mjs
├── package.json
└── README.md
```

---

## Content Schemas

### Vendor (src/content/vendors/*.md)

```markdown
---
name: "Samascott Orchards"
slug: "samascott-orchards"
tagline: "Family-owned since 1821"
image: "/images/vendors/samascott.jpg"
categories:
  - produce
  - fruit
  - cider
description: "Six generations of family farming..."
website: "https://samascottorchards.com"
instagram: "@samascottorchards"
facebook: ""
featured: true
active: true
---

Extended description and story goes here in markdown...
```

### Business (src/content/businesses/*.md)

```markdown
---
name: "Carolina House"
slug: "carolina-house"
type: "restaurant"
tagline: "Farm-to-table dining"
image: "/images/businesses/carolina-house.jpg"
address: "59 Broad Street, Kinderhook, NY"
phone: "(518) 758-1669"
website: ""
hours: "Thu-Sun, 5pm-9pm"
description: "Historic inn with seasonal menu..."
mapLocation:
  lat: 42.3951
  lng: -73.6982
---
```

### Recipe (src/content/recipes/*.md)

```markdown
---
title: "Summer Squash Ribbon Salad"
slug: "summer-squash-ribbon-salad"
image: "/images/recipes/squash-salad.jpg"
prepTime: "15 minutes"
cookTime: "0 minutes"
servings: 4
season:
  - summer
produce:
  - zucchini
  - yellow squash
  - cherry tomatoes
contributor: "Maria's Kitchen"
contributorLink: ""
difficulty: "easy"
tags:
  - vegetarian
  - no-cook
  - quick
---

## Ingredients

- 2 medium zucchini
- 2 medium yellow squash
...

## Instructions

1. Using a vegetable peeler...
```

### Seasonal Produce (src/data/seasonal-produce.json)

```json
{
  "seasons": {
    "spring": {
      "months": ["May", "June"],
      "produce": [
        { "name": "Asparagus", "icon": "🌱", "peak": true },
        { "name": "Rhubarb", "icon": "🌿", "peak": true },
        { "name": "Spring Greens", "icon": "🥬", "peak": true },
        { "name": "Radishes", "icon": "🔴", "peak": false }
      ]
    },
    "summer": {
      "months": ["July", "August"],
      "produce": [
        { "name": "Tomatoes", "icon": "🍅", "peak": true },
        { "name": "Sweet Corn", "icon": "🌽", "peak": true },
        { "name": "Berries", "icon": "🍓", "peak": true },
        { "name": "Zucchini", "icon": "🥒", "peak": true }
      ]
    },
    "fall": {
      "months": ["September", "October"],
      "produce": [
        { "name": "Apples", "icon": "🍎", "peak": true },
        { "name": "Pumpkins", "icon": "🎃", "peak": true },
        { "name": "Winter Squash", "icon": "🥜", "peak": true },
        { "name": "Brussels Sprouts", "icon": "🥬", "peak": false }
      ]
    }
  }
}
```

### Site Config (src/data/site-config.json)

```json
{
  "marketName": "Kinderhook Farmers' Market",
  "tagline": "It's OK!",
  "season": {
    "start": "2026-05-09",
    "end": "2026-10-10"
  },
  "schedule": {
    "day": "Saturday",
    "startTime": "9:00 AM",
    "endTime": "1:00 PM"
  },
  "location": {
    "name": "Village Green",
    "address": "Broad Street, Kinderhook, NY 12106",
    "coordinates": {
      "lat": 42.3951,
      "lng": -73.6982
    }
  },
  "contact": {
    "email": "info@kinderhookfarmersmarket.com",
    "facebook": "https://www.facebook.com/KinderhookFarmersMarket"
  },
  "sponsor": "Kinderhook Business and Professional Association"
}
```

---

## Key Features to Implement

### Phase 1: Core Site (MVP)

1. **Homepage**
   - Hero with market countdown ("Next Market: Saturday in 3 days!")
   - Featured vendors carousel
   - What's fresh this week preview
   - Upcoming events
   - Quick links to visit info

2. **Vendor Directory**
   - Grid of vendor cards with photos
   - Filter by category (produce, baked goods, crafts, etc.)
   - Search functionality
   - Individual vendor pages with full details

3. **Visit Page**
   - Location map (use Leaflet, not Google Maps - free!)
   - Parking information
   - Accessibility info
   - What to bring (bags, cash, etc.)
   - Nearby things to do

4. **About & History**
   - Market story
   - "Old Kinderhook" / Van Buren history
   - Dutch heritage of the region
   - KBPA sponsor info

5. **Contact**
   - Contact form (Netlify Forms)
   - Social links
   - Vendor application info

### Phase 2: Enhanced Features

6. **Village Business Directory**
   - Permanent local businesses beyond the market
   - Interactive map
   - Categories and filtering
   - Supports "shop local" mission

7. **What's Fresh / Seasonal Guide**
   - Interactive seasonal produce wheel
   - Links to relevant recipes
   - Tips for selecting/storing produce

8. **Recipes**
   - Community recipe collection
   - Filter by season, produce type, difficulty
   - Submission form for community contributions

### Phase 3: Future Possibilities

9. **Events Calendar**
   - Special markets, festivals, live music
   - iCal export

10. **Newsletter Integration**
    - Email signup
    - Mailchimp or similar integration

11. **Local Currency Tie-in**
    - Your wife's heritage currency project!
    - "Accepted here" badges for businesses

12. **QR Scavenger Hunt**
    - Historical locations integration
    - Digital passport/rewards

---

## Coding Standards

### General

- Use semantic HTML5 elements
- Ensure WCAG 2.1 AA accessibility compliance
- Mobile-first responsive design
- Optimize all images (WebP with fallbacks)
- Aim for 95+ Lighthouse scores

### Astro/Components

- Keep components small and focused
- Use TypeScript for type safety in data files
- Props should be clearly typed
- Use Astro's built-in image optimization

### CSS/Tailwind

- Use design tokens from the design system
- Extract repeated patterns to @apply classes
- Keep utility classes readable (break long lists)
- Use CSS custom properties for theming

### Content

- All user-editable content in /content or /data
- Use frontmatter for metadata
- Keep markdown simple and accessible
- Include alt text for all images

### Git

- Conventional commits (feat:, fix:, docs:, etc.)
- Feature branches off main
- Clear PR descriptions

---

## Accessibility Requirements

- Skip navigation link
- Proper heading hierarchy (h1 -> h2 -> h3)
- Alt text on all images
- Sufficient color contrast (check orange on white!)
- Keyboard navigable
- Focus indicators
- Reduced motion support
- Screen reader testing

---

## Performance Targets

- First Contentful Paint: < 1.5s
- Largest Contentful Paint: < 2.5s
- Cumulative Layout Shift: < 0.1
- Time to Interactive: < 3.5s
- Total bundle size: < 100kb JS

---

## Local Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Deployment

- **Production:** Netlify auto-deploy from `main` branch
- **Preview:** Netlify deploy previews for PRs
- **Domain:** kinderhookfarmersmarket.com (transfer from current host)

---

## Content Update Guide (For Coordinator)

### Adding a New Vendor

1. Create new file: `src/content/vendors/vendor-name.md`
2. Copy template from existing vendor
3. Fill in details, add image to `/src/assets/images/vendors/`
4. Commit and push (or edit directly in GitHub)

### Updating Market Info

1. Edit `src/data/site-config.json`
2. Update dates, times, or contact info
3. Commit and push

### Adding a Recipe

1. Create new file: `src/content/recipes/recipe-name.md`
2. Follow the recipe template format
3. Add image, commit, push

---

## Resources

- [Astro Docs](https://docs.astro.build)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Leaflet Maps](https://leafletjs.com/)
- [Netlify Forms](https://docs.netlify.com/forms/setup/)

---

## Notes

- The "It's OK!" tagline comes from Martin Van Buren's nickname "Old Kinderhook" - this became "OK" during his presidential campaign, possibly the origin of the word "okay"!
- Consider future integration with David's local currency project and QR historical scavenger hunt
- The site should feel warm, welcoming, and deeply connected to community - not corporate or generic
