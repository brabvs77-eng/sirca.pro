export type Task = {
  slug: string;
  title: string;
  h1: string;
  lead: string;
  brands: Array<'gnature' | 'sirca'>;
};

export const tasks: Task[] = [
  {
    slug: 'fasad',
    title: 'Фасад',
    h1: 'Масло и краска для деревянного фасада',
    lead: 'Сруб, брус, имитация, планкен. G Nature 280 / 425 / 460 или водная система Sirca IMW. Доставка по Москве и России.',
    brands: ['gnature', 'sirca'],
  },
  {
    slug: 'terrassa',
    title: 'Терраса',
    h1: 'Масло для террасы, лиственницы и ДПК',
    lead: 'Настил, причал, садовая мебель. G Nature 277 для дерева, 271 для ДПК, грунт 870 и защита торцов 860.',
    brands: ['gnature', 'sirca'],
  },
  {
    slug: 'banya',
    title: 'Баня',
    h1: 'Воск и масло для бани и сауны',
    lead: 'Полки и стены парной: жаростойкий воск G Nature 290 до 120 °C. Предбанник и комнаты — твёрдое масло 245.',
    brands: ['gnature'],
  },
  {
    slug: 'pol',
    title: 'Пол',
    h1: 'Масло для деревянного пола и лестницы',
    lead: 'G Nature 245 / 255 / 266 — без плёнки лака, обновление без перешлифовки. Паркетный лак Sirca — если нужен твёрдый слой.',
    brands: ['gnature', 'sirca'],
  },
  {
    slug: 'steny',
    title: 'Стены',
    h1: 'Масло и воск-лазурь для стен и потолков',
    lead: 'Интерьер: 245 Hartöl или водная воск-лазурь 475/476. Колеровка «Вокруг цвета», без запаха после высыхания.',
    brands: ['gnature'],
  },
  {
    slug: 'mebel',
    title: 'Мебель',
    h1: 'Масло для столешницы и мебели',
    lead: 'Столешница и доска — G Nature 227. Мебельный цех — полиуретаны Sirca OPU / OPP с открытой ценой.',
    brands: ['gnature', 'sirca'],
  },
  {
    slug: 'okna-dveri',
    title: 'Окна и двери',
    h1: 'Краска и грунт для деревянных окон и дверей',
    lead: 'Sirca: OWP330, OWE, OPA9330, ПУ-циклы. G Nature — 280 / 425 на уличные двери и ставни.',
    brands: ['sirca', 'gnature'],
  },
  {
    slug: 'parket',
    title: 'Паркет',
    h1: 'Лак и масло для паркета',
    lead: 'Водный OW1fG40 и ПУ OPU60G / OPU379G — Sirca. Масляный пол — G Nature 255 и 266.',
    brands: ['sirca', 'gnature'],
  },
];

export function taskBySlug(slug: string): Task | undefined {
  return tasks.find((t) => t.slug === slug);
}
