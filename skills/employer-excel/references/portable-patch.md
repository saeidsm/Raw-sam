# Portable scalar edits, followed by native finalization

Evidence: `validation/portability/2026-11-20/excel.json`. Local and Linux DevOps executions produced the identical XLSX bytes; Windows Excel subsequently recalculated, saved, reopened and printed the candidate. This is scoped acceptance, not full cloud Office equivalence.

Use the source pointed to by catalog.modules.employer_excel.latest_output. Prepare a JSON plan with `source_sha256` and `changes[{sheet,cell,old,new}]`; exact sheet names, including spaces, matter. Numeric values stay numbers; text stays text. Every update requires reconciled weekly evidence. Never reuse the synthetic test plan as real inputs.

Run from repository root:

```sh
python skills/employer-excel/scripts/patch_existing_cells.py --source source.xlsx --plan changes.json --output candidate.xlsx --audit patch-audit.json
```

The helper only changes existing non-formula scalar cells. It preserves every untouched ZIP member byte-for-byte, preserves target cell styles, protects formulas, and sets full calculation on load. It refuses a mismatched source hash, stale old value, duplicate cell, missing cell or formula target. It does not add records, rename sheets, modify formulas, resize charts or redesign a template. Route unsupported edits to native Excel or a separately verified method; do not silently omit them. Do not save this template through openpyxl or full artifact re-export on the strength of this narrow test.

Formula/chart caches are NOT refreshed by this helper. Treat the result as a candidate, not a fully calculated workbook. A Windows Excel operator/agent must rebuild calculations, save, reopen, compare formulas/objects/layouts against a native baseline control, check dependent totals and render affected pages. Do not claim a repair-free open from an unavailable COM RepairMode property; inspect native opening outcome and preserved content. Release only after documented finalization. Cloud inspection should calculate headline amounts independently from the reviewed input, not stale caches.

For a reproducible guard test against the archived reference:

```sh
python skills/employer-excel/scripts/test_patch_existing_cells.py --source source.xlsx --plan validation/portability/2026-11-20/excel-test-plan.json
```

That plan intentionally changes staff and quantity for testing; it must never enter a production period. The reference hash is fixed and mismatch rejection is expected on a newer workbook.
