# Horní předsíň

## Vypínače

Dvě ovládací místa v rámci horní předsíně:
- **U schodů:** 1 rámeček se 2 jednovypínači vedle sebe (SW-H1 + SW-H2)
- **U pokoje:** samostatný jednovypínač (SW-CP) — **krabice BEZ Shelly**

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-H1 | H1 | L-01 Schodiště | non-HUE | SH-01 SW1 (obývák) | paralelka k SW-A přes stáv. schodišťák |
| SW-H2 | H2 | L-03 Lustr horní předs. | non-HUE | SH-03 SW1 (za SW-H2) | attached |
| SW-CP | CP | L-03 Lustr horní předs. | non-HUE | SH-03 SW1 | paralelně s SW-H2 přes stáv. schodišťák |

## Shelly v této místnosti

| ID | Model | Umístění | Výstup |
|---|---|---|---|
| SH-03 | Shelly 1 Mini | Za SW-H2 (krabice u schodů) | O1 → L-03 |

## Krabice BEZ Shelly

**SW-CP (vypínač u pokoje v horní předsíni)** — jen tlačítko a WAGO svorka.
- Stávající schodišťákový drát od SW-H2 → k tlačítku SW-CP → zpět druhým drátem → do SH-03 SW1
- Funguje offline bez HA (přímá paralelní topologie)

## Instalační poznámky

- Krabice u SW-H2: Mini SH-03 (kompaktní) se vejde po prosekání / s KU68 kroužkem
- Krabice u SW-H1: **bez Shelly**, jen WAGO svorka pro paralelku schodišťákového drátu do SH-01 v obýváku
- Pozor: **SW-H1 (schodiště) a SW-H2 (lustr) jsou dva jednovypínače ve stejném rámečku**, ale vedou signál do jiných Shelly — SW-H1 přes drát do SH-01 v obýváku, SW-H2 do SH-03 přímo za sebou. Elektrikář by neměl zaměnit!

## Scénáře ovládání

- SW-H1 stisk → přes stáv. schodišťákový drát → SH-01 SW1 v obýváku → toggle L-01 (offline OK)
- SW-H2 stisk → SH-03 SW1 (Mini za SW-H2) → toggle L-03 (offline OK)
- SW-CP stisk → přes stáv. schodišťákový drát → SH-03 SW1 paralelně → stejný efekt jako SW-H2

## Ověřit

- [ ] Stávající schodišťákový drát mezi SW-H2 (u schodů) a SW-CP (u pokoje) existuje (2 volné vodiče)?
- [ ] Hloubka krabic za SW-H1+H2 pro Mini SH-03 + WAGO svorku paralelky
