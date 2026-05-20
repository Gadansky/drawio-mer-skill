# draw.io XML Rules

## Format

Prefer uncompressed XML.

The root may be:

- `<mxfile>`
- `<mxGraphModel>`

## Required Cells

Every diagram must preserve:

```xml
<mxCell id="0"/>
<mxCell id="1" parent="0"/>
```

## MER Entities

MER entities are rectangles with `vertex="1"` and a value containing only the entity name.

Example:

```xml
<mxCell id="entity_cliente" value="Cliente" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="120" y="120" width="120" height="50" as="geometry"/>
</mxCell>
```

## MER Attributes

MER attributes are ovals with `vertex="1"` and style containing `ellipse`.

Example:

```xml
<mxCell id="attr_cliente_nombre" value="nombre" style="ellipse;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="90" y="60" width="120" height="45" as="geometry"/>
</mxCell>
```

## MER Relationships

MER relationships are diamonds/rhombi with `vertex="1"` and style containing `rhombus`.

Example:

```xml
<mxCell id="rel_realiza" value="realiza" style="rhombus;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="280" y="120" width="120" height="70" as="geometry"/>
</mxCell>
```

## Connectors

Connectors use `edge="1"` and valid `source` and `target` IDs.

Example:

```xml
<mxCell id="edge_cliente_realiza" value="1" edge="1" source="entity_cliente" target="rel_realiza" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

Prefer explicit orthogonal routing with intermediate `mxPoint` waypoints when a direct connector would cross a node:

```xml
<mxCell id="edge_cliente_realiza" value="1" edge="1" source="entity_cliente" target="rel_realiza" parent="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="280" y="305"/>
      <mxPoint x="320" y="305"/>
    </Array>
  </mxGeometry>
</mxCell>
```

## mxGeometry and Layout

Every visible vertex must have an `mxGeometry` child with:

- `x`
- `y`
- `width`
- `height`
- `as="geometry"`

Visible nodes must not share overlapping bounding boxes. Attribute ovals, relationship diamonds, entity rectangles, MERE table blocks, and notes should all have explicit non-overlapping geometry unless the overlap is intentionally marked with `ignoreLayoutOverlap=1` in the cell style.

Labels and cardinalities should be placed outside entity rectangles, attribute ovals, relationship diamonds, and MERE blocks.

Edge routes should use planned horizontal and vertical lanes in the grid. Do not route connector segments through the bounding boxes of visible nodes. Connect from the nearest practical side of the node and reserve free lanes between functional zones. If a crossing is intentionally unavoidable, mark the edge style with `ignoreRouteCrossing=1`.

Recommended sizes:

- MER entity rectangle: `140 x 50`.
- MER attribute oval: `120 x 45`.
- MER relationship diamond: `120 x 70`.
- MERE entity/table block: `180-260 px` wide, variable height based on attributes.

For medium diagrams, use at least `2400 x 1600 px` canvas. This is a minimum baseline, not a maximum. For large relational databases, expand the canonical canvas first. Create module pages only when the user explicitly requests support views.

When validating a `.drawio` file with multiple `<diagram>` pages, layout metrics must be computed per page. Never compare bounding boxes from different pages as if they shared one canvas.

## Validation

Check:

- XML is parseable.
- IDs are unique.
- `mxCell id="0"` exists.
- `mxCell id="1"` exists.
- Edges have valid source cells.
- Edges have valid target cells.
- Cardinalities are standard.
- In MER, entity cells do not contain internal attribute lists.
- In MER, attribute ovals exist.
- In MER, relationship diamonds exist.
- In MER, data types are absent.
- In MERE, data types and internal attributes are allowed.
- With layout validation enabled, every visible vertex has geometry.
- With layout validation enabled, visual nodes do not overlap.
- With layout validation enabled, edge route segments do not cross visible node bounding boxes.
- With layout validation enabled, page-level summaries are reported separately.
- With layout validation enabled, estimated canvas size is reported.
