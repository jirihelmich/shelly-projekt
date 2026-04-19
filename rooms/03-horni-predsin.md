# Horní předsíň (chodba u schodů)

## Vypínače

Dvě ovládací místa:
- **U schodů:** 2× jednovypínač vedle sebe (SW-H1 + SW-H2)
- **Samostatný vypínač** (jinde v prostoru): 1× jednovypínač (SW-H3) — **krabice BEZ Shelly**

Stávající schodišťákové zapojení existuje mezi SW-H2 a SW-H3.

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-H1 | H1 | L-01 Schodiště | non-HUE | SH-09 IN1 | detached → HA → SH-01 |
| SW-H2 | H2 | L-03 Lustr horní předs. | non-HUE | SH-03 SW1 (u lustru) | attached, přes signálový vodič |
| SW-H3 | H3 | L-03 Lustr horní předs. | non-HUE | SH-03 SW1 | paralelně s SW-H2 přes stáv. schodišťák |

## Shelly v této místnosti

| ID | Model | Umístění | Výstup |
|---|---|---|---|
| SH-03 | Plus 1PM | U lustru horní předsíně (stropní krabice) | O1 → L-03 |
| SH-09 | i4 | Za SW-H1 (krabice u schodů) | čte H1 |

## Krabice BEZ Shelly

**SW-H3 (samostatný vypínač v prostoru)** — jen tlačítko a WAGO svorka.
- Stávající schodišťákový drát od SW-H2 → pokračuje k tlačítku H3 → zpět druhým drátem → do SH-03 SW1
- Druhá strana tlačítka H3: signálový potenciál (L nebo N dle konfigurace SH-03 SW1)

## Instalační poznámky

- Krabice u schodů s SH-09: **prosekat** nebo KU68 kroužek
- SH-03 u lustru: stropní krabice by měla mít víc místa než mělké krabice vypínačů
- Pozor: **vypínač SW-H1 (schodiště) a vypínač SW-H2 (lustr) jsou dva jednovypínače vedle sebe** — jeden jde do i4 (H1), druhý přes signálový drát do Plus 1PM (H2). Elektrikář by neměl zaměnit!

## Scénáře ovládání

- SW-H1 stisk → HA → toggle SH-01 (schodišťové svítidlo)
- SW-H2 stisk → přímo SH-03 SW1 → toggle SH-03 výstup → L-03 on/off (offline OK)
- SW-H3 stisk → přes stávající drát → SH-03 SW1 paralelně → stejný efekt

## Ověřit

- [ ] Stávající schodišťákové dráty mezi SW-H2 a SW-H3 existují (2 volné vodiče)?
- [ ] Umístění SW-H3 (kde přesně v prostoru "horní předsíň")?
- [ ] Dostupnost stropní krabice u lustru pro SH-03
