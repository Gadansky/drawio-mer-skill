# MER vs MERE

## Mapping

- `MER` = Spanish course notation for a conceptual ER model.
- `MERE` = Spanish course notation for an EER / Extended Entity-Relationship model.

## MER

A MER represents the conceptual structure of a domain.

It includes:

- Entities.
- Attributes.
- Relationships.
- Cardinalities.

It does not include:

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

## MERE

MERE means `Modelo Entidad-Relacion Extendido`.

It includes MER elements and may add:

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

If the user asks for `MER`, generate entities, attributes, relationships, and cardinalities without data types.

If the user asks for `MERE`, `MER extendido`, weak entities, inheritance, specialization, generalization, composite attributes, multivalued attributes, derived attributes, or ternary relationships, generate MERE and allow data types.

MER = entities + attributes + relationships + cardinalities, without data types.

MERE = MER + extended elements + data types allowed.
