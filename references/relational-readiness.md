# Relational Readiness for MER

Use this reference when a MER must be good enough to support later relational database design.

## Goal

A MER can be conceptually valid while still being incomplete for relational design. Before finalizing the diagram, identify what is confirmed, what is missing, and what was assumed.

## Required Checks

- Entities: each entity should have a clear identifier candidate.
- Attributes: each attribute should belong to one entity or, when it describes a relationship, the relationship should become an associative entity.
- Relationships: each relationship should have a name, participating entities, cardinality, and optionality on each side.
- M:N relationships: direct diamonds are valid in conceptual MER, but use an associative entity when the relationship has attributes, lifecycle, state, date, amount, quantity, role, grade, status, or another fact of its own.
- Weak/dependent entities: mark them visually and show the identifying relationship.
- Multivalued attributes: flag them because they often become separate relations later.
- Composite attributes: clarify whether they remain conceptual or will be decomposed later.
- Derived attributes: mark them as derived and avoid treating them as stored data unless requested.

## Missing Concept Report

When the domain is incomplete, report:

- `Confirmed concepts`: what is clear enough to diagram.
- `Missing concepts`: identifiers, cardinalities, optionalities, attributes, relationship ownership, or business rules still unknown.
- `Assumptions`: anything inferred to make progress.
- `Pending questions`: only the questions needed to close the MER.
- `Relational design impact`: how unresolved items would affect tables, PKs, FKs, associative entities, or normalization.

## M:N Rule

Use this distinction:

- Conceptual MER: `Estudiante 0..N -- inscribe -- 0..N Asignatura` is allowed.
- MER ready for relational design: if `inscribe` has `fecha_inscripcion`, `estado`, `nota`, `monto`, `cantidad`, or similar attributes, replace it with an associative entity such as `Inscripcion`.
- Logical relational model: every M:N becomes an intermediate table, but that is a separate model unless the user asks for it.

## Do Not Invent Silently

If a required concept is missing, either ask for it or mark an assumption explicitly. Do not hide inferred identifiers, cardinalities, optionalities, or associative entities as if they were provided by the domain.
