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

The skill scripts use only Python standard library modules.

## Repository Safety Notes

This repository intentionally includes only the skill files, examples, references, and scripts. It should not include local Codex state, API keys, `.env` files, private diagrams, local course repositories, or machine-specific paths.
