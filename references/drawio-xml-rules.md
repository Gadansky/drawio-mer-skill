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

## Entities

Entities are nodes with `vertex="1"`.

Example:

```xml
<mxCell id="entity_cliente" value="Cliente&lt;br&gt;id_cliente&lt;br&gt;nombre&lt;br&gt;email" vertex="1" parent="1">
  <mxGeometry x="120" y="120" width="180" height="120" as="geometry"/>
</mxCell>
```

## Relationships

Relationships are connectors with `edge="1"`.

Example:

```xml
<mxCell id="edge_cliente_pedido" value="1 realiza 0..N" edge="1" source="entity_cliente" target="entity_pedido" parent="1">
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
- In MER, data types are absent.
- In MERE, data types are allowed.
