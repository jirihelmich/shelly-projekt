# Schodiště (L-01)

## Princip

2-cestné ovládání jednoho svítidla (L-01) ze dvou míst, **attached přes paralelní drát** — funguje offline bez HA:
- Obývák (SW-A) attached přímo
- Horní předsíň u schodů (SW-H1) paralelka přes stávající schodišťákový drát

Spínání fáze: **SH-01 (Shelly 1 Mini) v obývákové konzoli za SW-A**. Stávající schodišťákový drát vede signál z SW-H1 na stejný vstup SH-01 SW1.

## Shelly u tohoto okruhu

| ID | Model | Umístění | Výstup |
|---|---|---|---|
| SH-01 | Shelly 1 Mini | Za SW-A v obývákové konzoli | O1 → L-01 |

## Ovládání

| Vypínač | Tlačítko | Cesta |
|---|---|---|
| SW-A (obývák) | A | attached → SH-01 SW1 → O1 toggle → L-01 |
| SW-H1 (horní předsíň) | H1 | paralelka přes stáv. drát → SH-01 SW1 (stejný vstup) |

## Zapojení

- Fáze k svítidlu schodiště je vedena z **SH-01 O1 v obývákové konzoli** (předtím vedená přímo z rozvaděče se odpojí, Shelly bude v cestě).
- SW-A i SW-H1 se sejdou na stejném vstupu SH-01 SW1 → obě tlačítka toggle identicky.
- Schodišťákový drát Obývák (SW-A) ↔ Horní předsíň (SW-H1) existuje a je použit jako signálový vodič.

## Offline chování

Funguje **offline bez HA**. Stisk libovolného tlačítka mechanicky toggluje SH-01.

## Trade-off

- SW-A je attached — **negeneruje HA event** pro scény (long-press, double-press).
- Pokud bychom chtěli scény z SW-A, přidat paralelní propoj na SH-07 IN1 (dnes rezerva).

## Instalační poznámky

- SH-01 do krabice za SW-A (obývák, mělká krabice → KU68 kroužek)
- Stávající schodišťákový drát využit jako signál — ověřit, že jsou 2 volné vodiče
