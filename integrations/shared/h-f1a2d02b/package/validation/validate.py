from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET,re
import openpyxl
P=Path(__file__).resolve().parents[1]
def load(p):return json.loads((P/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources=load('history/sources.json')
for s in sources:assert sha(P/s['path'])==s['sha256'],s['source_id']
a=load('examples/evidence/current-baseline.native.json');b=load('examples/evidence/latest.native.json')
old={t['uid']:t for t in a['tasks']};new={t['uid']:t for t in b['tasks']}
assert old.keys()==new.keys() and len(old)==1104
assert a['fields']==b['fields'] and b['structurePreserved'] and b['reopened']
plan=load('examples/evidence/latest-plan.json');changes={r['uid']:r['new'] for r in plan['changes']}
assert len(changes)==18
for uid,t in old.items():
 n=new[uid];assert n['Number5']>=t['Number5']-1e-7
 for k,v in t.items():
  if k in ['Number3','Number4','Number5','Number7']:continue
  assert abs(v-n[k])<1e-7 if type(v) in (int,float) else v==n[k],(uid,k)
 if not n['summary']:assert abs(n['Number5']-changes.get(uid,t['Number5']))<1e-7
assert sha(P/'examples/msp/after-1405.08.25.mpp')==load('examples/evidence/release-verification.json')['sha256']
mapping=load('mappings/msp-418.json');assert len(mapping)==418 and len({m['uid'] for m in mapping})==418
wb=openpyxl.load_workbook(P/'examples/employer/after-1405.08.25.xlsx',data_only=True)
assert len(wb.sheetnames)==11
assert abs(wb['Sheet2']['P2'].value-b['summaryAfter']/100)<1e-10
assert wb['1405-08-25']['D48'].value==9400
assert wb['جدول ورود زیرسازی']['G210'].value==1074533
assert '۵ نفر' in wb['نیروی انسانی']['B14'].value
assert wb['نیروی انسانی']['D8'].value=='داده ناقص'
assert wb['نیروی انسانی']['D6'].value==193 and wb['نیروی انسانی']['E6'].value==64
assert wb['نیروی انسانی']['D7'].value==270 and wb['نیروی انسانی']['E7'].value==32
errors=[(s.title,c.coordinate,c.value) for s in wb for row in s for c in row if c.data_type=='e']
template=openpyxl.load_workbook(P/'templates/employer-1405.07.28.xlsx',data_only=True)
prior_errors={(s.title,c.coordinate,c.value) for s in template for row in s for c in row if c.data_type=='e'}
new_errors=[e for e in errors if e not in prior_errors]
with zipfile.ZipFile(P/'examples/employer/after-1405.08.25.xlsx') as z:
 charts=[n for n in z.namelist() if re.match(r'xl/charts/chart\d+\.xml$',n)];assert len(charts)==11
 for n in charts:assert '#REF!' not in z.read(n).decode('utf-8'),n
records=load('history/records.json');ids={r['record_id'] for r in records}
assert len(ids)==len(records)
req='record_id project_id contract_id building_id system phase face metric value unit denominator as_of calendar source_id source_locator status decision_id'.split()
srcids={s['source_id'] for s in sources}
for r in records:
 assert all(k in r for k in req),r['record_id']
 assert r['source_id'] in srcids
 if r.get('supersedes'):assert r['supersedes'] in ids
 if r['status']=='missing':assert r['value'] is None
for p in P.rglob('*'):
 if p.suffix in ['.json','.md','.py','.ps1']:
  text=p.read_text(encoding='utf-8-sig');assert not re.search(r'[A-Za-z]:[\\/](?:Users|Program Files)',text),p
result={'status':'passed_scoped_checks_with_workbook_findings','checks':['source hashes','1104 task snapshot comparisons','18 actual increases','418 unique mappings','native formula equality','11 sheets and charts','MSP/employer progress agreement','9400kg period delivery','staff revision persisted','required record keys and supersedes','no personal absolute paths in text'],'records':len(records),'source_files':len(sources),'all_workbook_formula_errors':errors,'template_error_count':len(prior_errors),'new_error_cells_vs_template':new_errors,'native_rerun':False,'native_evidence':'historically saved/reopened; this test revalidates bundled evidence','employer_completeness':'partial; see open questions','resource_assignment_full_fidelity':'not independently proved'}
(P/'validation/results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(result['status'], 'records',len(records),'errors',len(errors),'new_errors',len(new_errors))
