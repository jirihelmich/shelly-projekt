# Otevřené otázky / věci k ověření

Seznam věcí, které jsou v current draft **předpokládané**, ale nepotvrzené.
Každá z nich může ovlivnit kusovník nebo zapojení.

## P1 — blokující, nutno ověřit před objednávkou

### 1. Stávající schodišťákové dráty

- [ ] **L-02 LED pásek dolní předsíň**: skutečně existují 2 volné vodiče mezi krabicí SW-F1 (pracovna) a krabicí SW-G (dveře)? Lze jeden použít jako signálový k SH-02 SW1?
- [ ] **L-09 Předsíň strop (HUE)**: potvrzeno "schodišťák na obou okruzích". Ověřit fyzicky, že druhý volný drát existuje.
- [ ] **L-03 Lustr horní předsíň**: 2 volné vodiče mezi SW-H2 (u schodů) a SW-H3 (samostatný)?

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

### 6. L-11 vs. L-09 — dvě různá "předsíň strop"?

- [ ] V původním nákresu je "předsíň strop" u dvou různých vypínačů:
  - v obýváku u vstupu (B1) — to je L-11
  - u dveří dolní předsíně (F2, G2) — to je L-09
- [ ] Jsou to **dvě různá svítidla** v dolní předsíni, nebo **totéž svítidlo ovládané odjinud**?
- [ ] Pokud totéž → je potřeba sjednotit ovládání přes HA (všechna tlačítka B1, F2, G2 → jedna Hue skupina)

## P3 — optimalizace, není blokující

### 7. SH-06 K2 — zapojení výstupu O2

- [ ] Lustr K je HUE (trvale pod proudem). SH-06 K2 čte tlačítko SW-D2, ale výstup O2 nespíná nic.
- [ ] **Varianta A:** O2 nechat nezapojený (čistší, ale vypadá jako chyba pro elektrikáře)
- [ ] **Varianta B:** O2 propojit paralelně s L (fáze vždy zapnutá) — Hue žárovka dostane trvalou fázi, O2 je "zbytečný ale bezpečný"

**Doporučení:** Varianta A + komentář v elektrotechnické dokumentaci.

### 8. Offline fallback pro schodiště

- [ ] Schodiště je 3-cestné přes HA. Pokud HA spadne, žádný vypínač nefunguje.
- [ ] Stojí za to zapojit jedno tlačítko (nejbližší k SH-01) přímo do SH-01 SW1 jako fallback?

**Rozhodnutí:** ne, schodiště je chodba, v nouzi bez světla se projde.

### 9. Scény na long-press / double-click

- [ ] Které tlačítka budou mít jaké scény? (short = toggle, long = ?, double = ?)
- [ ] Dokumentovat v `ha/scenes.md` (zatím neexistuje)

## Log změn rozhodnutí

Viz `changelog.md`.
