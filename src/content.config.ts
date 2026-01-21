import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const vendors = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/vendors' }),
  schema: z.object({
    name: z.string(),
    slug: z.string(),
    tagline: z.string(),
    categories: z.array(z.string()),
    description: z.string(),
    website: z.string().optional(),
    instagram: z.string().optional(),
    facebook: z.string().optional(),
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
    tagline: z.string().optional(),
    address: z.string(),
    phone: z.string().optional(),
    website: z.string().optional(),
    hours: z.string().optional(),
    description: z.string(),
  }),
});

const recipes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/recipes' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    prepTime: z.string().optional(),
    cookTime: z.string().optional(),
    servings: z.number().optional(),
    season: z.array(z.string()).optional(),
    produce: z.array(z.string()).optional(),
    contributor: z.string().optional(),
    difficulty: z.enum(['easy', 'medium', 'hard']).optional(),
    tags: z.array(z.string()).optional(),
  }),
});

export const collections = { vendors, businesses, recipes };
