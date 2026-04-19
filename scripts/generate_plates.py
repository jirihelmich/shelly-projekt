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
OUTPUT_DIR = PROJECT / "plates"

COLORS = {
    "HUE": "#ffedd5",      # teplá oranžová = Hue (fáze trvalá)
    "non-HUE": "#dbeafe",  # chladná modrá = klasický okruh
    "neutral": "#f3f4f6",  # šedá = zásuvka / neklasifikovaný modul
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
    tag = "HUE" if t.upper().startswith("HUE") else "non-HUE"
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

CELL_W = 110
CELL_H = 84
SOCKET_W = 90
PADDING = 10
LABEL_H = 18  # prostor nahoře pro ID a tag badge
PLATE_GAP = 18
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
    if orientation == "vertical":
        w = max(component_width(c) for c in comps) + 2 * PADDING
        h = len(comps) * CELL_H + LABEL_H + 2 * PADDING
    else:
        w = sum(component_width(c) for c in comps) + 2 * PADDING
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


def render_cell(cell: dict, x: int, y: int, w: int) -> list[str]:
    parts: list[str] = []
    circ = cell.get("circuit")
    info = CIRCUITS.get(circ) if circ else None
    tag = info["tag"] if info else "neutral"
    voltage = cell.get("voltage") or (info["voltage"] if info else None)
    bg = COLORS.get(tag, COLORS["neutral"])

    # Buňkové pozadí (barva dle HUE/non-HUE)
    parts.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{CELL_H}" fill="{bg}" '
        f'stroke="{BORDER}" stroke-width="1.5"/>'
    )

    # Klapka (tlačítko)
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

    # Label
    label = esc(cell["label"])
    parts.append(
        f'<text x="{x + w/2}" y="{y + CELL_H - 19}" text-anchor="middle" '
        f'font-family="sans-serif" font-size="11" font-weight="600" fill="{TEXT}">{label}</text>'
    )

    # Circuit ID
    if circ:
        parts.append(
            f'<text x="{x + w/2}" y="{y + CELL_H - 5}" text-anchor="middle" '
            f'font-family="monospace" font-size="9" fill="{MUTED}">{esc(circ)}</text>'
        )

    # Voltage badge (vpravo nahoře)
    if voltage:
        parts.extend(voltage_badge(x + w - 4, y + 4, voltage))

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
        for i, cell in enumerate(c["cells"]):
            parts += render_cell(cell, x + CELL_W * i, y, CELL_W)
        parts.append(
            f'<line x1="{x + CELL_W}" y1="{y+6}" x2="{x + CELL_W}" y2="{y+CELL_H-6}" '
            f'stroke="{BORDER}" stroke-width="1" stroke-dasharray="3,3"/>'
        )
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
            cell_y += CELL_H
    else:
        cx = x + PADDING
        for c in plate["components"]:
            comp_parts, cw = render_component(c, cx, cell_y)
            parts.extend(comp_parts)
            cx += cw

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
    # HUE / non-HUE
    for label in ("HUE", "non-HUE"):
        color = COLORS[label]
        parts.append(
            f'<rect x="{x}" y="{y-11}" width="14" height="14" fill="{color}" '
            f'stroke="{BORDER}" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x+20}" y="{y}" font-size="11" fill="{TEXT}">{esc(label)}</text>'
        )
        x += 100
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
    "Chodba u pokoje",
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


DEVICE_PILL_W = 146
DEVICE_PILL_H = 30
DEVICE_PILL_GAP_X = 8
DEVICE_PILL_GAP_Y = 6
DEVICE_STRIP_PAD_TOP = 6
DEVICE_STRIP_PAD_BOT = 10
DEVICE_STRIP_TITLE_H = 18


def render_device_pill(dev: dict, x: int, y: int) -> list[str]:
    tag = dev["tag"]
    fill = COLORS.get(tag, COLORS["neutral"])
    voltage = dev.get("voltage")
    parts = [
        f'<rect x="{x}" y="{y}" width="{DEVICE_PILL_W}" height="{DEVICE_PILL_H}" '
        f'fill="{fill}" stroke="{BORDER}" stroke-width="1" rx="14" ry="14"/>',
        f'<text x="{x+10}" y="{y+12}" font-family="monospace" font-size="8" fill="{MUTED}">{esc(dev["id"])}</text>',
        f'<text x="{x+10}" y="{y+24}" font-size="11" font-weight="600" fill="{TEXT}">{esc(dev["name"])}</text>',
    ]
    if voltage:
        parts.extend(voltage_badge(x + DEVICE_PILL_W - 6, y + 4, voltage))
    return parts


def device_strip_dims(devices: list[dict], max_w: int) -> tuple[int, int, list[list[dict]]]:
    """Vrátí (width, height, layout_rows). Rozloží pilulky do řádků tak, aby se vešly do max_w."""
    if not devices:
        return 0, 0, []
    per_row = max(1, (max_w + DEVICE_PILL_GAP_X) // (DEVICE_PILL_W + DEVICE_PILL_GAP_X))
    rows: list[list[dict]] = []
    for i in range(0, len(devices), per_row):
        rows.append(devices[i : i + per_row])
    w = min(max_w, max(len(r) for r in rows) * (DEVICE_PILL_W + DEVICE_PILL_GAP_X) - DEVICE_PILL_GAP_X)
    h = DEVICE_STRIP_TITLE_H + len(rows) * (DEVICE_PILL_H + DEVICE_PILL_GAP_Y) - DEVICE_PILL_GAP_Y + DEVICE_STRIP_PAD_TOP + DEVICE_STRIP_PAD_BOT
    return w, h, rows

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
OVERVIEW_TOP_PAD = 140  # prostor nad místnostmi na oblouky propojení


def cell_anchors_in_plate(plate: dict, plate_x: float, plate_y: float):
    """Yield (circuit_id, cell_center_x, cell_top_y) pro každou buňku s circuit v plate."""
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
                    yield circ, ccx, cell_y
            cell_y += CELL_H
    else:
        cx_base = plate_x + PADDING
        for comp in plate["components"]:
            cw = component_width(comp)
            if comp["type"] != "socket":
                for i, cell in enumerate(comp.get("cells", [])):
                    circ = cell.get("circuit")
                    if not circ:
                        cx_base_next = cx_base
                        continue
                    if comp["type"] == "double_switch":
                        ccx = cx_base + CELL_W * i + CELL_W / 2
                    else:
                        ccx = cx_base + CELL_W / 2
                    yield circ, ccx, cell_y
            cx_base += cw


def render_overview(plates: list[dict]) -> str:
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

        # Device strip
        devs = devices_per_room.get(room, [])
        dev_max_w = max(plates_inner_w, DEVICE_PILL_W * 2 + DEVICE_PILL_GAP_X) if devs else 0
        dev_w, dev_h, dev_rows = device_strip_dims(devs, dev_max_w if dev_max_w else DEVICE_PILL_W * 3)

        inner_w = max(plates_inner_w, dev_w)
        inner_h = dev_h + plates_inner_h
        box_w = max(inner_w, DEVICE_PILL_W + 2 * ROOM_BOX_PAD) + 2 * ROOM_BOX_PAD
        box_h = inner_h + ROOM_TITLE_H + 2 * ROOM_BOX_PAD

        room_blocks.append((room, loc_columns, dev_rows, dev_h, box_w, box_h))

    # Arrange room boxes left-to-right, wrap if needed.
    max_row_w = 1600
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

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(total_w)} {int(total_h)}" '
        f'width="{int(total_w)}" height="{int(total_h)}" font-family="sans-serif">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="20" y="36" font-size="24" font-weight="700" fill="{TEXT}">Přehled — svítidla, vypínače a okruhy mezi nimi</text>',
        f'<text x="20" y="58" font-size="12" font-style="italic" fill="{MUTED}">'
        f'Každý vypínač je čarou propojen se zařízením, které ovládá. '
        f'Více čar k jedné pilulce = víc vypínačů na stejný okruh (3-cestné nebo paralelka).</text>',
    ]

    row_y = OVERVIEW_TOP_PAD
    for row in rows:
        row_h = max(b[5] for b in row)
        bx = 20
        for room, loc_columns, dev_rows, dev_h, box_w, box_h in row:
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

            # Device strip
            if dev_rows:
                parts.append(
                    f'<text x="{bx + ROOM_BOX_PAD}" y="{inner_top + 11}" font-size="10" '
                    f'font-style="italic" fill="{MUTED}">Svítidla</text>'
                )
                pill_y = inner_top + DEVICE_STRIP_TITLE_H + DEVICE_STRIP_PAD_TOP
                for drow in dev_rows:
                    pill_x = bx + ROOM_BOX_PAD
                    for dev in drow:
                        parts.extend(render_device_pill(dev, pill_x, pill_y))
                        # Kotva čáry = spodní hrana pilulky (střed)
                        device_positions[dev["id"]] = (
                            pill_x + DEVICE_PILL_W / 2,
                            pill_y + DEVICE_PILL_H,
                        )
                        pill_x += DEVICE_PILL_W + DEVICE_PILL_GAP_X
                    pill_y += DEVICE_PILL_H + DEVICE_PILL_GAP_Y

            plates_top = inner_top + dev_h

            # Locations + plates inside
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
    for circ, cx, ty, pid in all_anchors:
        if circ not in device_positions:
            continue
        dx, dy = device_positions[circ]
        color = color_map[circ]
        # Křivka z buňky nahoru k zařízení. Buňka je níž než pilulka (větší Y).
        # Kontrolní body: horizontálně rovnou cestu přes peak.
        peak_y = min(ty, dy) - 24
        path = (
            f"M {cx} {ty} "
            f"C {cx} {peak_y}, {dx} {peak_y}, {dx} {dy}"
        )
        conn_svgs.append(
            f'<path d="{path}" fill="none" stroke="{color}" stroke-width="1.5" opacity="0.7"/>'
        )
        conn_svgs.append(f'<circle cx="{cx}" cy="{ty}" r="2.5" fill="{color}"/>')
        conn_svgs.append(f'<circle cx="{dx}" cy="{dy}" r="2.5" fill="{color}"/>')

    parts.extend(conn_svgs)

    # Legend
    parts.extend(render_legend(20, total_h - 30))
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    global CIRCUITS
    CIRCUITS = load_circuits()
    data = yaml.safe_load(PLATES_YAML.read_text(encoding="utf-8"))
    plates = data["plates"]
    by_room: dict[str, list[dict]] = defaultdict(list)
    for p in plates:
        by_room[p["room"]].append(p)

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Overall overview first
    overview_svg = render_overview(plates)
    (OUTPUT_DIR / "prehled.svg").write_text(overview_svg, encoding="utf-8")
    print(f"Wrote {(OUTPUT_DIR / 'prehled.svg').relative_to(PROJECT)}")

    index_lines = [
        "# Rámečky — digitální nákres",
        "",
        "Generováno z `devices/plates.yaml` skriptem `scripts/generate_plates.py`.",
        "",
        "## Přehled (všechny místnosti + propojení okruhů)",
        "",
        "![Přehled](prehled.svg)",
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
