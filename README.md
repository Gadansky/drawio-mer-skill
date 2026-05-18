# Draw.io MER Skill

Codex skill for creating, editing, validating, and reviewing MER/MERE diagrams in draw.io/diagrams.net XML format.

## What It Does

- Creates and edits `.drawio`, `.drawio.xml`, and diagrams.net XML files.
- Uses uncompressed, versionable XML.
- Supports MER course notation using classic Chen-style shapes.
- Supports MERE / EER notation using extended blocks, internal attributes, and data types when appropriate.
- Provides Python scripts to generate and validate sample diagrams.

## MER vs MERE

- `MER` = entity rectangles + attribute ovals + relationship diamonds + cardinalities, without data types.
- `MERE` = MER concepts + extended elements + data types allowed.

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

Correct MERE entity:

```text
Cliente
----------------
id_cliente: int
nombre: varchar(100)
email: varchar(150)
telefono: varchar(20)
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

For connector readability, reserve horizontal and vertical lanes in the grid. Prefer explicit draw.io waypoints (`mxPoint` inside `<Array as="points">`) so relationship and attribute connectors do not pass through entities, attributes, relationship diamonds, MERE blocks, or labels.

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

`--check-layout` reports vertex geometry, estimated canvas size, visual overlaps, and edge route crossings. Overlaps and route crossings are warnings, not critical XML errors.

Test the negative overlap fixture:

```powershell
python scripts/validate_drawio_mer.py examples/overlap_invalid.drawio --mode mer --check-layout
```

Test the negative route-crossing fixture:

```powershell
python scripts/validate_drawio_mer.py examples/route_crossing_invalid.drawio --mode mer --check-layout
```

The skill scripts use only Python standard library modules.

## Repository Safety Notes

This repository intentionally includes only the skill files, examples, references, and scripts. It should not include local Codex state, API keys, `.env` files, private diagrams, local course repositories, or machine-specific paths.
