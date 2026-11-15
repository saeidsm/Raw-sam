from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parents[1]
c=json.loads((R/'catalog.json').read_text(encoding='utf8'))
checks=json.loads((R/'checksums.json').read_text(encoding='utf8'))
for p,h in checks.items():
 q=R/p
 assert q.is_file(),p
 assert hashlib.sha256(q.read_bytes()).hexdigest()==h,p
for p in R.rglob('*.json'):
 if '.git' in p.parts:continue
 json.loads(p.read_text(encoding='utf8'))
for p in list(c['latest'].values())+list(c['templates'].values())+[c['finance'],c['decisions'],c['sources'],c['entrypoint'],c['user_guide'],c['handoff_prompt']]+[x['path'] for x in c['history']+c['outputs']]:assert (R/p).is_file(),p
for s in json.loads((R/'sources.json').read_text(encoding='utf8'))['sources']:
 assert hashlib.sha256((R/s['path']).read_bytes()).hexdigest()==s['sha256']
print('PASS:',len(checks),'files; JSON, pointers, source and artifact checksums verified')
