/** Расход и слои ПУ/акрилового блока — из TDS .doc (sources/sirca/). */

export type PuSpecHint = { wetGsm: number; coats: number };

export const sircaPuSpecs: Record<string, PuSpecHint> = {
  FL3100: { wetGsm: 110, coats: 1 },
  FPP20: { wetGsm: 125, coats: 3 },
  FPP26: { wetGsm: 130, coats: 2 },
  FPP47: { wetGsm: 125, coats: 3 },
  FPU15: { wetGsm: 110, coats: 2 },
  LPU002: { wetGsm: 125, coats: 2 },
  'OPP053-BLACK': { wetGsm: 140, coats: 1 },
  'OPP053-WHITE': { wetGsm: 140, coats: 1 },
  OPU277: { wetGsm: 110, coats: 2 },
  OPU379G: { wetGsm: 100, coats: 3 },
  OPU57: { wetGsm: 120, coats: 2 },
  OPU60G: { wetGsm: 125, coats: 2 },
  OPU77: { wetGsm: 125, coats: 2 },
  OPU79: { wetGsm: 110, coats: 2 },
  OPU91: { wetGsm: 110, coats: 1 },
};
