# Dolní předsíň

## Vypínače

Dvě ovládací místa:
- **U pracovny:** 2× jednovypínač vedle sebe (SW-F1 + SW-F2)
- **U dveří:** 1× dvojvypínač (SW-G) — **krabice BEZ Shelly**

Stávající schodišťákové zapojení existuje pro oba okruhy (LED pásek i předsíň strop) mezi pracovnou a dveřmi.

**Pozor:** _Předsíň strop_ (L-09) je **totéž HUE svítidlo** jako _Předsíň strop_ v rámečku obýváku (tlačítko SW-B1). Tj. L-09 má **3 ovládací tlačítka** v různých místnostech (B1 obývák, F2 pracovna, G2 dveře) — synchronizace přes HA.

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-F1 | F1 | L-02 LED pásek | non-HUE | SH-02 SW1 (u trafa) | attached, přes signálový vodič |
| SW-F2 | F2 | L-09 Předsíň strop | HUE | SH-08 IN1 | detached |
| SW-G | G1 | L-02 LED pásek | non-HUE | SH-02 SW1 | paralelně s SW-F1 přes stáv. schodišťák |
| SW-G | G2 | L-09 Předsíň strop | HUE | SH-08 IN1 | paralelně s SW-F2 přes stáv. schodišťák |

## Shelly v této místnosti

| ID | Model | Umístění | Výstup |
|---|---|---|---|
| SH-02 | Plus 1PM | U trafa LED pásku | O1 → 230V primár trafa → L-02 |
| SH-08 | i4 | Za SW-F2 (krabice u pracovny) | čte F2+G2 paralelně |

## Krabice BEZ Shelly

**SW-G (dvojvypínač u dveří)** — jen tlačítka a WAGO svorky.
- Tlačítko G1: stávající schodišťákový drát od SW-F1 → dál do SH-02 SW1
- Tlačítko G2: stávající schodišťákový drát od SW-F2 → dál do SH-08 IN1
- Druhé strany tlačítek (G1, G2): signálový potenciál (L nebo N dle konfigurace SH-02/SH-08 SW vstupů)

## Instalační poznámky

- Krabice u pracovny s SH-08: **prosekat** nebo KU68 kroužek
- SH-02 u trafa: záleží kde je trafo instalované (podhled, skříň). Ověřit přístupnost a napájení (L, N, PE).
- Ověřit: stávající schodišťákové dráty pro oba okruhy skutečně existují a jsou volné.

## Logika paralelního zapojení tlačítek

Pro oba okruhy platí stejný princip:
- Obě tlačítka (z pracovny i z dveří) připojena paralelně na **stejný SW vstup Shelly**
- Shelly vidí "někdo stiskl" → toggle výstupu (pro L-02) nebo pošle event (pro L-09)
- Funguje bez HA (alespoň pro L-02, kde SH-02 toggle je lokální)

## Ověřit

- [ ] Stávající schodišťákové dráty pro L-02 existují (2 volné vodiče mezi pracovnou a dveřmi)?
- [ ] Stávající schodišťákové dráty pro L-09 existují?
- [ ] Trafo LED pásku toleruje spínání 230V primáru?
- [ ] Kde je trafo umístěno (přístup pro SH-02)?
