import { gnatureProducts, gnFromPrice, type GnProduct } from './products-gnature';
import { sircaProducts, sircaFromPrice, type SircaProduct } from './products-sirca';

export type AnyProduct = GnProduct | SircaProduct;

export function productHref(product: AnyProduct): string {
  return product.brand === 'gnature'
    ? `/product/gnature/${product.slug}`
    : `/product/sirca/${product.slug}`;
}

export function productFromPrice(product: AnyProduct): number {
  return product.brand === 'gnature' ? gnFromPrice(product) : sircaFromPrice(product);
}

export function productsForTask(slug: string): AnyProduct[] {
  return [...gnatureProducts, ...sircaProducts].filter((p) => p.tasks.includes(slug));
}

export function brandLabel(brand: 'gnature' | 'sirca'): string {
  return brand === 'gnature' ? 'G Nature' : 'Sirca';
}

export const calcProducts = [
  ...gnatureProducts
    .filter((p) => p.coverage1)
    .map((p) => ({
      id: `gn-${p.slug}`,
      brand: 'G Nature' as const,
      sku: p.sku,
      name: p.name,
      coverage1: p.coverage1!,
      coverage2: p.coverage2,
      packs: p.packs,
    })),
];
