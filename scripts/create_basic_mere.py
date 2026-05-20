#!/usr/bin/env python3
"""Create a basic uncompressed draw.io conceptual MERE/EER example."""

from __future__ import annotations

import argparse
from pathlib import Path
from xml.etree import ElementTree as ET


ENTITY_STYLE = (
    "rounded=0;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
    "fontSize=14;strokeColor=#1d4ed8;fillColor=#eff6ff;"
)
SUBTYPE_STYLE = (
    "rounded=0;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
    "fontSize=14;strokeColor=#7c3aed;fillColor=#f5f3ff;"
)
ATTRIBUTE_STYLE = (
    "ellipse;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
    "fontSize=12;strokeColor=#334155;fillColor=#ffffff;"
)
KEY_ATTRIBUTE_STYLE = ATTRIBUTE_STYLE + "fontStyle=4;"
RELATIONSHIP_STYLE = (
    "rhombus;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
    "fontSize=12;strokeColor=#334155;fillColor=#fff7ed;"
)
GENERALIZATION_STYLE = (
    "triangle;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
    "fontSize=12;strokeColor=#0f766e;fillColor=#ccfbf1;direction=north;"
)
EDGE_STYLE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
    "html=1;endArrow=none;endFill=0;strokeColor=#64748b;fontSize=11;"
)
ATTRIBUTE_EDGE_STYLE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
    "html=1;endArrow=none;endFill=0;strokeColor=#94a3b8;"
)
ZONE_STYLE = (
    "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;"
    "whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;fontColor=#334155;"
)


def add_vertex(
    root: ET.Element,
    cell_id: str,
    value: str,
    style: str,
    x: int,
    y: int,
    width: int,
    height: int,
) -> None:
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": cell_id,
            "value": value,
            "style": style,
            "vertex": "1",
            "parent": "1",
        },
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(height),
            "as": "geometry",
        },
    )


def add_edge(
    root: ET.Element,
    cell_id: str,
    value: str,
    source: str,
    target: str,
    style: str = EDGE_STYLE,
    points: list[tuple[float, float]] | None = None,
) -> None:
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": cell_id,
            "value": value,
            "style": style,
            "edge": "1",
            "parent": "1",
            "source": source,
            "target": target,
        },
    )
    geometry = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
    if points:
        array = ET.SubElement(geometry, "Array", {"as": "points"})
        for x, y in points:
            ET.SubElement(array, "mxPoint", {"x": str(x), "y": str(y)})


def build_diagram() -> ET.ElementTree:
    mxfile = ET.Element(
        "mxfile",
        {
            "host": "app.diagrams.net",
            "agent": "drawio-mer-skill",
            "version": "24.7.17",
        },
    )
    diagram = ET.SubElement(mxfile, "diagram", {"id": "mere_ejemplo", "name": "MERE"})
    graph = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": "1200",
            "dy": "900",
            "grid": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": "2400",
            "pageHeight": "1600",
            "math": "0",
            "shadow": "0",
        },
    )
    root = ET.SubElement(graph, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    add_vertex(root, "zone_personas", "Especializacion de personas", ZONE_STYLE, 80, 20, 320, 40)

    add_vertex(root, "entity_persona", "Persona", ENTITY_STYLE, 520, 120, 140, 50)
    add_vertex(root, "entity_cliente", "Cliente", SUBTYPE_STYLE, 260, 480, 140, 50)
    add_vertex(root, "entity_empleado", "Empleado", SUBTYPE_STYLE, 860, 480, 140, 50)
    add_vertex(root, "gen_persona_tipo", "d", GENERALIZATION_STYLE, 550, 270, 80, 70)
    add_vertex(root, "rel_atiende", "atiende", RELATIONSHIP_STYLE, 560, 610, 120, 70)

    add_vertex(root, "attr_persona_id_persona", "id_persona", KEY_ATTRIBUTE_STYLE, 330, 70, 120, 45)
    add_vertex(root, "attr_persona_nombre", "nombre", ATTRIBUTE_STYLE, 720, 70, 120, 45)
    add_vertex(root, "attr_cliente_id_cliente", "id_cliente", KEY_ATTRIBUTE_STYLE, 80, 440, 120, 45)
    add_vertex(root, "attr_cliente_segmento", "segmento", ATTRIBUTE_STYLE, 80, 540, 120, 45)
    add_vertex(root, "attr_empleado_id_empleado", "id_empleado", KEY_ATTRIBUTE_STYLE, 1060, 440, 120, 45)
    add_vertex(root, "attr_empleado_cargo", "cargo", ATTRIBUTE_STYLE, 1060, 540, 120, 45)

    add_edge(root, "edge_persona_gen", "total", "entity_persona", "gen_persona_tipo", points=[(590, 230)])
    add_edge(root, "edge_gen_cliente", "ISA", "gen_persona_tipo", "entity_cliente", points=[(590, 390), (330, 390)])
    add_edge(root, "edge_gen_empleado", "ISA", "gen_persona_tipo", "entity_empleado", points=[(590, 390), (930, 390)])

    add_edge(root, "edge_cliente_atiende", "0..1", "entity_cliente", "rel_atiende", points=[(330, 645)])
    add_edge(root, "edge_empleado_atiende", "0..N", "entity_empleado", "rel_atiende", points=[(930, 645)])

    add_edge(
        root,
        "edge_persona_attr_id",
        "",
        "attr_persona_id_persona",
        "entity_persona",
        ATTRIBUTE_EDGE_STYLE,
        points=[(390, 145)],
    )
    add_edge(
        root,
        "edge_persona_attr_nombre",
        "",
        "attr_persona_nombre",
        "entity_persona",
        ATTRIBUTE_EDGE_STYLE,
        points=[(780, 145)],
    )
    add_edge(
        root,
        "edge_cliente_attr_id",
        "",
        "attr_cliente_id_cliente",
        "entity_cliente",
        ATTRIBUTE_EDGE_STYLE,
        points=[(210, 462), (260, 462)],
    )
    add_edge(
        root,
        "edge_cliente_attr_segmento",
        "",
        "attr_cliente_segmento",
        "entity_cliente",
        ATTRIBUTE_EDGE_STYLE,
        points=[(210, 562), (260, 562)],
    )
    add_edge(
        root,
        "edge_empleado_attr_id",
        "",
        "attr_empleado_id_empleado",
        "entity_empleado",
        ATTRIBUTE_EDGE_STYLE,
        points=[(1040, 462), (1000, 462)],
    )
    add_edge(
        root,
        "edge_empleado_attr_cargo",
        "",
        "attr_empleado_cargo",
        "entity_empleado",
        ATTRIBUTE_EDGE_STYLE,
        points=[(1040, 562), (1000, 562)],
    )

    return ET.ElementTree(mxfile)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a conceptual MERE .drawio file.")
    parser.add_argument("output", help="Output .drawio path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    tree = build_diagram()
    ET.indent(tree, space="  ")
    tree.write(output, encoding="utf-8", xml_declaration=True)
    print(f"MERE generated: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
