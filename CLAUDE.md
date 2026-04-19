# Shelly instalace — projekt

## Kontext

Osazení Shelly zařízení v domě pro ovládání osvětlení. Integrace s Home Assistant, koexistence s Philips Hue (HUE okruhy) a stávajícími Shelly RGBW PM (LED strop obývák, LED jídelna).

**Fyzické vypínače:** ABB Tango s pružinkami = tlačítka (monostabilní, posílají eventy, ne stavy).

**Instalační omezení:** všechny krabice za vypínači jsou mělké → nutno proseknout hlouběji nebo použít KU68 prodlužovací kroužek.

## Principy návrhu

1. **HUE okruhy** (stmívatelná svítidla trvale pod proudem): tlačítko → i4 vstup (detached) → HA → Hue. Fáze v žárovce je trvalá, nikdy neodpojovat.
2. **Non-HUE okruhy** (spínané): Plus 1PM / 2PM spíná fázi. Tlačítko do SW vstupu (attached, funguje offline) nebo přes i4 (detached, přes HA).
3. **Vícemístné ovládání jednoho okruhu:** tlačítka paralelně na stejný SW vstup Shelly. Využití stávajících schodišťákových drátů jako signálových vodičů. Shelly vidí „někdo stiskl" → toggle. Funguje bez HA.
4. **3-cestné schodiště:** detached přes i4 v každé krabici → HA → SH-01. HA je nutná.
5. **Shelly umísťovat preferenčně u svítidel** (stropní krabice s víc místem), ne za vypínači (mělké krabice).

## Struktura projektu

- `devices/shelly.yaml` — inventář všech Shelly zařízení (ID, model, umístění, funkce)
- `devices/circuits.yaml` — světelné okruhy (co Shelly ovládá)
- `devices/switches.yaml` — fyzické vypínače, tlačítka, zapojení
- `rooms/` — rozpis per místnost (markdown, pro elektrikáře)
- `open-questions.md` — otevřené body k ověření
- `changelog.md` — historie změn specifikace

## Jak s tím pracovat v Claude Code

### Když něco měním:
1. Editovat příslušný YAML (`devices/*.yaml`) nebo markdown v `rooms/`
2. Zapsat změnu do `changelog.md` s datem a důvodem
3. Pokud to ovlivní otevřené otázky, updatovat `open-questions.md`
4. Regenerovat rozpis per místnost: `python scripts/generate_rooms.py` *(až bude)*

### Konzistence:
- Všechna zařízení mají ID prefix: `SH-` (Shelly), `L-` (okruh/light), `SW-` (switch/tlačítko)
- YAML je source of truth. Markdown v `rooms/` se generuje z YAML.
- Stávající zařízení mají prefix `SH-E` (existing).

### Konvence pojmenování HA entit:
- `switch.sh_01_schodiste` — Plus 1PM výstupy
- `light.l_08_lustr_k` — Hue skupiny / světla
- `event.sh_07_button_1` — tlačítková eventy z i4

## Aktuální stav

**Verze specifikace:** DRAFT v0.1
**Celkový počet nových Shelly:** 7 ks (3× Shelly 1 Mini, 2× Plus 2PM, 2× i4). Mini už nakoupené.
**Odhad k nákupu:** ~3 600 Kč (2× 2PM + 2× i4 + rezerva)

Viz `open-questions.md` pro seznam věcí k ověření.

## Zdroj

Původní nákres: fotografie ručně psaného schématu (`sources/nakres-puvodni.png`).
Chatová historie návrhu: Claude chat, duben 2026.
