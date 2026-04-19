# Horní předsíň

## Vypínače

Dvě ovládací místa v rámci horní předsíně:
- **U schodů:** 1 rámeček se 2 jednovypínači vedle sebe (SW-H1 + SW-H2)
- **U pokoje:** samostatný jednovypínač (SW-CP) — **krabice BEZ Shelly**

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-H1 | H1 | L-01 Schodiště | non-HUE | SH-09 IN1 | detached → HA → SH-01 |
| SW-H2 | H2 | L-03 Lustr horní předs. | non-HUE | SH-03 SW1 (u lustru) | attached, přes signálový vodič |
| SW-CP | CP | L-03 Lustr horní předs. | non-HUE | SH-03 SW1 | paralelně s SW-H2 přes stáv. schodišťák |

## Shelly v této místnosti

| ID | Model | Umístění | Výstup |
|---|---|---|---|
| SH-03 | Plus 1PM | U lustru horní předsíně (stropní krabice) | O1 → L-03 |
| SH-09 | i4 | Za SW-H1 (krabice u schodů) | čte H1 |

## Krabice BEZ Shelly

**SW-CP (vypínač u pokoje v horní předsíni)** — jen tlačítko a WAGO svorka.
- Stávající schodišťákový drát od SW-H2 → k tlačítku SW-CP → zpět druhým drátem → do SH-03 SW1
- Funguje offline bez HA (přímá paralelní topologie)

## Instalační poznámky

- Krabice u schodů s SH-09: **prosekat** nebo KU68 kroužek
- SH-03 u lustru: stropní krabice by měla mít víc místa než mělké krabice vypínačů
- Pozor: **vypínač SW-H1 (schodiště) a vypínač SW-H2 (lustr) jsou dva jednovypínače ve stejném rámečku** — jeden jde do i4 (H1), druhý přes signálový drát do Plus 1PM (H2). Elektrikář by neměl zaměnit!

## Scénáře ovládání

- SW-H1 stisk → HA → toggle SH-01 (schodišťové svítidlo)
- SW-H2 stisk → přímo SH-03 SW1 → toggle SH-03 výstup → L-03 on/off (offline OK)
- SW-CP stisk → přes stávající drát → SH-03 SW1 paralelně → stejný efekt

## Ověřit

- [ ] Stávající schodišťákový drát mezi SW-H2 (u schodů) a SW-CP (u pokoje) existuje (2 volné vodiče)?
- [ ] Dostupnost stropní krabice u lustru pro SH-03
