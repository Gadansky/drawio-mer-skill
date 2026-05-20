# Draw.io MER Skill

Codex skill for creating, editing, validating, and reviewing MER/MERE diagrams in draw.io/diagrams.net XML format.

## What It Does

- Creates and edits `.drawio`, `.drawio.xml`, and diagrams.net XML files.
- Uses uncompressed, versionable XML.
- Supports MER course notation using classic Chen-style shapes.
- Supports compact MER for large models: identifier ovals plus compact non-key attribute lists.
- Supports conceptual MERE / EER notation with specialization/generalization, supertypes/subtypes, inheritance, and categories/unions.
- Keeps logical/relational outputs separate from conceptual MER/MERE: tables, data types, PK/FK, SQL, and field sizes are not part of MER/MERE.
- Warns about MER completeness issues before relational design, such as missing identifiers, missing cardinalities, and M:N relationships that may need associative entities.
- Provides Python scripts to generate and validate sample diagrams.

## MER vs MERE

- `MER` = entity rectangles + attribute ovals + relationship diamonds + cardinalities, without data types.
- `Compact MER` = entity rectangles + identifier ovals + compact non-key attribute lists + relationship diamonds + cardinalities, without data types.
- `MERE` = MER concepts + extended conceptual elements such as specialization/generalization, supertypes/subtypes, inheritance, and categories/unions, without data types.
- `Logical/relational model` = separate output for tables, columns, data types, PK/FK, SQL, and field sizes.

Correct MER structure:

```text
[Cliente] -- (id_cliente)
[Cliente] -- (nombre)
[Cliente] -- (email)
[Cliente] -- (telefono)
Cliente -- 1 -- <realiza> -- 0..N -- Pedido
```

Incorrect MER structure:

```text
Cliente
----------------
id_cliente
nombre
email
telefono
```

Correct MERE specialization:

```text
[Persona] -- ISA -- [Cliente]
[Persona] -- ISA -- [Empleado]
[Persona] -- (id_persona)
[Cliente] -- (segmento)
[Empleado] -- (cargo)
```

## Install

Copy this repository folder into your Codex skills directory as `drawio-mer`.

Windows example:

```powershell
git clone https://github.com/Gadansky/drawio-mer-skill.git "$env:USERPROFILE\.codex\skills\drawio-mer"
```

The skill entrypoint is `SKILL.md`.

## Scripts

Generate readable diagrams by planning zones first. For medium diagrams, use at least a `2400 x 1600` canvas. For large databases, expand the canvas or split the model into pages by module, for example overview, sales, users/permissions, production, audit/tracing, and notifications.

By default, generate one canonical MER page as the final source of truth. Use module pages only when explicitly requested as support views.

For connector readability, reserve horizontal and vertical lanes in the grid. Prefer explicit draw.io waypoints (`mxPoint` inside `<Array as="points">`) so relationship and attribute connectors do not pass through entities, attributes, relationship diamonds, MERE extended elements, or labels.

Generate a basic Chen-style MER example:

```powershell
python scripts/create_basic_mer.py examples/mer_ejemplo.drawio
```

Generate a basic MERE example:

```powershell
python scripts/create_basic_mere.py examples/mere_ejemplo.drawio
```

Validate a MER diagram:

```powershell
python scripts/validate_drawio_mer.py examples/mer_ejemplo.drawio --mode mer
```

Validate a MERE diagram:

```powershell
python scripts/validate_drawio_mer.py examples/mere_ejemplo.drawio --mode mere
```

Run visual layout validation:

```powershell
python scripts/validate_drawio_mer.py examples/mer_ejemplo.drawio --mode mer --check-layout
python scripts/validate_drawio_mer.py examples/mere_ejemplo.drawio --mode mere --check-layout
```

`--check-layout` reports vertex geometry, estimated canvas size, visual overlaps, and edge route crossings. For multi-page `.drawio` files, layout is summarized per page so unrelated pages are not compared against each other. Overlaps and route crossings are warnings, not critical XML errors.

Run relational-readiness validation:

```powershell
python scripts/validate_drawio_mer.py examples/mer_ejemplo.drawio --mode mer
python scripts/validate_drawio_mer.py examples/relationship_attribute_valid.drawio --mode mer
python scripts/validate_drawio_mer.py examples/readiness_many_to_many_with_attribute.drawio --mode mer
python scripts/validate_drawio_mer.py examples/readiness_missing_identifier.drawio --mode mer
python scripts/validate_drawio_mer.py examples/readiness_missing_cardinality.drawio --mode mer
```

Readiness warnings are not critical XML errors. They identify concepts to close before using the MER as input for relational database design. Relationship attributes are valid in conceptual MER; warnings should only prompt review for logical/relational impact.

Test the negative overlap fixture:

```powershell
python scripts/validate_drawio_mer.py examples/overlap_invalid.drawio --mode mer --check-layout
```

Test the negative route-crossing fixture:

```powershell
python scripts/validate_drawio_mer.py examples/route_crossing_invalid.drawio --mode mer --check-layout
```

Test conceptual-boundary fixtures:

```powershell
python scripts/validate_drawio_mer.py examples/invalid_mer_data_types.drawio --mode mer
python scripts/validate_drawio_mer.py examples/invalid_mere_fk.drawio --mode mere
```

The skill scripts use only Python standard library modules.

## Repository Safety Notes

This repository intentionally includes only the skill files, examples, references, and scripts. It should not include local Codex state, API keys, `.env` files, private diagrams, local course repositories, or machine-specific paths.
