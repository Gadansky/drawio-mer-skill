#!/usr/bin/env python3
"""Validate uncompressed draw.io XML for MER/MERE diagrams."""

from __future__ import annotations

import argparse
import html
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


ALLOWED_CARDINALITIES = {"1", "0..1", "1..N", "0..N"}

CARDINALITY_PATTERN = re.compile(
    r"(?<![\w.])(?:0\.\.[A-Za-z0-9]+|1\.\.[A-Za-z0-9]+|[MN]\.\.[MN]|[MN]:[MN]|[01]:[MN]|[MN]:[01])(?!(?:[\w.]))",
    re.IGNORECASE,
)

TYPE_PATTERN = re.compile(
    r"(?im)"
    r"(?:^|[\n\r<>\s;|])"
    r"([A-Za-z_][A-Za-z0-9_]*"
    r"\s*:\s*"
    r"(?:"
    r"varchar\s*\(\s*\d+\s*\)"
    r"|char\s*\(\s*\d+\s*\)"
    r"|decimal\s*\(\s*\d+\s*,\s*\d+\s*\)"
    r"|numeric\s*\(\s*\d+\s*,\s*\d+\s*\)"
    r"|int(?:eger)?"
    r"|date"
    r"|datetime"
    r"|timestamp"
    r"|boolean"
    r"|bool"
    r"|float"
    r"|double"
    r"|text"
    r")"
    r")"
    r"(?=$|[\s<>\n\r;|])",
)


@dataclass(frozen=True)
class BoundingBox:
    cell_id: str
    x: float
    y: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a draw.io MER/MERE XML file.",
    )
    parser.add_argument("path", help="Path to a .drawio, .drawio.xml, or XML file.")
    parser.add_argument(
        "--mode",
        choices=("mer", "mere"),
        help="Diagram mode. MER warns on data types; MERE allows them.",
    )
    parser.add_argument(
        "--check-layout",
        action="store_true",
        help="Check vertex geometry, estimated canvas, and visual overlaps.",
    )
    return parser.parse_args()


def infer_mode(path: Path, explicit_mode: str | None) -> tuple[str, list[str]]:
    if explicit_mode:
        return explicit_mode, []

    name = path.name.lower()
    if "mere" in name:
        return "mere", []
    if "mer" in name:
        return "mer", []

    return "mer", [
        "Could not infer mode from file name; defaulted to MER."
    ]


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def find_mxcells(root: ET.Element) -> list[ET.Element]:
    return [element for element in root.iter() if local_name(element.tag) == "mxCell"]


def find_graph_models(root: ET.Element) -> list[ET.Element]:
    return [element for element in root.iter() if local_name(element.tag) == "mxGraphModel"]


def find_geometry(cell: ET.Element) -> ET.Element | None:
    for child in cell:
        if local_name(child.tag) == "mxGeometry":
            return child
    return None


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def visible_value(cell: ET.Element) -> str:
    value = cell.get("value") or ""
    value = html.unescape(value)
    value = re.sub(r"(?i)<br\s*/?>", "\n", value)
    value = re.sub(r"<[^>]+>", " ", value)
    return value


def raw_value(cell: ET.Element) -> str:
    return html.unescape(cell.get("value") or "")


def cell_style(cell: ET.Element) -> str:
    return (cell.get("style") or "").lower()


def is_attribute_oval(cell: ET.Element) -> bool:
    return cell.get("vertex") == "1" and "ellipse" in cell_style(cell)


def is_relationship_diamond(cell: ET.Element) -> bool:
    style = cell_style(cell)
    return cell.get("vertex") == "1" and ("rhombus" in style or "shape=rhombus" in style)


def ignores_layout_overlap(cell: ET.Element) -> bool:
    return "ignorelayoutoverlap=1" in cell_style(cell)


def has_internal_attribute_list(cell: ET.Element) -> bool:
    value = raw_value(cell).lower()
    if "<br" in value or "<hr" in value:
        return True
    return "\n" in visible_value(cell)


def collect_type_warnings(cells: list[ET.Element], mode: str) -> list[str]:
    if mode == "mere":
        return []

    warnings: list[str] = []
    for cell in cells:
        value = visible_value(cell)
        matches = [match.group(1).strip() for match in TYPE_PATTERN.finditer(value)]
        if matches:
            cell_id = cell.get("id", "(no id)")
            joined = ", ".join(sorted(set(matches)))
            warnings.append(
                f"Data types detected in MER mode in mxCell {cell_id}: {joined}"
            )
    return warnings


def collect_mer_notation_warnings(cells: list[ET.Element]) -> list[str]:
    warnings: list[str] = []
    entity_cells = [
        cell
        for cell in cells
        if cell.get("vertex") == "1" and (cell.get("id") or "").startswith("entity_")
    ]
    attribute_ovals = [cell for cell in cells if is_attribute_oval(cell)]
    relationship_diamonds = [cell for cell in cells if is_relationship_diamond(cell)]

    for cell in entity_cells:
        if has_internal_attribute_list(cell):
            cell_id = cell.get("id", "(no id)")
            warnings.append(
                f"MER entity {cell_id} appears to contain internal attributes; "
                "MER should use separate attribute ovals connected to the entity."
            )

    if not attribute_ovals:
        warnings.append(
            "MER mode did not find attribute ovals (style containing 'ellipse')."
        )

    if not relationship_diamonds:
        warnings.append(
            "MER mode did not find relationship diamonds (style containing 'rhombus')."
        )

    return warnings


def collect_layout_warnings(
    cells: list[ET.Element],
    graph_models: list[ET.Element],
) -> tuple[list[str], dict[str, object]]:
    warnings: list[str] = []
    vertex_cells = [cell for cell in cells if cell.get("vertex") == "1"]
    cell_by_id = {cell.get("id", ""): cell for cell in vertex_cells if cell.get("id")}
    boxes: list[BoundingBox] = []
    missing_geometry: list[str] = []

    for cell in vertex_cells:
        cell_id = cell.get("id", "(no id)")
        geometry = find_geometry(cell)
        if geometry is None:
            missing_geometry.append(cell_id)
            continue

        values = {
            "x": parse_float(geometry.get("x")),
            "y": parse_float(geometry.get("y")),
            "width": parse_float(geometry.get("width")),
            "height": parse_float(geometry.get("height")),
        }
        if any(value is None for value in values.values()):
            missing_geometry.append(cell_id)
            continue

        boxes.append(
            BoundingBox(
                cell_id=cell_id,
                x=values["x"] or 0.0,
                y=values["y"] or 0.0,
                width=values["width"] or 0.0,
                height=values["height"] or 0.0,
            )
        )

    overlaps: list[tuple[str, str]] = []
    for index, left in enumerate(boxes):
        left_cell = cell_by_id.get(left.cell_id)
        if left_cell is not None and ignores_layout_overlap(left_cell):
            continue
        for right in boxes[index + 1 :]:
            right_cell = cell_by_id.get(right.cell_id)
            if right_cell is not None and ignores_layout_overlap(right_cell):
                continue
            if boxes_overlap(left, right):
                overlaps.append((left.cell_id, right.cell_id))

    for cell_id in missing_geometry:
        warnings.append(f"Visible vertex missing complete geometry: {cell_id}")

    for left_id, right_id in overlaps:
        warnings.append(f"Visual overlap detected: {left_id} overlaps {right_id}")

    max_right = max((box.right for box in boxes), default=0.0)
    max_bottom = max((box.bottom for box in boxes), default=0.0)
    page_width = max((parse_float(model.get("pageWidth")) or 0.0 for model in graph_models), default=0.0)
    page_height = max((parse_float(model.get("pageHeight")) or 0.0 for model in graph_models), default=0.0)
    dx = max((parse_float(model.get("dx")) or 0.0 for model in graph_models), default=0.0)
    dy = max((parse_float(model.get("dy")) or 0.0 for model in graph_models), default=0.0)

    summary = {
        "nodes_with_geometry": len(boxes),
        "nodes_without_geometry": len(missing_geometry),
        "overlaps": len(overlaps),
        "estimated_canvas": (round(max_right), round(max_bottom)),
        "page_canvas": (round(page_width), round(page_height)),
        "viewport": (round(dx), round(dy)),
    }
    return warnings, summary


def boxes_overlap(left: BoundingBox, right: BoundingBox) -> bool:
    return left.x < right.right and left.right > right.x and left.y < right.bottom and left.bottom > right.y


def collect_cardinality_warnings(cells: list[ET.Element]) -> list[str]:
    warnings: list[str] = []
    for cell in cells:
        value = visible_value(cell)
        for match in CARDINALITY_PATTERN.finditer(value):
            cardinality = match.group(0)
            normalized = cardinality.upper()
            if normalized not in ALLOWED_CARDINALITIES:
                cell_id = cell.get("id", "(no id)")
                warnings.append(
                    f"Non-standard cardinality in mxCell {cell_id}: {cardinality}"
                )
    return warnings


def validate(path: Path, mode: str, check_layout: bool = False) -> tuple[list[str], list[str], dict[str, object]]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [f"XML is not parseable: {exc}"], [], {}
    except OSError as exc:
        return [f"Could not read file: {exc}"], [], {}

    root = tree.getroot()
    cells = find_mxcells(root)
    graph_models = find_graph_models(root)
    ids = [cell.get("id") for cell in cells if cell.get("id")]
    id_set = set(ids)
    duplicate_ids = sorted(cell_id for cell_id, count in Counter(ids).items() if count > 1)

    if "0" not in id_set:
        errors.append('Missing mxCell id="0".')
    if "1" not in id_set:
        errors.append('Missing mxCell id="1".')
    if duplicate_ids:
        errors.append("Duplicate IDs: " + ", ".join(duplicate_ids))

    missing_id_count = sum(1 for cell in cells if not cell.get("id"))
    if missing_id_count:
        errors.append(f"There are {missing_id_count} mxCell elements without id.")

    edge_count = 0
    vertex_count = 0
    attribute_oval_count = 0
    relationship_diamond_count = 0
    for cell in cells:
        if cell.get("vertex") == "1":
            vertex_count += 1
        if is_attribute_oval(cell):
            attribute_oval_count += 1
        if is_relationship_diamond(cell):
            relationship_diamond_count += 1
        if cell.get("edge") == "1":
            edge_count += 1
            cell_id = cell.get("id", "(no id)")
            source = cell.get("source")
            target = cell.get("target")
            if not source:
                errors.append(f"Edge {cell_id} has no source.")
            elif source not in id_set:
                errors.append(f"Edge {cell_id} references missing source: {source}.")
            if not target:
                errors.append(f"Edge {cell_id} has no target.")
            elif target not in id_set:
                errors.append(f"Edge {cell_id} references missing target: {target}.")

    warnings.extend(collect_cardinality_warnings(cells))
    warnings.extend(collect_type_warnings(cells, mode))
    if mode == "mer":
        warnings.extend(collect_mer_notation_warnings(cells))

    layout_summary: dict[str, object] = {}
    if check_layout:
        layout_warnings, layout_summary = collect_layout_warnings(cells, graph_models)
        warnings.extend(layout_warnings)

    summary = {
        "mx_cells": len(cells),
        "vertices": vertex_count,
        "edges": edge_count,
        "attribute_ovals": attribute_oval_count,
        "relationship_diamonds": relationship_diamond_count,
        "warnings": len(warnings),
        "errors": len(errors),
    }
    summary.update(layout_summary)
    return errors, warnings, summary


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    mode, mode_warnings = infer_mode(path, args.mode)

    errors, warnings, summary = validate(path, mode, args.check_layout)
    warnings = mode_warnings + warnings

    print("draw.io MER/MERE validation")
    print(f"File: {path}")
    print(f"Mode: {mode.upper()}")

    if summary:
        print(f"mxCell: {summary['mx_cells']}")
        print(f"Vertices: {summary['vertices']}")
        print(f"Edges: {summary['edges']}")
        if mode == "mer":
            print(f"Attribute ovals: {summary['attribute_ovals']}")
            print(f"Relationship diamonds: {summary['relationship_diamonds']}")
        if args.check_layout:
            estimated_width, estimated_height = summary["estimated_canvas"]
            page_width, page_height = summary["page_canvas"]
            viewport_width, viewport_height = summary["viewport"]
            print(f"Nodes with geometry: {summary['nodes_with_geometry']}")
            print(f"Nodes without geometry: {summary['nodes_without_geometry']}")
            print(f"Visual overlaps: {summary['overlaps']}")
            print(f"Estimated canvas: {estimated_width} x {estimated_height}")
            print(f"Page canvas: {page_width} x {page_height}")
            print(f"Viewport: {viewport_width} x {viewport_height}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("\nCritical errors:")
        for error in errors:
            print(f"- {error}")
        print("\nResult: FAIL")
        return 1

    print("\nResult: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
