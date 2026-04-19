#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Generuje SVG vizualizaci rámečků (plates) per místnost z devices/plates.yaml."""

from __future__ import annotations

import html
import re
from collections import defaultdict
from pathlib import Path

import yaml

PROJECT = Path(__file__).resolve().parent.parent
PLATES_YAML = PROJECT / "devices" / "plates.yaml"
CIRCUITS_YAML = PROJECT / "devices" / "circuits.yaml"
SHELLY_YAML = PROJECT / "devices" / "shelly.yaml"
OUTPUT_DIR = PROJECT / "plates"

COLORS = {
    "HUE": "#e9d5ff",       # fialová = Hue (fáze trvalá) — odlišně od trafo
    "non-HUE": "#dbeafe",   # chladná modrá = klasický spínaný 230V okruh
    "LED-trafo": "#fef3c7", # žlutá = LED přes driver/trafo (Shelly spíná 220V)
    "RGBW-PM": "#dcfce7",   # zelená = LED 24V přímo přes Shelly RGBW PM
    "neutral": "#f3f4f6",   # šedá = zásuvka / neklasifikovaný modul
}
VOLTAGE_COLORS = {
    "220V": "#1e3a8a",  # tmavě modrá
    "24V": "#047857",   # zelená
}
BORDER = "#374151"
TEXT = "#111827"
MUTED = "#6b7280"


def classify_circuit(c: dict) -> tuple[str, str | None]:
    """Vrátí (tag, voltage) pro okruh z circuits.yaml."""
    t = (c.get("type") or "").strip()
    t_upper = t.upper()
    if t_upper.startswith("HUE"):
        tag = "HUE"
    elif "RGBW" in t_upper or "RGBW-PM" in t_upper:
        tag = "RGBW-PM"
    elif "TRAFO" in t_upper or "LED-TRAFO" in t_upper:
        tag = "LED-trafo"
    else:
        tag = "non-HUE"
    v = (c.get("voltage") or "").strip()
    voltage: str | None = None
    if "230" in v or "220" in v:
        voltage = "220V"
    elif "24" in v:
        voltage = "24V"
    return tag, voltage


def load_circuits() -> dict[str, dict]:
    data = yaml.safe_load(CIRCUITS_YAML.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for c in data["circuits"]:
        tag, voltage = classify_circuit(c)
        out[c["id"]] = {
            "name": c.get("name", c["id"]),
            "room": c.get("room", ""),
            "tag": tag,
            "voltage": voltage,
            "dimmable": c.get("dimmable"),
            "raw": c,
        }
    return out


CIRCUITS: dict[str, dict] = {}


def shelly_mount_type(sh: dict) -> str:
    """Heuristika: 'at_switch' pokud je Shelly za vypínačem, jinak 'at_device'."""
    loc = (sh.get("location") or "").lower()
    if "za vypínač" in loc:
        return "at_switch"
    return "at_device"


def load_shelly() -> list[dict]:
    data = yaml.safe_load(SHELLY_YAML.read_text(encoding="utf-8"))
    out: list[dict] = []
    for s in data.get("devices", []):
        s = dict(s)
        s["mount"] = shelly_mount_type(s)
        out.append(s)
    return out


SHELLY: list[dict] = []

CELL_W = 110
CELL_H = 84
SOCKET_W = 90
PADDING = 10
LABEL_H = 18  # prostor nahoře pro ID a tag badge
PLATE_GAP = 18
MODULE_GAP = 8  # mezera mezi moduly (jednotlivými mechanismy) v rámečku
COLUMN_GAP = 48
TITLE_H = 54
LOC_HEADER_H = 28
BOTTOM_PAD = 56


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def slugify(s: str) -> str:
    table = str.maketrans(
        "áéěíóůúýžščřďťňÁÉĚÍÓŮÚÝŽŠČŘĎŤŇ",
        "aeeiouuyzscrdtnAEEIOUUYZSCRDTN",
    )
    s = s.translate(table).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def component_width(c: dict) -> int:
    t = c["type"]
    if t == "socket":
        return SOCKET_W
    if t == "single_switch":
        return CELL_W
    if t == "double_switch":
        return CELL_W * 2
    return CELL_W


def plate_dims(plate: dict) -> tuple[int, int]:
    orientation = plate.get("orientation", "horizontal")
    comps = plate["components"]
    gap_total = MODULE_GAP * max(0, len(comps) - 1)
    if orientation == "vertical":
        w = max(component_width(c) for c in comps) + 2 * PADDING
        h = len(comps) * CELL_H + gap_total + LABEL_H + 2 * PADDING
    else:
        w = sum(component_width(c) for c in comps) + gap_total + 2 * PADDING
        h = CELL_H + LABEL_H + 2 * PADDING
    return w, h


def voltage_badge(x: int, y: int, voltage: str) -> list[str]:
    """Badge ~32x14 s textem '220V' nebo '24V'."""
    color = VOLTAGE_COLORS[voltage]
    w = 32
    return [
        f'<rect x="{x-w}" y="{y}" width="{w}" height="13" fill="white" '
        f'stroke="{color}" stroke-width="1" rx="2" ry="2"/>',
        f'<text x="{x-w/2}" y="{y+9.5}" text-anchor="middle" '
        f'font-family="sans-serif" font-size="8" font-weight="700" fill="{color}">{voltage}</text>',
    ]


def render_socket(c: dict, x: int, y: int) -> list[str]:
    cx = x + SOCKET_W / 2
    cy = y + CELL_H / 2
    cell = c["cells"][0]
    label = esc(cell["label"])
    voltage = cell.get("voltage", "220V")
    parts = [
        f'<rect x="{x}" y="{y}" width="{SOCKET_W}" height="{CELL_H}" fill="{COLORS["neutral"]}" stroke="{BORDER}" stroke-width="1.5"/>',
        f'<circle cx="{cx}" cy="{cy-6}" r="22" fill="white" stroke="{BORDER}" stroke-width="1.5"/>',
        f'<circle cx="{cx-7}" cy="{cy-6}" r="2.5" fill="{BORDER}"/>',
        f'<circle cx="{cx+7}" cy="{cy-6}" r="2.5" fill="{BORDER}"/>',
        f'<text x="{cx}" y="{y + CELL_H - 8}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="{TEXT}">{label}</text>',
    ]
    if voltage in VOLTAGE_COLORS:
        parts.extend(voltage_badge(x + SOCKET_W - 4, y + 4, voltage))
    return parts


def cell_tag_voltage(cell: dict) -> tuple[str, str | None]:
    circ = cell.get("circuit")
    info = CIRCUITS.get(circ) if circ else None
    tag = info["tag"] if info else "neutral"
    voltage = cell.get("voltage") or (info["voltage"] if info else None)
    return tag, voltage


def render_cell_bg(cell: dict, x: int, y: int, w: int) -> list[str]:
    tag, _ = cell_tag_voltage(cell)
    bg = COLORS.get(tag, COLORS["neutral"])
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{CELL_H}" fill="{bg}"/>']


def render_cell_content(cell: dict, x: int, y: int, w: int) -> list[str]:
    """Klapka + label + circuit + voltage badge (bez vnějšího borderu)."""
    parts: list[str] = []
    _, voltage = cell_tag_voltage(cell)
    circ = cell.get("circuit")

    inner_x = x + 14
    inner_y = y + 12
    inner_w = w - 28
    inner_h = CELL_H - 44
    blind = cell.get("blind")
    klapka_fill = "#f3f4f6" if blind else "white"
    parts.append(
        f'<rect x="{inner_x}" y="{inner_y}" width="{inner_w}" height="{inner_h}" '
        f'fill="{klapka_fill}" stroke="{BORDER}" stroke-width="1" rx="3" ry="3"/>'
    )
    if blind:
        parts.append(
            f'<text x="{x + w/2}" y="{inner_y + inner_h/2 + 3}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="10" font-style="italic" fill="{MUTED}">neobsazeno</text>'
        )
    label = esc(cell["label"])
    parts.append(
        f'<text x="{x + w/2}" y="{y + CELL_H - 19}" text-anchor="middle" '
        f'font-family="sans-serif" font-size="11" font-weight="600" fill="{TEXT}">{label}</text>'
    )
    if circ:
        parts.append(
            f'<text x="{x + w/2}" y="{y + CELL_H - 5}" text-anchor="middle" '
            f'font-family="monospace" font-size="9" fill="{MUTED}">{esc(circ)}</text>'
        )
    if voltage:
        parts.extend(voltage_badge(x + w - 4, y + 4, voltage))
    return parts


def render_cell(cell: dict, x: int, y: int, w: int) -> list[str]:
    """Kompletní buňka samostatného modulu: pozadí + border + obsah."""
    parts = render_cell_bg(cell, x, y, w)
    parts.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{CELL_H}" fill="none" '
        f'stroke="{BORDER}" stroke-width="1.5"/>'
    )
    parts.extend(render_cell_content(cell, x, y, w))
    return parts


def render_component(c: dict, x: int, y: int) -> tuple[list[str], int]:
    t = c["type"]
    if t == "socket":
        return render_socket(c, x, y), SOCKET_W
    if t == "single_switch":
        return render_cell(c["cells"][0], x, y, CELL_W), CELL_W
    if t == "double_switch":
        w = CELL_W * 2
        parts: list[str] = []
        # Pozadí per buňka (různé tagy možné)
        for i, cell in enumerate(c["cells"]):
            parts.extend(render_cell_bg(cell, x + CELL_W * i, y, CELL_W))
        # Jeden vnější border kolem celého modulu — vizuálně JEDEN mechanismus
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{CELL_H}" fill="none" '
            f'stroke="{BORDER}" stroke-width="1.5"/>'
        )
        # Vnitřní čárkovaný předěl mezi 2 tlačítky
        parts.append(
            f'<line x1="{x + CELL_W}" y1="{y+6}" x2="{x + CELL_W}" y2="{y+CELL_H-6}" '
            f'stroke="{BORDER}" stroke-width="1" stroke-dasharray="3,3"/>'
        )
        # Obsah per buňka
        for i, cell in enumerate(c["cells"]):
            parts.extend(render_cell_content(cell, x + CELL_W * i, y, CELL_W))
        return parts, w
    return [], 0


def render_plate(plate: dict, x: int, y: int) -> tuple[list[str], int, int]:
    w, h = plate_dims(plate)

    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f9fafb" '
        f'stroke="{BORDER}" stroke-width="2" rx="8" ry="8"/>',
    ]
    orientation = plate.get("orientation", "horizontal")
    inner_w = w - 2 * PADDING
    cell_y = y + PADDING + LABEL_H
    if orientation == "vertical":
        for c in plate["components"]:
            cw = component_width(c)
            cx = x + PADDING + (inner_w - cw) / 2
            comp_parts, _ = render_component(c, cx, cell_y)
            parts.extend(comp_parts)
            cell_y += CELL_H + MODULE_GAP
    else:
        cx = x + PADDING
        for c in plate["components"]:
            comp_parts, cw = render_component(c, cx, cell_y)
            parts.extend(comp_parts)
            cx += cw + MODULE_GAP

    parts.append(
        f'<text x="{x+10}" y="{y + PADDING + 10}" font-family="monospace" font-size="9" fill="{MUTED}">{esc(plate["id"])}</text>'
    )
    return parts, w, h


def render_room(room: str, plates: list[dict]) -> str:
    by_location: dict[str, list[dict]] = defaultdict(list)
    for p in plates:
        by_location[p.get("location") or "—"].append(p)
    for loc in by_location:
        by_location[loc].sort(key=lambda p: p.get("stack_position", 0))

    columns = []
    for loc, ps in by_location.items():
        col_w = max(plate_dims(p)[0] for p in ps)
        columns.append((loc, ps, col_w))

    total_w = sum(w for _, _, w in columns) + COLUMN_GAP * (len(columns) - 1) + 40
    max_col_h = 0
    for _, ps, _ in columns:
        notes_extra = sum(16 for p in ps if p.get("note"))
        col_h = sum(plate_dims(p)[1] for p in ps) + PLATE_GAP * (len(ps) - 1) + notes_extra
        max_col_h = max(max_col_h, col_h)
    total_h = TITLE_H + LOC_HEADER_H + max_col_h + BOTTOM_PAD

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(total_w)} {int(total_h)}" '
        f'width="{int(total_w)}" height="{int(total_h)}" font-family="sans-serif">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="20" y="32" font-size="22" font-weight="700" fill="{TEXT}">{esc(room)}</text>',
        f'<line x1="20" y1="42" x2="{int(total_w)-20}" y2="42" stroke="{BORDER}" stroke-width="1"/>',
    ]

    cx = 20
    for loc, ps, col_w in columns:
        parts.append(
            f'<text x="{cx}" y="{TITLE_H + 18}" font-size="12" font-style="italic" fill="{MUTED}">{esc(loc)}</text>'
        )
        cy = TITLE_H + LOC_HEADER_H
        for plate in ps:
            plate_parts, pw, ph = render_plate(plate, cx, cy)
            parts.extend(plate_parts)
            cy += ph
            note = plate.get("note")
            if note:
                parts.append(
                    f'<text x="{cx}" y="{cy + 12}" font-size="10" fill="{MUTED}">{esc(note)}</text>'
                )
                cy += 16
            cy += PLATE_GAP
        cx += col_w + COLUMN_GAP

    parts.extend(render_legend(20, total_h - 24))
    parts.append("</svg>")
    return "\n".join(parts)


def render_legend(x: int, y: int) -> list[str]:
    parts: list[str] = []
    # Tags (HUE, non-HUE, LED-trafo, RGBW-PM)
    for label in ("HUE", "non-HUE", "LED-trafo", "RGBW-PM"):
        color = COLORS[label]
        parts.append(
            f'<rect x="{x}" y="{y-11}" width="14" height="14" fill="{color}" '
            f'stroke="{BORDER}" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x+20}" y="{y}" font-size="11" fill="{TEXT}">{esc(label)}</text>'
        )
        x += 110
    # Voltage badges
    for v in ("220V", "24V"):
        parts.extend(voltage_badge(x + 32, y - 11, v))
        parts.append(
            f'<text x="{x+38}" y="{y}" font-size="11" fill="{TEXT}">{esc(v)}</text>'
        )
        x += 100
    return parts


ROOM_ORDER = [
    "Obývák",
    "Schodiště",
    "Horní předsíň",
    "Dolní předsíň",
    "Kuchyň",
    "Jídelna",
]


def normalize_device_room(r: str) -> str:
    r = r.strip()
    if r.startswith("Obývák"):
        return "Obývák"
    if r.startswith("Dolní"):
        return "Dolní předsíň"
    if r.startswith("Horní"):
        return "Horní předsíň"
    if r.startswith("Kuchyň") or r.startswith("Kuchyn"):
        return "Kuchyň"
    return r


def devices_by_room() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    for circ_id, info in CIRCUITS.items():
        room = normalize_device_room(info.get("room", ""))
        if not room:
            continue
        out[room].append({"id": circ_id, **info})
    for room in out:
        out[room].sort(key=lambda d: d["id"])
    return out


def shelly_for_plate(plate: dict) -> list[dict]:
    """Vrátí seznam Shelly umístěných 'za' tímto rámečkem (at_switch mount)."""
    plate_switch_refs = set()
    for comp in plate.get("components", []):
        sr = comp.get("switch_ref")
        if sr:
            plate_switch_refs.add(sr)
    out = []
    for sh in SHELLY:
        if sh.get("mount") != "at_switch":
            continue
        ctrl = sh.get("controlled_by") or []
        # Shelly.controlled_by zahrnuje konkrétní buttony (SW-A, SW-C1 atd.);
        # sjednotit na prefix "SW-X" pro porovnání.
        ctrl_roots = {c.split("-")[0] + "-" + c.split("-")[1][0] if "-" in c and len(c.split("-")[1]) > 1 and c.split("-")[1][1:].isdigit() else c for c in ctrl}
        # jednodušší: kontrola, zda jakýkoliv controlled_by začíná s některým switch_ref
        for sw_ref in plate_switch_refs:
            if any(c == sw_ref or c.startswith(sw_ref) for c in ctrl):
                out.append(sh)
                break
    return out


def shelly_for_circuit(circuit_id: str) -> list[dict]:
    """Vrátí Shelly, která ovládají / jsou u tohoto svítidla (at_device mount)."""
    info = CIRCUITS.get(circuit_id, {})
    raw = info.get("raw", {})
    switched_by = raw.get("switched_by")
    if not switched_by:
        return []
    # switched_by může být 'SH-01' nebo 'SH-05 K1' — vezmeme první token
    sh_id = switched_by.split()[0] if isinstance(switched_by, str) else None
    if not sh_id:
        return []
    return [sh for sh in SHELLY if sh["id"] == sh_id and sh.get("mount") == "at_device"]


SHELLY_BADGE_W = 58
SHELLY_BADGE_H = 16
SHELLY_BG = "#1f2937"  # tmavě šedá
SHELLY_FG = "#f9fafb"


def render_shelly_badge(sh_id: str, model: str, x: float, y: float) -> list[str]:
    """Malá tmavá pilulka 'SH-XX' — na rámečku nebo u svítidla."""
    label = f"📦 {sh_id}"
    return [
        f'<rect x="{x}" y="{y}" width="{SHELLY_BADGE_W}" height="{SHELLY_BADGE_H}" '
        f'fill="{SHELLY_BG}" rx="3" ry="3"/>',
        f'<text x="{x + SHELLY_BADGE_W/2}" y="{y + SHELLY_BADGE_H - 4}" text-anchor="middle" '
        f'font-family="monospace" font-size="10" font-weight="700" fill="{SHELLY_FG}">{esc(sh_id)}</text>',
    ]


DEVICE_PILL_W = 156
DEVICE_PILL_H = 36
DEVICE_PILL_GAP_Y = 8
DEVICE_STRIP_TITLE_H = 18
DEVICE_COL_GAP = 28  # mezera mezi rámečky a sloupcem svítidel


def render_device_pill(dev: dict, x: int, y: int) -> list[str]:
    tag = dev["tag"]
    fill = COLORS.get(tag, COLORS["neutral"])
    voltage = dev.get("voltage")
    parts = [
        f'<rect x="{x}" y="{y}" width="{DEVICE_PILL_W}" height="{DEVICE_PILL_H}" '
        f'fill="{fill}" stroke="{BORDER}" stroke-width="1" rx="14" ry="14"/>',
        f'<text x="{x+10}" y="{y+13}" font-family="monospace" font-size="8" fill="{MUTED}">{esc(dev["id"])}</text>',
        f'<text x="{x+10}" y="{y+28}" font-size="11" font-weight="600" fill="{TEXT}">{esc(dev["name"])}</text>',
    ]
    if voltage:
        parts.extend(voltage_badge(x + DEVICE_PILL_W - 6, y + 4, voltage))
    return parts


def device_col_dims(devices: list[dict]) -> tuple[int, int]:
    """Vrátí (w, h) sloupce svítidel: pillulky stackované vertikálně."""
    if not devices:
        return 0, 0
    w = DEVICE_PILL_W
    h = DEVICE_STRIP_TITLE_H + len(devices) * (DEVICE_PILL_H + DEVICE_PILL_GAP_Y) - DEVICE_PILL_GAP_Y
    return w, h

CONNECTION_PALETTE = [
    "#dc2626",  # red
    "#2563eb",  # blue
    "#16a34a",  # green
    "#c026d3",  # purple
    "#ea580c",  # orange
    "#0891b2",  # cyan
    "#ca8a04",  # amber
    "#be185d",  # pink
]

ROOM_BOX_PAD = 16
ROOM_TITLE_H = 26
ROOM_GAP = 30
OVERVIEW_TOP_PAD = 90  # prostor nad místnostmi (title + podtitle)


def cell_anchors_in_plate(plate: dict, plate_x: float, plate_y: float):
    """Yield (circuit_id, anchor_x, anchor_y) — střed buňky, pro kreslení čar vypínač→zařízení."""
    orientation = plate.get("orientation", "horizontal")
    pw, _ = plate_dims(plate)
    inner_w = pw - 2 * PADDING
    cell_y = plate_y + PADDING + LABEL_H

    if orientation == "vertical":
        for comp in plate["components"]:
            cw = component_width(comp)
            cx_base = plate_x + PADDING + (inner_w - cw) / 2
            if comp["type"] != "socket":
                for i, cell in enumerate(comp.get("cells", [])):
                    circ = cell.get("circuit")
                    if not circ:
                        continue
                    if comp["type"] == "double_switch":
                        ccx = cx_base + CELL_W * i + CELL_W / 2
                    else:
                        ccx = cx_base + CELL_W / 2
                    yield circ, ccx, cell_y + CELL_H / 2
            cell_y += CELL_H + MODULE_GAP
    else:
        cx_base = plate_x + PADDING
        for comp in plate["components"]:
            cw = component_width(comp)
            if comp["type"] != "socket":
                for i, cell in enumerate(comp.get("cells", [])):
                    circ = cell.get("circuit")
                    if not circ:
                        continue
                    if comp["type"] == "double_switch":
                        ccx = cx_base + CELL_W * i + CELL_W / 2
                    else:
                        ccx = cx_base + CELL_W / 2
                    yield circ, ccx, cell_y + CELL_H / 2
            cx_base += cw + MODULE_GAP


def plates_for_mode(plates: list[dict], mode: str) -> list[dict]:
    """Filtruje plates pro daný mode ('before' nebo 'after')."""
    out = []
    for p in plates:
        state = p.get("state", "both")
        if mode == "before" and state == "after_only":
            continue
        if mode == "after" and state == "before_only":
            continue
        out.append(p)
    return out


def render_overview(plates: list[dict], mode: str = "before") -> str:
    plates = plates_for_mode(plates, mode)
    by_room: dict[str, list[dict]] = defaultdict(list)
    for p in plates:
        by_room[p["room"]].append(p)

    devices_per_room = devices_by_room()

    # Sjednocená sada místností — i ty bez plates (např. Schodiště) se objeví, pokud mají zařízení.
    all_rooms = set(by_room.keys()) | set(devices_per_room.keys())
    rooms = [r for r in ROOM_ORDER if r in all_rooms] + sorted(
        r for r in all_rooms if r not in ROOM_ORDER
    )

    # Pre-compute plate layout within each room box (locations = sub-columns).
    room_blocks = []
    for room in rooms:
        plates_in_room = by_room.get(room, [])
        by_location: dict[str, list[dict]] = defaultdict(list)
        for p in plates_in_room:
            by_location[p.get("location") or ""].append(p)
        for loc in by_location:
            by_location[loc].sort(key=lambda p: p.get("stack_position", 0))

        loc_columns = []
        for loc, ps in by_location.items():
            col_w = max(plate_dims(p)[0] for p in ps)
            col_h = sum(plate_dims(p)[1] for p in ps) + PLATE_GAP * (len(ps) - 1)
            loc_columns.append((loc, ps, col_w, col_h))

        plates_inner_w = (
            sum(w for _, _, w, _ in loc_columns) + COLUMN_GAP * (len(loc_columns) - 1)
            if loc_columns else 0
        )
        plates_inner_h = (
            max(h for _, _, _, h in loc_columns) + LOC_HEADER_H
            if loc_columns else 0
        )

        # Device column (vpravo od rámečků, pilulky stackované vertikálně)
        devs = devices_per_room.get(room, [])
        dev_col_w, dev_col_h = device_col_dims(devs)

        inner_w = plates_inner_w + (DEVICE_COL_GAP + dev_col_w if devs else 0)
        inner_h = max(plates_inner_h, dev_col_h)
        box_w = inner_w + 2 * ROOM_BOX_PAD
        box_h = inner_h + ROOM_TITLE_H + 2 * ROOM_BOX_PAD

        room_blocks.append((room, loc_columns, devs, plates_inner_w, box_w, box_h))

    # Arrange room boxes left-to-right, wrap if needed.
    max_row_w = 1800
    rows: list[list[tuple]] = [[]]
    row_w = 0
    for block in room_blocks:
        bw = block[4]
        if row_w + bw > max_row_w and rows[-1]:
            rows.append([])
            row_w = 0
        rows[-1].append(block)
        row_w += bw + ROOM_GAP

    # Compute overall canvas
    total_w = max(sum(b[4] for b in row) + ROOM_GAP * (len(row) - 1) for row in rows) + 40
    total_h = OVERVIEW_TOP_PAD + sum(max(b[5] for b in row) for row in rows) + ROOM_GAP * (len(rows) - 1) + 80

    plate_positions: dict[str, tuple[int, int, int, int]] = {}
    # device_positions[circuit_id] = (cx, bottom_y) — kotva čáry na spodní hraně pilulky
    device_positions: dict[str, tuple[float, float]] = {}

    if mode == "after":
        title = "Stav po úpravě — svítidla, vypínače a namontované Shelly"
        subtitle = (
            "Shelly (tmavá pilulka) je na rámečku (za vypínačem) nebo u svítidla podle umístění. "
            "Kuchyňský rámeček upravený: 2× zásuvka + dvojvypínač Lišta 3/LED digestoř (220V, s relé) + dvojvypínač LED A/B."
        )
    else:
        title = "Přehled — svítidla, vypínače a okruhy mezi nimi"
        subtitle = (
            "Každý vypínač je čarou propojen se zařízením, které ovládá. "
            "Více čar k jedné pilulce = víc vypínačů na stejný okruh (3-cestné nebo paralelka)."
        )

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(total_w)} {int(total_h)}" '
        f'width="{int(total_w)}" height="{int(total_h)}" font-family="sans-serif">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="20" y="36" font-size="24" font-weight="700" fill="{TEXT}">{esc(title)}</text>',
        f'<text x="20" y="58" font-size="12" font-style="italic" fill="{MUTED}">{esc(subtitle)}</text>',
    ]

    row_y = OVERVIEW_TOP_PAD
    for row in rows:
        row_h = max(b[5] for b in row)
        bx = 20
        for room, loc_columns, devs, plates_inner_w, box_w, box_h in row:
            # Room box
            parts.append(
                f'<rect x="{bx}" y="{row_y}" width="{box_w}" height="{box_h}" '
                f'fill="#fefefe" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4,3" rx="6" ry="6"/>'
            )
            parts.append(
                f'<text x="{bx + ROOM_BOX_PAD}" y="{row_y + ROOM_BOX_PAD + 14}" '
                f'font-size="16" font-weight="700" fill="{TEXT}">{esc(room)}</text>'
            )

            inner_top = row_y + ROOM_BOX_PAD + ROOM_TITLE_H
            plates_top = inner_top

            # Rámečky (vlevo)
            cx = bx + ROOM_BOX_PAD
            for loc, ps, col_w, _ in loc_columns:
                if loc:
                    parts.append(
                        f'<text x="{cx}" y="{plates_top + 12}" font-size="11" '
                        f'font-style="italic" fill="{MUTED}">{esc(loc)}</text>'
                    )
                cy = plates_top + LOC_HEADER_H
                for plate in ps:
                    plate_parts, pw, ph = render_plate(plate, cx, cy)
                    parts.extend(plate_parts)
                    plate_positions[plate["id"]] = (cx, cy, pw, ph)
                    cy += ph + PLATE_GAP
                cx += col_w + COLUMN_GAP

            # Svítidla (vpravo, sloupec pilulek)
            if devs:
                dev_col_x = bx + ROOM_BOX_PAD + plates_inner_w + DEVICE_COL_GAP
                parts.append(
                    f'<text x="{dev_col_x}" y="{inner_top + 11}" font-size="10" '
                    f'font-style="italic" fill="{MUTED}">Svítidla</text>'
                )
                pill_y = inner_top + DEVICE_STRIP_TITLE_H
                for dev in devs:
                    parts.extend(render_device_pill(dev, dev_col_x, pill_y))
                    # Kotva čáry = levá hrana pilulky, svisle uprostřed
                    device_positions[dev["id"]] = (
                        dev_col_x,
                        pill_y + DEVICE_PILL_H / 2,
                    )
                    pill_y += DEVICE_PILL_H + DEVICE_PILL_GAP_Y

            bx += box_w + ROOM_GAP
        row_y += row_h + ROOM_GAP

    # Čáry: vypínač → zařízení
    # Pro každou buňku s circuit najdi pilulku zařízení a nakresli čáru.
    all_anchors: list[tuple[str, float, float, str]] = []
    for p in plates:
        if p["id"] not in plate_positions:
            continue
        px, py, _, _ = plate_positions[p["id"]]
        for circ, cx, ty in cell_anchors_in_plate(p, px, py):
            all_anchors.append((circ, cx, ty, p["id"]))

    # Stabilní barva per okruh
    seen_circuits = sorted({c for c, *_ in all_anchors})
    color_map = {
        c: CONNECTION_PALETTE[i % len(CONNECTION_PALETTE)]
        for i, c in enumerate(seen_circuits)
    }

    conn_svgs: list[str] = []
    for circ, sx, sy, pid in all_anchors:
        if circ not in device_positions:
            continue
        ex, ey = device_positions[circ]
        color = color_map[circ]
        # Horizontální S-křivka mezi buňkou (střed) a pilulkou (levá hrana).
        mid_x = (sx + ex) / 2
        path = f"M {sx} {sy} C {mid_x} {sy}, {mid_x} {ey}, {ex} {ey}"
        conn_svgs.append(
            f'<path d="{path}" fill="none" stroke="{color}" stroke-width="1.5" opacity="0.75"/>'
        )
        conn_svgs.append(f'<circle cx="{sx}" cy="{sy}" r="2.5" fill="{color}"/>')
        conn_svgs.append(f'<circle cx="{ex}" cy="{ey}" r="2.5" fill="{color}"/>')

    parts.extend(conn_svgs)

    # V "after" módu vykreslit Shelly badges na rámečcích a svítidlech
    if mode == "after":
        # Badges na rámečcích (Shelly za vypínačem)
        for p in plates:
            if p["id"] not in plate_positions:
                continue
            px, py, pw, ph = plate_positions[p["id"]]
            shellies = shelly_for_plate(p)
            for i, sh in enumerate(shellies):
                badge_x = px + pw - SHELLY_BADGE_W - 6
                badge_y = py + 6 + i * (SHELLY_BADGE_H + 3)
                parts.extend(render_shelly_badge(sh["id"], sh.get("model", ""), badge_x, badge_y))
        # Badges u svítidel (Shelly u spotřebiče)
        for dev_id, (dpx, dpy) in device_positions.items():
            shellies = shelly_for_circuit(dev_id)
            for i, sh in enumerate(shellies):
                # pilulka vpravo od svítidlové pilulky
                badge_x = dpx + DEVICE_PILL_W + 6
                badge_y = dpy - SHELLY_BADGE_H / 2 + i * (SHELLY_BADGE_H + 3)
                parts.extend(render_shelly_badge(sh["id"], sh.get("model", ""), badge_x, badge_y))

    # Legend
    parts.extend(render_legend(20, total_h - 30))
    if mode == "after":
        # Vysvětlivka k Shelly badge
        lg_x = 20
        lg_y = total_h - 52
        parts.extend(render_shelly_badge("SH-XX", "", lg_x, lg_y))
        parts.append(
            f'<text x="{lg_x + SHELLY_BADGE_W + 8}" y="{lg_y + SHELLY_BADGE_H - 4}" '
            f'font-size="11" fill="{TEXT}">namontovaný Shelly (za vypínačem nebo u svítidla)</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    global CIRCUITS, SHELLY
    CIRCUITS = load_circuits()
    SHELLY = load_shelly()
    data = yaml.safe_load(PLATES_YAML.read_text(encoding="utf-8"))
    plates = data["plates"]

    # Per-room rendery používají "before" plates
    plates_before = plates_for_mode(plates, "before")
    by_room: dict[str, list[dict]] = defaultdict(list)
    for p in plates_before:
        by_room[p["room"]].append(p)

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Přehled (plánovaný stav) + stav po úpravě s namontovanými Shelly
    (OUTPUT_DIR / "prehled.svg").write_text(
        render_overview(plates, mode="before"), encoding="utf-8"
    )
    print(f"Wrote {(OUTPUT_DIR / 'prehled.svg').relative_to(PROJECT)}")
    (OUTPUT_DIR / "prehled-po.svg").write_text(
        render_overview(plates, mode="after"), encoding="utf-8"
    )
    print(f"Wrote {(OUTPUT_DIR / 'prehled-po.svg').relative_to(PROJECT)}")

    index_lines = [
        "# Rámečky — digitální nákres",
        "",
        "Generováno z `devices/plates.yaml` skriptem `scripts/generate_plates.py`.",
        "",
        "## Přehled (plánovaný stav)",
        "",
        "![Přehled](prehled.svg)",
        "",
        "## Stav po úpravě (s namontovanými Shelly)",
        "",
        "![Stav po](prehled-po.svg)",
        "",
        "## Detail per místnost",
        "",
    ]
    for room in sorted(by_room):
        slug = slugify(room)
        svg = render_room(room, by_room[room])
        out = OUTPUT_DIR / f"{slug}.svg"
        out.write_text(svg, encoding="utf-8")
        print(f"Wrote {out.relative_to(PROJECT)}")
        index_lines += [f"### {room}", "", f"![{room}]({slug}.svg)", ""]

    (OUTPUT_DIR / "README.md").write_text("\n".join(index_lines), encoding="utf-8")
    print(f"Wrote {(OUTPUT_DIR / 'README.md').relative_to(PROJECT)}")


if __name__ == "__main__":
    main()
