---
name: employer-excel
description: Update the Pardis employer workbook from shared construction evidence while preserving native Excel features and checking delivery, staffing and formula completeness.
---

Repository: https://github.com/saeidsm/Raw-sam

Read root `SKILL.md`, `integrations/employer-excel/manifest.json`, `docs/shared-freeze.md`, and the mapping README beneath the manifest's `handoff_root`. All paths here resolve from the repository root. The originally received workbook is an archived partial-data example with 179 inherited and 10 new formula errors. Later scoped revisions have repaired those errors; follow catalog modules.employer_excel.latest_output and latest_review_qa for the current workbook. Do not rerun historical fixes blindly, treat the archived sample as current, or equate formula cleanliness with complete project data.

Use the 9971-cell inventory for address, formulas, cached values and provenance, plus employer-summary UID mappings and historical edit plans. Do not replay a prior plan as new-period input. Sheet names include trailing spaces. Preserve 11 sheets, 11 charts, tables, logos/images, merges, formulas, number formats and print settings. Verify the actual latest template rather than hard-coding these counts forever.

Use the same reviewed freeze as the MSP and management outputs. Preserve distinct bases: schedule-normalized versus physical quantities; 17→25 versus 18→25 period comparisons; procurement, production, shipment, site receipt and installation; full-week executive averages versus observed-day totals including office staff. Existing user-confirmed 25/40 executive averages cannot be replaced by partial daily attendance averages or fabricated into daily rosters.

Intake delivery date/material/unit/quantity/building/contract/receipt ID and original/replacement status. Deduplicate receipts, not merely filenames. The historical period receipt is 9400 kg, cumulative 1074533 kg; these are dated evidence, not constants. For attendance averages/person-days, require daily attendance, category and observed-day coverage. A user-confirmed headcount may be entered numerically without a fabricated roster; label the metric as headcount and retain the non-permanent note. Five fixed plus four variable members is nine team members, not nine daily attendees. Do not infer transport/office split or missing-day attendance. Record missing input internally; client text follows the approved management rules and must not claim unsupported totals.

Native Excel COM editing of a copy, CalculateFullRebuild, save/reopen and PDF/visual verification is the tested preservation path. Discover any authoring library from the host runtime. Full artifact export and XML splicing failed historical preservation/opening checks; they are not verified release paths. Use openpyxl only for reading/validation here, not saving the template.

Before release, repair the dependent P/Q formulas for unknown inputs and review the 179 inherited errors. Guards must propagate unknown values as blank/explicit unavailable state, never numerical zero; unexpected formula faults must remain detectable. Do not blanket IFERROR(...,0). Preserve the original sample. Native recalculation must confirm cached values and chart behavior across the whole workbook, with no unexplained new formula errors. Missing material/attendance/supervision data requires completion or an explicit decision about report coverage, not a guessed value.

Record source cells, freeze ID, changes, formula findings and native/visual QA. Existing sample outputs were produced before the shared freeze integration; do not retroactively label them products of a new freeze. Deliver a dated revision only when its actual completeness and validation support release.

When reconciling deliveries and staffing, read `skills/employer-excel/references/receipts-and-headcount.md`. Follow `catalog.json` → `modules.employer_excel` for the latest intake, decisions and open questions. The current workbook remains a review copy until its remaining material questions are resolved.
