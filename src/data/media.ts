const gnPacks: Record<string, string> = {
  '227': '/img/products/227.webp',
  '245': '/img/products/245.webp',
  '255': '/img/products/255.webp',
  '266': '/img/products/266.webp',
  '271': '/img/products/271.webp',
  '277': '/img/products/277.webp',
  '280': '/img/products/280.webp',
  '285': '/img/products/285.webp',
  '425': '/img/products/425.webp',
  '460': '/img/products/460.webp',
  '461': '/img/products/461.webp',
  '475': '/img/products/475.webp',
  '476': '/img/products/476.webp',
  '870': '/img/products/870.webp',
};

export const covers = {
  gn: '/img/covers/gn.webp',
  sirca: '/img/covers/sirca.webp',
  family: '/img/covers/family.webp',
  house: '/img/life/house.webp',
};

export function gnPackImage(sku: string): string | undefined {
  return gnPacks[sku];
}

export const colorRail = [
  { n: '01', name: 'Арктический лёд', hex: '#d9e2e6' },
  { n: '02', name: 'Китайский фарфор', hex: '#e8e0d4' },
  { n: '03', name: 'Бельгийские сливки', hex: '#c9c2b4' },
  { n: '06', name: 'Итальянский латте', hex: '#c9a56b' },
  { n: '07', name: 'Эфиопский кофе', hex: '#6e4b2a' },
  { n: '08', name: 'Швейцарский шоколад', hex: '#4a2f1c' },
  { n: '10', name: 'Тибетское плато', hex: '#8d4a2b' },
  { n: '13', name: 'Хвойный', hex: '#3b5d34' },
  { n: '18', name: 'Венге', hex: '#2b1d14' },
  { n: '20', name: 'Ливанский кедр', hex: '#6e4b2a' },
];
