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
OUTPUT_DIR = PROJECT / "plates"

COLORS = {
    "HUE": "#ffedd5",
    "non-HUE": "#dbeafe",
    "mixed": "#ede9fe",
    "existing": "#e5e7eb",
}
BORDER = "#374151"
TEXT = "#111827"
MUTED = "#6b7280"

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
    w = sum(component_width(c) for c in plate["components"]) + 2 * PADDING
    h = CELL_H + LABEL_H + 2 * PADDING
    return w, h


def render_socket(c: dict, x: int, y: int, fill: str) -> list[str]:
    cx = x + SOCKET_W / 2
    cy = y + CELL_H / 2
    label = esc(c["cells"][0]["label"])
    return [
        f'<rect x="{x}" y="{y}" width="{SOCKET_W}" height="{CELL_H}" fill="{fill}" stroke="{BORDER}" stroke-width="1.5"/>',
        f'<circle cx="{cx}" cy="{cy-6}" r="22" fill="white" stroke="{BORDER}" stroke-width="1.5"/>',
        f'<circle cx="{cx-7}" cy="{cy-6}" r="2.5" fill="{BORDER}"/>',
        f'<circle cx="{cx+7}" cy="{cy-6}" r="2.5" fill="{BORDER}"/>',
        f'<text x="{cx}" y="{y + CELL_H - 8}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="{TEXT}">{label}</text>',
    ]


def render_cell(cell: dict, x: int, y: int, w: int) -> list[str]:
    parts: list[str] = []
    # button plate (the actual "klapka")
    inner_x = x + 14
    inner_y = y + 12
    inner_w = w - 28
    inner_h = CELL_H - 44
    blind = cell.get("blind")
    fill = "#f3f4f6" if blind else "white"
    parts.append(
        f'<rect x="{inner_x}" y="{inner_y}" width="{inner_w}" height="{inner_h}" fill="{fill}" stroke="{BORDER}" stroke-width="1" rx="3" ry="3"/>'
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
    circ = cell.get("circuit")
    if circ:
        parts.append(
            f'<text x="{x + w/2}" y="{y + CELL_H - 5}" text-anchor="middle" '
            f'font-family="monospace" font-size="9" fill="{MUTED}">{esc(circ)}</text>'
        )
    return parts


def render_component(c: dict, x: int, y: int, fill: str) -> tuple[list[str], int]:
    t = c["type"]
    if t == "socket":
        return render_socket(c, x, y, fill), SOCKET_W
    if t == "single_switch":
        parts = [
            f'<rect x="{x}" y="{y}" width="{CELL_W}" height="{CELL_H}" fill="{fill}" stroke="{BORDER}" stroke-width="1.5"/>'
        ]
        parts += render_cell(c["cells"][0], x, y, CELL_W)
        return parts, CELL_W
    if t == "double_switch":
        w = CELL_W * 2
        parts = [
            f'<rect x="{x}" y="{y}" width="{w}" height="{CELL_H}" fill="{fill}" stroke="{BORDER}" stroke-width="1.5"/>',
            f'<line x1="{x + CELL_W}" y1="{y+6}" x2="{x + CELL_W}" y2="{y+CELL_H-6}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="3,3"/>',
        ]
        for i, cell in enumerate(c["cells"]):
            parts += render_cell(cell, x + CELL_W * i, y, CELL_W)
        return parts, w
    return [], 0


def render_plate(plate: dict, x: int, y: int) -> tuple[list[str], int, int]:
    w, h = plate_dims(plate)
    tag = plate.get("tag", "")
    fill = COLORS.get(tag, "#ffffff")

    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f9fafb" '
        f'stroke="{BORDER}" stroke-width="2" rx="8" ry="8"/>',
    ]
    cx = x + PADDING
    cell_y = y + PADDING + LABEL_H
    for c in plate["components"]:
        comp_parts, cw = render_component(c, cx, cell_y, fill)
        parts.extend(comp_parts)
        cx += cw

    parts.append(
        f'<text x="{x+10}" y="{y + PADDING + 10}" font-family="monospace" font-size="9" fill="{MUTED}">{esc(plate["id"])}</text>'
    )
    if tag:
        parts.append(
            f'<text x="{x+w-10}" y="{y + PADDING + 10}" text-anchor="end" font-family="sans-serif" '
            f'font-size="9" font-weight="700" fill="{MUTED}">{esc(tag.upper())}</text>'
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

    legend_y = total_h - 24
    legend_x = 20
    for label, color in COLORS.items():
        parts.append(
            f'<rect x="{legend_x}" y="{legend_y-11}" width="14" height="14" fill="{color}" '
            f'stroke="{BORDER}" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{legend_x+20}" y="{legend_y}" font-size="11" fill="{TEXT}">{esc(label)}</text>'
        )
        legend_x += 100

    parts.append("</svg>")
    return "\n".join(parts)


ROOM_ORDER = [
    "Obývák",
    "Horní předsíň",
    "Chodba u pokoje",
    "Dolní předsíň",
    "Kuchyň",
    "Jídelna",
]

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


def collect_circuits(plates_in_order: list[dict]) -> dict[str, list[tuple[str, int]]]:
    """Map circuit_id -> list of (plate_id, cell_index_in_plate)."""
    out: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for p in plates_in_order:
        idx = 0  # global cell index within this plate (across components)
        for comp in p["components"]:
            if comp["type"] == "socket":
                idx += 1
                continue
            for cell in comp.get("cells", []):
                circ = cell.get("circuit")
                if circ:
                    out[circ].append((p["id"], idx))
                idx += 1
    return out


def render_overview(plates: list[dict]) -> str:
    by_room: dict[str, list[dict]] = defaultdict(list)
    for p in plates:
        by_room[p["room"]].append(p)

    rooms = [r for r in ROOM_ORDER if r in by_room] + [
        r for r in by_room if r not in ROOM_ORDER
    ]

    # Pre-compute plate layout within each room box (locations = sub-columns).
    room_blocks = []
    for room in rooms:
        plates_in_room = by_room[room]
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

        inner_w = sum(w for _, _, w, _ in loc_columns) + COLUMN_GAP * (len(loc_columns) - 1)
        inner_h = max(h for _, _, _, h in loc_columns) + LOC_HEADER_H
        box_w = inner_w + 2 * ROOM_BOX_PAD
        box_h = inner_h + ROOM_TITLE_H + 2 * ROOM_BOX_PAD
        room_blocks.append((room, loc_columns, box_w, box_h))

    # Arrange room boxes left-to-right, wrap if needed.
    max_row_w = 1600
    rows: list[list[tuple]] = [[]]
    row_w = 0
    for block in room_blocks:
        bw = block[2]
        if row_w + bw > max_row_w and rows[-1]:
            rows.append([])
            row_w = 0
        rows[-1].append(block)
        row_w += bw + ROOM_GAP

    # Compute overall canvas
    total_w = max(sum(b[2] for b in row) + ROOM_GAP * (len(row) - 1) for row in rows) + 40
    total_h = OVERVIEW_TOP_PAD + sum(max(b[3] for b in row) for row in rows) + ROOM_GAP * (len(rows) - 1) + 80

    plate_positions: dict[str, tuple[int, int, int, int]] = {}

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(total_w)} {int(total_h)}" '
        f'width="{int(total_w)}" height="{int(total_h)}" font-family="sans-serif">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="20" y="36" font-size="24" font-weight="700" fill="{TEXT}">Přehled — propojení okruhů napříč místnostmi</text>',
        f'<text x="20" y="58" font-size="12" font-style="italic" fill="{MUTED}">'
        f'Čáry spojují rámečky, které ovládají stejný okruh (3-cestné nebo paralelka).</text>',
    ]

    row_y = OVERVIEW_TOP_PAD
    for row in rows:
        row_h = max(b[3] for b in row)
        bx = 20
        for room, loc_columns, box_w, box_h in row:
            # Room box
            parts.append(
                f'<rect x="{bx}" y="{row_y}" width="{box_w}" height="{box_h}" '
                f'fill="#fefefe" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4,3" rx="6" ry="6"/>'
            )
            parts.append(
                f'<text x="{bx + ROOM_BOX_PAD}" y="{row_y + ROOM_BOX_PAD + 14}" '
                f'font-size="16" font-weight="700" fill="{TEXT}">{esc(room)}</text>'
            )
            # Locations + plates inside
            cx = bx + ROOM_BOX_PAD
            inner_top = row_y + ROOM_BOX_PAD + ROOM_TITLE_H
            for loc, ps, col_w, _ in loc_columns:
                if loc:
                    parts.append(
                        f'<text x="{cx}" y="{inner_top + 12}" font-size="11" '
                        f'font-style="italic" fill="{MUTED}">{esc(loc)}</text>'
                    )
                cy = inner_top + LOC_HEADER_H
                for plate in ps:
                    plate_parts, pw, ph = render_plate(plate, cx, cy)
                    parts.extend(plate_parts)
                    plate_positions[plate["id"]] = (cx, cy, pw, ph)
                    cy += ph + PLATE_GAP
                cx += col_w + COLUMN_GAP
            bx += box_w + ROOM_GAP
        row_y += row_h + ROOM_GAP

    # Connection lines for circuits spanning multiple plates
    circuits = collect_circuits(plates)
    multi = {c: ps for c, ps in circuits.items() if len({pid for pid, _ in ps}) > 1}

    # Assign colors per circuit
    conn_svgs = []
    for i, (circ, refs) in enumerate(sorted(multi.items())):
        color = CONNECTION_PALETTE[i % len(CONNECTION_PALETTE)]
        # Unique plates for this circuit (preserve order of first occurrence)
        seen = []
        for pid, _ in refs:
            if pid not in seen:
                seen.append(pid)
        # Arch height is spaced per circuit so arcs don't fully overlap
        arch_offset = 30 + (i * 14) % 90
        # Draw arcs between consecutive plates in `seen`
        for a_id, b_id in zip(seen, seen[1:]):
            ax, ay, aw, _ = plate_positions[a_id]
            bx, by, bw, _ = plate_positions[b_id]
            ax_c = ax + aw / 2
            bx_c = bx + bw / 2
            ay_top = ay
            by_top = by
            # Peak of arc: average y minus offset
            peak_y = min(ay_top, by_top) - arch_offset
            mid_x = (ax_c + bx_c) / 2
            path = (
                f"M {ax_c} {ay_top} "
                f"Q {ax_c} {peak_y}, {mid_x} {peak_y} "
                f"T {bx_c} {by_top}"
            )
            conn_svgs.append(
                f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2" opacity="0.85"/>'
            )
            # Dot at both ends
            conn_svgs.append(f'<circle cx="{ax_c}" cy="{ay_top}" r="3" fill="{color}"/>')
            conn_svgs.append(f'<circle cx="{bx_c}" cy="{by_top}" r="3" fill="{color}"/>')
            # Circuit label at peak
            conn_svgs.append(
                f'<rect x="{mid_x-24}" y="{peak_y-10}" width="48" height="14" '
                f'fill="white" stroke="{color}" stroke-width="1" rx="3" ry="3"/>'
            )
            conn_svgs.append(
                f'<text x="{mid_x}" y="{peak_y+1}" text-anchor="middle" '
                f'font-family="monospace" font-size="10" font-weight="700" fill="{color}">{esc(circ)}</text>'
            )

    parts.extend(conn_svgs)

    # Legend
    legend_y = total_h - 30
    legend_x = 20
    for label, color in COLORS.items():
        parts.append(
            f'<rect x="{legend_x}" y="{legend_y-11}" width="14" height="14" fill="{color}" '
            f'stroke="{BORDER}" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{legend_x+20}" y="{legend_y}" font-size="11" fill="{TEXT}">{esc(label)}</text>'
        )
        legend_x += 100

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
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
