"""Explain model-space LINE/CIRCLE/ARC extents per layer in bounded ASCII DXF."""
from __future__ import annotations
import argparse,json,math,re,sys
from collections import Counter
from pathlib import Path
MAX_BYTES=2*1024*1024
def num(s):
    if len(s)>64 or not re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]{1,3})?',s):raise ValueError('bounded decimal coordinate required')
    x=float(s)
    if not math.isfinite(x) or abs(x)>1e9:raise ValueError('coordinate/angle magnitude budget1e9')
    return x
def analyze(text):
    if len(text.encode('ascii'))>MAX_BYTES or '\0' in text:raise ValueError('ASCII DXF<=2MiB without NUL required')
    lines=text.splitlines()
    if len(lines)%2 or len(lines)>100000:raise ValueError('complete code/value pairs, at most50000')
    tags=[]
    for i in range(0,len(lines),2):
        if not re.fullmatch(r'\s*[0-9]{1,4}\s*',lines[i]) or not 0<=int(lines[i])<=1071 or len(lines[i+1])>1024:raise ValueError('invalid group code/value budget')
        code=int(lines[i]);value=lines[i+1].strip()
        if code!=999:tags.append((code,value))
    section=None;seen_entities=False;eof=False;kind=None;fields=[];entities=[];layers={};ignored=Counter();sections=Counter()
    def flush():
        nonlocal kind,fields
        if kind is None:return
        if len(entities)>=10000:raise ValueError('entity budget10000')
        if kind not in ('LINE','CIRCLE','ARC'):raise ValueError('unsupported entity '+kind+'; no block inserts, polylines or text')
        d={};geometry={8,10,20,30,11,21,31,39,40,50,51,67,210,220,230,410}
        for code,value in fields:
            if code in geometry:
                if code in d:raise ValueError('duplicate geometry/layer field')
                d[code]=value
            else:ignored[str(code)]+=1
        layer=d.get(8,'0')
        if not layer or len(layer)>128 or not layer.isprintable():raise ValueError('printable layer identity<=128 required')
        if d.get(67,'0')!='0' or d.get(410,'Model')!='Model':raise ValueError('model space only')
        if any(num(d.get(c,'0'))!=0 for c in (30,31,39,210,220)) or num(d.get(230,'1'))!=1:raise ValueError('zero Z/thickness and default extrusion only')
        def get(code):
            if code not in d:raise ValueError('missing entity coordinate '+str(code))
            return num(d[code])
        x,y=get(10),get(20);degenerate=False
        if kind=='LINE':
            if any(c in d for c in (40,50,51)):raise ValueError('unsupported LINE geometry fields')
            xx,yy=get(11),get(21);points=[(x,y),(xx,yy)];length=math.hypot(xx-x,yy-y);degenerate=length==0
        else:
            if any(c in d for c in (11,21,31)):raise ValueError('unsupported circular entity geometry fields')
            radius=get(40)
            if radius<=0:raise ValueError('positive radius required')
            if kind=='CIRCLE':
                if 50 in d or 51 in d:raise ValueError('CIRCLE has no arc angles')
                points=[(x-radius,y-radius),(x+radius,y+radius)];length=2*math.pi*radius
            else:
                start,end=get(50)%360,get(51)%360;sweep=(end-start)%360
                if sweep==0:raise ValueError('zero/whole-turn ARC ambiguous; use CIRCLE for full circle')
                angles=[start,end]+[a for a in (0,90,180,270) if (a-start)%360<=sweep]
                points=[(x+radius*math.cos(math.radians(a)),y+radius*math.sin(math.radians(a))) for a in angles];length=radius*math.radians(sweep)
        bounds=[min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points),max(p[1] for p in points)]
        entity={'entity':len(entities)+1,'kind':kind,'layer':layer,'bounds_xy':bounds,'length_approx':length,'zero_length':degenerate};entities.append(entity)
        if layer not in layers:
            if len(layers)>=256:raise ValueError('layer budget256')
            layers[layer]={'counts':Counter(),'entity_ids':[],'lengths':[],'bounds_xy':bounds.copy()}
        entry=layers[layer];entry['counts'][kind]+=1;entry['entity_ids'].append(entity['entity']);entry['lengths'].append(length)
        old=entry['bounds_xy'];entry['bounds_xy']=[min(old[0],bounds[0]),min(old[1],bounds[1]),max(old[2],bounds[2]),max(old[3],bounds[3])];kind=None;fields=[]
    i=0
    while i<len(tags):
        code,value=tags[i];i+=1
        if eof:raise ValueError('tags after EOF')
        if code==0 and value=='SECTION':
            if section is not None or i==len(tags) or tags[i][0]!=2:raise ValueError('malformed/nested SECTION')
            section=tags[i][1];i+=1;sections[section]+=1
            if section=='ENTITIES':
                if seen_entities:raise ValueError('one ENTITIES section required')
                seen_entities=True
        elif code==0 and value=='ENDSEC':
            if section is None:raise ValueError('unmatched ENDSEC')
            if section=='ENTITIES':flush()
            section=None
        elif code==0 and value=='EOF':
            if section is not None:raise ValueError('EOF inside section')
            eof=True
        elif section=='ENTITIES':
            if code==0:flush();kind=value
            elif kind is None:raise ValueError('entity fields before entity type')
            else:fields.append((code,value))
        elif section is None:raise ValueError('tags outside section')
    if not eof or section is not None or not seen_entities or not entities:raise ValueError('terminated nonempty ENTITIES section required')
    result=[]
    for name,v in sorted(layers.items()):result.append({'layer':name,'counts':dict(sorted(v['counts'].items())),'entity_ids':v['entity_ids'],'bounds_xy':v['bounds_xy'],'length_approx':math.fsum(v['lengths'])})
    return {'layers':result,'entities':entities,'zero_length_entities':[e['entity'] for e in entities if e['zero_length']],'sections':dict(sorted(sections.items())),'ignored_entity_tags':dict(sorted(ignored.items())),
      'scope':'Raw planar model-space geometry in drawing units; no unit conversion, block insertion, OCS transforms, display/layer visibility filtering, clipping, text extents or CAD repair. Invisible entities remain included. Bounds/lengths use floating-point analytic LINE/CIRCLE/CCW-ARC geometry, not certification of manufacturing dimensions.'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
    try:
        with Path(a.input).open('rb') as f:raw=f.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:raise ValueError('DXF exceeds2MiB')
        r=analyze(raw.decode('ascii'));print(json.dumps(r,indent=2,sort_keys=True));return int(bool(r['zero_length_entities']))
    except (ValueError,OSError,UnicodeError,OverflowError) as e:print(json.dumps({'error':str(e)}),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
