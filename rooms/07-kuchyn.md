# Kuchyň

## Stav

Stávající rámeček obsahuje zásuvku + 4 vypínače. 24V LED systém je stávající ("vyřešeno"). Jediný dotyk s novou instalací:

- Tlačítko **Lišta 3** v kuchyni ovládá **totéž svítidlo** jako obývákova Lišta 3 (L-07) — tj. **220V okruh**, ne 24V. Zapojeno paralelně k SW-D1 přes stávající schodišťákový drát do SH-06 SW1 v obýváku.

## Rámeček P-KU (5 modulů)

| Modul | Typ | Ovládá | Napětí | Poznámka |
|---|---|---|---|---|
| 1 | Zásuvka | — | 220V | |
| 2 | Jednovypínač | L-07 Lišta 3 | **220V** | paralelka k SW-D1 obývák, SH-06 SW1 |
| 3+4 | Dvojvypínač | 2× LED (A, B) | 24V | stávající, jiná svítidla |
| 5 | Jednovypínač | LED digestoř | 24V | stávající |

## Shelly v této místnosti

Žádný nový. Stávající SH-E3 (model neznámý) ovládá 24V okruhy — beze změny.

## Ověřit

- [ ] Existuje stávající schodišťákový drát Obývák (SW-D) → Kuchyň (SW-KU-L3)?
- [ ] Pokud ne: Lišta 3 v kuchyni ztratí funkci, nebo doplnit i4 za kuchyňský vypínač (+1× i4)

## Poznámky

- 24V okruhy (LED A, LED B, LED digestoř) neřešíme — beze změny
- Pokud by se v budoucnu něco měnilo, přidat sem
