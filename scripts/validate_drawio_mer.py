#!/usr/bin/env python3
"""Validate uncompressed draw.io XML for MER/MERE diagrams."""

from __future__ import annotations

import argparse
import html
import re
import sys
from collections import Counter
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


def validate(path: Path, mode: str) -> tuple[list[str], list[str], dict[str, int]]:
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

    summary = {
        "mx_cells": len(cells),
        "vertices": vertex_count,
        "edges": edge_count,
        "attribute_ovals": attribute_oval_count,
        "relationship_diamonds": relationship_diamond_count,
        "warnings": len(warnings),
        "errors": len(errors),
    }
    return errors, warnings, summary


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    mode, mode_warnings = infer_mode(path, args.mode)

    errors, warnings, summary = validate(path, mode)
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
