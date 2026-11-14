"""Inspect shipped frame pixels and native-clock gate combinations; not an MPC UI emulation."""
from pathlib import Path
from PIL import Image
import numpy as np,json
P=Path(__file__).resolve().parents[1]
t=json.loads((P/'skins/TUI.json').read_text());items=t['pageData']['tabs'][0]['componentDefinition']['componentsData'];items=[x for x in items if x['componentData']['name'].startswith('Native reel ')]
turns={1:5,0:10,2:15,3:18}
for idx,n in turns.items():
 for rev in [0,1]:
  im=np.array(Image.open(P/f'skins/reel_native_{idx}_{rev}.png').convert('RGBA'))
  assert im.shape==(56*400,56,4)
  phases=[]
  for frame in range(400):
   a=im[frame*56:(frame+1)*56];y,x=np.nonzero((a[:,:,0]==242)&(a[:,:,1]==233)&(a[:,:,2]==195));assert len(x)>0
   phases.append(np.arctan2(y.mean()-28,x.mean()-28))
  angle=np.unwrap(phases);actual=(angle[-1]-angle[0])/(2*np.pi);expected=n*399/400*(-1 if rev else 1)
  assert abs(actual-expected)<.025,(idx,rev,actual,expected)
  print(f'PASS speed index {idx}, reverse {rev}: frame pixels rotate {actual:.3f} turns over 399 ticks (target {expected:.3f})')
# Evaluate conditions independently from DSP/transport. Each active speed selects exactly two native strips.
def visible(item,values):
 for h in item['bounds']['additionalInvalidatingHandles']:
  a=h.split('/');want=int(a[1]);param=int(a[-1].split()[1])
  if values[param]!=want:return False
 return True
for idx in turns:
 for rev in [0,1]:
  v={5:1,3:0,11:0,8:rev,13:idx};assert sum(visible(x,v) for x in items)==2
  for off in [5,3,11]:
   vv=v.copy();vv[off]=0 if off==5 else 1;assert not any(visible(x,vv) for x in items)
assert all(x['componentData']['data']['animated'] and x['componentData']['data']['numFrames']==400 for x in items)
print('PASS: exact 5:10:15:18 closed-cycle speeds; native timer enabled; one pair per selection; no transport/audio telemetry gating; bypass/Brake/Speed-off hide motion')
