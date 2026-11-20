"""Portable, narrow XLSX patch. Preserve untouched ZIP members and XML bytes.

Only existing, non-formula scalar cells; no rows/sheets/formulas/styles added.
Output is a candidate requiring native Excel recalculation and review.
Plan: {source_sha256, changes:[{sheet,cell,old,new}]}.
"""
import argparse, hashlib, json, math, posixpath, re, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

NS = {'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'

def patch(source, plan, output):
    source, output = Path(source), Path(output)
    if output.exists() or source.resolve() == output.resolve(): raise ValueError('Output must be new')
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if plan.get('source_sha256') != source_hash: raise ValueError('Source hash mismatch')
    with zipfile.ZipFile(source) as zin:
        if len(zin.namelist()) != len(set(zin.namelist())): raise ValueError('Duplicate ZIP parts')
        payload = {n:zin.read(n) for n in zin.namelist()}
        original = dict(payload)
        wb = ET.fromstring(payload['xl/workbook.xml'])
        rels = {r.attrib['Id']:posixpath.normpath(posixpath.join('xl',r.attrib['Target'])).lstrip('/') for r in ET.fromstring(payload['xl/_rels/workbook.xml.rels'])}
        # Absolute package targets start at package root.
        for r in ET.fromstring(payload['xl/_rels/workbook.xml.rels']):
            if r.attrib['Target'].startswith('/'): rels[r.attrib['Id']]=r.attrib['Target'].lstrip('/')
        sheets = {s.attrib['name']:rels[s.attrib[R]] for s in wb.find('s:sheets',NS)}
        strings=[]
        if 'xl/sharedStrings.xml' in payload:
            strings=[''.join(t.text or '' for t in si.iter('{'+NS['s']+'}t')) for si in ET.fromstring(payload['xl/sharedStrings.xml'])]
        seen=set()
        for c in plan['changes']:
            key=(c['sheet'],c['cell'])
            if key in seen: raise ValueError('Duplicate cell')
            seen.add(key)
            if not re.fullmatch(r'[A-Z]+[1-9][0-9]*',c['cell']): raise ValueError('Invalid cell')
            part=sheets[c['sheet']]; raw=payload[part].decode('utf-8')
            cells=ET.fromstring(payload[part]).findall('.//s:sheetData/s:row/s:c',NS)
            matches=[x for x in cells if x.attrib.get('r')==c['cell']]
            if len(matches)!=1: raise ValueError('Only existing cells supported')
            x=matches[0]
            if x.find('s:f',NS) is not None: raise ValueError('Formula cells are protected')
            if any(child.tag not in ('{'+NS['s']+'}v','{'+NS['s']+'}is') for child in x): raise ValueError('Unsupported cell metadata')
            kind=x.attrib.get('t','n'); v=x.find('s:v',NS)
            if kind=='s': old=strings[int(v.text)]
            elif kind=='inlineStr': old=''.join(t.text or '' for t in x.findall('.//s:t',NS))
            elif kind=='n': old=float(v.text) if v is not None and v.text is not None else None
            else: raise ValueError('Unsupported existing cell type')
            if old != c['old']: raise ValueError(f'Old value mismatch: {key}')
            new=c['new']
            if isinstance(new,bool) or not isinstance(new,(str,int,float)): raise ValueError('Use number or text')
            if isinstance(new,(int,float)) and not math.isfinite(new): raise ValueError('Nonfinite number')
            rx=re.compile(r'<c\b(?=[^>]*\br="'+c['cell']+r'")(?:[^>]*/>|[^>]*>.*?</c>)',re.S)
            m=list(rx.finditer(raw))
            if len(m)!=1: raise ValueError('Unsupported XML cell encoding')
            opening=m[0].group().split('>',1)[0].rstrip('/')
            opening=re.sub(r'\s+t="[^"]*"','',opening)
            if isinstance(new,str): replacement=opening+' t="inlineStr"><is><t xml:space="preserve">'+escape(new)+'</t></is></c>'
            else: replacement=opening+'><v>'+str(new)+'</v></c>'
            raw=raw[:m[0].start()]+replacement+raw[m[0].end():]
            ET.fromstring(raw)
            payload[part]=raw.encode('utf-8')
        # Preserve cached values as historical caches; force native rebuild on open.
        # Consumers must not treat caches as updated results before native validation.
        raw=payload['xl/workbook.xml'].decode('utf-8')
        m=re.search(r'<calcPr\b[^>]*/>',raw)
        if not m: raise ValueError('Missing scalar calcPr; unsupported workbook')
        tag=m.group()
        for k,v in [('fullCalcOnLoad','1'),('forceFullCalc','1')]:
            tag=re.sub(r'\s+'+k+r'="[^"]*"','',tag)
            tag=tag[:-2]+f' {k}="{v}"/>'
        raw=raw[:m.start()]+tag+raw[m.end():];ET.fromstring(raw)
        payload['xl/workbook.xml']=raw.encode('utf-8')
        output.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(output,'w') as zout:
            for item in zin.infolist(): zout.writestr(item,payload[item.filename])
    return {'source_sha256':source_hash,'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'changed_parts':[p for p in payload if payload[p]!=original[p]],'changes':plan['changes'],
            'native_recalculation_required':True,'status':'candidate_not_native_verified'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--plan',required=True);p.add_argument('--output',required=True);p.add_argument('--audit',required=True);a=p.parse_args()
    report=patch(a.source,json.loads(Path(a.plan).read_text(encoding='utf-8-sig')),a.output)
    Path(a.audit).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
