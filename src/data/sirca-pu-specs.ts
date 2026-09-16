/** Расход и слои ПУ/акрилового блока — из каталога sirca-domostroenie.pdf (нет .doc TDS в репо). */

export type PuSpecHint = { wetGsm: number; coats: number };

export const sircaPuSpecs: Record<string, PuSpecHint> = {
  FPU16TIX: { wetGsm: 130, coats: 1 },
  OPU99G: { wetGsm: 140, coats: 2 },
  OPP1930G: { wetGsm: 150, coats: 2 },
  FPU932E: { wetGsm: 120, coats: 1 },
  OPU979: { wetGsm: 135, coats: 2 },
  OPA9330: { wetGsm: 130, coats: 2 },
  FA930: { wetGsm: 125, coats: 2 },
  OPU60G: { wetGsm: 120, coats: 2 },
  OPU379G: { wetGsm: 125, coats: 2 },
  OPU79: { wetGsm: 130, coats: 2 },
  OPU57: { wetGsm: 125, coats: 2 },
  OPU77: { wetGsm: 130, coats: 2 },
  OPU91: { wetGsm: 140, coats: 2 },
  OPU277: { wetGsm: 125, coats: 2 },
  LPU002: { wetGsm: 150, coats: 2 },
  FPP26: { wetGsm: 160, coats: 1 },
  FPP20: { wetGsm: 155, coats: 1 },
  FPP47: { wetGsm: 150, coats: 1 },
  FPU15: { wetGsm: 120, coats: 1 },
  'OPP053-BLACK': { wetGsm: 140, coats: 2 },
  'OPP053-WHITE': { wetGsm: 140, coats: 2 },
  FL3100: { wetGsm: 150, coats: 2 },
  TH52: { wetGsm: 0, coats: 0 },
  TH43: { wetGsm: 0, coats: 0 },
};
