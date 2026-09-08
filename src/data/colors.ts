export type Colorway = {
  n: string;
  slug: string;
  name: string;
  img: string;
  collection: 'vokrug-cveta' | 'prosto-kosmos';
};

export const vokrugCveta: Colorway[] = [
  { n: '01', slug: 'arkticheskij-led', name: 'Арктический лёд', img: '/img/colors/vc-01.webp', collection: 'vokrug-cveta' },
  { n: '02', slug: 'kitajskij-farfor', name: 'Китайский фарфор', img: '/img/colors/vc-02.webp', collection: 'vokrug-cveta' },
  { n: '03', slug: 'belgijskie-slivki', name: 'Бельгийские сливки', img: '/img/colors/vc-03.webp', collection: 'vokrug-cveta' },
  { n: '04', slug: 'vetnamskij-lotos', name: 'Вьетнамский лотос', img: '/img/colors/vc-04.webp', collection: 'vokrug-cveta' },
  { n: '05', slug: 'tureckaya-halva', name: 'Турецкая халва', img: '/img/colors/vc-05.webp', collection: 'vokrug-cveta' },
  { n: '06', slug: 'italyanskij-latte', name: 'Итальянский латте', img: '/img/colors/vc-06.webp', collection: 'vokrug-cveta' },
  { n: '07', slug: 'efiopskij-kofe', name: 'Эфиопский кофе', img: '/img/colors/vc-07.webp', collection: 'vokrug-cveta' },
  { n: '08', slug: 'shvejcarskij-shokolad', name: 'Швейцарский шоколад', img: '/img/colors/vc-08.webp', collection: 'vokrug-cveta' },
  { n: '09', slug: 'francuzskoe-krem-bryule', name: 'Французское крем-брюле', img: '/img/colors/vc-09.webp', collection: 'vokrug-cveta' },
  { n: '10', slug: 'tibetskoe-plato', name: 'Тибетское плато', img: '/img/colors/vc-10.webp', collection: 'vokrug-cveta' },
  { n: '11', slug: 'avstrijskie-alpy', name: 'Австрийские Альпы', img: '/img/colors/vc-11.webp', collection: 'vokrug-cveta' },
  { n: '12', slug: 'shotlandskij-veresk', name: 'Шотландский вереск', img: '/img/colors/vc-12.webp', collection: 'vokrug-cveta' },
  { n: '13', slug: 'tumannyj-albion', name: 'Туманный Альбион', img: '/img/colors/vc-13.webp', collection: 'vokrug-cveta' },
  { n: '14', slug: 'sibirskaya-tajga', name: 'Сибирская тайга', img: '/img/colors/vc-14.webp', collection: 'vokrug-cveta' },
  { n: '15', slug: 'kalifornijskij-zaliv', name: 'Калифорнийский залив', img: '/img/colors/vc-15.webp', collection: 'vokrug-cveta' },
  { n: '16', slug: 'markkanskaya-glina', name: 'Маркканская глина', img: '/img/colors/vc-16.webp', collection: 'vokrug-cveta' },
  { n: '17', slug: 'indijskij-chaj', name: 'Индийский чай', img: '/img/colors/vc-17.webp', collection: 'vokrug-cveta' },
  { n: '18', slug: 'meksikanskij-kaktus', name: 'Мексиканский кактус', img: '/img/colors/vc-18.webp', collection: 'vokrug-cveta' },
  { n: '19', slug: 'novozelandskij-moh', name: 'Новозеландский мох', img: '/img/colors/vc-19.webp', collection: 'vokrug-cveta' },
  { n: '20', slug: 'livanskij-kedr', name: 'Ливанский кедр', img: '/img/colors/vc-20.webp', collection: 'vokrug-cveta' },
];

export const prostoKosmos: Colorway[] = [
  { n: '01', slug: 'kosmicheskij-rassvet', name: 'Космический рассвет', img: '/img/colors/pk-01.webp', collection: 'prosto-kosmos' },
  { n: '10', slug: 'serebro-saturna', name: 'Серебро Сатурна', img: '/img/colors/pk-10.webp', collection: 'prosto-kosmos' },
  { n: '11', slug: 'asteroidnyj-seryj', name: 'Астероидный серый', img: '/img/colors/pk-11.webp', collection: 'prosto-kosmos' },
  { n: '12', slug: 'marsianskij-zakat', name: 'Марсианский закат', img: '/img/colors/pk-12.webp', collection: 'prosto-kosmos' },
  { n: '13', slug: 'zvezdnyj-svet', name: 'Звёздный свет', img: '/img/colors/pk-13.webp', collection: 'prosto-kosmos' },
  { n: '14', slug: 'eho-vselennoj', name: 'Эхо вселенной', img: '/img/colors/pk-14.webp', collection: 'prosto-kosmos' },
  { n: '15', slug: 'otkrytyj-kosmos', name: 'Открытый космос', img: '/img/colors/pk-15.webp', collection: 'prosto-kosmos' },
  { n: '16', slug: 'mlechnyj-put', name: 'Млечный путь', img: '/img/colors/pk-16.webp', collection: 'prosto-kosmos' },
];

export const allColors = [...vokrugCveta, ...prostoKosmos];

export function colorBySlug(slug: string): Colorway | undefined {
  return allColors.find((c) => c.slug === slug);
}
