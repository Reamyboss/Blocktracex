Decision #001

## Title

Preserve Strict Engine Separation

## Status

Accepted

## Sprint

15

## Decision

Inspection Engine collects facts.

Knowledge Engine performs reasoning.

Report Engine presents knowledge.

CLI orchestrates execution.

## Motivation

Separating responsibilities allows each engine
to evolve independently while preserving
maintainability, explainability, and testability.

## Consequences

Business logic never appears in the CLI.

Reasoning never accesses the filesystem.

Reports never calculate engineering knowledge.

This architecture forms the foundation of
the Engineering Intelligence Platform.
