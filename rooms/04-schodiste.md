# Schodiště (L-01)

## Princip

2-cestné ovládání jednoho svítidla (L-01) ze dvou míst:
- Obývák (SW-A)
- Horní předsíň u schodů (SW-H1)

Spínání fáze: **SH-01 (Plus 1PM) u svítidla**.
Logika přes **Home Assistant** — obě tlačítka → events → HA automation → `switch.toggle SH-01`.

## Shelly v této místnosti

| ID | Model | Umístění | Výstup |
|---|---|---|---|
| SH-01 | Plus 1PM | U svítidla schodiště (stropní krabice) | O1 → L-01 |

## Ovládání (tlačítka jsou v jiných místnostech)

| Vypínač | Tlačítko | i4 v krabici | Cesta |
|---|---|---|---|
| SW-A (obývák) | A | SH-07 IN1 | event → HA → SH-01 toggle |
| SW-H1 (horní předsíň) | H1 | SH-09 IN1 | event → HA → SH-01 toggle |

## HA automatizace

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

## Offline fallback

**Žádný aktuálně.** Pokud HA spadne, žádný vypínač nefunguje. Schodiště je chodba → přijatelné riziko.

**Alternativa (pokud by se rozhodlo přidat):** nejbližší tlačítko (pravděpodobně SW-H1) zapojit paralelně přímo do SH-01 SW1 přes signálový drát. Vyžaduje novou kabeláž od vypínače k svítidlu.

## Instalační poznámky

- SH-01 do stropní krabice u svítidla — trvalé napájení L, N z jističe schodiště
- Výstup O1 spíná fázi do svítidla
- SW1 vstup SH-01: nezapojený (pokud nebude offline fallback)

## Ověřit

- [ ] Stropní krabice u svítidla schodiště: dostupná, dostatek místa pro Plus 1PM?
- [ ] Kde je jistič schodiště? (pro přivedení L, N k SH-01)
