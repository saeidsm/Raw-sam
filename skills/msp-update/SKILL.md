---
name: msp-update
description: Update Pardis native MPP cumulative quantities from a reconciled shared freeze, preserving native formulas, schedule fields and prior quantities.
---

Repository: https://github.com/saeidsm/Raw-sam

Read root `SKILL.md`, `integrations/msp-update/manifest.json`, and `docs/shared-freeze.md`. Resolve paths from the repository root. The handoff is registered and historically tested, but coverage is partial; discover current native capabilities before execution. Windows with licensed Microsoft Project COM and Windows PowerShell 5.1 is the tested path. A cloud agent needs an equivalent verified native service; Markdown alone cannot edit/recalculate MPP. Never present renamed XML as MPP.

Read `mappings/README.md`, `mappings/native-fields.json` and the source decisions under the manifest's `handoff_root`. Those are dated evidence; current shared decisions and unresolved questions govern new runs. Use `integrations/msp-update/mappings.json` for canonical identities. Recheck workbook headers, cells, face, phase and unit each period; the 418-row map is not complete project coverage.

- Write leaf `Number5` only, keyed by UniqueID. Compute full-precision Excel fraction × existing native `Number9`, after reconciling fraction with min(quantity / workbook total, 1). Physical spreadsheet volumes and schedule-normalized volumes are different measures. Preserve `Number9`, weights, formulas, hierarchy, calendars, status date, costs and planned progress; `% Complete` is planned in this schedule.
- Respect the confirmed nonnegative-update rule. A proposed decrease is a recorded exception, never silently applied or changed into physical progress. Preserve prior values above the total when the fraction is already capped. Missing reports are null and keep prior schedule values with an explicit exception. Summary rows are calculated, not written.
- Scope exclusion for management analysis does not authorize deleting native tasks or rebasing the schedule. The west/all-faces cement-board discrepancy is recorded in the shared questions. Agriculture clamp belongs to Aran; unknown contract allocation stays null. Hold applies only to brick-faced panel installation, not ordinary concrete or retained substrates.
- Preserve the historical 17→25 Aban schedule comparison separately from the published management 18→25 period. The archived native StatusDate is 2026-09-22; do not replace it with the output date without a decision.

Prepare a new dated run with source hashes, shared freeze ID and `changes[{uid,name,old,new}]`. First run `python skills/msp-update/scripts/preflight.py --source previous.mpp --snapshot before.native.json --plan plan.json`. This validates a plan against a supplied snapshot; obtain that snapshot freshly from the same native file before a real run. Copy sidecars explicitly.

The historical native apply helper is at `<handoff_root>/skills/msp-update/scripts/apply_quantity_plan.ps1`. It rejects negative quantities but does NOT reject decreases; the preflight is mandatory. The helper opens a copy and saves/reopens it. Preserve and restore application settings when adapting it; never close unrelated user documents. Empty plans require a separately verified dated-copy path because the helper rejects them. Confirm all source hashes again immediately before applying.

After native save/reopen, compare changed and unchanged leaves, summary rollups, all Number1–20 formulas, outline codes, status date, schedule/cost fields and sidecars. The historical helper does not independently prove every resource, assignment, calendar and additional baseline; obtain additional snapshots if those claims are required. Record exact checks and exceptions. A bundled evidence test is not a new native execution. Release only the supported scope and link output hash, audit and freeze ID.
