"""Exercise the shipped patcher against a real supplied template, in temp copies."""
import argparse,copy,hashlib,json,tempfile,zipfile
from pathlib import Path
from patch_existing_cells import patch

def run(source,plan):
    before=hashlib.sha256(Path(source).read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory() as d:
        target=Path(d)/'candidate.xlsx';report=patch(source,plan,target)
        with zipfile.ZipFile(source) as a,zipfile.ZipFile(target) as b:
            assert a.namelist()==b.namelist()
            for n in a.namelist():
                if n not in report['changed_parts']:assert a.read(n)==b.read(n)
        rejected=[]
        for name,mutate in [('hash',lambda p:p.update(source_sha256='0'*64)),('duplicate',lambda p:p['changes'].append(p['changes'][0])),('old_value',lambda p:p['changes'][0].update(old='WRONG')),('formula_write',lambda p:p['changes'][0].update(sheet='ریز تحویل پنل این دوره',cell='M10')),('missing_cell',lambda p:p['changes'][0].update(cell='XFD1048576'))]:
            wrong=copy.deepcopy(plan);mutate(wrong);dest=Path(d)/(name+'.xlsx')
            try:patch(source,wrong,dest)
            except ValueError:assert not dest.exists();rejected.append(name)
            else:raise AssertionError('Invalid plan accepted: '+name)
        assert hashlib.sha256(Path(source).read_bytes()).hexdigest()==before
        return {'status':'passed','rejected_plans':rejected,'unchanged_parts_byte_identical':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--plan',required=True);a=p.parse_args();print(json.dumps(run(a.source,json.loads(Path(a.plan).read_text(encoding='utf-8-sig')))))
