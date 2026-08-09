import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://marinkoco.github.io',
  base: '/cock-tail/',
  integrations: [tailwind()],
});
