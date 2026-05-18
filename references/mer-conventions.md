# MER/MERE Conventions

## Allowed Cardinalities

- `1`
- `0..1`
- `1..N`
- `0..N`

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
- In MER, do not include data types.
- In MERE, allow data types.

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

- Entities.
- Attributes.
- Relationships.
- Cardinalities.

Must not include data types.

## MERE

May include:

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
- Specialization/generalization.
- Inheritance.
- Ternary or higher-degree relationships.
- Additional constraints.
