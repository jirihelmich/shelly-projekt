# Otevřené otázky / věci k ověření

Seznam věcí, které jsou v current draft **předpokládané**, ale nepotvrzené.
Každá z nich může ovlivnit kusovník nebo zapojení.

## P1 — blokující, nutno ověřit před objednávkou

### 1. Stávající schodišťákové dráty

- [ ] **L-02 LED pásek dolní předsíň**: skutečně existují 2 volné vodiče mezi krabicí SW-F1 (pracovna) a krabicí SW-G (dveře)? Lze jeden použít jako signálový k SH-02 SW1?
- [ ] **L-09 Předsíň strop (HUE)**: potvrzeno "schodišťák na obou okruzích". Ověřit fyzicky, že druhý volný drát existuje.
- [ ] **L-03 Lustr horní předsíň**: 2 volné vodiče mezi SW-H2 (u schodů v horní předsíni) a SW-CP (chodba u pokoje)?
- [ ] **L-07 Lišta 3**: existuje drát mezi SW-D v obýváku a kuchyňským rámečkem (paralelka pro Lišta 3)?

**Fallback pokud dráty nejsou:** místo paralelního zapojení přes existující dráty použít i4 navíc za krabicí bez Shelly → přidá +2× i4 (+1200 Kč).

### 2. Trafo LED pásku

- [ ] Toleruje stávající trafo časté spínání 230V primáru? Moderní elektronická LED trafa obvykle ano. Staré EI/toroidní mohou mít inrush problém.

**Fallback:** výměna trafa za moderní LED driver tolerantní ke spínání primáru.

### 3. Rozměry krabic

- [ ] Všechny krabice jsou potvrzeně mělké → musí se prosekat / frézovat
- [ ] Ověřit, že po proseknutí se vejde Shelly + svorkovnice + rezerva kabelu
- [ ] Pro krabice s víc Shelly (např. obývák: SH-05 + SH-06 + SH-07 v řadě) ověřit, že jsou fyzicky vedle sebe a jsou propojitelné

**Fallback:** KU68 prodlužovací kroužek (Kopos KPL64), objednat 10 ks do zásoby.

## P2 — důležité, může ovlivnit kusovník

### 4. Umístění Plus 1PM u svítidel

- [ ] **SH-01 schodiště**: stropní krabice u svítidla — existuje? Dostupná?
- [ ] **SH-03 horní předsíň lustr**: stropní krabice?
- [ ] **SH-04 jídelna lustr**: stropní krabice?
- [ ] **SH-02 u trafa**: kde přesně je trafo? Instalační prostor s přístupem?

**Fallback:** pokud není stropní krabice dostupná, Plus 1PM za vypínač → mělká krabice → problém s místem.

### 5. Obývák — rozmístění vypínačů

- [ ] SW-A, SW-B, SW-C, SW-D jsou v jednom rámečku (4× dvojvypínač v řadě)? Nebo rozdělené?
- [ ] SH-07 (i4) má pokrýt tlačítka A, B1, B2 (3 vstupy). Pokud SW-A je v samostatné krabici daleko od SW-B, potřeba +1× i4.

### 6. ~~L-11 vs. L-09 — dvě různá "předsíň strop"?~~ — VYŘEŠENO (2026-04-19)

**Výsledek:** je to totéž svítidlo (L-11 bylo sloučeno do L-09). Ovládá se ze 3 míst:
- SW-B1 obývák vstup (SH-07 IN2 → HA → Hue)
- SW-F2 dolní předsíň u pracovny (SH-08 IN1 → HA → Hue, paralelně s G2)
- SW-G2 dolní předsíň u dveří (SH-08 IN1 → HA → Hue, paralelně s F2)

HA automatizace: 2 trigger entity (sh_07_input_2 + sh_08_input_1) → `light.toggle` na Hue skupinu.

## P3 — optimalizace, není blokující

### 7. SH-06 K2 — zapojení výstupu O2

- [ ] SW-D2 čte SH-06 SW2 jako event (detached). Tlačítko ve skutečnosti ovládá Lustr jídelna (L-04) přes HA → SH-04.
- [ ] Výstup O2 SH-06 nespíná nic (L-04 se spíná v jídelně přes SH-04).
- [ ] **Varianta A:** O2 nechat nezapojený (čistší)
- [ ] **Varianta B:** O2 propojit s L (fáze trvalá) — zbytečné, ale bezpečné

**Doporučení:** Varianta A + komentář v elektrotechnické dokumentaci.

### 8. Offline fallback pro schodiště

- [ ] Schodiště je 2-cestné přes HA (SW-A obývák, SW-H1 horní předsíň). Pokud HA spadne, žádný vypínač nefunguje.
- [ ] Stojí za to zapojit jedno tlačítko (nejbližší k SH-01) přímo do SH-01 SW1 jako fallback?

**Rozhodnutí:** ne, schodiště je chodba, v nouzi bez světla se projde.

### 9. Scény na long-press / double-click

- [ ] Které tlačítka budou mít jaké scény? (short = toggle, long = ?, double = ?)
- [ ] Dokumentovat v `ha/scenes.md` (zatím neexistuje)

## Log změn rozhodnutí

Viz `changelog.md`.
