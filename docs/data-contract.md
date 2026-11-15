# Shared data contract — version 1

UTF-8 JSON. Keys and machine numbers use ASCII for portability; render Persian digits only in human-facing reports. Dates use explicit calendar (`jalali`) and ISO-shaped `YYYY-MM-DD`, not an inferred Gregorian date. Unknown numeric values are null. Units use explicit `m2`, `m`, `kg`, `IRR`, `person`, `person_day`, `percent`, `percentage_point`.

## Paths
- `raw/<source-hash-prefix>/source.<ext>` — immutable authorized source file.
- `sources.json` — source_id, relative path, SHA256, format and actual source/report periods.
- `data/<project_id>/<period>/<revision>/snapshot.json` — published project facts.
- `data/shared/<period>/<revision>/finance.json` and `decisions.json` — cross-contract records.
- `data/history/<period>/<record-id>.json` — imported historical payloads, explicitly `legacy_snapshot`; never assume these are already normalized observations.
- `outputs/<project_id>/<period>/<revision>/<report-name>-<date>.<ext>`.
- `templates/<project_id>/<date>/<revision>/` — selected approved reference.
- `skills/<module>/SKILL.md`; `integrations/<module>/manifest.json` — supplied module and handoff.

Project IDs: p-7c21 library; p-a963 agriculture; p-49bc shared skylight contract. Contract IDs: c-71af library facade; c-a641 Adram facade; c-49bc skylight. Keep building_id separately for shared contracts. Never invent new identifiers for these existing entities.

## New normalized observation
Required: record_id, project_id, contractor_id, contract_id, building_id, system, phase, face, metric, value, unit, as_of, calendar, period_start, period_end, source_id, source_locator, status, decision_id. Use null for inapplicable/unknown fields; specify why in `missing_reason`. Optional: denominator, scope_version, previous_record_id, supersedes, derivation (formula and input record IDs). `status`: extracted, verified, user_confirmed, unresolved, superseded. An unresolved observation cannot become a confirmed output by renaming it.

## Source locator and decisions
Locator is sheet+cell/range for Excel, page/table for PDF, task_uid+field for MSP, event_id for site logs. Preserve original value and corrected value with decision ID; never rewrite history. A decision records question, answer, decision_date, effective_period, affected_ids and basis. Technical formula corrections may cite deterministic calculation rather than user approval.

## Finance
Per contract retain statement and adjustment identifiers, initial contract value, submitted/reviewed/approved amounts and dates, advance approvals, actual payments, deductions and their evidence. Each payment has payment_id, date, amount and allocation. Iron payments have allocation=`adjustment_advance`; use actual_paid only once as an offset at settlement. Keep aggregate approval and cash movement separate. No payment is inferred from the approval column. `net_payable` remains null until all applicable terms and actual payment/deduction evidence are available.

## Module handoff
Manifest fields: schema_version, module_id, version, status, skill_path, input_requirements, mappings_path, history_paths, template_paths, sample_paths, validation_path, dependencies, unresolved_questions, shared_contract_version. Allowed status: ready, partial, awaiting_handoff. Explicitly distinguish executable tools from instructions/reference assets. Every relative path must resolve. Add only the module namespace during parallel handoff; the coordinating agent merges catalog registration after checks.

## Publication
Never overwrite a published revision. Save new revision plus explicit supersession and update catalog.latest only after QA. Preserve remote changes and do not force-push. Read-only users can generate local outputs; the owner or an explicitly authorized account publishes. Markdown alone does not enforce GitHub permissions.
