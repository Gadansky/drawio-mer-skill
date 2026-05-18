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
