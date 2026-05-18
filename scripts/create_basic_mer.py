#!/usr/bin/env python3
"""Create a basic uncompressed draw.io MER example using Chen-style notation."""

from __future__ import annotations

import argparse
from pathlib import Path
from xml.etree import ElementTree as ET


ENTITY_STYLE = (
    "rounded=0;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
    "fontSize=14;strokeColor=#334155;fillColor=#f8fafc;"
)
ATTRIBUTE_STYLE = (
    "ellipse;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
    "fontSize=12;strokeColor=#334155;fillColor=#ffffff;"
)
RELATIONSHIP_STYLE = (
    "rhombus;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
    "fontSize=12;strokeColor=#334155;fillColor=#fff7ed;"
)
EDGE_STYLE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
    "html=1;endArrow=none;endFill=0;strokeColor=#64748b;fontSize=11;"
)
ATTRIBUTE_EDGE_STYLE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
    "html=1;endArrow=none;endFill=0;strokeColor=#94a3b8;"
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
    points: list[tuple[int, int]] | None = None,
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


def add_attribute_group(
    root: ET.Element,
    entity_id: str,
    entity_key: str,
    attributes: list[tuple[str, int, int]],
    entity_center: tuple[int, int],
    top_lane_y: int,
    bottom_lane_y: int,
) -> None:
    entity_center_x, entity_center_y = entity_center
    for index, (attribute, x, y) in enumerate(attributes, start=1):
        attr_id = f"attr_{entity_key}_{attribute}"
        attr_center_x = x + 60
        attr_center_y = y + 22
        lane_y = top_lane_y if attr_center_y < entity_center_y else bottom_lane_y
        add_vertex(root, attr_id, attribute, ATTRIBUTE_STYLE, x, y, 120, 45)
        add_edge(
            root,
            f"edge_{entity_key}_attr_{index}",
            "",
            attr_id,
            entity_id,
            ATTRIBUTE_EDGE_STYLE,
            points=[(attr_center_x, lane_y), (entity_center_x, lane_y)],
        )


def build_diagram() -> ET.ElementTree:
    mxfile = ET.Element(
        "mxfile",
        {
            "host": "app.diagrams.net",
            "agent": "drawio-mer-skill",
            "version": "24.7.17",
        },
    )
    diagram = ET.SubElement(mxfile, "diagram", {"id": "mer_ejemplo", "name": "MER"})
    graph = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": "1200",
            "dy": "800",
            "grid": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": "1600",
            "pageHeight": "1000",
            "math": "0",
            "shadow": "0",
        },
    )
    root = ET.SubElement(graph, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    add_vertex(root, "entity_cliente", "Cliente", ENTITY_STYLE, 120, 280, 140, 50)
    add_vertex(root, "entity_pedido", "Pedido", ENTITY_STYLE, 500, 280, 140, 50)
    add_vertex(root, "entity_producto", "Producto", ENTITY_STYLE, 880, 280, 140, 50)

    add_vertex(root, "rel_realiza", "realiza", RELATIONSHIP_STYLE, 320, 270, 120, 70)
    add_vertex(root, "rel_contiene", "contiene", RELATIONSHIP_STYLE, 700, 270, 120, 70)

    add_edge(
        root,
        "edge_cliente_realiza",
        "1",
        "entity_cliente",
        "rel_realiza",
        points=[(285, 305)],
    )
    add_edge(
        root,
        "edge_realiza_pedido",
        "0..N",
        "rel_realiza",
        "entity_pedido",
        points=[(455, 305)],
    )
    add_edge(
        root,
        "edge_pedido_contiene",
        "1..N",
        "entity_pedido",
        "rel_contiene",
        points=[(665, 305)],
    )
    add_edge(
        root,
        "edge_contiene_producto",
        "0..N",
        "rel_contiene",
        "entity_producto",
        points=[(855, 305)],
    )

    add_attribute_group(
        root,
        "entity_cliente",
        "cliente",
        [
            ("id_cliente", 70, 130),
            ("nombre", 220, 130),
            ("email", 70, 430),
            ("telefono", 220, 430),
        ],
        entity_center=(190, 305),
        top_lane_y=220,
        bottom_lane_y=380,
    )
    add_attribute_group(
        root,
        "entity_pedido",
        "pedido",
        [
            ("id_pedido", 450, 130),
            ("fecha_pedido", 600, 130),
            ("total", 450, 430),
            ("estado", 600, 430),
        ],
        entity_center=(570, 305),
        top_lane_y=220,
        bottom_lane_y=380,
    )
    add_attribute_group(
        root,
        "entity_producto",
        "producto",
        [
            ("id_producto", 830, 130),
            ("nombre", 980, 130),
            ("precio", 830, 430),
            ("stock", 980, 430),
        ],
        entity_center=(950, 305),
        top_lane_y=220,
        bottom_lane_y=380,
    )

    return ET.ElementTree(mxfile)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a basic Chen-style MER .drawio file.")
    parser.add_argument("output", help="Output .drawio path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    tree = build_diagram()
    ET.indent(tree, space="  ")
    tree.write(output, encoding="utf-8", xml_declaration=True)
    print(f"MER generated: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
