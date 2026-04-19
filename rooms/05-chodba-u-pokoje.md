# Chodba u pokoje

## Vypínače

Jeden jednovypínač (SW-CP) — **paralelka k SW-H2** v horní předsíni (ovládá lustr horní předsíň).

| ID | Tlačítko | Okruh | Typ | Shelly vstup | Režim |
|---|---|---|---|---|---|
| SW-CP | CP | L-03 Lustr horní předs. | non-HUE | SH-03 SW1 | paralelně s SW-H2 přes stáv. schodišťák |

## Shelly v této místnosti

**Žádná.** Krabice bez Shelly — jen tlačítko a WAGO svorka.

## Zapojení

- Tlačítko SW-CP má jeden pól připojený přes stávající schodišťákový drát k **SH-03 SW1** (Shelly u lustru horní předsíně)
- Druhý pól připojen k signálovému potenciálu (L nebo N podle konfigurace SH-03)
- Stisk tlačítka → krátké zkratování SW1 → Shelly toggle → L-03 on/off
- **Funguje offline bez HA** (přímé paralelní zapojení)

## Instalační poznámky

- Stávající schodišťákový drát mezi SW-H2 (horní předsíň, u schodů) a SW-CP (chodba u pokoje) musí existovat — původně byl pro 3-cestné/schodišťákové zapojení, teď využit jako signálový.
- V krabici stačí WAGO svorka pro propojení tlačítka s příchozím drátem.

## Ověřit

- [ ] Stávající schodišťákový drát Horní předsíň (SW-H2) → Chodba u pokoje (SW-CP) existuje (2 volné vodiče)?
- [ ] Potvrzení umístění SW-CP (kde přesně v chodbě u pokoje?)
