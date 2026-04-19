# Shelly instalace — projekt

Specifikace osazení Shelly zařízení pro ovládání osvětlení v domě.
Koexistence s Philips Hue, integrace s Home Assistant.

## Rychlý přehled

- **10 nových Shelly** (4× Plus 1PM, 2× Plus 2PM, 4× i4)
- **~7 600 Kč** hardware
- **11 vypínačů** (z toho 2 krabice bez Shelly)
- **14 světelných okruhů** (11 nových/upravených + 3 stávající)

## Struktura

```
shelly-projekt/
├── CLAUDE.md                    # Instrukce pro Claude Code
├── README.md                    # Tento soubor
├── changelog.md                 # Historie změn specifikace
├── open-questions.md            # Otevřené body k ověření
├── devices/
│   ├── shelly.yaml              # Inventář Shelly zařízení (SH-01 až SH-10, SH-E*)
│   ├── circuits.yaml            # Světelné okruhy (L-01 až L-14)
│   └── switches.yaml            # Fyzické vypínače a tlačítka (SW-*)
├── rooms/                       # Rozpis per místnost (pro elektrikáře)
│   ├── 01-obyvak.md
│   ├── 02-dolni-predsin.md
│   ├── 03-horni-predsin.md
│   ├── 04-schodiste.md
│   ├── 05-chodba-u-pokoje.md
│   ├── 06-jidelna.md
│   └── 07-kuchyn.md
└── ha/
    └── automations.md           # Home Assistant automatizace (draft)
```

## Konvence ID

- **SH-XX** = Shelly zařízení (SH-E* = stávající)
- **L-XX** = světelný okruh (L = light/circuit)
- **SW-X** = vypínač (switch)

YAML v `devices/` je **source of truth**. Markdown v `rooms/` je odvozený (manuálně udržovaný zatím).

## Stav

**DRAFT v0.1** — průběžně laděno. Viz `open-questions.md` pro seznam věcí k ověření.

## Další kroky

1. Ověřit otevřené otázky (stávající schodišťákové dráty, rozměry krabic, trafo)
2. Finalizovat kusovník
3. Objednat Shelly + KU68 kroužky
4. Domluvit elektrikáře
5. Po instalaci: HA konfigurace (scény, automatizace)
