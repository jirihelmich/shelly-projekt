# Home Assistant — automatizace a entity mapping

**Stav:** DRAFT, zatím jen kostra. Doplnit až se finalizuje hardware specifikace.

## Entity mapping

| Shelly device | HA entity (switch) | HA entity (event/button) |
|---|---|---|
| SH-01 | switch.sh_01_schodiste | — |
| SH-02 | switch.sh_02_led_pasek | — |
| SH-03 | switch.sh_03_lustr_horni_predsin | — |
| SH-04 | switch.sh_04_lustr_jidelna | — |
| SH-05 | switch.sh_05_lista_1, switch.sh_05_lista_2 | — |
| SH-06 | switch.sh_06_lista_3 | event.sh_06_input_2 (pro Lustr K) |
| SH-07 | — | event.sh_07_input_1/2/3 (pro A, B1, B2) |
| SH-08 | — | event.sh_08_input_1 (F2+G2 paralelně) |
| SH-09 | — | event.sh_09_input_1 (H1) |

## Hue entity mapping

| Okruh | HA entity | Ovládáno tlačítky |
|---|---|---|
| L-08 Lustr K | light.obyvak_lustr_k | event.sh_06_input_2 |
| L-09 Předsíň strop | light.dolni_predsin_strop | event.sh_07_input_2 (B1 obývák), event.sh_08_input_1 (F2+G2 paralelně) |
| L-10 Obývák strop | light.obyvak_strop | event.sh_07_input_3 |

## Automatizace — schodiště (2-cestné toggle)

```yaml
alias: Schodiště — 2-cestný toggle
description: Tlačítko schodiště v obýváku nebo horní předsíni přepne SH-01
trigger:
  - platform: state
    entity_id:
      - event.sh_07_input_1  # SW-A obývák
      - event.sh_09_input_1  # SW-H1 horní předsíň
    attribute: event_type
    to: single_push
action:
  - service: switch.toggle
    target:
      entity_id: switch.sh_01_schodiste
mode: single
```

## Automatizace — HUE okruhy (šablona)

```yaml
alias: Hue toggle — <okruh>
trigger:
  - platform: state
    entity_id: event.<shelly_input>
    attribute: event_type
    to: single_push
action:
  - service: light.toggle
    target:
      entity_id: light.<hue_entity>
```

Konkrétní instance doplnit pro L-08, L-09, L-10. L-09 má 2 trigger entity (event.sh_07_input_2 + event.sh_08_input_1) → stejný toggle.

## Scény (short / long / double)

**Short press:** toggle (výše)
**Long press:** TBD — návrhy:
- Obývák (SW-A, SW-B, SW-C, SW-D long): scéna "kino" (ztlumit strop, zapnout lišty na 30 %)
- Horní předsíň (SW-H long): zhasnout celé patro

**Double click:** TBD — návrhy:
- Obývák: scéna "čtení"
- Schodiště: noční režim (20 % na všech chodbách)

## TODO

- [ ] Ověřit přesná jména entit po instalaci Shelly (Shelly integration vs. MQTT)
- [ ] Rozhodnout detail scén
- [ ] Napsat automatizace pro Hue okruhy (4 ks)
- [ ] Napsat "master off" automatizaci (všechno zhasnout)
