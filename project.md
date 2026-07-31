---
name: "hr8799-jwst-orbits"
version: "0.1.0"
status: "active"
created: "2026-07-29"
goal: "Analyze JWST high-contrast imaging data of HR 8799 exoplanets (b, c, d, e), extract astrometry, and fit orbital parameters and periods."
deadline: ""
downstream: []
dod:
  - "Query and download public MAST JWST FITS datasets for HR 8799"
  - "Extract relative astrometry (separation & PA) for visible planets"
  - "Combine JWST astrometry with historical ground-based records"
  - "Perform Bayesian orbit fitting to calculate orbital periods (P, a, e, i)"
active_plan: ""
strategy: ~
roadmap: ~
csa:
  spec_threshold: 90
  doc_threshold: 50
  doc_gate: soft
has_rules: false  # DEPRECATED v1.6.2 — kept for backward compat
last_reviewed: ""
tags: ["jwst", "astronomy", "exoplanets", "hr8799", "orbit-fitting"]
milestones: []
---

# Project: hr8799-jwst-orbits

## Goal

Query and process public JWST imaging data for the HR 8799 exoplanetary system, extract precision astrometry for planets b, c, d, and e, and perform orbital fitting to determine their orbital periods.

## Scope

- **In Scope**:
  - MAST API querying & archival data fetching for HR 8799 (NIRCam / MIRI coronagraphy).
  - Relative astrometry extraction (pixel offset, separation in mas, position angle in degrees).
  - Orbit fitting using `orbitize!` combining JWST and archival astrometry.
  - Derivation of orbital periods, semi-major axes, eccentricities, and inclinations.
- **Out of Scope**:
  - Raw atmospheric spectral fitting (chemistry modeling).

## Definition of Done

1. MAST query script to download HR 8799 FITS files.
2. Astrometry extraction script / notebook for planetary positions.
3. Orbit fitting script producing MCMC posterior distributions for orbital periods.
4. Summary walkthrough / report of derived orbital parameters.

## Links

- Backlog: `artifacts/tasks/backlog.md`
- Sessions: `sessions/`

