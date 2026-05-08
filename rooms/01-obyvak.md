# Obývák

## Vypínače (tlačítka ABB Tango s pružinkami)

U vstupu do obýváku: 4× dvojvypínač v řadě + 1× stávající vypínač pro LED strop.

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-A | A | L-01 Schodiště | non-HUE | SH-01 SW1 (Mini v krabici u schodů P-HP) | **paralelka** přes stáv. schodišťák Obývák↔H. předsíň |
| SW-B | B1 | L-09 Předsíň strop (sdíleno) | HUE | SH-07 IN2 | detached |
| SW-B | B2 | L-10 Obývák strop | HUE | SH-07 IN3 | detached |
| SW-C | C1 | L-05 Lišta 1 | non-HUE | SH-05 SW1 | attached |
| SW-C | C2 | L-06 Lišta 2 | non-HUE | SH-05 SW2 | attached |
| SW-D | D1 | L-07 Lišta 3 | non-HUE | SH-06 SW1 | attached (+ paralelka z kuchyně) |
| SW-D | D2 | L-04 Lustr jídelna | HUE | SH-06 SW2 | detached, paralelně se SW-J2 v jídelně |
| SW-E | E | L-12 LED strop | stávající | SH-E1 | stávající |

## Shelly v této místnosti

| ID | Model | Umístění | Výstupy |
|---|---|---|---|
| SH-05 | Plus 2PM | Za SW-C | O1→L-05, O2→L-06 |
| SH-06 | Plus 2PM | Za SW-D | O1→L-07; O2 nezapojen (L-04 je HUE) |
| SH-07 | i4 | Za SW-B (přízemní konzole) | IN2=SW-B1, IN3=SW-B2; IN1, IN4 rezerva |

> **Pozor:** SH-01 (Mini, jen schodiště L-01) **nesedí v obýváku** — sedí v krabici u schodů v horní předsíni (P-HP, za SW-H1), kde je dostupný N pro okruh L-01. Krabice za SW-A v obýváku je tedy **bez Shelly**, jen tlačítko + WAGO + signální vodič přes stáv. schodišťák.

## Stávající

- SH-E1 Shelly RGBW PM u LED stropu (L-12) — beze změny

## Instalační poznámky

- Všechny krabice jsou mělké → **prosekat** nebo použít KU68 kroužek
- SH-05, SH-06, SH-07 by měly být za vypínači C, D a B — ověřit, že jsou fyzicky vedle sebe
- Krabice za SW-A je BEZ Shelly: jen tlačítko, WAGO, signální vodič přes stáv. schodišťák do SH-01 SW1 (v horní předsíni)

## Zapojení SH-06 K2 (detached, paralelka s jídelnou pro Hue Lustr)

- SW-D2 (tlačítko v obývákovém rámečku, v nákresu označeno „Lustr K") ovládá **Lustr jídelna (L-04, HUE)**
- SW-D2 → SH-06 SW2 (detached, event-only)
- **Paralelka:** SW-J2 (jídelna) je připojen na stejný vstup SH-06 SW2 přes stávající schodišťákový drát Obývák↔Jídelna → žádná Shelly v jídelně
- SH-06 výstup O2: **nezapojit** (L-04 je HUE, fáze trvalá — Hue bridge toggluje žárovku)
- V HA: disable entity `switch.sh_06_output_2`
- V HA: `event.sh_06_input_2` → `light.toggle` na Hue skupinu L-04

## Ověřit

- [ ] Fyzické rozmístění SW-A, SW-B, SW-C, SW-D (stejný rámeček?)
- [ ] Krabice za SW-A: vejde se WAGO + signální vodič ze schodišťáku po proseknutí (Shelly tam **není**)
