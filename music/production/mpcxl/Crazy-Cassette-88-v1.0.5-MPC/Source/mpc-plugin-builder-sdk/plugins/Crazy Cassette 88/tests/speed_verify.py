"""Check measured audio, correct fraction order, captions in native assets, and unobstructed touch bounds."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parents[1]
for index,target in [(1,250),(0,500),(2,750),(3,900)]:
 x=np.fromfile(P/f'build/speedcheck-{index}.f32',dtype=np.float32)[96000:]
 y=abs(np.fft.rfft(x*np.hanning(len(x))));freq=np.fft.rfftfreq(len(x),1/48000);peak=freq[y.argmax()]
 assert abs(peak-target)<1,(index,peak,target)
 assert float(np.sqrt(np.mean(x*x)))>.01
 print(f'PASS 1 kHz input, setting index {index}: measured {peak:.2f} Hz; expected {target} Hz')
t=json.loads((P/'skins/TUI.json').read_text());es=t['pageData']['tabs'][0]['componentDefinition']['componentsData']
def mapping(e):return dict((m['key'],m['value']) for m in e['handle remapping']['map']).get('Data')
def data(e):return e['componentData']['data']
bs=[e for e in es if e['componentData']['type']=='Button' and mapping(e)=='Parameter 13']
bs.sort(key=lambda e:float(e['bounds']['bounds'].split()[1]))
assert [data(e)['buttonId'] for e in bs]==[1,0,2,3]
assert [e['componentData']['name'] for e in bs]==['Setting 1/4','Setting 1/2','Setting 3/4','Setting 9/10']
targets=bs+[e for e in es if e['componentData']['name'] in ('View SPEED','Hold','Engage SPEED')]
for e in targets:
 for side in ['onImage','offImage']:
  f=P/'skins'/data(e)[side];assert f.is_file()
  if e in bs:
   a=np.array(Image.open(f).convert('RGB'));assert ((a[:,:,0]>210)&(a[:,:,1]>230)&(a[:,:,2]>230)).sum()>80
for e in es:
 if e['componentData']['type']!='Label':continue
 inv=e['bounds'].get('additionalInvalidatingHandles',[])
 if any('/8/Parameter 25' in x and '/0/8/' not in x for x in inv):continue
 x,y,w,h=map(float,e['bounds']['bounds'].split())
 for b in targets:
  xx,yy,ww,hh=map(float,b['bounds']['bounds'].split())
  assert not (x<xx+ww and xx<x+w and y<yy+hh and yy<y+h),f'Label blocks {b["componentData"]["name"]}'
print('PASS: quarter/half/three-quarter/nine-tenths top-to-bottom; caption pixels in all eight Speed images; no overlapping Labels on Speed, mode name, Hold or engage pad')
