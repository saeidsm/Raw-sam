# One dataset, separate measurement bases

Start with root catalog and every registered integration receipt. Read the current period's existing report decisions, imported decisions, unresolved questions and source crosswalk. The received handoff is preserved under `integrations/shared/h-f1a2d02b/package/`; its statements about repository state and integration readiness describe the sending chat's historical view. The root catalog is the current registry.

## Freeze contract

A production freeze contains `freeze_id`, period and calendar, source/document/map/decision SHA256 references, explicit `accepted_record_ids`, excluded IDs with reasons, unresolved questions and per-output coverage. It is immutable. Each output records the same freeze ID plus its own measurement basis, period, source record IDs, calculations and QA. A changed answer creates a successor freeze; it does not rewrite a prior release.

`data/shared/1405-08-25/h1/freeze-candidate.json` is a candidate index with null acceptance and no outputs. It is not a production freeze. The historical PPTX, MPP and workbook samples were generated separately and must not be relabeled as having consumed it. Review candidate facts, resolve consequential conflicts and populate accepted/excluded records before new shared production. `source_conflict`, missing and superseded facts cannot become accepted facts merely by normalizing a status label. Native verification establishes the stored schedule value, not physical completion in the field.

## Identity and provenance

Contract IDs are `c-71af`, `c-a641`, `c-49bc`; project/scope IDs retain their root registry meaning. Canonical building IDs are `p-7c21` and `p-a963`. The imported `building-library/agriculture` values are mapped accordingly. Agriculture clamp from the library workbook is located in agriculture, belongs to Aran, and retains null contract allocation. Source IDs deduplicate by content SHA256. Original source aliases, observations and decisions remain in the preserved handoff. Imported record/decision IDs are namespaced to avoid collisions.

The 1688 normalized imported records retain origin status and value. `fraction` means 0–1; its quantity denominator is not a percent base. A source phase combining production and shipment remains `production_and_shipment`; do not split it into fabricated component observations.

## Measures that must remain distinct

- Physical installed quantity is not MSP Number5 when Number9 differs from the spreadsheet total. Store the conversion and both denominators. Do not use schedule-normalized volumes to forecast physical installation weeks.
- The MSP comparison 17→25 Aban does not replace the accepted management report dated18Aban. Define each metric's interval explicitly before comparing growth.
- The management workforce values25/40 are user-confirmed executive means. Imported staffing includes193/64 person-days over6observed days and270/32 over5days for executive/office categories. Their totals42.8333/60.4 are observed-day combined means, not the same measure. Missing days and categories remain unknown.
- Scope removal for active-progress analysis does not modify native baseline weights or erase tasks. The user confirmed all-four-faces transfer, including substrate and panel execution. Read catalog decision_updates/current_scope_policy; regenerate active-scope and crew calculations before the next release.
- Receipt, shipment and installation remain separate. Names of archives or documents do not prove actual daily coverage.

## Completion gates

Receive inputs once, ask grouped consequential questions, record answers with provenance, freeze accepted facts, and route to requested output modules. Do not block unrelated report areas for an unresolved leaf; record per-output coverage. Release gate includes arithmetic/source reconciliation, full formula scan for Excel, native reopen checks for MPP/Excel, rendered layout and editability for PPTX, and immutable output hashes. Never represent environment prerequisites as installed merely because a skill exists.

The bundled validator is a historical evidence test. Run it on a disposable copy because it writes `validation/results.json`. Keep originals and their hashes unchanged. Integration receipt verification does not execute Office or prove a new native update.
