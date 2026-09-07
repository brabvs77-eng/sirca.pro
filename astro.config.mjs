import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://sirca.pro',
  trailingSlash: 'never',
  compressHTML: true,
  build: {
    inlineStylesheets: 'always',
  },
});
