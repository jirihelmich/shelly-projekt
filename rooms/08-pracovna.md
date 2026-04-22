# Pracovna

## Vypínače

U dveří: **2× dvojvypínač vedle sebe** (SW-PR-D1 + SW-PR-D2), celkem 4 tlačítka → 4 Lišty.
Žádné paralelky (každá buňka ovládá jednu Lištu, jeden okruh).

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-PR-D1 | PR-D1-1 | L-30 Lišta 1 | non-HUE 230V | SH-14 SW1 | attached |
| SW-PR-D1 | PR-D1-2 | L-31 Lišta 2 | non-HUE 230V | SH-14 SW2 | attached |
| SW-PR-D2 | PR-D2-1 | L-32 Lišta 3 | non-HUE 230V | SH-15 SW1 | attached |
| SW-PR-D2 | PR-D2-2 | L-33 Lišta 4 | non-HUE 230V | SH-15 SW2 | attached |

### Stávající (mimo scope, beze změny)

- **SW-PR-V** — jednovypínač u pracovního stolu pro venkovní svítidlo. Ponecháno v původním zapojení, žádná Shelly.

## Shelly v této místnosti

| ID | Model | Umístění | Výstupy |
|---|---|---|---|
| SH-14 | Plus 2PM | Za SW-PR-D1 (u dveří) | O1→L-30 Lišta 1, O2→L-31 Lišta 2 |
| SH-15 | Plus 2PM | Za SW-PR-D2 (u dveří, vedle SH-14) | O1→L-32 Lišta 3, O2→L-33 Lišta 4 |

Obě Shelly **attached** — tlačítka přímo togglují výstupy, funguje **offline bez HA**.

## Instalační poznámky

- Krabice za SW-PR-D1 a SW-PR-D2 jsou mělké → **prosekat** nebo **KU68 kroužek**
- 2× Plus 2PM = 2 samostatné Shelly v samostatných krabicích (každá pod svým dvojvypínačem)
- Všechny 4 Lišty jsou 230V → non-HUE, spínání fáze normálně
- Bez paralelek — zjednodušené zapojení, každé tlačítko jeden okruh

## Ověřit

- [ ] Hloubka krabic za SW-PR-D1 a SW-PR-D2 (po proseknutí se vejde 2PM + svorky?)
- [ ] Fyzické rozmístění — jsou oba dvojvypínače vedle sebe v jednom rámečku nebo ve dvou separátních?
- [ ] Jsou všechny 4 Lišty typu s tolerancí spínání 230V (klasické LED žárovky OK; u levnějších LED zvážit inrush)?
