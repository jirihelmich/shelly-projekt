# Changelog

Historie klíčových rozhodnutí a změn ve specifikaci.

## DRAFT v0.1 — 2026-04-19

**Initial draft na základě chatové konverzace s Claude.**

### Rozhodnutí

- **Fyzické vypínače = tlačítka ABB Tango s pružinkami** (monostabilní). Posílají eventy, ne stavy.
- **Shelly pod vypínače** (Plus/i4), ne do rozvaděče.
- **HUE okruhy přes i4** (detached, fáze trvalá, nikdy se nespíná).
- **Non-HUE okruhy přes Plus 1PM / 2PM** (spíná fázi).
- **Vícemístné ovládání = tlačítka paralelně na jeden SW vstup** (využití stávajících schodišťákových drátů jako signálových). Funguje bez HA.
- **Schodiště 3-cestné přes HA** (detached přes 3× i4 + 1× Plus 1PM u svítidla).
- **Krabice bez Shelly:** SW-G (dveře dolní předsíň), SW-H3 (samostatný horní předsíň). Jen tlačítka a svorky.
- **Plus 1PM u svítidel, ne za vypínači** (mělké krabice jsou problém, stropní krabice mají víc místa).

### Kusovník

- Nové Shelly: 4× Plus 1PM + 2× Plus 2PM + 4× i4 = **10 ks**
- Stávající: 2× RGBW PM + kuchyňská instalace
- Odhad hardware: ~7 600 Kč

### Iterace během konverzace (co se měnilo)

1. Lišta 3 byla nejprve označena jako HUE — opraveno na non-HUE
2. LED strop obývák byl nejprve vynechán — doplněn jako stávající (SH-E1)
3. LED strop obývák byl nejprve plánován s i4 vstupem — opraveno, ovládá ho přímo SH-E1 ze svého SW vstupu (stávající zapojení, nic se nemění)
4. Lustr K (D2) měl být původně přes samostatnou i4 — přesunut do SH-06 K2 (detached kanál 2PM)
5. 2-cestné ovládání bylo původně plánováno přes HA i pro LED pásek a lustr horní předsíně — změněno na paralelní zapojení tlačítek přes stávající schodišťákové dráty (ušetřilo 2× i4)
6. Samostatný vypínač horní předsíně (SW-H3) původně měl i4 — odstraněno, je to krabice bez Shelly
7. Dvojvypínač u dveří dolní předsíně (SW-G) původně měl i4 — odstraněno, je to krabice bez Shelly

## DRAFT v0.2 — 2026-04-19

### Korekce struktury rámečků (dle foto nákresu + zpětné vazby)

- **Obývák vstup** — sjednoceno do **1 vertikálního rámečku** (5 modulů shora dolů):
  jednovypínač → dvojvypínač → jednovypínač → dvojvypínač → dvojvypínač
  (SW-A byl dříve chybně označen jako dvojvypínač)
- **Dolní předsíň** — 2 rámečky:
  - vertikální rámeček u pracovny (SW-F1 + SW-F2)
  - samostatný dvojvypínač u dveří (SW-G)
- **Horní předsíň u schodů** — 1 rámeček se 2 jednovypínači (SW-H1 + SW-H2)
- **Kuchyň** — labely upraveny: `dřezák` → `LED digestoř`, 2× LED rozlišeno jako `LED A` / `LED B` (sloučení zrušeno)

### Topologická korekce: SW-CP = SW-H3 (dříve mylně 2 samostatné)

- **SW-H3 odstraněn** — byl duplicita SW-CP
- **SW-CP** nyní ovládá **L-03 Lustr horní předsíň** (ne L-01 schodiště), paralelka k SW-H2 přes stávající schodišťákový drát → SH-03 SW1
- **L-01 Schodiště** je nyní **2-cestné** (SW-A obývák + SW-H1 horní předsíň), ne 3-cestné
- **SH-10 i4 odstraněno** — krabice v Chodbě u pokoje je bez Shelly (paralelka stačí)
- Nové Shelly: 4× Plus 1PM + 2× Plus 2PM + **3× i4** = **9 ks** (~7 000 Kč)

### L-09 paralelka přes schodišťák do i4 v obýváku → SH-02 zpět na Mini

- Uživatel si všiml redundance: SH-07 IN2 už čte SW-B1 pro L-09. Stačí přidat paralelku z SW-F2 + SW-G2 na stejný vstup přes stáv. schodišťákový drát Obývák↔Dolní předsíň.
- **SH-02 vrácené na Shelly 1 Mini** (jen K1 pro LED pásek). Plus 2PM tam už není potřeba.
- **SH-07 IN2 čte nyní 3 tlačítka paralelně**: SW-B1 lokálně + SW-F2 + SW-G2 přes schodišťák.
- Krabice za SW-F2 je bez Shelly (jen WAGO paralelky).
- **K nákupu: ~4 000 → ~3 000 Kč** (jen 2× Plus 2PM + 1× i4 + rezerva). Všechny 3 Mini se použijí (žádná rezerva).
- **Podmínka:** drát Obývák (SW-B) ↔ Dolní předsíň (SW-F2) — flagováno v open-questions.

### Další konsolidace + voltage badge přesun

- **SH-03 přesunuto** ze za SW-H2 (u schodů) na **za SW-CP (u pokoje, P-CP)** — víc místa v samostatném rámečku. SW-CP attached, SW-H2 paralelka přes stáv. schodišťák.
- **SH-02: Mini → Plus 2PM.** K1 spíná LED pásek (L-02, attached), K2 čte event pro Hue Předsíň strop (L-09, detached). SH-08 i4 odstraněno — Plus 2PM pokrývá oba kanály.
- **Krabice za SW-H1+H2 je zcela bez Shelly** — SW-H1 paralelka do SH-01 v obýváku, SW-H2 paralelka do SH-03 za SW-CP.
- **Nové Shelly: 7 → 6** (2× Mini + 3× 2PM + 1× i4). 1 Mini zbude jako rezerva.
- **K nákupu: ~3 600 Kč → ~4 000 Kč** (+400 Kč; Plus 2PM stojí víc než Mini+i4, ale Mini byla zdarma).
- **Voltage badge** přesunut do pravého dolního rohu buňky (nahoře byl kryt Shelly badgem).

### Konsolidace Shelly do obývákové konzole; 1PM → 1 Mini

Úpravy koncentrovány do obývákové konzole (místo stropních krabic u svítidel).
Shelly Plus 1PM nahrazeny **Shelly 1 Mini** (už nakoupené).

- **SH-01 Shelly 1 Mini**: za SW-A v obývákové konzoli (ne u schodiště svítidla).
  SW-A attached, SW-H1 paralelka přes stáv. schodišťákový drát Obývák↔Horní předsíň.
  Funguje offline bez HA.
- **SH-02 Shelly 1 Mini**: za SW-F1 v dolní předsíni (ne u trafa).
- **SH-03 Shelly 1 Mini**: za SW-H2 v horní předsíni (ne u lustru).
- **SH-09 odstraněno** (i4 pro SW-H1 → HA → SH-01); SW-H1 je nyní přímá paralelka.
- **SH-07 IN1 → rezerva** (SW-A už neposílá event, stačí attached toggle).
- **Nové Shelly: 8 → 7** (3× Mini + 2× 2PM + 2× i4). Mini už nakoupené.
- **K nákupu: ~5 900 Kč → ~3 600 Kč** (2× 2PM + 2× i4 + rezerva).
- **Trade-off**: SW-A ztratilo HA event (scény jen přes state change SH-01, ne tlačítkový event).

### Zjednodušení: SH-04 odstraněno, SW-J2 paralelka přes schodišťákový drát

- **SH-04 zrušeno.** Původně i4 v jídelně (event reader pro SW-J2). Nahrazeno paralelkou: SW-J2 připojen paralelně k SW-D2 přes stávající schodišťákový drát Obývák↔Jídelna do SH-06 SW2 (Plus 2PM v obýváku, detached kanál K2). Jeden vstup čte obě tlačítka.
- **Nové Shelly: 9 → 8** (3× Plus 1PM + 2× Plus 2PM + **3× i4**). Odhad: ~6 500 → **~5 900 Kč**.
- Krabice v jídelně je teď bez Shelly (jen WAGO svorky pro paralelní drát).

### Další opravy: L-04 HUE, kuchyň zjednodušena, Chodba u pokoje není místnost

- **L-04 Lustr jídelna je HUE** (ne non-HUE). Fáze trvalá, žádná Shelly fázi nespíná.
  SH-04 přetypováno z Plus 1PM na **Shelly i4** (čte event ze SW-J2). Obě tlačítka (SW-J2 jídelna + SW-D2 obývák) → detached → HA → Hue toggle.
  Cena: 3× Plus 1PM + 2× Plus 2PM + 4× i4 = **~6 500 Kč** (bylo ~7 000).
- **Kuchyň P-KU zjednodušena** — z rámečku dokumentujeme už jen zásuvku a tlačítko Lišta 3 (sdíleno s obývákem). LED A/B/digestoř odstraněny jako mimo scope. L-14 „Kuchyň okruhy" zrušeno (neexistující okruh). SH-E3 odstraněno z inventáře.
- **„Chodba u pokoje" není samostatná místnost** — je to jen umístění vypínače SW-CP v rámci **Horní předsíně**. P-CP zmigrováno do Horní předsíně s `location: U pokoje`. `rooms/05-chodba-u-pokoje.md` smazáno. ROOM_ORDER v generátoru upraveno.

### Topologické opravy: L-08 zrušeno, L-07 sdíleno s kuchyní

- **L-08 Lustr K zrušeno.** V nákresu "Lustr K" u obývákového SW-D2 je ve skutečnosti Lustr jídelna (L-04). SW-D2 posílá event přes SH-06 SW2 do HA, HA toggluje SH-04 v jídelně. L-04 má nyní 2 ovladače (SW-J2 attached, SW-D2 detached).
- **Lišta 3 v kuchyni = Lišta 3 v obýváku (L-07), 220V.** Kuchyňský stávající vypínač je paralelka k SW-D1 přes stávající schodišťákový drát do SH-06 SW1. Přidáno SW-KU-L3 do switches.yaml.
- **Okruhů celkem: 13 → 12.**

### Další topologická oprava: L-11 sloučeno do L-09

- `Předsíň strop` u obývákového vstupu (dříve L-11) je **totéž Hue svítidlo** jako `Předsíň strop` v dolní předsíni (L-09)
- L-11 odstraněno z circuits.yaml; SW-B1 přidán do L-09 controlled_from
- L-09 má nyní 3 ovládací tlačítka: SW-B1 (obývák) + SW-F2 (pracovna) + SW-G2 (dveře)
- HA toggle musí reagovat na 2 trigger entity: `event.sh_07_input_2` + `event.sh_08_input_1`
- **Okruhů celkem: 14 → 13**

### Vizualizace

- Přidán digitální nákres: `plates/prehled.svg` — svítidla (HUE/non-HUE + napětí 220V/24V) + rámečky + čáry vypínač→zařízení
- Per-místnost SVG: `plates/<room>.svg`
- `scripts/generate_plates.py` generátor z `devices/plates.yaml` + `devices/circuits.yaml`

## DRAFT v0.3 — 2026-04-22

### Rozšíření scope před objednávkou (pracovna, koupelna horní, WC)

Cíl: jedna objednávka Shelly pro celý dům (včetně ložnice). Přidány místnosti:

- **Pracovna:** 2× dvojvypínač u dveří, 4× Lišta 220V non-HUE, bez paralelek.
  Hardware: **2× Shelly Plus 2PM** (SH-14 za SW-PR-D1, SH-15 za SW-PR-D2), všechny kanály attached.
  Nové okruhy: L-30..L-33 (Lišta pracovna 1–4).
- **Koupelna horní:** 1× dvojvypínač u dveří (LED trafo 220V + HUE strop).
  Hardware: **1× Shelly Plus 2PM** (SH-16) — K1 attached pro LED trafo, K2 detached pro HUE event (O2 nezapojen).
  Nové okruhy: L-34 (LED trafo), L-35 (HUE strop).
  Zrcadlové světlo (SW-KH-ZRC) ponecháno v původním zapojení.
- **WC:** 1× dvojvypínač u dveří — levá buňka LED+ventilátor společně na jednom výstupu, pravá HUE strop.
  Hardware: **1× Shelly Plus 2PM** (SH-17) — K1 attached pro LED+vent, K2 detached pro HUE event (O2 nezapojen).
  Nové okruhy: L-36 (LED+vent), L-37 (HUE strop).

### Dokumentováno jen pro úplnost (beze změny, žádná Shelly)

- Garáž (SW-GA), koupelna dolní (SW-KD-1/2), pokoj hostů (SW-PH), prázdný pokoj (SW-PP),
  venkovní svítidlo pracovna (SW-PR-V), zrcadlo koupelna horní (SW-KH-ZRC)
- Souhrn v `rooms/11-ignored.md`

### Kusovník — ložnice už hotová, mimo objednávku

| Ks | Shelly typ | Kde | Volné | Chybí |
|---:|---|---|---:|---:|
| 3 | Shelly 1 Mini | SH-01/02/03 | 2 | **1** (~300 Kč) |
| 6 | Shelly Plus 2PM | SH-05/06 + SH-14/15 (pracovna) + SH-16 (koupelna h.) + SH-17 (WC) | 5 | **1** (~1 000 Kč) |
| 1 | Shelly i4 | SH-07 | 2 | 0 (1 zbyde rezerva) |

**Celkem k nákupu: ~1 700 Kč** (300 + 1 000 + rezerva 400 Kč KU68/WAGO).
Ložnice (SH-11..13: 2× i4 + 1× RGBW PM) **už hotová** — v provozu, mimo objednávku, volný inventář i4 nedotčen.
Plus 2PM po objednávce 0 rezervy — zvážit +1 ks navíc (~1 000 Kč).

### Místnosti beze změny

- Každá má vlastní `rooms/NN-*.md` (beze změny, jen dokumentace):
  - `11-garaz.md`, `12-koupelna-dolni.md`, `13-pokoj-hostu.md`, `14-prazdny-pokoj.md`
- `rooms/11-ignored.md` zrušeno (původní souhrnný soubor) — rozděleno na samostatné místnosti.

### Filozofická změna

- Philosophy v README upravena: přízemí je koncentrace v obýváku, patro/pracovna/koupelny/WC mají Shelly lokálně za vypínačem. Bez paralelek mimo přízemí.
- 2PM se stává "výchozím modelem pro dvojvypínač s HUE+non-HUE kombinací" (K1 attached, K2 detached, O2 nezapojen).

## Další plánované iterace

- [ ] Ověřit otevřené otázky z `open-questions.md`
- [ ] Doplnit `rooms/*.md` s rozpisem per místnost pro elektrikáře
- [ ] Vygenerovat SVG diagramy pro pracovna / koupelna horní / WC (zatím jen YAML)
- [ ] Případně vygenerovat schéma zapojení per krabice (svg nebo mermaid)
