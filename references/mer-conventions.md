# MER/MERE Conventions

## Allowed Cardinalities

- `1`
- `0..1`
- `1..N`
- `0..N`

## MER Shape Rules

- Entity: rectangle, name only.
- Attribute: oval/bubble connected to the owning entity.
- Key attribute: oval/bubble with underline style or another explicit key marker.
- Relationship: diamond/rhombus connected to participating entities.
- Relationship attribute: oval/bubble connected to the relationship diamond.
- Cardinality: connector label between an entity and a relationship diamond.
- Weak entity: double rectangle or an explicit weak-entity style.
- Identifying relationship: double diamond or an explicit identifying-relationship style.
- Partial key: key-style attribute marked as partial.
- Composite attribute: parent attribute oval connected to component ovals.
- Multivalued attribute: double oval or explicit multivalued style.
- Derived attribute: dashed oval or explicit derived style.
- Ternary relationship: one diamond connected to three entities.

## Compact MER Shape Rules

Use compact MER only when full Chen-style attributes would make the model unreadable.

- Entity: rectangle, name only.
- Identifier: oval/bubble connected to the owning entity.
- Non-key attributes: compact list block below the entity, marked with `attrs_` ID prefix or `drawioMerCompactAttrs=1`.
- Relationship: diamond/rhombus placed between participating entities.
- Cardinality: connector label between an entity and a relationship diamond.
- Data types: not allowed.

## MERE Shape Rules

- Use MER shape rules as the base conceptual notation.
- Specialization/generalization: connect supertype and subtypes through a clear ISA/generalization node.
- Mark disjoint/overlap and total/partial constraints when known.
- Categories/unions must be visually distinguished.
- Data types, `PK`, `FK`, SQL, field sizes, and internal table-like attributes are not allowed in conceptual MERE.

## Entity Names

- Use singular nouns.
- Use clear names.
- Use PascalCase or initial uppercase.

Examples:

- Cliente
- Pedido
- Producto
- DetallePedido

## Attribute Names

- Use clear names.
- Use `snake_case` or `camelCase`.
- Keep naming consistent.
- In MER, draw each attribute as an oval.
- In MERE, draw each conceptual attribute as an oval.
- In MER and MERE, do not include data types, `PK`, `FK`, SQL syntax, or field sizes.

Correct MER examples:

- id_cliente
- nombre
- email
- fecha_pedido
- total

Correct MERE examples:

- id_persona
- nombre
- segmento
- cargo

Incorrect for conceptual MER/MERE:

- id_cliente INT
- PK id_cliente
- FK id_cliente
- nombre VARCHAR(100)
- fecha_pedido DATE
- total DECIMAL(10,2)

## Relationship Names

Use verbs or descriptive phrases.

Examples:

- realiza
- contiene
- pertenece a
- paga
- genera
- administra
- referencia

## MER

Must include:

- Entity rectangles.
- Attribute ovals.
- Relationship diamonds.
- Cardinalities.

For compact MER, only identifiers need attribute ovals; non-key attributes may use compact list blocks below entities.

Must not include internal entity attributes or data types. Compact list blocks are allowed only when they are outside the entity rectangle and marked as compact attributes.

For relational-design readiness, also check:

- Every entity has an identifier candidate, usually an attribute like `id_entidad`, `codigo`, `numero`, or a clearly named natural key.
- Every relationship has cardinality and optionality on both participating entity sides.
- Direct M:N relationships are allowed in conceptual MER.
- Relationship attributes are allowed in conceptual MER.
- M:N relationships with relationship attributes should be reviewed for relational design, but only become associative entities when they have their own identity, lifecycle, participation in other relationships, or explicit relational-design intent.
- Weak or dependent entities should be visually distinguished and tied to their identifying relationship.

## MERE

May include:

- Entities.
- Attribute ovals.
- Relationships.
- Cardinalities.
- Weak entities.
- Associative entities.
- Composite attributes.
- Multivalued attributes.
- Derived attributes.
- Specialization/generalization.
- Inheritance.
- Ternary or higher-degree relationships.
- Additional constraints.

Must not include data types, `PK`, `FK`, SQL syntax, field sizes, or internal table-like attributes unless the user asks for a separate logical/relational model.
