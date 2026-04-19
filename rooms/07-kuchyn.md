# Kuchyň

## Stav

Ze stávajícího kuchyňského rámečku se nové instalace dotýká **jen tlačítko Lišta 3** — je to paralelka k SW-D1 v obýváku (ovládá totéž svítidlo L-07 Lišta 3 v obýváku, 220V).

Ostatní moduly v kuchyňském rámečku (LED pásky, digestoř, zásuvka) jsou **mimo scope** tohoto projektu.

## Rámeček (dokumentovaná část)

| Modul | Typ | Ovládá | Napětí | Poznámka |
|---|---|---|---|---|
| Zásuvka (Z) | socket | — | 220V | stávající, pro úplnost |
| Jednovypínač „Lišta 3" | single | L-07 Lišta 3 (obývák) | **220V** | paralelka k SW-D1, SH-06 SW1 přes stáv. schodišťákový drát |

## Shelly v této místnosti

Žádná nová. Stávající kuchyňské řízení 24V LED neřešíme.

## Zapojení SW-KU-L3

- Tlačítko SW-KU-L3 v kuchyňském rámečku má jeden pól připojený přes stávající schodišťákový drát k **SH-06 SW1** (Plus 2PM za SW-D v obýváku).
- Druhý pól na signálovém potenciálu (L nebo N).
- Stisk → krátké zkratování SW1 → SH-06 toggle → L-07 on/off.
- **Funguje offline bez HA** (attached paralelka).

## Ověřit

- [ ] Existuje stávající schodišťákový drát Obývák (SW-D) → Kuchyň (SW-KU-L3)?
- [ ] Pokud ne: Lišta 3 z kuchyně ztratí funkci, nebo doplnit i4 za kuchyňský vypínač (+1× i4)
