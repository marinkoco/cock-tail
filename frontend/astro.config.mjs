import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://marinkoco.github.io',
  base: process.env.ASTRO_BASE ?? '/cock-tail/',
  integrations: [tailwind()],
});
