# Jídelna

## Stav před úpravou

2 jednovypínače v jednom rámečku, pořadí zleva: **Lustr** (SW-J2) — **LED** (SW-J1).

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-J2 | J2 (vlevo) | L-04 Lustr jídelna | HUE | SH-06 SW2 (v obýváku) | paralelka k SW-D2 přes stáv. schodišťák |
| SW-J1 | J1 (vpravo) | L-13 LED 24V | stávající RGBW PM | SH-E2 SW (přímo) | stávající attached |

## Stav po úpravě (plánované)

Do krabičky je přivedený **zásuvkový okruh** (220V s N+PE). Toho se využije ke sjednocení 2 jednovypínačů do **1 dvojvypínače** + přidání **zásuvky vlevo**:

| Pozice | Modul | Co dělá |
|---|---|---|
| 1 (vlevo) | Zásuvka 220V | nová zásuvka |
| 2.1 (levá buňka dvojvypínače) | Lustr (SW-J-LUSTR) | tlačítko 220V → paralelka přes stáv. schodišťák do SH-06 SW2 (HUE event) |
| 2.2 (pravá buňka dvojvypínače) | LED (SW-J-LED) | tlačítko 220V → **relé 220→24V** → vstup stávajícího SH-E2 |

**Trik s relé:** stejný princip jako u kuchyně (LED digestoř). Místo přímého 24V signálu má tlačítko 220V (z napájení zásuvkového okruhu) a relé převede stisk na 24V puls do vstupu SH-E2 RGBW PM (24V Shelly se nemění).

## Shelly v této místnosti

**Žádný Shelly v jídelně se nemění.** Stávající **SH-E2 RGBW PM** zůstává — jen vstup je nyní spínán přes relé 220→24V z 220V tlačítka místo dřívějšího 24V drátu.

L-04 (Hue lustr) ovládá Hue bridge; event přichází z SH-06 v obýváku přes stáv. schodišťák.

## Cross-room paralelka (L-04)

Stisk SW-J-LUSTR (jídelna, levá buňka) → přes stáv. schodišťákový drát → SH-06 SW2 v obýváku → event `sh_06_input_2` → HA → `light.toggle` na Hue skupinu.

Stisk SW-D2 v obývákovém rámečku → stejný vstup SH-06 SW2 → stejný event → stejná akce.

## Kusovník navíc (mimo Shelly)

| Ks | Položka | Účel |
|---:|---|---|
| 1 | Relé 220→24V (impulsní převodník signálu) | Před SH-E2 vstup pro LED jídelna (L-13) |
| 1 | Dvojvypínač pružinový | SW-J — sjednocení SW-J1+SW-J2 |
| 1 | Zásuvka 220V | Levá pozice nového rámečku |

## Instalační poznámky

- Krabice je napojena na **zásuvkový okruh** (220V s N+PE) — proto nový rámeček obsahuje zásuvku
- Stávající schodišťákový drát Obývák (SW-D) ↔ Jídelna (SW-J) zůstává využitý jako signální vodič pro Hue paralelku (vede 220V puls)
- Relé 220→24V umístit v krabici za dvojvypínačem (nebo v krabici u SH-E2, podle dostupnosti místa). Vstupní strana relé = 220V puls z pravé buňky tlačítka; výstupní strana = 24V puls do SW vstupu SH-E2.
- L-04 Hue lustr: trvalá fáze, nikdy neodpojovat

## Ověřit

- [ ] Stávající schodišťákový drát Obývák (SW-D) → Jídelna (SW-J) existuje (1 volný vodič pro 220V signál)
- [ ] Hue setup pro Lustr jídelna (skupina, adresace)
- [ ] Vhodný typ relé 220→24V (impulsní, krátký puls = krátký výstup) — kompatibilní se vstupem SH-E2 RGBW PM
- [ ] Hloubka krabice za dvojvypínačem (vejde se relé + svorky?)
