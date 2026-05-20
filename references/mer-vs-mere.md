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
- PK/FK markers.
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

MERE means `Modelo Entidad-Relacion Extendido`. It is a conceptual EER / extended ER model, not a logical table model.

It includes MER concepts and may add:

- Weak entities.
- Associative entities.
- Composite attributes.
- Multivalued attributes.
- Derived attributes.
- Specialization/generalization.
- Supertypes and subtypes.
- Inheritance.
- Categories/unions.
- Ternary or higher-degree relationships.
- Additional constraints.

It does not include data types, PK/FK markers, SQL syntax, field sizes, physical database details, or internal table-like attributes unless the user explicitly asks for a separate logical/relational model.

Correct MERE example:

```text
[Persona] -- ISA -- [Cliente]
[Persona] -- ISA -- [Empleado]
[Persona] -- (id_persona)
[Cliente] -- (segmento)
[Empleado] -- (cargo)
```

## Practical Rule

If the user asks for `MER`, generate Chen-style entities, attributes, relationships, and cardinalities without data types.

If the user asks for `MERE`, `MER extendido`, EER, inheritance, specialization, generalization, subtype, supertype, category, union, or extended constraints, generate conceptual MERE.

Do not switch to MERE only because the user asks for weak entities, relationship attributes, composite attributes, multivalued attributes, derived attributes, or ternary relationships; those are valid in conceptual MER.

MER = entity rectangles + attribute ovals + relationship diamonds + cardinalities, without data types.

MERE = MER concepts + extended conceptual elements, without data types or logical/relational markers.

Logical/relational model = separate deliverable for tables, columns, data types, PK/FK, SQL, and field sizes.
