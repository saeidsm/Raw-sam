from pathlib import Path
import json,hashlib,importlib.util,copy,tempfile
R=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((R/p).read_text(encoding='utf-8-sig'))
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
B='integrations/shared/h-f1a2d02b';D='data/shared/1405-08-25/h1'
check=load(B+'/package-integrity.json')
for p,h in check['files'].items():assert digest(R/B/'package'/p)==h,p
records=load(D+'/observations.json')['records'];original=load(B+'/package/history/records.json');assert len(records)==len(original)==1688
ids={r['record_id'] for r in records};assert len(ids)==1688
sources={s['source_id']:s for s in load('sources.json')['sources']}
decisions={d['decision_id'] for d in load(D+'/decisions.json')}
for old,r in zip(original,records):
 assert old['value']==r['value'] and old['source_locator']==r['source_locator']
 assert r['source_id'] in sources and (not r['decision_id'] or r['decision_id'] in decisions)
 assert r['unit'] in ['kg','m2','m','fraction','person_day','person',None]
 assert r['contract_id'] in ['c-71af','c-a641','c-49bc',None]
 if old['project_id']=='p-7c21' and old['building_id']=='building-agriculture':
  assert r['project_id']=='p-a963' and r['contractor_id']=='k-31db' and r['contract_id'] is None
 if old['status']=='missing':assert r['value'] is None and r['status']=='unresolved'
 if old['status']=='derived_partial_coverage':assert r['coverage']=='observed_days_only'
 if r.get('supersedes'):assert r['supersedes'] in ids
mapping=load('integrations/msp-update/mappings.json');assert len(mapping)==len({x['uid'] for x in mapping})==418
assert len(load(B+'/package/mappings/employer-cells.json'))==9971
for m in ['msp-update','employer-excel']:
 manifest=load(f'integrations/{m}/manifest.json')
 for k in ['skill_path','input_requirements','mappings_path','validation_path','unresolved_questions','handoff_root']:assert (R/manifest[k]).exists()
 for k in ['history_paths','template_paths','sample_paths']:
  for path in manifest[k]:assert (R/path).exists()
candidate=load(D+'/freeze-candidate.json');assert candidate['release_ready'] is False and candidate['accepted_record_ids'] is None
for p,h in candidate['paths'].items():assert digest(R/p)==h,p
spec=importlib.util.spec_from_file_location('preflight',R/'skills/msp-update/scripts/preflight.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
source=R/B/'package/examples/msp/before-1405.08.17.mpp';snap=load(B+'/package/examples/evidence/current-baseline.native.json');plan=load(B+'/package/examples/evidence/latest-plan.json')
assert mod.validate(source,snap,plan)['changes']==18
mutations=[]
p=copy.deepcopy(plan);p['changes'][0]['new']=p['changes'][0]['old']-1;mutations.append(p)
p=copy.deepcopy(plan);p['changes'].append(copy.deepcopy(p['changes'][0]));mutations.append(p)
p=copy.deepcopy(plan);p['sourceSha256']='0'*64;mutations.append(p)
p=copy.deepcopy(plan);p['changes'][0]['old']+=1;mutations.append(p)
for p in mutations:
 try:mod.validate(source,snap,p)
 except ValueError:pass
 else:raise AssertionError('Unsafe plan accepted')
q=load(B+'/validation.json');assert len(q['all_workbook_formula_errors'])==189 and len(q['new_error_cells_vs_template'])==10
print('PASS: immutable handoff,1688 records,418 mappings,9971 cells,source/decision links,candidate hashes;18-change plan passes,4 unsafe plans rejected. Native apps not rerun; workbook remains partial.')
