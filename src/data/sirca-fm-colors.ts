/** Ferro Micacei — из sources/sirca/specs/Cartella colori FM.XLSX */

export type FmColorSystem = {
  label: string;
  formula: string;
};

export type FmColor = {
  name: string;
  systems: Record<'grossa' | 'fine' | 'acr', FmColorSystem>;
};

export const sircaFmColors: FmColor[] = [
  {
    "name": "Antracite 1",
    "systems": {
      "grossa": {
        "label": "F4FMGG / F6FMGG — крупная фракция",
        "formula": "F4FMGG01/F6FMGG01 99%"
      },
      "fine": {
        "label": "F404FM / F406FM — мелкая фракция",
        "formula": "F404FM01/F406FM01 97%"
      },
      "acr": {
        "label": "F7FMGG — акрил 1k",
        "formula": "F7FMGG01 99%"
      }
    }
  },
  {
    "name": "Antracite 2",
    "systems": {
      "grossa": {
        "label": "F4FMGG / F6FMGG — крупная фракция",
        "formula": "F4FMGG01/F6FMGG01 95%"
      },
      "fine": {
        "label": "F404FM / F406FM — мелкая фракция",
        "formula": "F404FM01/F406FM01 95%"
      },
      "acr": {
        "label": "F7FMGG — акрил 1k",
        "formula": "F7FMGG01 95%"
      }
    }
  },
  {
    "name": "Antracite 3",
    "systems": {
      "grossa": {
        "label": "F4FMGG / F6FMGG — крупная фракция",
        "formula": "F4FMGG01/F6FMGG01 91%"
      },
      "fine": {
        "label": "F404FM / F406FM — мелкая фракция",
        "formula": "F404FM01/F406FM01 90%"
      },
      "acr": {
        "label": "F7FMGG — акрил 1k",
        "formula": "F7FMGG01 90%"
      }
    }
  },
  {
    "name": "Argento Base",
    "systems": {
      "grossa": {
        "label": "F4FMGG / F6FMGG — крупная фракция",
        "formula": "F4FMgg01 1%"
      },
      "fine": {
        "label": "F404FM / F406FM — мелкая фракция",
        "formula": "F404FM01 1%"
      },
      "acr": {
        "label": "F7FMGG — акрил 1k",
        "formula": "F7FMGG01 1%"
      }
    }
  },
  {
    "name": "Blu",
    "systems": {
      "grossa": {
        "label": "F4FMGG / F6FMGG — крупная фракция",
        "formula": "F4FMGG01/F6FMGG01 91.5%"
      },
      "fine": {
        "label": "F404FM / F406FM — мелкая фракция",
        "formula": "F404FM01/F406FM01 91.5%"
      },
      "acr": {
        "label": "F7FMGG — акрил 1k",
        "formula": "F7FMGG01 91.5%"
      }
    }
  },
  {
    "name": "Bronzo",
    "systems": {
      "grossa": {
        "label": "F4FMGG / F6FMGG — крупная фракция",
        "formula": "F4FMGG01/F6FMGG01 90%"
      },
      "fine": {
        "label": "F404FM / F406FM — мелкая фракция",
        "formula": "F404FM01/F406FM01 90%"
      },
      "acr": {
        "label": "F7FMGG — акрил 1k",
        "formula": "F7FMGG01 90%"
      }
    }
  },
  {
    "name": "Corten/Ruggine",
    "systems": {
      "grossa": {
        "label": "F4FMGG / F6FMGG — крупная фракция",
        "formula": "F4FMGG01/F6FMGG01 90%"
      },
      "acr": {
        "label": "F7FMGG — акрил 1k",
        "formula": "F7FMGG01 90%"
      }
    }
  },
  {
    "name": "Grigio chiaro",
    "systems": {
      "grossa": {
        "label": "F4FMGG / F6FMGG — крупная фракция",
        "formula": "F4FMGG01/F6FMGG01 90%"
      },
      "fine": {
        "label": "F404FM / F406FM — мелкая фракция",
        "formula": "F404FM01/F406FM01 90%"
      },
      "acr": {
        "label": "F7FMGG — акрил 1k",
        "formula": "F7FMGG01 90%"
      }
    }
  },
  {
    "name": "Marrone",
    "systems": {
      "grossa": {
        "label": "F4FMGG / F6FMGG — крупная фракция",
        "formula": "F4FMGG01/F6FMGG01 90%"
      },
      "acr": {
        "label": "F7FMGG — акрил 1k",
        "formula": "F7FMGG01 90%"
      }
    }
  },
  {
    "name": "Marrone chiaro",
    "systems": {
      "fine": {
        "label": "F404FM / F406FM — мелкая фракция",
        "formula": "F404FM01/F406FM01 91%"
      }
    }
  },
  {
    "name": "Marrone scuro",
    "systems": {
      "fine": {
        "label": "F404FM / F406FM — мелкая фракция",
        "formula": "F404FM01/F406FM01 90%"
      }
    }
  },
  {
    "name": "Verde",
    "systems": {
      "grossa": {
        "label": "F4FMGG / F6FMGG — крупная фракция",
        "formula": "F4FMGG01/F6FMGG01 93%"
      },
      "fine": {
        "label": "F404FM / F406FM — мелкая фракция",
        "formula": "F404FM01/F406FM01 93%"
      },
      "acr": {
        "label": "F7FMGG — акрил 1k",
        "formula": "F7FMGG01 93%"
      }
    }
  }
] as FmColor[];
