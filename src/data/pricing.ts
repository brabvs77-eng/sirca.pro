/** Округление до 10 ₽. */
export function round10(value: number): number {
  return Math.round(value / 10) * 10;
}

/** Наша цена: ≈ −10% к открытой витрине конкурента. */
export function belowMarket(market: number): number {
  return round10(market * 0.9);
}

export function formatRub(value: number): string {
  return `${new Intl.NumberFormat('ru-RU').format(value)}\u00a0₽`;
}

/**
 * Кривая фасовок G Nature по официальным ценам 245 Hartöl на gnature.ru:
 * 0,375 / 0,75 / 2,5 / 10 л = 2470 / 3840 / 11540 / 44370.
 */
export const GN_PACK_RATIO_FROM_0375 = {
  0.375: 1,
  0.75: 3840 / 2470,
  2.5: 11540 / 2470,
  10: 44370 / 2470,
} as const;

export const GN_PACK_RATIO_FROM_075 = {
  0.75: 1,
  2.5: 11540 / 3840,
  10: 44370 / 3840,
} as const;

export type Pack = {
  volume: string;
  liters: number;
  marketPrice: number;
  price: number;
};

export function gnPacksFrom375(market375: number, liters: number[], source: string): (Pack & { source: string })[] {
  return liters.map((l) => {
    const key = l as keyof typeof GN_PACK_RATIO_FROM_0375;
    const market = round10(market375 * GN_PACK_RATIO_FROM_0375[key]);
    return {
      volume: formatVolume(l),
      liters: l,
      marketPrice: market,
      price: belowMarket(market),
      source,
    };
  });
}

export function gnPacksFrom075(market075: number, liters: number[], source: string): (Pack & { source: string })[] {
  return liters.map((l) => {
    const key = l as keyof typeof GN_PACK_RATIO_FROM_075;
    const market = round10(market075 * GN_PACK_RATIO_FROM_075[key]);
    return {
      volume: formatVolume(l),
      liters: l,
      marketPrice: market,
      price: belowMarket(market),
      source,
    };
  });
}

export function singlePack(liters: number, market: number, source: string): (Pack & { source: string })[] {
  return [
    {
      volume: formatVolume(liters),
      liters,
      marketPrice: market,
      price: belowMarket(market),
      source,
    },
  ];
}

function formatVolume(liters: number): string {
  if (liters < 1) return `${String(liters).replace('.', ',')} л`;
  return `${String(liters).replace('.', ',')} л`;
}
