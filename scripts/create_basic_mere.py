#!/usr/bin/env python3
"""Create a basic uncompressed draw.io MERE example."""

from __future__ import annotations

import argparse
from pathlib import Path
from xml.etree import ElementTree as ET


ENTITY_STYLE = (
    "rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;"
    "spacing=8;fontSize=12;strokeColor=#6c8ebf;fillColor=#dae8fc;"
)
ASSOCIATIVE_STYLE = (
    "rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;"
    "spacing=8;fontSize=12;strokeColor=#9673a6;fillColor=#e1d5e7;"
    "strokeWidth=2;dashed=1;"
)
RELATIONSHIP_STYLE = (
    "rhombus;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
    "fontSize=12;strokeColor=#334155;fillColor=#fff7ed;"
)
EDGE_STYLE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
    "html=1;endArrow=none;endFill=0;strokeColor=#64748b;fontSize=11;"
)
ZONE_STYLE = (
    "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;"
    "whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;fontColor=#334155;"
)


def entity_value(name: str, attributes: list[str], note: str | None = None) -> str:
    lines = [name, "----------------", *attributes]
    if note:
        lines.extend(["----------------", note])
    return "<br>".join(lines)


def add_entity(
    root: ET.Element,
    cell_id: str,
    name: str,
    attributes: list[str],
    x: int,
    y: int,
    style: str = ENTITY_STYLE,
    note: str | None = None,
) -> None:
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": cell_id,
            "value": entity_value(name, attributes, note),
            "style": style,
            "vertex": "1",
            "parent": "1",
        },
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {"x": str(x), "y": str(y), "width": "220", "height": "155", "as": "geometry"},
    )


def add_relationship(
    root: ET.Element,
    cell_id: str,
    value: str,
    x: int,
    y: int,
) -> None:
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": cell_id,
            "value": value,
            "style": RELATIONSHIP_STYLE,
            "vertex": "1",
            "parent": "1",
        },
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {"x": str(x), "y": str(y), "width": "120", "height": "80", "as": "geometry"},
    )


def add_zone_label(root: ET.Element, cell_id: str, value: str, x: int, y: int) -> None:
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": cell_id,
            "value": value,
            "style": ZONE_STYLE,
            "vertex": "1",
            "parent": "1",
        },
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {"x": str(x), "y": str(y), "width": "260", "height": "40", "as": "geometry"},
    )


def add_edge(
    root: ET.Element,
    cell_id: str,
    value: str,
    source: str,
    target: str,
) -> None:
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": cell_id,
            "value": value,
            "style": EDGE_STYLE,
            "edge": "1",
            "parent": "1",
            "source": source,
            "target": target,
        },
    )
    ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})


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

    add_zone_label(root, "zone_comercial", "Zona comercial", 80, 40)
    add_zone_label(root, "zone_catalogo", "Zona catalogo", 1320, 40)
    add_zone_label(root, "zone_detalle", "Zona detalle / asociativa", 760, 640)

    add_entity(
        root,
        "entity_cliente",
        "Cliente",
        [
            "id_cliente: int",
            "nombre: varchar(100)",
            "email: varchar(150)",
            "telefono: varchar(20)",
        ],
        80,
        120,
    )
    add_entity(
        root,
        "entity_pedido",
        "Pedido",
        [
            "id_pedido: int",
            "id_cliente: int",
            "fecha_pedido: date",
            "total: decimal(10,2)",
            "estado: varchar(30)",
        ],
        650,
        120,
    )
    add_entity(
        root,
        "entity_producto",
        "Producto",
        [
            "id_producto: int",
            "nombre: varchar(100)",
            "precio: decimal(10,2)",
            "stock: int",
        ],
        1320,
        120,
    )
    add_entity(
        root,
        "entity_detalle_pedido",
        "DetallePedido",
        [
            "id_pedido: int",
            "id_producto: int",
            "cantidad: int",
            "precio_unitario: decimal(10,2)",
        ],
        810,
        760,
        style=ASSOCIATIVE_STYLE,
        note="Entidad asociativa/debil",
    )

    add_relationship(root, "rel_realiza", "realiza", 410, 155)
    add_relationship(root, "rel_contiene", "contiene", 700, 470)
    add_relationship(root, "rel_referencia", "referencia", 1190, 470)

    add_edge(root, "edge_cliente_realiza", "1", "entity_cliente", "rel_realiza")
    add_edge(root, "edge_realiza_pedido", "0..N", "rel_realiza", "entity_pedido")
    add_edge(root, "edge_pedido_contiene", "1", "entity_pedido", "rel_contiene")
    add_edge(root, "edge_contiene_detalle", "1..N", "rel_contiene", "entity_detalle_pedido")
    add_edge(root, "edge_detalle_referencia", "0..N", "entity_detalle_pedido", "rel_referencia")
    add_edge(root, "edge_referencia_producto", "1", "rel_referencia", "entity_producto")

    return ET.ElementTree(mxfile)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a basic MERE .drawio file.")
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
