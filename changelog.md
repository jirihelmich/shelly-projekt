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

## Další plánované iterace

- [ ] Ověřit otevřené otázky z `open-questions.md`
- [ ] Doplnit `rooms/*.md` s rozpisem per místnost pro elektrikáře
- [ ] Doplnit `ha/automations.yaml` s HA automatizacemi (schodiště toggle, Hue mapping)
- [ ] Případně vygenerovat schéma zapojení per krabice (svg nebo mermaid)
