import type { SircaProduct } from './products-sirca';

export type SircaFamily = {
  id: string;
  label: string;
  href?: string;
};

const FAMILIES: Array<SircaFamily & { test: (sku: string) => boolean }> = [
  { id: 'imw', label: 'Пропитки IMW / IWJ', href: '/sirca/exterior-water', test: (s) => /^(IMW|IWJ)/.test(s) },
  { id: 'iwc', label: 'Лазури IWC', href: '/sirca/oils', test: (s) => /^IWC/.test(s) },
  { id: 'fiw', label: 'Грунты FIW', href: '/sirca/exterior-water', test: (s) => /^FIW|^FWBP/.test(s) },
  { id: 'fwe', label: 'Эмали FWE', href: '/sirca/exterior-water', test: (s) => /^FWE/.test(s) },
  { id: 'fwp', label: 'Грунт-эмали FWP', href: '/sirca/exterior-water', test: (s) => /^FWP\d/.test(s) },
  { id: 'owe', label: 'Финиши OWE / OWP / WOP', href: '/sirca/exterior-water', test: (s) => /^OWE|^OWP|^WOP/.test(s) },
  { id: 'siw', label: 'Герметики SIW', href: '/sirca/exterior-water', test: (s) => /^SIW/.test(s) },
  {
    id: 'parquet-water',
    label: 'Паркет водный',
    href: '/sirca/parquet',
    test: (s) => /^(FWPI|IDROFLOOR|SPORTFLOOR|OWB)/.test(s) || (/^OW/.test(s) && !/^OWE|^OWP|^OWPI/.test(s)),
  },
  {
    id: 'furniture-water',
    label: 'Мебель водная',
    href: '/sirca/furniture-water',
    test: (s) =>
      /^(OWPI|SO-|CRW)/.test(s) || (/^FW/.test(s) && !/^(FWP|FWE|FIW|FWPI|FWBP)/.test(s)),
  },
  { id: 'oil', label: 'Масла OIL', href: '/sirca/oils', test: (s) => /^OIL/.test(s) },
  { id: 'pu-ext', label: 'ПУ экстерьер', href: '/sirca/exterior-pu', test: (s) => /^(OPU99|OPP19|FPU16)/.test(s) },
  { id: 'acrylic', label: 'Акрил', href: '/sirca/exterior-acrylic', test: (s) => /^(OPA|FA|FPU93)/.test(s) },
  {
    id: 'furniture-pu',
    label: 'Мебель ПУ / полиэфир',
    href: '/sirca/furniture-pu',
    test: (s) => /^(OPU|OPP05|FPP|FPU|FL|LPU|TH)/.test(s) && !/^(OPU99|OPP19|FPU16|FPU93|OPU60|OPU379)/.test(s),
  },
];

export function sircaFamilyOf(product: SircaProduct): SircaFamily {
  const sku = product.sku.toUpperCase();
  for (const fam of FAMILIES) {
    if (fam.test(sku)) return { id: fam.id, label: fam.label, href: fam.href };
  }
  return { id: 'other', label: 'Прочее' };
}

export function groupSircaProducts(products: SircaProduct[]): Array<SircaFamily & { items: SircaProduct[] }> {
  const buckets = new Map<string, SircaFamily & { items: SircaProduct[] }>();

  for (const product of products) {
    const fam = sircaFamilyOf(product);
    const key = fam.id;
    if (!buckets.has(key)) buckets.set(key, { ...fam, items: [] });
    buckets.get(key)!.items.push(product);
  }

  const order = FAMILIES.map((f) => f.id);
  return [...buckets.values()].sort((a, b) => {
    const ai = order.indexOf(a.id);
    const bi = order.indexOf(b.id);
    return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
  });
}

export function productsInFamily(products: SircaProduct[], familyId: string): SircaProduct[] {
  return products.filter((p) => sircaFamilyOf(p).id === familyId);
}
