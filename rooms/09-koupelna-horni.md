# Koupelna horní

## Vypínače

U dveří: **1× dvojvypínač** (SW-KH-D):
- levá buňka → LED trafo 220V (non-HUE)
- pravá buňka → HUE strop (detached, event)

Zrcadlové svítidlo má **samostatný vypínač** (SW-KH-ZRC), ponecháno v původním zapojení — **bez Shelly, beze změny**.

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-KH-D | KH-D-1 | L-34 LED trafo | non-HUE (LED-trafo, 220V) | SH-16 SW1 | attached |
| SW-KH-D | KH-D-2 | L-35 Strop | HUE | SH-16 SW2 | detached (event → HA → Hue) |
| SW-KH-ZRC | KH-ZRC | — (stávající zrcadlové) | stávající | — | beze změny |

## Shelly v této místnosti

| ID | Model | Umístění | Výstupy |
|---|---|---|---|
| SH-16 | Plus 2PM | Za SW-KH-D (u dveří) | O1→L-34 LED trafo; O2 nezapojen (L-35 je HUE) |

**Kanál K1 (attached):** spíná 220V primár LED trafa. Funguje offline.
**Kanál K2 (detached):** posílá event `sh_16_input_2` → HA → `light.toggle` na Hue skupinu. Vyžaduje HA.

## Instalační poznámky

- Krabice za SW-KH-D je mělká → **prosekat** nebo **KU68 kroužek**
- L-35 (HUE strop): **fáze trvale pod proudem** ⚡ — Shelly O2 nezapojen
- LED trafo pro L-34: ověřit toleranci ke spínání primáru (obvykle moderní elektronická trafa OK)
- **Koupelna = vlhké prostředí** — ověřit zóny podle ČSN 33 2000-7-701 a vzdálenost krabice od vany/sprchy; Shelly **nesmí** být v zóně 0/1

## Zapojení SH-16 K2 (detached)

- V HA: disable entity `switch.sh_16_output_2` (výstup není fyzicky zapojen)
- V HA: `event.sh_16_input_2` → `light.toggle` na Hue skupinu `light.koupelna_horni_strop`

## Ověřit

- [ ] Hloubka krabice za SW-KH-D (po proseknutí se vejde 2PM + svorky?)
- [ ] Zóna umístění krabice vůči vodě (ČSN 33 2000-7-701)
- [ ] Tolerance LED trafa ke spínání 220V primáru
- [ ] Hue setup pro Strop koupelna horní (skupina, adresace)
