---
name: drawio-mer
description: "Create, edit, validate, and review conceptual MER/MERE, DER, ER, and EER diagrams in .drawio, .drawio.xml, or diagrams.net XML files. Use this skill when Codex needs to generate, modify, fix, layout, or validate draw.io entity-relationship diagrams with Chen-style conceptual notation: entity rectangles, attribute ovals, relationship diamonds, cardinalities, weak entities, relationship attributes, composite/multivalued/derived attributes, ternary relationships, specialization/generalization, supertypes/subtypes, inheritance, categories/unions, or MER/MERE course notation. Logical/relational outputs with tables, data types, PK/FK, SQL, or field sizes are separate deliverables."
---

# Draw.io MER / MERE

Use this skill to work with entity-relationship models in draw.io/diagrams.net using editable, versionable, uncompressed XML.

## Core Mapping

- `MER` = Spanish course notation for a conceptual ER model.
- `MERE` = Spanish course notation for an EER / Extended Entity-Relationship model.
- `DER` is often used by the user as a diagram artifact for MER/MERE.

Definitive rule:

- MER = conceptual ER in classic Chen-style notation: entity rectangles + attribute ovals + relationship diamonds + cardinalities, without data types, PK/FK, SQL, field sizes, or internal table-like attributes.
- Compact MER = conceptual MER variant for large models: entity rectangles + key attribute ovals + compact non-key attribute lists + relationship diamonds + cardinalities, without data types, PK/FK, SQL, or field sizes.
- MERE = conceptual EER / extended ER model: MER concepts plus specialization/generalization, supertypes/subtypes, inheritance, categories/unions, and extended constraints, still without data types, PK/FK, SQL, field sizes, or internal table-like attributes by default.
- Logical/relational model = separate deliverable for tables, internal columns, data types, PK/FK, SQL, field sizes, and physical database details.
- The default deliverable for a MER is one canonical final page. Extra module pages are optional support material only when the user explicitly asks for them.

## Trigger Cases

Use this skill when the user asks to:

- Create or edit a MER, MERE, DER, ER model, or EER model.
- Work with `.drawio`, `.drawio.xml`, or diagrams.net XML files.
- Convert a domain description into an entity-relationship diagram.
- Add or correct entities, attributes, relationships, or cardinalities.
- Add weak entities, associative entities, relationship attributes, composite/multivalued/derived attributes, inheritance, specialization/generalization, supertypes/subtypes, categories/unions, or ternary relationships.
- Validate draw.io XML or review consistency between entities, attributes, relationships, cardinalities, identifiers, optionality, and readiness for relational design.

## MER Rules

A MER must use classic Chen-style visual notation.

MER must show:

- Entities as rectangles containing only the entity name.
- Attributes as ovals/bubbles connected to the owning entity.
- Identifiers as key attributes, visually marked with underline style or another explicit key marker.
- Relationships as diamonds/rhombi connected to entities.
- Cardinalities on the connectors between entities and relationship diamonds.
- Relationship attributes as ovals connected to the relationship diamond when the attribute describes the relationship.
- Weak entities, composite attributes, multivalued attributes, derived attributes, and ternary relationships when the domain requires them.

For large models, MER may use compact notation:

- Show each entity identifier as an oval connected to the entity.
- Show non-key attributes in a compact list block under the entity.
- Mark compact list blocks with an `attrs_` ID prefix or `drawioMerCompactAttrs=1` style flag.
- Keep compact list blocks free of data types.
- Place relationship diamonds inside the entity graph, close to the participating entities.

MER must not show:

- Attributes inside entity rectangles, except compact non-key attribute list blocks outside the entity rectangle.
- Data types.
- `PK` or `FK` markers.
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

Correct MER relationship attribute:

```text
Estudiante -- 0..N -- <inscribe> -- 0..N -- Asignatura
<inscribe> -- (fecha_inscripcion)
```

## MERE Rules

A MERE is a conceptual EER / extended ER model. It includes MER concepts and may add extended modeling features while staying conceptual.

MERE may show:

- Entities as rectangles containing only the entity name.
- Attributes as ovals/bubbles connected to entities or relationships.
- Relationships as diamonds/rhombi or clear labeled connectors when the model is dense.
- Cardinalities.
- Weak entities.
- Associative entities.
- Composite attributes.
- Multivalued attributes.
- Derived attributes.
- Identifying relationships.
- Specialization/generalization.
- Supertypes and subtypes.
- Inheritance.
- Categories/unions.
- Ternary or higher-degree relationships.
- Additional constraints.

MERE must not show data types, `PK`/`FK`, SQL syntax, field sizes, physical database details, or table-like internal attributes unless the user explicitly asks for a separate logical/relational model.

Correct MERE specialization:

```text
[Persona] -- ISA -- [Cliente]
[Persona] -- ISA -- [Empleado]
[Persona] -- (id_persona)
[Cliente] -- (segmento)
[Empleado] -- (cargo)
```

## Decision Rules

- When the user says `MER`, create Chen-style diagrams: rectangles for entities, ovals for attributes, diamonds for relationships, and connector labels for cardinalities.
- When the user says `MERE`, `MER extendido`, EER, inheritance, specialization/generalization, subtype, supertype, category, union, or extended constraints, create a conceptual extended model.
- Do not switch to MERE only because the user mentions weak entities, relationship attributes, composite attributes, multivalued attributes, derived attributes, or ternary relationships; those are valid in conceptual MER.
- If the user asks for data types, `PK`, `FK`, SQL, field sizes, or table/column blocks in MER or MERE, explain that conceptual MER/MERE does not include them and offer a separate logical/relational model instead.
- Do not add data types, `PK`, `FK`, SQL syntax, field sizes, or physical details in MER or MERE.
- Use compact MER for large conceptual models when full Chen-style attribute ovals make the diagram unreadable.
- A conceptual MER may show a direct M:N relationship with a diamond.
- A conceptual MER may show attributes on relationship diamonds.
- Use an associative entity only when the relationship has its own identity, meaningful lifecycle, must participate in other relationships, or the user explicitly asks for relational-design preparation.
- The logical/relational model is separate from the MER; mention likely tables, PKs, and FKs only as warnings or notes unless the user asks for that model.
- Do not split a MER into multiple pages by default. If a single canonical page would be unreadable, warn that the scope must be reduced, grouped, or explicitly approved for support pages.

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
4. Keep the final MER as one canonical source-of-truth page by default.
5. Create module/support pages only after the user explicitly asks for them.
6. If the model is too large for a readable single page, report the problem before generating a fragmented diagram.

Minimum spacing:

- Keep at least `120 px` horizontal separation between entities and relationship diamonds.
- Keep at least `100 px` vertical separation between entities and relationship diamonds.
- Keep at least `60 px` separation between attribute ovals.
- Do not place relationships on top of entities.
- Do not place attributes on top of entities.
- Do not place cardinality labels on top of nodes.
- Place relationship diamonds between the participating entities.
- Use orthogonal connectors whenever possible.
- In compact MER, place relationship diamonds within the entity graph, not in a separate band or column.
- In compact MER, place non-key attribute list blocks directly below their entity.

Edge routing rules:

- Plan free horizontal and vertical connector lanes in the same grid used for nodes.
- Reserve space between functional zones for connector lanes.
- Connect from the nearest logical side of each node; do not rely on center-to-center lines when that would cross other shapes.
- Use explicit intermediate `mxPoint` waypoints inside `<Array as="points">` for routed connectors.
- Route attribute connectors through short lanes above, below, or beside the owning entity.
- Route entity-relationship-entity paths through clean orthogonal segments.
- Do not allow edge segments to pass through the bounding boxes of entities, attributes, relationship diamonds, MERE extended elements, or labels.
- Line-line crossings are acceptable only when the diagram remains readable.
- Line-node crossings are not acceptable in final output.
- If a crossing is intentionally unavoidable, mark only that edge with `ignoreRouteCrossing=1` in its style and explain why.

Recommended visual sizes:

- MER entity rectangle: `140 x 50`.
- MER attribute oval: `120 x 45`.
- MER relationship diamond: `120 x 70`.
- Compact MER non-key attribute block: `220-320 px` wide, variable height based on attributes.
- MERE subtype/supertype rectangle: `140 x 50`.
- MERE specialization/generalization node: `70-90 px` wide.

## Visual Conventions

MER:

- Entities: rectangles with entity name only.
- Attributes: ovals/bubbles connected to the owning entity.
- Key attributes: attribute ovals with underline style, or another visible key marker when underline is not practical.
- Relationships: diamonds/rhombi connected between entities.
- Relationship attributes: ovals/bubbles connected to the relationship diamond.
- Cardinalities: labels on entity-to-relationship connectors.
- Weak entities: double rectangle or an explicit weak-entity style.
- Identifying relationships: double diamond or an explicit identifying-relationship style.
- Partial keys: key-style attribute ovals marked as partial keys.
- Composite attributes: parent attribute oval connected to component attribute ovals.
- Multivalued attributes: double oval or explicit multivalued style.
- Derived attributes: dashed oval or explicit derived style.
- Ternary relationships: one relationship diamond connected to three participating entities.
- For large models, show only identifiers as ovals and put non-key attributes in compact list blocks below each entity.

MERE:

- Use the MER visual conventions as the base notation.
- Specialization/generalization: connect supertype and subtypes through a clear ISA/generalization node.
- Mark disjoint/overlap and total/partial constraints when known.
- Categories/unions: visually distinguish the category/union node and participating supertypes.
- Data types, `PK`, `FK`, SQL, field sizes, and table-like internal attributes are not part of conceptual MERE.

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
- For compact MER, draw each identifier as an oval and put non-key attributes in a compact list block.
- For MER, do not include data types.
- For MERE, draw conceptual attributes as ovals; do not use internal table-like attribute lists.
- For MER and MERE, do not include data types, `PK`, `FK`, SQL syntax, or field sizes.
- Use underlined text or another visible marker for identifier attributes.
- Reserve `PK` and `FK` prefixes for a separate logical/relational model requested by the user.

MER attribute example:

```text
(id_producto) -- [Producto]
(nombre) -- [Producto]
(precio) -- [Producto]
(stock) -- [Producto]
```

MERE attribute example:

```text
(id_producto) -- [Producto]
(nombre) -- [Producto]
(precio) -- [Producto]
(stock) -- [Producto]
```

## Workflow

To create a MER:

1. Identify entities.
2. Identify attributes.
3. Identify relationships.
4. Determine cardinalities.
5. Determine optionality on each side of every relationship.
6. Identify candidate identifiers for every entity.
7. Add relationship attributes to the relationship diamond when they describe the relationship.
8. Use an associative entity only when the relationship has its own identity, lifecycle, participation in other relationships, or explicit relational-design intent.
9. Group entities by functional zone.
10. Plan the node table with coordinates and dimensions.
11. Create entity rectangles with names only.
12. For small MER, create attribute ovals and connect them to entities or relationships.
13. For compact MER, create identifier ovals and compact non-key attribute blocks below entities.
14. Create relationship diamonds between participating entities.
15. Add cardinality labels on entity-to-relationship connectors.
16. Add weak entity, identifying relationship, composite/multivalued/derived attribute, or ternary notation only when needed.
17. Expand the single canonical canvas as needed.
18. Ask for scope reduction or explicit module-page approval if the single page becomes illegible.
19. Validate in MER mode, and use `--check-layout` for visual overlap and edge route checks.

To create a MERE:

1. Identify entities and attributes.
2. Identify extended elements: specialization/generalization, supertypes/subtypes, inheritance, categories/unions, or extended constraints.
3. Group entities by functional zone.
4. Plan the node table with coordinates and dimensions.
5. Create conceptual entity rectangles and attribute ovals.
6. Add relationships and cardinalities.
7. Add specialization/generalization, inheritance, supertypes/subtypes, categories/unions, or constraints.
8. Keep the model free of data types, `PK`, `FK`, SQL syntax, field sizes, and table-like internal attributes.
9. Expand canvas or split pages if needed.
10. Validate in MERE mode, and use `--check-layout` for visual overlap and edge route checks.

To modify an existing file:

1. Read the complete file.
2. Detect `<mxfile>`, `<diagram>`, and `<mxGraphModel>`.
3. Identify all `mxCell` IDs.
4. Preserve existing IDs.
5. Add only unique new IDs.
6. Make the smallest necessary XML change.
7. Validate edges, sources, and targets.
8. Keep the existing visual style unless the user asks to convert notation.
9. Do not add data types, `PK`, `FK`, SQL, field sizes, or internal table-like attributes if the diagram is MER or MERE.
10. If the existing file is logical/relational, keep it separate from conceptual MER/MERE or ask before converting notation.

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
- Compact MER has identifier ovals connected to entities and compact non-key attribute blocks below entities.
- MER relationships are diamonds/rhombi connected to entities.
- MER has no data types.
- MERE has no data types, `PK`, `FK`, SQL, field sizes, or table-like internal attributes unless it is explicitly a separate logical/relational model.
- Every entity has a recognizable identifier or an explicit warning explaining what identifier is missing.
- Every relationship has visible cardinality on each entity side.
- Relationship attributes are connected to relationship diamonds.
- M:N relationships with attributes are represented as associative entities only when they have identity, lifecycle, participation in other relationships, or explicit relational-design intent.
- Weak/dependent entities are visually distinguished or flagged as unresolved.
- Visual vertices have `mxGeometry` with `x`, `y`, `width`, and `height`.
- Visible nodes do not overlap unless explicitly justified with `ignoreLayoutOverlap=1` in style.
- Edge routes do not cross visible node bounding boxes unless explicitly justified with `ignoreRouteCrossing=1` in the edge style.
- The canonical page canvas is large enough for the number of nodes.
- Multiple pages are present only when explicitly requested as support views.

## Included Scripts

- `scripts/create_basic_mer.py`: creates a basic Chen-style MER example without data types.
- `scripts/create_basic_mere.py`: creates a conceptual MERE example with specialization/generalization, attribute ovals, and no logical/relational data types or keys.
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
