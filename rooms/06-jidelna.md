# Jídelna

## Vypínače

1× dvojvypínač (SW-J) ovládá LED pásek 24V (stávající) a lustr Hue (L-04).

L-04 (Lustr jídelna) je **HUE** — fáze trvale pod proudem, žádná Shelly fázi nespíná. Tlačítka jen posílají eventy přes HA do Hue bridge.

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-J | J1 | L-13 LED 24V | stávající RGBW | SH-E2 SW | stávající (attached) |
| SW-J | J2 | L-04 Lustr jídelna | HUE | SH-04 IN1 | detached → HA → Hue |
| SW-D2 (obývák) | D2 | L-04 Lustr jídelna | HUE | SH-06 SW2 | detached → HA → Hue |

## Shelly v této místnosti

| ID | Model | Umístění | Vstupy / Výstup | Status |
|---|---|---|---|---|
| SH-04 | Shelly i4 | Za vypínačem SW-J | IN1 = SW-J2 (event), IN2-4 rezerva | nová |
| SH-E2 | Shelly RGBW PM | Stávající | L-13 | stávající |

## Důležité (HUE princip)

- L-04 Hue žárovka/pásek má **trvalou fázi** — **nikdy neodpojovat**.
- SH-04 je i4 (čte tlačítko), ne Plus 1PM (nespíná). Dřívější plán s Plus 1PM byl chybný.
- V HA automatizaci: `event.sh_04_input_1` → `light.toggle` na Hue skupinu.

## Cross-room paralelka

L-04 má druhé tlačítko v obývákovém rámečku (SW-D2 — v nákresu označeno „Lustr K", což je ale chybné). Oba eventy sbíhají se v HA na jednu Hue akci.

## Instalační poznámky

- Krabice za SW-J: **prosekat** nebo KU68 kroužek (pro SH-04 i4)
- Trvalá fáze k L-04 — z jističe přes stropní krabici k Hue žárovce
- Krabice u SW-J: tlačítkový vypínač, i4 za ním

## Ověřit

- [ ] Fyzická hloubka krabice za SW-J (pro i4)
- [ ] Trvalá fáze k lustru — existuje, nebo je třeba protáhnout?
- [ ] Konfigurace Hue entity v HA (Hue skupina pro L-04)
