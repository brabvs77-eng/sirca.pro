export const covers = {
  gn: '/img/covers/gn-hero.webp',
  sirca: '/img/covers/sirca.webp',
  family: '/img/covers/family.webp',
  house: '/img/life/house.webp',
};

const gnPacks: Record<string, string> = {
  '110': '/img/products/110.webp',
  '120': '/img/products/120.webp',
  '140': '/img/products/140.webp',
  '170': '/img/products/170.webp',
  '227': '/img/products/227.webp',
  '245': '/img/products/245.webp',
  '255': '/img/products/255.webp',
  '266': '/img/products/266.webp',
  '271': '/img/products/271.webp',
  '277': '/img/products/277.webp',
  '280': '/img/products/280.webp',
  '285': '/img/products/285.webp',
  '290': '/img/products/290.webp',
  '425': '/img/products/425.webp',
  '460': '/img/products/460.webp',
  '461': '/img/products/461.webp',
  '475': '/img/products/475.webp',
  '476': '/img/products/476.webp',
  '860': '/img/products/860.webp',
  '870': '/img/products/870.webp',
  '875': '/img/products/875.webp',
  'brush-50': '/img/tools/kist-50.webp',
  'brush-70': '/img/tools/kist-70.webp',
  'brush-100': '/img/tools/kist-100.webp',
};

const gnLife: Record<string, string> = {
  '227': '/img/life/227.webp',
  '245': '/img/life/245.webp',
  '255': '/img/life/255.webp',
  '266': '/img/life/266.webp',
  '280': '/img/life/280.webp',
  '285': '/img/life/285.webp',
  '425': '/img/life/425.webp',
  '460': '/img/life/460.webp',
};

const extraPackFiles: Record<string, Array<{ label: string; file: string }>> = {
  '227': [{ label: '0,375 л', file: '227_0375.webp' }],
  '245': [
    { label: '0,375 л', file: '245_0375.webp' },
    { label: '2,5 л', file: '245_2-5.webp' },
    { label: '10 л', file: '245_10.webp' },
  ],
  '255': [
    { label: '0,375 л', file: '255_0375.webp' },
    { label: '2,5 л', file: '255_2-5.webp' },
  ],
  '266': [
    { label: '0,375 л', file: '266_0375.webp' },
    { label: '2,5 л', file: '266_2-5.webp' },
  ],
  '271': [{ label: '2,5 л', file: '271_2-5.webp' }],
  '277': [
    { label: '0,375 л', file: '277_0375.webp' },
    { label: '2,5 л', file: '277_2-5.webp' },
    { label: '10 л', file: '277_10.webp' },
  ],
  '280': [
    { label: '0,375 л', file: '280_0375.webp' },
    { label: '2,5 л', file: '280_2-5.webp' },
    { label: '10 л', file: '280_10.webp' },
  ],
  '285': [
    { label: '0,375 л', file: '285_0375.webp' },
    { label: '2,5 л', file: '285_2-5.webp' },
    { label: '10 л', file: '285_10.webp' },
  ],
  '425': [
    { label: '0,375 л', file: '425_0375.webp' },
    { label: '2,5 л', file: '425_2-5.webp' },
    { label: '10 л', file: '425_10.webp' },
  ],
  '460': [
    { label: '0,375 л', file: '460_0375.webp' },
    { label: '2,5 л', file: '460_2-5.webp' },
    { label: '10 л', file: '460_10.webp' },
  ],
  '461': [
    { label: '0,375 л', file: '461_0375.webp' },
    { label: '2,5 л', file: '461_2-5.webp' },
  ],
  '475': [
    { label: '0,375 л', file: '475_0375.webp' },
    { label: '2,5 л', file: '475_2-5.webp' },
    { label: '10 л', file: '475_10.webp' },
  ],
  '476': [
    { label: '0,375 л', file: '476_0375.webp' },
    { label: '2,5 л', file: '476_2-5.webp' },
    { label: '10 л', file: '476_10.webp' },
  ],
  '860': [{ label: '2,5 л', file: '860_2-5.webp' }],
  '870': [
    { label: '2,5 л', file: '870_2-5.webp' },
    { label: '10 л', file: '870_10.webp' },
  ],
  '875': [
    { label: '2,5 л', file: '875_2-5.webp' },
    { label: '10 л', file: '875_10.webp' },
  ],
};

export type PackShot = { label: string; src: string };

export function gnPackShots(sku: string): PackShot[] {
  const main = gnPacks[sku];
  const shots: PackShot[] = main ? [{ label: '0,75 л', src: main }] : [];
  for (const extra of extraPackFiles[sku] ?? []) {
    shots.push({ label: extra.label, src: `/img/packs/${extra.file}` });
  }
  if (shots.length === 1 && shots[0].label === '0,75 л') {
    shots[0].label = 'Банка';
  }
  return shots;
}

export const brandVideo = {
  gnature: { src: '/video/gnature.mp4', poster: '/img/posters/gnature.webp' },
  fasad: { src: '/video/fasad.mp4', poster: '/img/posters/fasad.webp' },
  terrassa: { src: '/video/terrassa.mp4', poster: '/img/posters/terrassa.webp' },
};

export const gnCatalogReels = [
  { title: 'G Nature', ...brandVideo.gnature },
  { title: 'Фасад', ...brandVideo.fasad },
  { title: 'Терраса', ...brandVideo.terrassa },
  { title: 'Масло 280', src: '/video/280.mp4', poster: '/img/posters/280.webp' },
  { title: 'Масло 277', src: '/video/277.mp4', poster: '/img/posters/277.webp' },
  { title: 'Лазурь 425', src: '/video/425.mp4', poster: '/img/posters/425.webp' },
] as const;

const gnVideo = new Set([
  '110',
  '120',
  '140',
  '170',
  '227',
  '245',
  '255',
  '266',
  '271',
  '277',
  '280',
  '285',
  '425',
  '460',
  '461',
  '860',
  '870',
  '875',
]);

export function gnPackImage(sku: string): string | undefined {
  return gnPacks[sku];
}

export function gnLifeImage(sku: string): string | undefined {
  return gnLife[sku];
}

export function gnVideoSrc(sku: string): string | undefined {
  return gnVideo.has(sku) ? `/video/${sku}.mp4` : undefined;
}

export function gnPoster(sku: string): string | undefined {
  return gnVideo.has(sku) ? `/img/posters/${sku}.webp` : gnPacks[sku];
}

export function sircaCardImage(slug: string): string {
  return `/img/sirca/${slug}.webp`;
}

export const colorRail = [
  { n: '01', name: 'Арктический лёд', hex: '#d9e2e6', img: '/img/colors/vc-01.webp' },
  { n: '02', name: 'Китайский фарфор', hex: '#e8e0d4', img: '/img/colors/vc-02.webp' },
  { n: '03', name: 'Бельгийские сливки', hex: '#c9c2b4', img: '/img/colors/vc-03.webp' },
  { n: '06', name: 'Итальянский латте', hex: '#c9a56b', img: '/img/colors/vc-06.webp' },
  { n: '07', name: 'Эфиопский кофе', hex: '#6e4b2a', img: '/img/colors/vc-07.webp' },
  { n: '08', name: 'Швейцарский шоколад', hex: '#4a2f1c', img: '/img/colors/vc-08.webp' },
  { n: '10', name: 'Тибетское плато', hex: '#8d4a2b', img: '/img/colors/vc-10.webp' },
  { n: '13', name: 'Туманный Альбион', hex: '#3b5d34', img: '/img/colors/vc-13.webp' },
  { n: '18', name: 'Мексиканский кактус', hex: '#2b1d14', img: '/img/colors/vc-18.webp' },
  { n: '20', name: 'Ливанский кедр', hex: '#6e4b2a', img: '/img/colors/vc-20.webp' },
];
