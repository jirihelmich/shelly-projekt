# Horní předsíň

## Vypínače a okruhy

L-01 (schodiště) a L-03 (lustr horní předsíň) jsou na **dvou různých okruzích**, každý má L+N v jiné krabici. Proto **2× Shelly 1 Mini**, jedna v každé krabici.

Dvě ovládací místa:
- **U schodů (P-HP):** 1 rámeček se 2 jednovypínači vedle sebe (SW-H1 + SW-H2)
  - Krabice za SW-H1 = okruh L-01 → **obsahuje SH-01 Mini**
  - Krabice za SW-H2 = okruh L-03 → **bez Shelly** (jen paralelka)
- **U pokoje (P-CP):** samostatný jednovypínač SW-CP, krabice na okruhu L-03 → **obsahuje SH-03 Mini**

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-H1 | H1 | L-01 Schodiště | non-HUE | SH-01 SW1 (lokálně v této krabici) | **attached** |
| SW-H2 | H2 | L-03 Lustr horní předs. | non-HUE | SH-03 SW1 (přes stáv. schodišťák do P-CP) | **paralelka** k SW-CP |
| SW-CP | CP | L-03 Lustr horní předs. | non-HUE | SH-03 SW1 (lokálně v této krabici) | **attached** |
| SW-A (obývák) | A | L-01 Schodiště | non-HUE | SH-01 SW1 (přes stáv. schodišťák do P-HP) | **paralelka** k SW-H1 |

## Shelly v této místnosti

| ID | Model | Umístění | Výstup |
|---|---|---|---|
| SH-01 | Shelly 1 Mini | V krabici u schodů (P-HP, za SW-H1, okruh L-01) | O1 → L-01 schodiště |
| SH-03 | Shelly 1 Mini | V krabici u pokoje (P-CP, za SW-CP, okruh L-03) | O1 → L-03 lustr horní předs. |

**Proč 2 Mini, ne sdílený 2PM:** L-01 a L-03 jsou na různých jističích/okruzích. L+N pro L-01 je v krabici u schodů (P-HP), L+N pro L-03 je v krabici P-CP u pokoje. Každý okruh = vlastní Mini lokálně. Šlo by sloučit do jednoho 2PM jen za cenu cross-circuit přemostění napájení, což není dobrá praxe.

## Krabice BEZ Shelly v této místnosti

### Krabice za SW-H2 (u schodů, vedle SW-H1)
- Sice ve stejném rámečku jako SW-H1, ale na **jiném okruhu** (L-03)
- L+N pro L-03 v této krabici **není** — okruh prochází přes P-CP
- Stisk SW-H2: lokální fáze L-03 (z PE/sdíleného propojení) → COM tlačítka → výstup → schodišťák žíla #1 → SH-03 SW1 v P-CP → toggle L-03

> Pozn.: prakticky to znamená, že krabice za SW-H1 a SW-H2 jsou _fyzicky vedle sebe v jednom rámečku_, ale **každá je napojena na jiný okruh**. Elektrikář musí mít přehled, kterému okruhu která žíla patří. Štítek v krabici doporučen.

## Krabice za SW-A (obývák, fyzicky obývák ale logicky souvisí)
- Stávající schodišťákový drát Obývák↔H. předsíň: 1 žíla = signál SW-A → SH-01 SW1 (v P-HP)
- Stisk SW-A → výstup tlačítka → schodišťák žíla #1 → SH-01 SW1 → toggle O1 (L-01)
- Bez Shelly v této krabici, jen tlačítko + WAGO

## Instalační poznámky

- **Krabice u SW-H1 (P-HP, okruh L-01):** sem se montuje SH-01 Mini. Mělká → **prosekat / KU68 kroužek**
- **Krabice u SW-H2 (P-HP, okruh L-03):** bez Shelly, jen tlačítko + WAGO + signální vodič přes stáv. schodišťák do P-CP
- **Krabice u SW-CP (P-CP, okruh L-03):** sem se montuje SH-03 Mini. Mělká → **prosekat / KU68 kroužek**
- **Krabice u SW-A (obývák):** bez Shelly, jen tlačítko + WAGO + signální vodič přes stáv. schodišťák do P-HP
- **Pozor — cross-circuit signál:** Krabice za SW-A v obýváku vypouští signál (fáze pulz) přes schodišťák do SH-01 v horní předsíni; jistič obýváku a jistič H. předsíně mohou být různé. Při údržbě SH-01 vypnout oba jističe. Štítek v krabicích doporučen.

## Scénáře ovládání

| Stisk | Cesta | Efekt |
|---|---|---|
| SW-H1 (lokálně, P-HP) | → SH-01 SW1 attached | toggle L-01 schodiště |
| SW-A (obývák) | → schodišťák Obývák↔P-HP → SH-01 SW1 | toggle L-01 (paralelka) |
| SW-CP (lokálně, P-CP) | → SH-03 SW1 attached | toggle L-03 lustr H. předs. |
| SW-H2 (P-HP) | → schodišťák P-HP↔P-CP → SH-03 SW1 | toggle L-03 (paralelka) |

Všechno funguje **offline bez HA**.

## Ověřit

- [ ] Stávající schodišťákový drát Obývák (SW-A) ↔ H. předsíň krabice u schodů (SH-01): **alespoň 1 volná žíla** pro signál
- [ ] Stávající schodišťákový drát H. předsíň (SW-H2) ↔ P-CP (SH-03): **alespoň 1 volná žíla** pro signál
- [ ] Hloubka krabic za SW-H1 a SW-CP pro Mini + svorky (KU68)
- [ ] Lokální L+N v krabici u SW-H1 (okruh L-01) — potvrdit jistič
- [ ] Lokální L+N v krabici u SW-CP (okruh L-03) — potvrdit jistič
- [ ] Identifikovat, na kterém jističi je která krabice — přidat štítky do krabic
