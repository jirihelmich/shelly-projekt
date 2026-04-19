# Dolní předsíň

## Vypínače

Dvě ovládací místa:
- **U pracovny:** 2× jednovypínač vedle sebe (SW-F1 + SW-F2) — **krabice BEZ Shelly** (jen tlačítka a WAGO)
- **U dveří:** 1× dvojvypínač (SW-G) — **krabice BEZ Shelly**

Stávající schodišťákové zapojení využito trojím způsobem:
- Pracovna ↔ Dveře (dva páry drátů): jeden pro L-02, jeden pro L-09
- Obývák (SW-B) ↔ Dolní předsíň (SW-F2): pro L-09 paralelka do SH-07 IN2 (i4 v obývákové konzoli)

**Pozor:** _Předsíň strop_ (L-09) je totéž HUE svítidlo jako _Předsíň strop_ v rámečku obýváku (tlačítko SW-B1). L-09 má 3 ovládací tlačítka (B1 obývák, F2 pracovna, G2 dveře) — všechna paralelně na SH-07 IN2.

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-F1 | F1 | L-02 LED pásek | non-HUE (LED-trafo) | SH-02 SW1 (u trafa/driveru ve stropě) | attached, přes signálový vodič |
| SW-F2 | F2 | L-09 Předsíň strop | HUE | SH-07 IN2 (v obýváku) | paralelka k SW-B1 přes stáv. schodišťák |
| SW-G | G1 | L-02 LED pásek | non-HUE | SH-02 SW1 | paralelka k SW-F1 přes stáv. schodišťák (pracovna↔dveře) |
| SW-G | G2 | L-09 Předsíň strop | HUE | SH-07 IN2 | paralelka k SW-B1/SW-F2 |

## Shelly v této místnosti

| ID | Model | Umístění | Výstup |
|---|---|---|---|
| SH-02 | Shelly 1 Mini | **V krabičce u LED driveru/trafa pásku** (stropní krabice) | O1 → 220V na driver → L-02 |

Žádná Shelly není za vypínači v této místnosti — všechna tlačítka jsou paralelky přes stávající schodišťákové dráty do Shelly v jiných místech (SH-02 ve stropě, SH-07 v obýváku).

## Krabice BEZ Shelly

**SW-F1 + SW-F2 (rámeček u pracovny)** — jen tlačítka a WAGO svorky.
- F1: signálový vodič k SH-02 SW1 (u trafa)
- F2: signálový vodič paralelně na stávajícím schodišťáku k SW-B1 → SH-07 IN2

**SW-G (dvojvypínač u dveří)** — jen tlačítka a WAGO svorky.
- G1: paralelka k SW-F1 přes stáv. schodišťák (pracovna↔dveře) → SH-02 SW1
- G2: paralelka k SW-F2 a SW-B1 → SH-07 IN2

## Instalační poznámky

- **SH-02 ve stropní krabici u trafa/driveru** — víc místa než za vypínačem, Shelly je přímo u spínaného zařízení. Ověřit přístupnost a napájení (L, N, PE).
- Krabice u pracovny (SW-F1+F2): bez Shelly, jen WAGO svorky — stačí standardní hloubka
- Krabice u dveří (SW-G): bez Shelly, jen WAGO svorky

## Logika paralelního zapojení

Pro L-02 (LED pásek):
- SW-F1 + SW-G1 paralelně → SH-02 SW1 → toggle L-02 (funguje offline)

Pro L-09 (Předsíň strop HUE):
- SW-F2 + SW-G2 + SW-B1 (obývák) paralelně → SH-07 IN2 → event → HA → Hue toggle (vyžaduje HA)

## Ověřit

- [ ] Stávající schodišťákový drát pracovna (SW-F1) ↔ dveře (SW-G) — 2 volné vodiče?
- [ ] Stávající schodišťákový drát pracovna (SW-F2) ↔ dveře (SW-G) — 2 volné vodiče?
- [ ] Stávající schodišťákový drát obývák (SW-B) ↔ pracovna (SW-F2) — 2 volné vodiče? (Pokud ne, potřeba i4 v dolní předsíni)
- [ ] Kde je trafo/driver L-02 umístěn (přístup pro SH-02 Mini)?
- [ ] Driver/trafo L-02 toleruje spínání 220V vstupu?
