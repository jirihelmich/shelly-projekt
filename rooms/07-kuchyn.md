# Kuchyň

## Stav

Kuchyňský rámeček je **stávající**. V novém projektu se dotýkáme pouze tlačítka **Lišta 3** (paralelka do obývákova SW-D1 pro L-07 Lišta 3, 220V). Ostatní tlačítka a 24V LED svítidla zůstávají beze změny — řídí je stávající SH-E3.

## Moduly v rámečku (zleva doprava)

| # | Modul | Typ | Ovládá | Napětí | Poznámka |
|---|---|---|---|---|---|
| 1 | Zásuvka (Z) | socket | — | 220V | stávající |
| 2 | Jednovypínač „Lišta 3" | single | **L-07 Lišta 3 (obývák)** | 220V | paralelka k SW-D1 přes stáv. drát → SH-06 SW1 |
| 3 | Dvojvypínač „LED A \| LED B" | double | L-14 LED A, L-15 LED B | 24V | stávající, SH-E3 |
| 4 | Jednovypínač „LED digestoř" | single | L-16 LED digestoř | 24V | stávající, SH-E3 |

## Svítidla

| ID | Název | Typ | Napětí | Status |
|---|---|---|---|---|
| L-07 | Lišta 3 | non-HUE | 220V | nová (ovládání sdíleno s obývákem) |
| L-14 | LED kuchyň A | RGBW-PM | 24V | stávající |
| L-15 | LED kuchyň B | RGBW-PM | 24V | stávající |
| L-16 | LED digestoř | RGBW-PM | 24V | stávající |

## Shelly v této místnosti

| ID | Model | Umístění | Funkce | Status |
|---|---|---|---|---|
| SH-E3 | (neznámý, pravděpodobně RGBW PM) | Kuchyň | Ovládá L-14, L-15, L-16 | stávající |

## Ověřit

- [ ] Existuje stávající schodišťákový drát Obývák (SW-D) → Kuchyň (SW-KU-L3)?
- [ ] Potvrdit model SH-E3 (Shelly RGBW PM?)
- [ ] Pokud drát neexistuje: Lišta 3 z kuchyně ztratí funkci, nebo doplnit i4 (+1× i4)
