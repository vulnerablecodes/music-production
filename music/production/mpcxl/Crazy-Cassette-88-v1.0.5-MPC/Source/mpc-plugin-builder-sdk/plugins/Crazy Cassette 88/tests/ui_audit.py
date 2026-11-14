"""Validate all eight selected panels and every sub-control binding against the manual map."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
t=json.loads((P/'skins/TUI.json').read_text());items=t['pageData']['tabs'][0]['componentDefinition']['componentsData']
def data(x):return x['componentData']['data']
def mapped(x):return {a['key']:a['value'] for a in x['handle remapping']['map']}.get('Data')
def kind(x):return x['componentData']['type']
views=[x for x in items if kind(x)=='Button' and mapped(x)=='Parameter 25']
assert sorted(data(x)['buttonId'] for x in views)==list(range(8))
assert all(data(x)['numButtonsInGroup']==8 for x in views)
for m in range(8):
 sel=f'IndexedEnabling/{m}/8/Parameter 25'
 if m in (2,3):assert any(x['componentData']['name']==('MUTE' if m==2 else 'REVERSE') and sel in x['bounds'].get('additionalInvalidatingHandles',[]) for x in items)
 for hold in (0,1):
  h=f'Parameter {m+5}' if hold else f'ResetOnGestureEnd/Parameter {m+5}'
  buttons=[x for x in items if kind(x)=='Button' and mapped(x)==h]
  assert len(buttons)==1
  assert f'IndexedEnabling/{hold}/2/Parameter 4' in buttons[0]['bounds']['additionalInvalidatingHandles']
 leds=[x for x in items if kind(x)=='Indicator' and mapped(x)==f'Parameter {m+5}'];assert len(leds)==1
spec={0:(13,[1,0,2,3]),1:(14,[1,0,2]),4:(15,list(range(7))),5:(16,list(range(8))),6:(17,list(range(4))),7:(18,[0,1,8,2,6,3,4,5])}
for m,(param,choices) in spec.items():
 sel=f'IndexedEnabling/{m}/8/Parameter 25'
 b=[x for x in items if kind(x)=='Button' and mapped(x)==f'Parameter {param}' and sel in x['bounds'].get('additionalInvalidatingHandles',[])]
 assert [data(x)['buttonId'] for x in b]==choices,(m,choices)
 print(f'PASS mode {m+1}: {len(b)} buttons map to DSP parameter {param}')
cs=[x for x in items if x['componentData']['name']=='Cassette'];assert len(cs)==1 and data(cs[0])['numFrames']==8 and mapped(cs[0])=='Parameter 25'
for n in ['Bypass','Hold']:assert len([x for x in items if x['componentData']['name']==n])==1
for param in (1,2):assert any(kind(x)=='Knob' and mapped(x)==f'Parameter {param}' for x in items)
params=json.loads((P/'build/params.json').read_text())['params'];assert len(params)==28 and all(p['automatable'] for p in params[:27]) and not params[27]['automatable']
for x in items:
 a=list(map(float,x['bounds']['bounds'].split()));assert a[0]>=0 and a[1]>=0 and a[0]+a[2]<=1280 and a[1]+a[3]<=628
print('PASS: eight view selectors and cassette frames; independent LEDs; 16 latch/momentary bindings; globals; all controls within screen; 27 automatable controls and non-automatable reel telemetry')

reels=[x for x in items if x['componentData']['name']=='Notified motor reel']
assert len(reels)==2
assert all(mapped(x)=='Parameter 27' and data(x)['numFrames']==64 and data(x)['animated'] is False for x in reels)
readouts=[x for x in items if kind(x)=='Label' and mapped(x)=='Parameter 27'];assert len(readouts)==1
print('PASS: two notified-phase reel bindings, no native auto-animation dependence, bound live counter')
