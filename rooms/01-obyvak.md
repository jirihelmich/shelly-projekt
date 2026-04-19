# Obývák

## Vypínače (tlačítka ABB Tango s pružinkami)

U vstupu do obýváku: 4× dvojvypínač v řadě + 1× stávající vypínač pro LED strop.

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-A | A | L-01 Schodiště | non-HUE | SH-07 IN1 | detached |
| SW-B | B1 | L-11 Předsíň strop | HUE | SH-07 IN2 | detached |
| SW-B | B2 | L-10 Obývák strop | HUE | SH-07 IN3 | detached |
| SW-C | C1 | L-05 Lišta 1 | non-HUE | SH-05 SW1 | attached |
| SW-C | C2 | L-06 Lišta 2 | non-HUE | SH-05 SW2 | attached |
| SW-D | D1 | L-07 Lišta 3 | non-HUE | SH-06 SW1 | attached |
| SW-D | D2 | L-08 Lustr K | HUE | SH-06 SW2 | detached |
| SW-E | E | L-12 LED strop | stávající | SH-E1 | stávající |

## Shelly v této místnosti

| ID | Model | Umístění | Výstupy |
|---|---|---|---|
| SH-05 | Plus 2PM | Za SW-C | O1→L-05, O2→L-06 |
| SH-06 | Plus 2PM | Za SW-D | O1→L-07, O2 nezapojen (L-08 je HUE) |
| SH-07 | i4 | Za SW-A + SW-B | čtení tlačítek, žádné výstupy |

## Stávající

- SH-E1 Shelly RGBW PM u LED stropu (L-12) — beze změny

## Instalační poznámky

- Všechny krabice jsou mělké → **prosekat** nebo použít KU68 kroužek
- SH-05, SH-06, SH-07 by měly být za vypínači C, D a A+B — ověřit, že jsou fyzicky vedle sebe (jeden rámeček / hnízdo)
- Pokud SW-A je daleko od SW-B, potřeba +1× i4

## Zapojení SH-06 K2 (detached pro Lustr K HUE)

- SW-D2 (tlačítko) → SH-06 SW2 vstup
- SH-06 výstup O2: **nezapojit** (Lustr K je HUE žárovka, trvale pod proudem mimo SH-06)
- V HA: disable entity `switch.sh_06_output_2`
- V HA: použít `event.sh_06_input_2` → `light.toggle` pro L-08

## Ověřit

- [ ] Fyzické rozmístění SW-A, SW-B, SW-C, SW-D (stejný rámeček?)
- [ ] L-11 "předsíň strop" — je to totéž svítidlo jako L-09, nebo jiné?
