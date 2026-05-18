# MER/MERE Conventions

## Allowed Cardinalities

- `1`
- `0..1`
- `1..N`
- `0..N`

## MER Shape Rules

- Entity: rectangle, name only.
- Attribute: oval/bubble connected to the owning entity.
- Relationship: diamond/rhombus connected to participating entities.
- Cardinality: connector label between an entity and a relationship diamond.

## MERE Shape Rules

- Entity: table/block style may contain internal attributes.
- Attribute data types are allowed.
- Relationship diamonds are preferred for clarity.
- Weak/associative entities must be visually distinguished.

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
- In MER, do not include data types.
- In MERE, internal attributes and data types are allowed.

Correct MER examples:

- id_cliente
- nombre
- email
- fecha_pedido
- total

Correct MERE examples:

- id_cliente: int
- nombre: varchar(100)
- fecha_pedido: date
- total: decimal(10,2)

Incorrect for conceptual MER:

- id_cliente INT
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

Must not include internal entity attributes or data types.

## MERE

May include:

- Entities.
- Internal attributes.
- Relationships.
- Cardinalities.
- Data types.
- Weak entities.
- Associative entities.
- Composite attributes.
- Multivalued attributes.
- Derived attributes.
- Specialization/generalization.
- Inheritance.
- Ternary or higher-degree relationships.
- Additional constraints.
