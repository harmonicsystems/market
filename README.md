# Kinderhook Farmers' Market

Website for the [Kinderhook Farmers' Market](https://harmonicsystems.github.io/market/) in Kinderhook, NY — Saturdays 8:30 AM – 12:30 PM on the Village Green, May through October.

Built as a community resource and village economic development hub, covering vendors, KBPA member businesses, historic landmarks, seasonal produce, and community recipes.

## Tech stack

- **[Astro 5](https://astro.build)** — static site generation
- **[Tailwind CSS 4](https://tailwindcss.com)** — styling
- **Content Collections** with Zod schemas — typed Markdown for vendors, businesses, landmarks, and recipes
- **GitHub Pages** — hosted via GitHub Actions on every push to `main`

## Local development

```sh
npm install
npm run dev
```

Site runs at `http://localhost:4321/market/`.

| Command | Action |
| :-- | :-- |
| `npm run dev` | Start the local dev server |
| `npm run build` | Build the production site to `./dist/` |
| `npm run preview` | Preview the production build locally |

## Project layout

```
src/
├── components/       Astro components (SEO, structured data, icons, hero blocks)
├── content/          Markdown content collections — vendors, businesses, landmarks, recipes
├── data/             JSON data (site config, this week's lineup)
├── layouts/          BaseLayout with nav, footer, SEO
└── pages/            Route files (one .astro per route)

public/               Static assets (icons, images, favicon)
```

## Updating content

Content lives in `src/content/` and `src/data/` — no code changes needed.

- **This week's market:** edit `src/data/this-week.json`
- **Add a vendor:** create `src/content/vendors/vendor-name.md`
- **Add a business:** create `src/content/businesses/business-name.md`
- **Add a landmark:** create `src/content/landmarks/landmark-name.md`
- **Add a recipe:** create `src/content/recipes/recipe-name.md`

Zod schemas in `src/content.config.ts` validate each collection's frontmatter.

## Deployment

Any push to `main` triggers `.github/workflows/deploy.yml`, which builds with Astro and publishes to GitHub Pages. The base path is `/market` (configured in `astro.config.mjs`).

## Credits

- Designed by [Susanne Lamb](https://susannelamb.com) — hand-drawn icons, dividers, sunflower banner, and signature
- Built and maintained by [Harmonic Systems](https://github.com/harmonicsystems)

## License

MIT — see [LICENSE](./LICENSE).
