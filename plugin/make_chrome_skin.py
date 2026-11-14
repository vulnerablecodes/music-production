"""Integrate approved generated artwork with native MPC controls and reel telemetry.
Image resizing/cropping creates registered sprites; live labels remain native.
Run after build.py --target native, then build.py to assemble the final folder.
"""
from pathlib import Path
import runpy, math, json
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
n=runpy.run_path(str(P/'make_skin.py'))
D=n['D'];g=n['g'];get=n['get'];put=n['put'];entry=n['entry'];label=n['label']
original_put=put
def put(o,k,v):
 if isinstance(o,dict):o[k]=v
 else:original_put(o,k,v)
base=Image.open(P/'artwork/chrome-neutral.png').convert('RGB').resize((1280,628),Image.Resampling.LANCZOS)
engage_on=Image.open(P/'artwork/chrome-engage-on.png').convert('RGBA')
base.save(D/'deck.png')
# Existing buttons keep native bindings; sprites align with approved artwork.
for mode in range(8):
 x=790+(mode%2)*235;y=95+(mode//2)*128
 for on in [0,1]:
  im=base.crop((x,y,x+217,y+30)).convert('RGBA')
  if on:ImageDraw.Draw(im).rounded_rectangle((2,2,214,27),5,outline='#ffd887',width=2)
  im.save(D/f'name{mode}_{"on" if on else "off"}.png')
  im=base.crop((x,y+35,x+217,y+43)).convert('RGBA')
  if on:ImageDraw.Draw(im).rounded_rectangle((2,1,214,6),3,fill='#ffcb61')
  im.save(D/f'led{mode}_{"on" if on else "off"}.png')
# Each key is an independent native control; selected-view outline is separate.
base.crop((790,143,1007,210)).convert('RGBA').save(D/'pad_off.png')
engage_on.save(D/'pad_on.png')
for on in [0,1]:
 im=base.crop((550,553,705,611)).convert('RGBA')
 if on:ImageDraw.Draw(im).rounded_rectangle((2,2,152,55),5,outline='#ffca62',width=3)
 im.save(D/f'hold_{"on" if on else "off"}.png')
 im=base.crop((30,532,255,602)).convert('RGBA')
 if on:ImageDraw.Draw(im).rounded_rectangle((3,3,221,66),8,outline='#ffca62',width=3)
 im.save(D/f'bypass_{"on" if on else "off"}.png')
# Opaque hardware fader wells cover the fixed caps in the concept image.
fader=Image.new('RGBA',(307,78*127))
for frame in range(127):
 im=Image.new('RGBA',(307,78),'#1b2418');a=ImageDraw.Draw(im)
 a.rounded_rectangle((1,1,305,76),8,outline='#9b9e8c',width=2)
 for x in range(15,298,18):a.line((x,8,x,17),fill='#dac79a')
 a.rounded_rectangle((10,29,296,46),6,fill='#080c09',outline='#e0e2d2',width=2)
 x=int(15+frame*275/126)
 for dx in range(-12,13):
  v=int(100+150*(1-abs(dx)/13));a.line((x+dx,21,x+dx,57),fill=(v,v,min(255,v+5)))
 a.rectangle((x-12,21,x+12,57),outline='#f3eee0',width=1)
 for dx in [-7,-3,1,5]:a.line((x+dx,25,x+dx,53),fill='#5a6056')
 fader.paste(im,(0,frame*78))
fader.save(D/'deck_fader.png')
# Chrome rims enhance existing code-rendered selectors without changing values.
for f in list(D.glob('sub*_choice*.png'))+list(D.glob('small*_choice*.png')):
 im=Image.open(f).convert('RGBA');a=ImageDraw.Draw(im);w,h=im.size
 a.rounded_rectangle((1,1,w-2,h-2),6,outline='#eef0db',width=2)
 a.rounded_rectangle((4,4,w-5,h-5),4,outline='#707c6c',width=1)
 im.save(f)
# Two separately photographed reel sprites, 64 frames each, bound to Parameter 27.
for side,cx in enumerate([174,363]):
 disk=base.crop((cx-46,184,cx+46,276)).convert('RGBA')
 mask=Image.new('L',(92,92));ImageDraw.Draw(mask).ellipse((2,2,89,89),fill=255)
 disk.putalpha(mask)
 strip=Image.new('RGBA',(92,92*64))
 for frame in range(64):strip.alpha_composite(disk.rotate(-frame*360/64,resample=Image.Resampling.BICUBIC),(0,92*frame))
 strip.save(D/f'chrome_reel_{side}.png')
E=[];side=0
for e in n['E']:
 cd=get(e,'componentData');name=get(cd,'name');data=get(cd,'data');bounds=get(e,'bounds')
 if name=='Cassette':continue
 if name=='Notified motor reel':
  put(data,'image',f'chrome_reel_{side}.png');put(bounds,'bounds',f'{128+side*189} 184 92 92');side+=1
 if name=='Bypass':put(bounds,'bounds','30 532 225 70')
 if name=='Vertical fader':
  put(data,'version',3);put(data,'dragOrientation','Horizontal')
 E.append(e)
assert side==2
T=n['T'];tabs=get(get(T,'pageData'),'tabs')
put(tabs[0],'componentDefinition',g.component_definition([],E,'ff263122'))
(D/'TUI.json').write_text(g.dump_json(T)+'\n')
# Render real assembled sprites for all eight views, not hardware screenshots.
for mode in range(8):
 im=base.convert('RGBA')
 for x,v,txt in [(35,0,'0%'),(380,126,'100%')]:
  im.alpha_composite(fader.crop((0,v*78,307,(v+1)*78)),(x,464))
  n['text'](ImageDraw.Draw(im),(x+153,542),txt,16,'#e3d6ad')
 for x,y,w,h,asset,caption,value in n['positions'].get(mode,[]):
  default=2 if mode==6 else 3 if mode==7 else 0
  im.alpha_composite(Image.open(D/f'{asset}_{"on" if value==default else "off"}.png'),(x,y))
 if mode in [2,3]:
  n['text'](ImageDraw.Draw(im),(638,215),'×' if mode==2 else '⇄',60,'#e3d6ad')
  n['text'](ImageDraw.Draw(im),(638,275),'MUTE' if mode==2 else 'REVERSE',17,'#e3d6ad')
 for j in range(8):
  x=790+(j%2)*235;y=95+(j//2)*128
  im.alpha_composite(Image.open(D/f'name{j}_{"on" if j==mode else "off"}.png'),(x,y))
  im.alpha_composite(Image.open(D/f'led{j}_{"on" if j==mode else "off"}.png'),(x,y+35))
  im.alpha_composite(Image.open(D/f'pad_{"on" if j==mode else "off"}.png'),(x,y+48))
 im.alpha_composite(Image.open(D/'hold_on.png'),(550,553))
 im.convert('RGB').save(P/'Previews'/f'{mode+1}-{n["names"][mode].lower()}.png')
 if mode==0:im.convert('RGB').save(P/'UI-preview.png')
contact=Image.new('RGB',(1280,1360),'#10170f')
for mode in range(8):
 im=Image.open(P/'Previews'/f'{mode+1}-{n["names"][mode].lower()}.png');im.thumbnail((636,312))
 contact.paste(im,(mode%2*640+2,mode//2*340+25))
contact.save(P/'All-eight-modes.png')
print('Chrome artwork integrated with native controls and telemetry reels.')
