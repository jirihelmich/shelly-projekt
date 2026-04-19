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

## Další plánované iterace

- [ ] Ověřit otevřené otázky z `open-questions.md`
- [ ] Doplnit `rooms/*.md` s rozpisem per místnost pro elektrikáře
- [ ] Doplnit `ha/automations.yaml` s HA automatizacemi (schodiště toggle, Hue mapping)
- [ ] Případně vygenerovat schéma zapojení per krabice (svg nebo mermaid)
