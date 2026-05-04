import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Treat empty strings as absent — allows gradual content population
const optionalString = z.string().transform(v => v || undefined).optional();
const optionalUrl = z.string().url().or(z.literal('')).transform(v => v || undefined).optional();

const vendors = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/vendors' }),
  schema: z.object({
    name: z.string(),
    slug: z.string(),
    tagline: optionalString,
    categories: z.array(z.string()).default([]),
    description: optionalString,
    image: optionalString,
    website: optionalUrl,
    instagram: optionalString,
    facebook: optionalUrl,
    featured: z.boolean().default(false),
    active: z.boolean().default(true),
    vendorType: z.enum(['regular', 'guest']).default('regular'),
  }),
});

const businesses = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/businesses' }),
  schema: z.object({
    name: z.string(),
    slug: z.string(),
    type: z.string(),
    tagline: optionalString,
    image: optionalString,
    address: z.string(),
    phone: optionalString,
    website: optionalUrl,
    hours: optionalString,
    description: optionalString,
  }),
});

const recipes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/recipes' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    emoji: optionalString,
    image: optionalString,
    prepTime: optionalString,
    cookTime: optionalString,
    servings: z.number().optional(),
    season: z.array(z.string()).optional(),
    produce: z.array(z.string()).optional(),
    contributor: optionalString,
    contributorLink: optionalUrl,
    difficulty: z.enum(['easy', 'medium', 'hard']).optional(),
    tags: z.array(z.string()).optional(),
  }),
});

const landmarks = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/landmarks' }),
  schema: z.object({
    name: z.string(),
    slug: z.string(),
    type: z.enum(['historic-site', 'museum', 'gallery', 'trail', 'neighborhood']),
    tagline: optionalString,
    image: optionalString,
    address: optionalString,
    phone: optionalString,
    website: optionalUrl,
    hours: optionalString,
    admission: optionalString,
    description: optionalString,
    featured: z.boolean().default(false),
    coordinates: z.object({
      lat: z.number(),
      lng: z.number(),
    }).optional(),
  }),
});

const events = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/events' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    host: z.string(),
    hostLink: optionalUrl,
    date: z.string(),           // ISO date, e.g. 2026-05-30
    endDate: optionalString,    // optional for multi-day runs
    time: optionalString,       // e.g. "6–8 PM"
    location: optionalString,   // e.g. "The School"
    address: optionalString,    // e.g. "25 Broad Street, Kinderhook, NY"
    link: optionalUrl,
    image: optionalString,
    category: z.enum(['art', 'library', 'music', 'community', 'food', 'other']).default('other'),
    description: optionalString,
    featured: z.boolean().default(false),
  }),
});

// Weeks — one entry per Saturday market in the season. The homepage selects
// the next upcoming week (date >= today in America/New_York), and the
// /share/[week] route generates one image-ready page per entry. File names
// must match the date field (YYYY-MM-DD.md). All per-week fields are
// optional — empty stubs are fine and just render the date + base info.
const weeks = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/weeks' }),
  schema: z.object({
    date: z.string(),                                    // ISO Saturday, e.g. 2026-05-09
    theme: optionalString,                               // e.g. "Opening Day"
    note: optionalString,                                // e.g. "Rain or Shine"
    music: z.object({                                    // optional override; default lookup is music-schedule.json
      name: z.string(),
      time: z.string(),
    }).optional(),
    specialEvents: z.array(z.object({
      name: z.string(),
      time: optionalString,
      description: optionalString,
    })).default([]),
    guestVendors: z.array(z.string()).default([]),
    communityPartners: z.array(z.string()).default([]),
    regularVendors: z.array(z.string()).default([]),     // override; empty = use weekly-vendors.json roster
  }),
});

// Performers — music acts that play the market. Each entity gets a durable
// profile page at /performers/[slug] that auto-aggregates appearances from
// the season schedule, plus optional streaming / tip-jar / contact links.
const performers = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/performers' }),
  schema: z.object({
    name: z.string(),
    slug: z.string(),
    genre: optionalString,           // e.g. "Bluegrass / Old-time"
    image: optionalString,           // optional press photo
    website: optionalUrl,
    instagram: optionalString,       // handle or full URL
    facebook: optionalUrl,
    youtube: optionalUrl,
    spotify: optionalUrl,
    bandcamp: optionalUrl,
    soundcloud: optionalUrl,
    appleMusic: optionalUrl,
    tipJar: optionalUrl,             // Venmo / PayPal / Buy Me a Coffee
    email: optionalString,
    active: z.boolean().default(true),
  }),
});

export const collections = { vendors, businesses, recipes, landmarks, events, performers, weeks };
