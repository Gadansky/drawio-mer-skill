---
name: drawio-mer
description: Create, edit, validate, and review MER/MERE, DER, ER, and EER diagrams in .drawio, .drawio.xml, or diagrams.net XML files. Use this skill when Codex needs to generate, modify, fix, layout, or validate draw.io entity-relationship diagrams with entities, attributes, relationships, cardinalities, weak entities, associative entities, specialization/generalization, inheritance, or MER/MERE course notation.
---

# Draw.io MER / MERE

Use this skill to work with entity-relationship models in draw.io/diagrams.net using editable, versionable, uncompressed XML.

## Core Mapping

- `MER` = Spanish course notation for a conceptual ER model.
- `MERE` = Spanish course notation for an EER / Extended Entity-Relationship model.
- `DER` is often used by the user as a diagram artifact for MER/MERE.

Definitive rule:

- MER = entities + attributes + relationships + cardinalities, without data types.
- MERE = MER + extended elements + data types allowed.

## Trigger Cases

Use this skill when the user asks to:

- Create or edit a MER, MERE, DER, ER model, or EER model.
- Work with `.drawio`, `.drawio.xml`, or diagrams.net XML files.
- Convert a domain description into an entity-relationship diagram.
- Add or correct entities, attributes, relationships, or cardinalities.
- Add weak entities, associative entities, composite/multivalued/derived attributes, inheritance, specialization/generalization, or ternary relationships.
- Validate draw.io XML or review consistency between entities, attributes, relationships, and cardinalities.

## MER Rules

A MER is a conceptual model.

It must show:

- Entities.
- Attributes.
- Relationships.
- Cardinalities.

It must not show:

- Data types.
- SQL syntax.
- Field sizes.
- Physical database details.

Correct MER example:

```text
Cliente
----------------
id_cliente
nombre
email
telefono
```

Incorrect MER example:

```text
Cliente
----------------
id_cliente: int
nombre: varchar(100)
email: varchar(150)
telefono: varchar(20)
```

## MERE Rules

A MERE includes MER elements and may add extended modeling features.

It may show:

- Entities.
- Attributes.
- Relationships.
- Cardinalities.
- Data types.
- Weak entities.
- Associative entities.
- Composite attributes.
- Multivalued attributes.
- Derived attributes.
- Identifying relationships.
- Specialization/generalization.
- Inheritance.
- Ternary or higher-degree relationships.
- Additional constraints.

Correct MERE example:

```text
Cliente
----------------
id_cliente: int
nombre: varchar(100)
email: varchar(150)
telefono: varchar(20)
```

## Decision Rules

- When the user says `MER`, create entities, attributes, relationships, and cardinalities without data types.
- When the user says `MERE`, `MER extendido`, weak entity, inheritance, specialization/generalization, composite attribute, multivalued attribute, derived attribute, or ternary relationship, create an extended model and allow data types.
- If the user asks for data types in a MER, explain that the course MER notation does not include them and offer MERE or a logical/relational model instead.
- Do not add data types in MER.
- Allow data types in MERE.

## XML Requirements

Always work with uncompressed draw.io XML unless the user explicitly requests otherwise.

Preserve or create:

```xml
<root>
  <mxCell id="0"/>
  <mxCell id="1" parent="0"/>
</root>
```

Rules:

- Root may be `<mxfile>` or `<mxGraphModel>`.
- Visual nodes must use `vertex="1"`.
- Connectors must use `edge="1"`.
- Every connector must have valid `source` and `target` IDs.
- Do not duplicate IDs.
- Do not use Base64/deflate/compressed XML unless explicitly requested.
- Read the full existing file before editing it.
- Preserve existing IDs and visual style when modifying a file.
- Validate after edits.

Entity example:

```xml
<mxCell id="entity_cliente" value="Cliente&lt;br&gt;id_cliente&lt;br&gt;nombre&lt;br&gt;email" vertex="1" parent="1">
  <mxGeometry x="120" y="120" width="180" height="120" as="geometry"/>
</mxCell>
```

Relationship example:

```xml
<mxCell id="edge_cliente_pedido" value="1 realiza 0..N" edge="1" source="entity_cliente" target="entity_pedido" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## Visual Conventions

Use a simple academic style:

- Entities: rectangles, conceptual tables, or blocks with internal attributes.
- Attributes: inside entity blocks by default; use ovals only when the user requests classic Chen notation.
- Relationships: labeled connectors.
- Cardinalities: include both ends in the connector label when practical.
- Main entities: center or upper area.
- Detail/bridge entities: between the entities they connect.
- Avoid excessive colors.

Recommended cardinalities:

- `1`
- `0..1`
- `1..N`
- `0..N`

Relationship examples:

```text
Cliente 1 ---- realiza ---- 0..N Pedido
Pedido 1..N ---- contiene ---- 0..N Producto
Pedido 1 ---- contiene ---- 1..N DetallePedido
DetallePedido 0..N ---- referencia ---- 1 Producto
```

## Attribute Conventions

- Use clear names.
- Keep one naming style: `snake_case` or `camelCase`.
- For MER, do not include data types.
- For MERE, allow data types when requested or when the extended example requires them.
- Mark identifiers visually only when useful.
- Avoid `PK` and `FK` prefixes unless the user asks for a more logical/relational model.

MER attribute example:

```text
Producto
----------------
id_producto
nombre
precio
stock
```

MERE attribute example:

```text
Producto
----------------
id_producto: int
nombre: varchar(100)
precio: decimal(10,2)
stock: int
```

## Extended Elements

For weak or associative entities:

- Use a double border, dashed border, color distinction, or visible note.
- Show the identifying or connecting relationships clearly.
- Show the discriminator if applicable.

For specialization/generalization:

- Place the general entity above specialized entities.
- Use a connector or generalization triangle.
- Indicate total/partial or disjoint/overlapping only when specified by the user.

Example:

```text
Persona
  |-- Cliente
  `-- Empleado
```

## Workflow

To create a MER:

1. Identify entities.
2. Identify attributes.
3. Identify relationships.
4. Determine cardinalities.
5. Create entity blocks.
6. Add attributes without data types.
7. Add labeled relationship connectors.
8. Add cardinalities.
9. Arrange the diagram.
10. Validate in MER mode.

To create a MERE:

1. Identify entities and attributes.
2. Identify extended elements.
3. Add weak/associative entities if needed.
4. Add relationships and cardinalities.
5. Add inheritance/specialization/generalization if needed.
6. Add ternary relationships if needed.
7. Add data types when appropriate.
8. Arrange the diagram.
9. Validate in MERE mode.

To modify an existing file:

1. Read the complete file.
2. Detect `<mxfile>`, `<diagram>`, and `<mxGraphModel>`.
3. Identify all `mxCell` IDs.
4. Preserve existing IDs.
5. Add only unique new IDs.
6. Make the smallest necessary XML change.
7. Validate edges, sources, and targets.
8. Keep the existing visual style.
9. Do not add data types if the diagram is MER.
10. Allow data types if the diagram is MERE.

## Validation Checklist

Before returning a `.drawio` file, check:

- XML is parseable.
- `mxCell id="0"` exists.
- `mxCell id="1"` exists.
- IDs are unique.
- Each edge references existing `source` and `target` cells.
- Cardinalities use the expected format.
- Entity names are clear.
- Relationship names are clear.
- MER has attributes but no data types.
- MERE may include data types and visually distinct extended elements.

## Included Scripts

- `scripts/create_basic_mer.py`: creates a basic MER example without data types.
- `scripts/create_basic_mere.py`: creates a basic MERE example with data types and an associative/weak detail entity.
- `scripts/validate_drawio_mer.py`: validates draw.io XML with `--mode mer` or `--mode mere`.

## User Response Format

When creating or modifying a MER/MERE, respond with:

1. Generated or modified file.
2. Diagram type: MER or MERE.
3. Entity summary.
4. Attribute summary.
5. Relationship summary.
6. Validations performed.
7. Warnings or inconsistencies, if any.
