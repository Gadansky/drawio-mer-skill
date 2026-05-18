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
EDGE_STYLE = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"


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
        {"x": str(x), "y": str(y), "width": "210", "height": "150", "as": "geometry"},
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
            "dx": "1100",
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
        110,
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
        350,
        110,
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
        755,
        110,
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
        500,
        360,
        style=ASSOCIATIVE_STYLE,
        note="Entidad asociativa/debil",
    )

    add_edge(root, "edge_cliente_pedido", "1 realiza 0..N", "entity_cliente", "entity_pedido")
    add_edge(
        root,
        "edge_pedido_detalle",
        "1 contiene 1..N",
        "entity_pedido",
        "entity_detalle_pedido",
    )
    add_edge(
        root,
        "edge_detalle_producto",
        "0..N referencia 1",
        "entity_detalle_pedido",
        "entity_producto",
    )

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
