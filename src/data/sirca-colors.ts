/** Палитра Colour Passion IMW4800 и масла IR17xx — из sources/sirca/specs/палитра пропиток.jpg */

export type SircaSwatch = {
  sku: string;
  name: string;
  hex?: string;
};

export const imw4800Swatches: SircaSwatch[] = [
  { sku: 'IMW4830', name: 'Бесцветный', hex: '#c8a66a' },
  { sku: 'IMW4835', name: 'Белый', hex: '#e8e4d8' },
  { sku: 'IMW4836', name: 'Светлый махагон', hex: '#b88858' },
  { sku: 'IMW4824', name: 'Сосна Дугласа', hex: '#d48838' },
  { sku: 'IMW4820', name: 'Лиственница', hex: '#c9a040' },
  { sku: 'IMW4815', name: 'Дуб', hex: '#a87840' },
  { sku: 'IMW4811', name: 'Тик', hex: '#9a7040' },
  { sku: 'IMW4816', name: 'Каштан', hex: '#7a5030' },
  { sku: 'IMW4822', name: 'Орех тёмный', hex: '#6a4028' },
  { sku: 'IMW4812', name: 'Ольха', hex: '#8a5840' },
  { sku: 'IMW4813', name: 'Орех тёмный', hex: '#5a3820' },
  { sku: 'IMW4821', name: 'Орех красный', hex: '#6a3020' },
  { sku: 'IMW4814', name: 'Чёрное дерево', hex: '#2a2018' },
  { sku: 'IMW4823', name: 'Зелёный', hex: '#2a4028' },
];

export const ir17OilSwatches: SircaSwatch[] = [
  { sku: 'IR17', name: 'Белый', hex: '#f0ece4' },
  { sku: 'IR17', name: 'Белёный дуб', hex: '#d8d4c8' },
  { sku: 'IR17', name: 'Песочный', hex: '#d0b888' },
  { sku: 'IR17', name: 'Дымчатый', hex: '#a8a8a0' },
  { sku: 'IR17', name: 'Серый', hex: '#808078' },
  { sku: 'IR17', name: 'Венге', hex: '#3a2820' },
  { sku: 'IR17', name: 'Дуб античный', hex: '#6a5848' },
  { sku: 'IR17', name: 'Сине-зелёный', hex: '#2a3838' },
  { sku: 'IR17', name: 'Орех', hex: '#7a5030' },
  { sku: 'IR17', name: 'Тик', hex: '#b08040' },
  { sku: 'IR17', name: 'Рябина', hex: '#8a4830' },
  { sku: 'IR17', name: 'Каштан', hex: '#6a3820' },
  { sku: 'IR17', name: 'Мербау', hex: '#4a2818' },
  { sku: 'IR17', name: 'Махагон', hex: '#3a2018' },
  { sku: 'IR17', name: 'Эбен', hex: '#1a1818' },
];

export const sircaPaletteImage = '/img/sirca/palette-imw4800.jpg';
