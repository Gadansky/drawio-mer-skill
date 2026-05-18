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
    ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})


def add_attribute_group(
    root: ET.Element,
    entity_id: str,
    entity_key: str,
    attributes: list[tuple[str, int, int]],
) -> None:
    for index, (attribute, x, y) in enumerate(attributes, start=1):
        attr_id = f"attr_{entity_key}_{attribute}"
        add_vertex(root, attr_id, attribute, ATTRIBUTE_STYLE, x, y, 130, 46)
        add_edge(
            root,
            f"edge_{entity_key}_attr_{index}",
            "",
            attr_id,
            entity_id,
            ATTRIBUTE_EDGE_STYLE,
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
            "pageWidth": "1100",
            "pageHeight": "850",
            "math": "0",
            "shadow": "0",
        },
    )
    root = ET.SubElement(graph, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    add_vertex(root, "entity_cliente", "Cliente", ENTITY_STYLE, 120, 280, 130, 55)
    add_vertex(root, "entity_pedido", "Pedido", ENTITY_STYLE, 480, 280, 130, 55)
    add_vertex(root, "entity_producto", "Producto", ENTITY_STYLE, 840, 280, 130, 55)

    add_vertex(root, "rel_realiza", "realiza", RELATIONSHIP_STYLE, 315, 270, 110, 75)
    add_vertex(root, "rel_contiene", "contiene", RELATIONSHIP_STYLE, 675, 270, 110, 75)

    add_edge(root, "edge_cliente_realiza", "1", "entity_cliente", "rel_realiza")
    add_edge(root, "edge_realiza_pedido", "0..N", "rel_realiza", "entity_pedido")
    add_edge(root, "edge_pedido_contiene", "1..N", "entity_pedido", "rel_contiene")
    add_edge(root, "edge_contiene_producto", "0..N", "rel_contiene", "entity_producto")

    add_attribute_group(
        root,
        "entity_cliente",
        "cliente",
        [
            ("id_cliente", 70, 130),
            ("nombre", 220, 130),
            ("email", 55, 410),
            ("telefono", 215, 410),
        ],
    )
    add_attribute_group(
        root,
        "entity_pedido",
        "pedido",
        [
            ("id_pedido", 430, 130),
            ("fecha_pedido", 585, 130),
            ("total", 430, 410),
            ("estado", 585, 410),
        ],
    )
    add_attribute_group(
        root,
        "entity_producto",
        "producto",
        [
            ("id_producto", 790, 130),
            ("nombre", 945, 130),
            ("precio", 790, 410),
            ("stock", 945, 410),
        ],
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
