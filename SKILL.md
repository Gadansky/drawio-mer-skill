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
- Validate draw.io XML or review consistency between entities, attributes, relationships, cardinalities, identifiers, optionality, and readiness for relational design.

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
- A conceptual MER may show a direct M:N relationship with a diamond.
- A MER ready for relational design must convert an M:N relationship into an associative entity when the relationship has its own attributes, meaningful lifecycle, or transactional identity.
- The logical/relational model is separate from the MER; mention likely tables, PKs, and FKs only as warnings or notes unless the user asks for that model.

## Pre-Diagram Completeness Check

Before generating or finalizing a MER intended for relational design, check whether the domain has enough information. Do not silently invent missing concepts. If information is missing, state it as a pending question or explicit assumption.

Report:

- Confirmed concepts: entities, attributes, relationships, identifiers, cardinalities, optionality, and business rules that are clear.
- Missing concepts: entities without identifiers, relationships without cardinality or optionality, ambiguous attributes, unresolved weak/dependent entities, and M:N relationships that may need an associative entity.
- Assumptions used: any inferred entity, cardinality, identifier, optionality, relationship name, or associative entity.
- Pending questions: the minimum questions needed to close the MER.

Read `references/relational-readiness.md` when the user asks for a MER suitable for database design, relational design, model review, normalization preparation, or conceptual completeness.

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

## Layout Rules

Use a geometric layout plan before writing XML. For medium diagrams, start with a minimum canvas of `2400 x 1600 px`; this is a baseline, not a maximum.

Required layout process:

1. Plan a node table before writing XML with `id`, `type`, `x`, `y`, `width`, `height`, and `zone`.
2. Use a grid and functional zones/modules instead of improvised coordinates.
3. Increase `pageWidth`, `pageHeight`, `dx`, and `dy` when the node count grows.
4. Split large databases into multiple pages when one page becomes illegible.
5. Prefer pages such as overview, sales, users/permissions, production, audit/tracing, and notifications when the domain is large.

Minimum spacing:

- Keep at least `120 px` horizontal separation between entities and relationship diamonds.
- Keep at least `100 px` vertical separation between entities and relationship diamonds.
- Keep at least `60 px` separation between attribute ovals.
- Do not place relationships on top of entities.
- Do not place attributes on top of entities.
- Do not place cardinality labels on top of nodes.
- Place relationship diamonds between the participating entities.
- Use orthogonal connectors whenever possible.

Edge routing rules:

- Plan free horizontal and vertical connector lanes in the same grid used for nodes.
- Reserve space between functional zones for connector lanes.
- Connect from the nearest logical side of each node; do not rely on center-to-center lines when that would cross other shapes.
- Use explicit intermediate `mxPoint` waypoints inside `<Array as="points">` for routed connectors.
- Route attribute connectors through short lanes above, below, or beside the owning entity.
- Route entity-relationship-entity paths through clean orthogonal segments.
- Do not allow edge segments to pass through the bounding boxes of entities, attributes, relationship diamonds, MERE blocks, or labels.
- If a crossing is intentionally unavoidable, mark only that edge with `ignoreRouteCrossing=1` in its style and explain why.

Recommended visual sizes:

- MER entity rectangle: `140 x 50`.
- MER attribute oval: `120 x 45`.
- MER relationship diamond: `120 x 70`.
- MERE entity/table block: `180-260 px` wide, variable height based on attributes.

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
5. Determine optionality on each side of every relationship.
6. Identify candidate identifiers for every entity.
7. Check whether M:N relationships have own attributes or lifecycle; if yes, model an associative entity.
8. Group entities by functional zone.
9. Plan the node table with coordinates and dimensions.
10. Create entity rectangles with names only.
11. Create attribute ovals and connect them to entities.
12. Create relationship diamonds and connect them to entities.
13. Add cardinality labels on entity-to-relationship connectors.
14. Expand canvas or split pages if needed.
15. Validate in MER mode, and use `--check-layout` for visual overlap and edge route checks.

To create a MERE:

1. Identify entities and attributes.
2. Identify extended elements.
3. Group entities by functional zone.
4. Plan the node table with coordinates and dimensions.
5. Add weak/associative entities if needed.
6. Add relationships and cardinalities.
7. Add inheritance/specialization/generalization if needed.
8. Add ternary relationships if needed.
9. Add data types when appropriate.
10. Expand canvas or split pages if needed.
11. Validate in MERE mode, and use `--check-layout` for visual overlap and edge route checks.

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
- Every entity has a recognizable identifier or an explicit warning explaining what identifier is missing.
- Every relationship has visible cardinality on each entity side.
- M:N relationships with attributes are represented as associative entities.
- Weak/dependent entities are visually distinguished or flagged as unresolved.
- Visual vertices have `mxGeometry` with `x`, `y`, `width`, and `height`.
- Visible nodes do not overlap unless explicitly justified with `ignoreLayoutOverlap=1` in style.
- Edge routes do not cross visible node bounding boxes unless explicitly justified with `ignoreRouteCrossing=1` in the edge style.
- The canvas is large enough for the number of nodes, or the model is split into pages.

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
6. Ready to diagram or finalize: yes/no.
7. Missing concepts needed to close the MER.
8. Assumptions applied.
9. Relational design impact.
10. Validations performed.
11. Warnings or inconsistencies, if any.
