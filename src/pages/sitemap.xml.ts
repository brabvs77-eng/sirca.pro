import type { APIRoute } from 'astro';
import { company } from '../data/company';
import { gnatureProducts } from '../data/products-gnature';
import { sircaProducts } from '../data/products-sirca';
import { tasks } from '../data/tasks';

export const GET: APIRoute = () => {
  const pages = [
    '/',
    '/gnature',
    '/sirca',
    '/contacts',
    '/requisites',
    '/privacy',
    '/delivery',
    '/b2b',
    '/calc/raskhod',
    '/colors/vokrug-cveta',
    '/colors/prosto-kosmos',
    ...tasks.map((t) => `/tasks/${t.slug}`),
    ...gnatureProducts.map((p) => `/product/gnature/${p.slug}`),
    ...sircaProducts.map((p) => `/product/sirca/${p.slug}`),
  ];

  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages
  .map(
    (path) => `  <url><loc>${company.site}${path === '/' ? '' : path}</loc></url>`
  )
  .join('\n')}
</urlset>`;

  return new Response(body, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
};
