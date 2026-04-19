# Jídelna

## Vypínače

2 jednovypínače v jednom rámečku (SW-J1 + SW-J2):

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-J1 | J1 | L-13 LED 24V | stávající RGBW | SH-E2 SW | stávající (attached) |
| SW-J2 | J2 | L-04 Lustr jídelna | HUE | SH-06 SW2 (v obýváku) | paralelně s SW-D2 přes stáv. schodišťák |

L-04 (Lustr jídelna) je **HUE** — fáze trvale pod proudem. Tlačítka jen posílají event přes HA do Hue bridge.

## Shelly v této místnosti

**Žádný nový Shelly v jídelně.**

- L-13: stávající SH-E2 (RGBW PM, beze změny)
- L-04: spíná Hue bridge (ne Shelly), event přichází z SH-06 v obýváku

## Cross-room paralelka (L-04)

Stisk SW-J2 v jídelně → přes stáv. schodišťákový drát → SH-06 SW2 v obýváku → event `sh_06_input_2` → HA → `light.toggle` na Hue skupinu.

Stisk SW-D2 v obývákovém rámečku → stejný vstup SH-06 SW2 → stejný event → stejná akce.

Oba stisky jsou z pohledu Shelly nerozlišitelné (jeden vstup), HA nemusí řešit dva zdroje.

## Instalační poznámky

- Krabice za SW-J: **pouze tlačítkový vypínač a WAGO svorky** (žádná Shelly → plochá krabice stačí)
- Stávající schodišťákový drát Obývák (SW-D2) ↔ Jídelna (SW-J2) musí existovat — typicky 2 vodiče volně k dispozici
- L-04 Hue lustr: trvalá fáze, nikdy neodpojovat

## Ověřit

- [ ] Stávající schodišťákový drát Obývák (SW-D) → Jídelna (SW-J) existuje (2 volné vodiče)?
- [ ] Hue setup pro Lustr jídelna (skupina, adresace)
