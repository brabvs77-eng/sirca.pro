export type PaintSystem = {
  id: string;
  place: 'exterior' | 'interior';
  object: 'fasad' | 'terrassa' | 'torcy' | 'dpk' | 'steny' | 'pol' | 'mebel' | 'okna';
  wood: 'soft' | 'hard' | 'thermo' | 'dpk' | 'any';
  effect: 'lazur' | 'solid' | 'metal' | 'clear' | 'color';
  title: string;
  result: string;
  steps: string[];
  skus: string[];
};

export const paintSystems: PaintSystem[] = [
  {
    id: 'ext-hard-lazur',
    place: 'exterior',
    object: 'fasad',
    wood: 'hard',
    effect: 'lazur',
    title: 'Фасад, твёрдые породы, лессир',
    result: 'Полупрозрачное покрытие, текстура видна',
    steps: ['Шлифовка P100–120', 'Обеспыливание', '875 антисептик × 1', '280 или 425 × 2–3 слоя'],
    skus: ['875', '280', '425'],
  },
  {
    id: 'ext-hard-solid',
    place: 'exterior',
    object: 'fasad',
    wood: 'hard',
    effect: 'solid',
    title: 'Фасад, твёрдые породы, укрыв',
    result: 'Укрывное покрытие, текстура скрыта',
    steps: ['Шлифовка P100', 'Обеспыливание', '875 антисептик × 1', '460 / 461 × 2–3 слоя'],
    skus: ['875', '460', '461'],
  },
  {
    id: 'ext-soft-lazur',
    place: 'exterior',
    object: 'fasad',
    wood: 'soft',
    effect: 'lazur',
    title: 'Фасад, мягкие породы / термо, лессир',
    result: 'Полупрозрачное покрытие',
    steps: ['Шлифовка P100–120', 'Обеспыливание', '870 грунт-масло × 1', '280 или 425 × 2–3 слоя'],
    skus: ['870', '280', '425'],
  },
  {
    id: 'ext-soft-metal',
    place: 'exterior',
    object: 'fasad',
    wood: 'soft',
    effect: 'metal',
    title: 'Фасад, мягкие породы, металлик',
    result: 'Металлик 285, 2 слоя',
    steps: ['Шлифовка P100–120', 'Обеспыливание', '870 грунт-масло × 1', '285 × 2 слоя'],
    skus: ['870', '285'],
  },
  {
    id: 'ext-soft-solid',
    place: 'exterior',
    object: 'fasad',
    wood: 'soft',
    effect: 'solid',
    title: 'Фасад, мягкие породы, укрыв',
    result: 'Укрывное покрытие',
    steps: ['Шлифовка P100', 'Обеспыливание', '870 грунт-масло × 1', '460 / 461 × 2–3 слоя'],
    skus: ['870', '460', '461'],
  },
  {
    id: 'ext-deck',
    place: 'exterior',
    object: 'terrassa',
    wood: 'any',
    effect: 'lazur',
    title: 'Терраса и садовая мебель',
    result: 'Лессир, текстура видна',
    steps: ['Шлифовка P100', 'Обеспыливание', '875 антисептик × 1', '277 × 2 слоя'],
    skus: ['875', '277'],
  },
  {
    id: 'ext-endgrain',
    place: 'exterior',
    object: 'torcy',
    wood: 'any',
    effect: 'solid',
    title: 'Торцы бревна и доски',
    result: 'Плотная защита торца в цвете',
    steps: ['Шлифовка P100', 'Обеспыливание', '870 грунт-масло × 1', '860 × 2 слоя'],
    skus: ['870', '860'],
  },
  {
    id: 'ext-wpc',
    place: 'exterior',
    object: 'dpk',
    wood: 'dpk',
    effect: 'clear',
    title: 'ДПК и бамбук',
    result: 'Прозрачное шелковистое покрытие',
    steps: ['Очистка 110', 'Полная сушка', '271 × 1 слой'],
    skus: ['110', '271'],
  },
  {
    id: 'int-soft-wax',
    place: 'interior',
    object: 'steny',
    wood: 'soft',
    effect: 'lazur',
    title: 'Стены, мягкие породы, воск-лазурь',
    result: 'Матовое полупрозрачное, быстро сохнет',
    steps: ['Шлифовка P120–150', 'Обеспыливание', '475 / 476 × 2 слоя'],
    skus: ['475', '476'],
  },
  {
    id: 'int-soft-hartol',
    place: 'interior',
    object: 'steny',
    wood: 'soft',
    effect: 'color',
    title: 'Стены, мягкие породы, твёрдое масло',
    result: 'Матовое износоустойчивое',
    steps: ['Шлифовка P120–150', 'Обеспыливание', '245 × 2 слоя или 425 × 2 слоя'],
    skus: ['245', '425'],
  },
  {
    id: 'int-hard-hartol',
    place: 'interior',
    object: 'steny',
    wood: 'hard',
    effect: 'color',
    title: 'Стены, твёрдые породы',
    result: 'Матовое или шелковисто-глянцевое',
    steps: ['Шлифовка P120–150', 'Обеспыливание', '245 × 2 или 425 × 2'],
    skus: ['245', '425'],
  },
  {
    id: 'int-floor-clear',
    place: 'interior',
    object: 'pol',
    wood: 'any',
    effect: 'clear',
    title: 'Пол и лестница, бесцветный',
    result: 'Шелковисто-матовое',
    steps: ['Шлифовка P120', 'Обеспыливание', '255 × 2 или 266 × 2'],
    skus: ['255', '266'],
  },
  {
    id: 'int-floor-color',
    place: 'interior',
    object: 'pol',
    wood: 'any',
    effect: 'color',
    title: 'Пол и лестница, цвет',
    result: 'Цвет + шелковистый финиш',
    steps: ['Шлифовка P120', 'Обеспыливание', '245 × 1–2', '255 или 266 × 1–2'],
    skus: ['245', '255', '266'],
  },
  {
    id: 'int-top',
    place: 'interior',
    object: 'mebel',
    wood: 'any',
    effect: 'clear',
    title: 'Столешница, доска, посуда',
    result: 'Контакт с пищей',
    steps: ['Шлифовка P120–150', 'Обеспыливание', '227 × 2 слоя'],
    skus: ['227'],
  },
  {
    id: 'sirca-windows-water',
    place: 'exterior',
    object: 'okna',
    wood: 'any',
    effect: 'lazur',
    title: 'Окна и двери Sirca, вода',
    result: 'Цикл IMW + грунт + финиш OWE / OWP',
    steps: ['Подготовка по TDS', 'IMW4800 пропитка', 'OWP330 или FIW грунт', 'OWE / FWE финиш'],
    skus: ['imw4800', 'owp330', 'owe500'],
  },
];

export const speciesCoeff = [
  { id: 'planed', label: 'Строганная / шлифованная', coeff: 1 },
  { id: 'sawn', label: 'Пилёная', coeff: 1.25 },
  { id: 'larch', label: 'Лиственница', coeff: 0.95 },
  { id: 'thermo', label: 'Термодревесина', coeff: 0.9 },
  { id: 'wpc', label: 'ДПК', coeff: 0.4 },
];

export const placeLabels = {
  exterior: 'Снаружи',
  interior: 'Внутри',
} as const;

export const objectLabels = {
  fasad: 'Фасад',
  terrassa: 'Терраса',
  torcy: 'Торцы',
  dpk: 'ДПК',
  steny: 'Стены',
  pol: 'Пол',
  mebel: 'Столешница',
  okna: 'Окна',
} as const;

export const woodLabels = {
  soft: 'Мягкие породы',
  hard: 'Твёрдые породы',
  thermo: 'Термо',
  dpk: 'ДПК',
  any: 'Любая',
} as const;

export const effectLabels = {
  lazur: 'Лессир',
  solid: 'Укрыв',
  metal: 'Металлик',
  clear: 'Бесцветный',
  color: 'Цвет',
} as const;

export function systemsForSku(sku: string): PaintSystem[] {
  const key = sku.toLowerCase();
  return paintSystems.filter((s) => s.skus.some((x) => x.toLowerCase() === key));
}
