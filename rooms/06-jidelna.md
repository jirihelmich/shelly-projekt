# Jídelna

## Vypínače

1× dvojvypínač (SW-J) ovládá LED pásek 24V (stávající) a lustr 220V (nový).

L-04 (Lustr jídelna) má navíc druhé ovládací tlačítko v obýváku (SW-D2 — v nákresu chybně označeno „Lustr K"), event přes HA toggluje SH-04.

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-J | J1 | L-13 LED 24V | stávající RGBW | SH-E2 SW | stávající |
| SW-J | J2 | L-04 Lustr 220V | non-HUE | SH-04 SW1 (u lustru) | attached |
| SW-D2 (obývák) | D2 | L-04 Lustr 220V | non-HUE | SH-06 SW2 | detached → HA → SH-04 toggle |

## Shelly v této místnosti

| ID | Model | Umístění | Výstup | Status |
|---|---|---|---|---|
| SH-04 | Plus 1PM | U lustru jídelny (stropní krabice) | O1 → L-04 | nová |
| SH-E2 | Shelly RGBW PM | Stávající | L-13 | stávající |

## Žádná i4 v jídelně

- J1 tlačítko → přímo do stávající SH-E2 (stávající zapojení, nemění se)
- J2 tlačítko → přímo do SH-04 SW1 (attached)
- Žádné detached okruhy, žádné HUE okruhy → i4 není potřeba

## Instalační poznámky

- SH-04 u lustru — stropní krabice by měla mít místo
- Krabice u SW-J: pouze tlačítkový vypínač, Shelly je jinde → minimum zabraného místa
- Signálové vodiče k SH-04 SW1: z krabice SW-J k lustru

## Ověřit

- [ ] Dostupnost stropní krabice u lustru pro SH-04
- [ ] Stávající zapojení SH-E2 a SW-J1 — funguje ok, nic se nemění?
