import { gnatureProducts } from './products-gnature';
import { sircaProducts } from './products-sirca';

export type CalcPack = { volume: string; liters: number; price: number };

export type CalcMaterial = {
  id: string;
  brand: 'G Nature' | 'Sirca';
  sku: string;
  name: string;
  href: string;
  kind: 'coverage' | 'wet';
  coverage1?: number;
  coverage2?: number;
  wetGsm?: number;
  density?: number;
  packs: CalcPack[];
};

function packsOf(packs: Array<{ volume: string; liters: number; price: number }>): CalcPack[] {
  return packs.map((p) => ({ volume: p.volume, liters: p.liters, price: p.price }));
}

export const calcMaterials: CalcMaterial[] = [
  ...gnatureProducts
    .filter((p) => p.coverage1)
    .map(
      (p): CalcMaterial => ({
        id: `gn-${p.slug}`,
        brand: 'G Nature',
        sku: p.sku,
        name: p.name,
        href: `/product/gnature/${p.slug}`,
        kind: 'coverage',
        coverage1: p.coverage1,
        coverage2: p.coverage2 ?? p.coverage1,
        packs: packsOf(p.packs),
      }),
    ),
  ...sircaProducts
    .filter((p) => ['exterior', 'windows', 'oils', 'parquet'].includes(p.use))
    .map(
      (p): CalcMaterial => ({
        id: `sirca-${p.slug}`,
        brand: 'Sirca',
        sku: p.sku,
        name: p.name,
        href: `/product/sirca/${p.slug}`,
        kind: 'wet',
        wetGsm: 125,
        density: 1.05,
        packs: packsOf(p.packs),
      }),
    ),
];

export const calcPrimers = [
  { id: 'none', label: 'Без грунта', sku: '', coverage: 0 },
  { id: '870', label: '870 грунт-масло', sku: '870', coverage: 12 },
  { id: '875', label: '875 антисептик', sku: '875', coverage: 10 },
];

export const houseZones = [
  {
    id: 'fasad',
    label: 'Фасад, м²',
    unit: 'м²',
    finish: '280',
    primer: '870',
    coats: 2,
    areaFactor: 1,
  },
  {
    id: 'torcy',
    label: 'Торцы, м.п. (грань ~200 мм)',
    unit: 'м.п.',
    finish: '860',
    primer: '870',
    coats: 2,
    areaFactor: 0.2,
  },
  {
    id: 'terrassa',
    label: 'Терраса, м²',
    unit: 'м²',
    finish: '277',
    primer: '875',
    coats: 2,
    areaFactor: 1,
  },
  {
    id: 'steny',
    label: 'Стены внутри, м²',
    unit: 'м²',
    finish: '245',
    primer: '',
    coats: 2,
    areaFactor: 1,
  },
  {
    id: 'pol',
    label: 'Пол, м²',
    unit: 'м²',
    finish: '255',
    primer: '',
    coats: 2,
    areaFactor: 1,
  },
] as const;

export function gnMaterialBySku(sku: string): CalcMaterial | undefined {
  return calcMaterials.find((m) => m.brand === 'G Nature' && m.sku === sku);
}
