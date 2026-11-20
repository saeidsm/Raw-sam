"""Read-only plan checks. Native freshness and save/reopen QA remain required."""
import argparse,hashlib,json,math
from pathlib import Path

def validate(source,snapshot,plan):
    if hashlib.sha256(Path(source).read_bytes()).hexdigest()!=plan.get('sourceSha256'):
        raise ValueError('Source hash mismatch')
    if snapshot.get('sourceSha256') is not None and snapshot['sourceSha256'].lower()!=plan['sourceSha256'].lower():
        raise ValueError('Snapshot source hash mismatch')
    rows=snapshot['tasks'];by_uid={x['uid']:x for x in rows}
    if len(by_uid)!=len(rows):raise ValueError('Duplicate snapshot UID')
    seen=set()
    for c in plan['changes']:
        uid=c['uid']
        if type(uid) is not int or uid in seen:raise ValueError('Invalid or duplicate UID')
        seen.add(uid);t=by_uid.get(uid)
        if t is None or t['summary']:raise ValueError('Unknown or summary UID')
        if t['name']!=c['name']:raise ValueError('Task name guard failed')
        for key in ['old','new']:
            if type(c[key]) not in (int,float) or not math.isfinite(c[key]) or c[key]<0:raise ValueError('Invalid quantity')
        if type(t.get('Number5')) not in (int,float) or not math.isfinite(t['Number5']):raise ValueError('Missing native prior quantity')
        if abs(t['Number5']-c['old'])>1e-6:raise ValueError('Old value mismatch')
        if c['new']<c['old']-1e-7:raise ValueError('Decrease rejected by confirmed policy')
    return {'status':'plan_checks_passed','changes':len(seen),'native_freshness_verified':False,'empty_plan_requires_dated_copy':not bool(seen)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--snapshot',required=True);p.add_argument('--plan',required=True);a=p.parse_args()
    load=lambda path:json.loads(Path(path).read_text(encoding='utf-8-sig'))
    print(json.dumps(validate(a.source,load(a.snapshot),load(a.plan))))
