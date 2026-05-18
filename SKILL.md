---
name: drawio-mer
description: Create, edit, validate, and review MER/MERE, DER, ER, and EER diagrams in .drawio, .drawio.xml, or diagrams.net XML files. Use this skill when Codex needs to generate, modify, fix, layout, or validate draw.io entity-relationship diagrams with Chen-style MER notation, entity rectangles, attribute ovals, relationship diamonds, cardinalities, weak entities, associative entities, specialization/generalization, inheritance, or MER/MERE course notation.
---

# Draw.io MER / MERE

Use this skill to work with entity-relationship models in draw.io/diagrams.net using editable, versionable, uncompressed XML.

## Core Mapping

- `MER` = Spanish course notation for a conceptual ER model.
- `MERE` = Spanish course notation for an EER / Extended Entity-Relationship model.
- `DER` is often used by the user as a diagram artifact for MER/MERE.

Definitive rule:

- MER = classic Chen-style notation: entity rectangles + attribute ovals + relationship diamonds + cardinalities, without data types.
- MERE = extended model: entity/table blocks with internal attributes are allowed, extended elements are allowed, and data types are allowed.

## Trigger Cases

Use this skill when the user asks to:

- Create or edit a MER, MERE, DER, ER model, or EER model.
- Work with `.drawio`, `.drawio.xml`, or diagrams.net XML files.
- Convert a domain description into an entity-relationship diagram.
- Add or correct entities, attributes, relationships, or cardinalities.
- Add weak entities, associative entities, composite/multivalued/derived attributes, inheritance, specialization/generalization, or ternary relationships.
- Validate draw.io XML or review consistency between entities, attributes, relationships, and cardinalities.

## MER Rules

A MER must use classic Chen-style visual notation.

MER must show:

- Entities as rectangles containing only the entity name.
- Attributes as ovals/bubbles connected to the owning entity.
- Relationships as diamonds/rhombi connected to entities.
- Cardinalities on the connectors between entities and relationship diamonds.

MER must not show:

- Attributes inside entity rectangles.
- Data types.
- SQL syntax.
- Field sizes.
- Physical database details.

Correct MER entity and attributes:

```text
[Cliente] -- (id_cliente)
[Cliente] -- (nombre)
[Cliente] -- (email)
[Cliente] -- (telefono)
```

Incorrect MER entity:

```text
Cliente
----------------
id_cliente
nombre
email
telefono
```

Incorrect MER attributes with data types:

```text
Cliente
----------------
id_cliente: int
nombre: varchar(100)
```

Correct MER relationship:

```text
Cliente -- 1 -- <realiza> -- 0..N -- Pedido
```

## MERE Rules

A MERE includes MER concepts and may add extended modeling features. MERE may use entity/table blocks with internal attributes, especially when data types are useful.

MERE may show:

- Entities with internal attributes.
- Relationships as diamonds/rhombi or clear labeled connectors.
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

Correct MERE entity:

```text
Cliente
----------------
id_cliente: int
nombre: varchar(100)
email: varchar(150)
telefono: varchar(20)
```

## Decision Rules

- When the user says `MER`, create Chen-style diagrams: rectangles for entities, ovals for attributes, diamonds for relationships, and connector labels for cardinalities.
- When the user says `MERE`, `MER extendido`, weak entity, inheritance, specialization/generalization, composite attribute, multivalued attribute, derived attribute, or ternary relationship, create an extended model and allow internal attributes/data types.
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

MER entity example:

```xml
<mxCell id="entity_cliente" value="Cliente" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="120" y="120" width="120" height="50" as="geometry"/>
</mxCell>
```

MER attribute example:

```xml
<mxCell id="attr_cliente_nombre" value="nombre" style="ellipse;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="80" y="60" width="120" height="45" as="geometry"/>
</mxCell>
```

MER relationship example:

```xml
<mxCell id="rel_realiza" value="realiza" style="rhombus;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="290" y="120" width="120" height="70" as="geometry"/>
</mxCell>
```

## Visual Conventions

MER:

- Entities: rectangles with entity name only.
- Attributes: ovals/bubbles connected to the owning entity.
- Relationships: diamonds/rhombi connected between entities.
- Cardinalities: labels on entity-to-relationship connectors.

MERE:

- Entities: table/block style may contain attributes internally.
- Data types: allowed.
- Relationships: prefer diamonds/rhombi for clarity, but labeled connectors are acceptable when the model is dense.
- Extended elements: visually distinguish weak/associative entities and inheritance structures.

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
- For MER, draw each attribute as an oval connected to an entity.
- For MER, do not include data types.
- For MERE, internal attributes and data types are allowed.
- Avoid `PK` and `FK` prefixes unless the user asks for a more logical/relational model.

MER attribute example:

```text
(id_producto) -- [Producto]
(nombre) -- [Producto]
(precio) -- [Producto]
(stock) -- [Producto]
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

## Workflow

To create a MER:

1. Identify entities.
2. Identify attributes.
3. Identify relationships.
4. Determine cardinalities.
5. Create entity rectangles with names only.
6. Create attribute ovals and connect them to entities.
7. Create relationship diamonds and connect them to entities.
8. Add cardinality labels on entity-to-relationship connectors.
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
8. Keep the existing visual style unless the user asks to convert notation.
9. Do not add data types or internal entity attributes if the diagram is MER.
10. Allow data types and internal attributes if the diagram is MERE.

## Validation Checklist

Before returning a `.drawio` file, check:

- XML is parseable.
- `mxCell id="0"` exists.
- `mxCell id="1"` exists.
- IDs are unique.
- Each edge references existing `source` and `target` cells.
- Cardinalities use the expected format.
- MER entities are rectangles with names only.
- MER attributes are ovals connected to entities.
- MER relationships are diamonds/rhombi connected to entities.
- MER has no data types.
- MERE may include internal attributes and data types.

## Included Scripts

- `scripts/create_basic_mer.py`: creates a basic Chen-style MER example without data types.
- `scripts/create_basic_mere.py`: creates a basic MERE example with internal attributes, data types, relationship diamonds, and an associative/weak detail entity.
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
