# MER vs MERE

## Mapping

- `MER` = Spanish course notation for a conceptual ER model.
- `MERE` = Spanish course notation for an EER / Extended Entity-Relationship model.

## MER

A MER represents the conceptual structure of a domain using classic Chen-style notation.

It includes:

- Entity rectangles.
- Attribute ovals connected to entities.
- Relationship diamonds connected to entities.
- Cardinalities on relationship connectors.

It does not include:

- Attributes inside entity rectangles.
- Data types.
- SQL syntax.
- Field sizes.
- Physical database details.

Correct MER example:

```text
[Cliente] -- (id_cliente)
[Cliente] -- (nombre)
[Cliente] -- (email)
[Cliente] -- (telefono)
Cliente -- 1 -- <realiza> -- 0..N -- Pedido
```

Incorrect MER example:

```text
Cliente
----------------
id_cliente
nombre
email
telefono
```

## MERE

MERE means `Modelo Entidad-Relacion Extendido`.

It includes MER concepts and may add:

- Entity/table blocks with internal attributes.
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

Correct MERE example:

```text
Cliente
----------------
id_cliente: int
nombre: varchar(100)
email: varchar(150)
telefono: varchar(20)
```

## Practical Rule

If the user asks for `MER`, generate Chen-style entities, attributes, relationships, and cardinalities without data types.

If the user asks for `MERE`, `MER extendido`, weak entities, inheritance, specialization, generalization, composite attributes, multivalued attributes, derived attributes, or ternary relationships, generate MERE and allow internal attributes/data types.

MER = entity rectangles + attribute ovals + relationship diamonds + cardinalities, without data types.

MERE = MER concepts + extended elements + data types allowed.
