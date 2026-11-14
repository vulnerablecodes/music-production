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

# v1.0.11: rebalance ONLY the approved chrome/canvas artwork and live controls.
from PIL import ImageOps
T=n['T']
art=base.copy();canvas=ImageOps.fit(Image.open(P/'artwork/multicam-black-v116.png').convert('RGB'),(1280,628),Image.Resampling.LANCZOS)
base.paste(canvas.crop((20,16,1260,610)),(20,16))
base.paste(art.crop((1260,16,1280,628)),(1260,16))
base.paste(art.crop((0,610,1280,628)),(0,610))
# Original chrome recorder and brass settings enclosure, retained at new sizes.
base.paste(art.crop((22,82,510,406)).resize((340,226),Image.Resampling.LANCZOS),(24,26))
base.paste(art.crop((521,82,755,406)).resize((246,512),Image.Resampling.LANCZOS),(378,26))
a=ImageDraw.Draw(base)
def txt(x,y,s,size=18,col='#eee3bf'):
 a.text((x,y),s,font=n['font'](size,True),fill=col,anchor='mm')
# Effect names occupy the freed header space.
for y,s in [(266,'TAPE NOISE'),(318,'VINYL CRACKLE'),(370,'RADIO STATIC'),(422,'WHITE NOISE'),(474,'MIX')]:txt(165,y,s,14)
txt(500,513,'TAP A NAME TO EDIT',11);txt(500,529,'UP = ON / DOWN = OFF',10)
a.rounded_rectangle((80,220,310,243),4,fill='#182416',outline='#515a35')
(D/'deck.png').write_bytes(b'')
base.save(D/'deck.png')
# New nameplates and switches are derived from the approved chrome/ivory assets.
full=['SPEED','SATURATION','MUTE','REVERSE','WARBLE','LO-FI','BRAKE','STUTTER']
plate=art.crop((790,95,1007,125)).resize((292,32),Image.Resampling.LANCZOS).convert('RGBA')
pad=art.crop((790,143,1007,210)).resize((292,58),Image.Resampling.LANCZOS).convert('RGBA')
for mode,name in enumerate(full):
 for on in [0,1]:
  im=plate.copy();d=ImageDraw.Draw(im)
  d.rounded_rectangle((18,3,273,28),5,fill='#f5f4ef',outline='#ffbd43' if on else '#c7c7b9',width=2)
  n['text'](d,(146,16),f'{mode+1:02d} / {name}',18,'#202821',True)
  if on:
   d.rounded_rectangle((2,2,289,29),6,outline='#fff3c4',width=2)
   d.rounded_rectangle((5,3,286,28),5,outline='#ffad24',width=2)
  im.save(D/f'circuit_name{mode}_{"on" if on else "off"}.png')
# Approved photorealistic lever artwork, used as a reproducible sprite atlas.
atlas=Image.open(P/'artwork/approved-toggle-preview.png').convert('RGBA')
def metal_switch(w,h,on,caption):
 crop=(910,98,1316,244) if on else (1340,98,1746,244)
 raw=atlas.crop(crop)
 mask=Image.new('L',(406*4,146*4));md=ImageDraw.Draw(mask)
 md.rounded_rectangle((0,22*4,405*4,128*4),radius=12*4,fill=255)
 if on:md.polygon([(96*4,0),(112*4,0),(120*4,8*4),(115*4,25*4),(88*4,31*4),(91*4,13*4)],fill=255)
 else:md.ellipse((76*4,112*4,112*4,145*4),fill=255)
 raw.putalpha(mask.resize((406,146),Image.Resampling.LANCZOS))
 im=raw.resize((w,h),Image.Resampling.LANCZOS)
 # Native captions keep globals readable; lever geometry is unchanged.
 if caption not in ['ON','OFF']:
  dr=ImageDraw.Draw(im);dr.rounded_rectangle((int(w*.36),int(h*.34),int(w*.77),int(h*.70)),3,fill='#122017')
  n['text'](dr,(w*.565,h*.52),caption,16 if w>210 else 15,'#ffdb96' if on else '#d9ddcd',True)
 # 28px amber jewel: obvious ON glow and an unlit dark OFF lens.
 size=28;lamp=Image.new('RGBA',(size,size));ld=ImageDraw.Draw(lamp)
 if on:
  for r in range(13,7,-1):ld.ellipse((14-r,14-r,14+r,14+r),fill=(255,170,25,int(20+(13-r)*8)))
 ld.ellipse((4,4,24,24),fill='#131b16',outline='#d6d7bd',width=2)
 ld.ellipse((7,7,21,21),fill='#ffd25e' if on else '#243028',outline='#a78539' if on else '#465143')
 if on:ld.ellipse((9,8,18,16),fill='#fff4b3');ld.ellipse((11,9,15,12),fill='#ffffff')
 im.alpha_composite(lamp,(int(w*.91)-14,int(h*.52)-14))
 return im
for on in [0,1]:metal_switch(292,102,on,'ON' if on else 'OFF').save(D/f'circuit_power_{"on" if on else "off"}.png')
for on in [0,1]:
 im=Image.new('RGBA',(28,28));dr=ImageDraw.Draw(im)
 if on:
  for r in range(13,7,-1):dr.ellipse((14-r,14-r,14+r,14+r),fill=(255,175,30,25+(13-r)*7))
 dr.ellipse((4,4,24,24),fill='#121b13',outline='#d6d7bd',width=2)
 dr.ellipse((7,7,21,21),fill='#ffd25e' if on else '#243028',outline='#a78539' if on else '#465143')
 if on:dr.ellipse((9,8,18,16),fill='#fff4b3');dr.ellipse((11,9,15,12),fill='#ffffff')
 im.save(D/f'circuit_led_{on}.png')
for on in [0,1]:
 im=art.crop((545,532,740,612)).resize((200,48),Image.Resampling.LANCZOS).convert('RGBA')
 if on:ImageDraw.Draw(im).rounded_rectangle((2,2,197,45),5,outline='#ffca62',width=2)
 im.save(D/f'hold_{"on" if on else "off"}.png')
def setting_face(w,h,caption,on):
 im=pad.resize((w,h),Image.Resampling.LANCZOS);dr=ImageDraw.Draw(im)
 if on:
  # Glow is contained inside native bounds, avoiding sprite clipping.
  dr.rounded_rectangle((1,1,w-2,h-2),7,fill='#a86c0d',outline='#fff7d5',width=2)
  dr.rounded_rectangle((4,4,w-5,h-5),6,fill='#ffb62d',outline='#ffe89a',width=2)
  for yy in range(9,h-9):
   t=(yy-9)/max(1,h-19);c=(255,int(220-44*t),int(113-65*t));dr.line((9,yy,w-10,yy),fill=c)
  dr.rounded_rectangle((8,8,w-9,h-9),4,outline='#fff3c9',width=1)
 else:
  dr.rounded_rectangle((6,7,w-7,h-8),5,fill='#26342e',outline='#839083',width=1)
 n['text'](dr,(w/2,h/2),caption,14 if len(caption)>6 else 17,'#201b0c' if on else '#e2e7d8',True)
 return im
# All settings use the same ivory/chrome control language as circuit switches.
options={0:(13,['1/2','1/4','3/4','9/10']),1:(14,['Boost','Amp','Drive']),3:(21,['1/8','1/4','1/2','1 bar']),4:(15,['Gentle','Wow','Flutter','Worn','Seasick','Unstable','Jungle']),5:(16,['Dust','Cassette','Narrow','8-bit','6-bit','4-bit','Broken','Telephone']),6:(17,['1/8 beat','1/2 beat','1 beat','2 beats']),7:(18,['1/2','1/4','1/8','1/16','1/32','1/64','1/8T','1/16T','1/4T'])}
E=[entry('Panel','Image',{'version':2,'imageType':'Regular','colour':'0','image':'deck.png'},'0 0 1280 628',focus='No')]
positions={}
for mode,name in enumerate(full):
 inv=[f'IndexedEnabling/{mode}/8/Parameter 25']
 E.append(label(name,'392 77 218 32',19,'ffffd58a',invalid=inv))
 if mode==2:E.append(label('MUTE HAS NO','394 160 214 30',16,'ffeee3bf',invalid=inv));E.append(label('EXTRA SETTINGS','394 195 214 30',16,'ffeee3bf',invalid=inv))
 if mode in options:
  idx,opts=options[mode]
  for j,caption in enumerate(opts):
   x=394+j%2*112;y=122+j//2*72;asset=f'polished_option_{mode}_{j}'
   for on in [0,1]:
    setting_face(102,50,caption,on).save(D/f'{asset}_{"on" if on else "off"}.png')
   E.append(entry(name+' setting '+caption,'Button',g.button_data(asset+'_on.png',asset+'_off.png',j,len(opts)),f'{x} {y} 102 50',f'Parameter {idx}',inv));positions.setdefault(mode,[]).append((x,y,asset,j))
for mode,name in enumerate(full):
 x=650+mode%2*306;y=22+mode//2*144
 E.append(entry('Select '+name,'Button',g.button_data(f'circuit_name{mode}_on.png',f'circuit_name{mode}_off.png',mode,8),f'{x} {y} 292 32','Parameter 25'))
 E.append(entry('Active '+name,'Indicator',{'version':1,'onImage':'circuit_led_1.png','offImage':'circuit_led_0.png','indicatorId':1,'numIndicatorsInGroup':1,'handleName':'Data'},f'{x+252} {y+73} 28 28',f'Parameter {5+mode}',focus='No'))
 for hold in [0,1]:
  data=g.button_data('circuit_power_on.png','circuit_power_off.png',1,1)
  if not hold:put(data,'gestureBehaviour','Hold')
  E.append(entry('Enable '+name,'Button',data,f'{x} {y+34} 292 102',f'Parameter {5+mode}' if hold else f'ResetOnGestureEnd/Parameter {5+mode}',[f'IndexedEnabling/{hold}/2/Parameter 4']))
# Generate exact native frame sizes: MPC crops sprites; it does not rescale them.
source_fader=fader
fader=Image.new('RGBA',(320,34*127))
for frame in range(127):fader.paste(source_fader.crop((0,frame*78,307,(frame+1)*78)).resize((320,34),Image.Resampling.LANCZOS),(0,frame*34))
fader.save(D/'deck_fader.png')
for on in [0,1]:
 metal_switch(225,79,on,'BYPASS').save(D/f'bypass_{"on" if on else "off"}.png')
 metal_switch(200,70,on,'HOLD').save(D/f'hold_{"on" if on else "off"}.png')
# Compact Noise/Mix; original chrome fader sprites, original bindings.
for y,idx in [(278,1),(330,28),(382,29),(434,30),(486,2)]:
 E.append(entry('Master horizontal fader','Knob',{'version':3,'knobType':'FilmStrip','filmStrip':'deck_fader.png','numFrames':127,'invert':False,'dragOrientation':'Horizontal','handleName':'Data'},f'34 {y} 320 34',f'Parameter {idx}'))
 E.append(label('',f'286 {y-20} 65 18',14,'ffeee3bf',param=f'WithSuffix[%]/Parameter {idx}'))
for name,idx,asset,bounds in [('Bypass',3,'bypass','30 527 225 79'),('Hold',4,'hold','398 536 200 70')]:E.append(entry(name,'Button',g.button_data(asset+'_on.png',asset+'_off.png',1,1),bounds,f'Parameter {idx}'))
# Exact-size host-notified reel strips; worker supplies continuous phase without audio processing.
for side in range(2):
 disk=art.crop((128+side*189,184,220+side*189,276)).convert('RGBA');mask=Image.new('L',(92,92));ImageDraw.Draw(mask).ellipse((2,2,89,89),fill=255);disk.putalpha(mask);disk=disk.resize((64,64),Image.Resampling.LANCZOS)
 strip=Image.new('RGBA',(64,64*64))
 for frame in range(64):strip.alpha_composite(disk.rotate(-frame*360/64,resample=Image.Resampling.BICUBIC),(0,frame*64))
 asset=f'polished_reel_{side}_0.png';strip.save(D/asset)
 inner=entry('Native motor value','Knob',{'version':3,'knobType':'FilmStrip','filmStrip':asset,'numFrames':64,'invert':False,'dragOrientation':'Vertical','handleName':'Data'},'0 0 64 64',focus='No')
 definition=g.component_definition([], [inner], '00000000', ignore_mouse=True)
 defs=get(get(get(T,'pageData'),'componentDefinitions'),'localComponentDefinitions')
 defs.append(g.Obj([('key',f'MotorDisplay{side}'),('value',definition)]))
 E.append(entry('Reel motor display',f'MotorDisplay{side}',{'version':1,'handleName':'Data'},f'{98+side*132} 97 64 64','Parameter 27',focus='No'))
# A visible Value label subscribes to the same cached model as standard MPC controls.
E.append(label('', '90 224 210 16',10,'ffd0c89f',param='Parameter 27'))
E=[e for e in E if get(get(e,'componentData'),'type')!='Indicator']+[e for e in E if get(get(e,'componentData'),'type')=='Indicator']
main=get(get(T,'pageData'),'tabs')[0];put(main,'componentDefinition',g.component_definition([],E,'ff263122'));put(main,'qlinkBoundsData',['650 22 598 280','650 310 598 280','30 260 324 346','378 26 246 510'])
# SOUNDS page: six independent noise sources with large native sliders.
texture=canvas.copy()
back=ImageDraw.Draw(texture)
for row in range(3):
 for col in range(2):
  xx=32+col*622;yy=16+row*200
  back.rounded_rectangle((xx,yy,xx+590,yy+180),12,fill='#182316',outline='#d1d2b5',width=3)
texture.save(D/'textures.png')
wide=Image.new('RGBA',(548,54*127))
for frame in range(127):wide.paste(source_fader.crop((0,frame*78,307,(frame+1)*78)).resize((548,54),Image.Resampling.LANCZOS),(0,frame*54))
wide.save(D/'texture_fader.png')
S=[entry('Texture panel','Image',{'version':2,'imageType':'Regular','colour':'0','image':'textures.png'},'0 0 1280 628',focus='No')]
textures=[(1,'TAPE NOISE','Smooth tape hiss'),(28,'VINYL CRACKLE','Record clicks and short crackles'),(29,'RADIO STATIC','Band-limited receiver noise and bursts'),(30,'WHITE NOISE','Broadband noise bed'),(31,'BROWN NOISE','Low, warm noise texture'),(32,'MAINS HUM','Electrical hum with harmonics')]
for j,(idx,title,helptext) in enumerate(textures):
 xx=32+(j%2)*622;yy=16+(j//2)*200
 S.append(label(title,f'{xx+16} {yy+14} 400 32',22,'ffffdda1'))
 S.append(label('',f'{xx+460} {yy+14} 110 32',20,'ffeee4c2',param=f'WithSuffix[%]/Parameter {idx}'))
 S.append(entry(title+' level','Knob',{'version':3,'knobType':'FilmStrip','filmStrip':'texture_fader.png','numFrames':127,'invert':False,'dragOrientation':'Horizontal','handleName':'Data'},f'{xx+21} {yy+58} 548 54',f'Parameter {idx}'))
 if idx!=32:S.append(label(helptext,f'{xx+20} {yy+130} 550 30',17,'ffc4c9b0'))
 else:
  for hz in [0,1]:
   asset=f'hum_{hz}'
   for on in [0,1]:
    setting_face(130,44,'50 Hz' if hz==0 else '60 Hz',on).save(D/f'{asset}_{"on" if on else "off"}.png')
   S.append(entry('Mains frequency','Button',g.button_data(asset+'_on.png',asset+'_off.png',hz,2),f'{xx+21+hz*146} {yy+124} 130 44','Parameter 33'))
tabs=get(get(T,'pageData'),'tabs')
tabs.append(g.Obj([('version',1),('tabName','SOUNDS'),('fnKeyIndex',3),('fnKeySubIndex',0),('componentDefinition',g.component_definition([],S,'ff21291a')),('qlinkBoundsData',['32 16 590 180','654 16 590 180','32 216 590 380','654 216 590 380'])]))
q=json.loads((D/'Q-Links.json').read_text());q['Screen Mode Q-Links']['map'].append({'Tab':4,'SubTab':1,'Bank Direction':'Row','Q-Links':{f'Q-Link {j+1}':idx for j,idx in enumerate([1,28,29,30,31,32,33,2,0,3,4,-1,-1,-1,-1,-1])}});(D/'Q-Links.json').write_text(json.dumps(q,indent=2))
(D/'TUI.json').write_text(g.dump_json(T)+'\n')
for mode in range(8):
 im=base.convert('RGBA');d=ImageDraw.Draw(im)
 n['text'](d,(501,93),full[mode],19,'#ffd58a',True)
 n['text'](d,(195,232),'TRANSPORT |',10,'#d0c89f',True)
 for j in range(8):
  x=650+j%2*306;y=22+j//2*144
  im.alpha_composite(Image.open(D/f'circuit_name{j}_{"on" if j==mode else "off"}.png'),(x,y));im.alpha_composite(Image.open(D/f'circuit_led_{1 if j==mode else 0}.png'),(x+252,y+73));im.alpha_composite(Image.open(D/f'circuit_power_{"on" if j==mode else "off"}.png'),(x,y+34))
 for x,y,asset,j in positions.get(mode,[]):im.alpha_composite(Image.open(D/f'{asset}_{"on" if j==(2 if mode==6 else 3 if mode==7 else 0) else "off"}.png'),(x,y))
 if mode==2:n['text'](d,(501,245),'NO EXTRA SETTINGS',14,'#eee3bf')
 for y,frame,caption in [(278,0,'0%'),(330,0,'0%'),(382,0,'0%'),(434,0,'0%'),(486,126,'100%')]:
  im.alpha_composite(fader.crop((0,frame*34,320,(frame+1)*34)),(34,y));n['text'](d,(318,y-12),caption,14,'#eee3bf')
 for side in range(2):im.alpha_composite(Image.open(D/f'polished_reel_{side}_0.png').crop((0,0,64,64)),(98+side*132,97))
 im.alpha_composite(Image.open(D/'bypass_off.png'),(30,527));im.alpha_composite(Image.open(D/'hold_on.png'),(398,536))
 im.convert('RGB').save(P/'Previews'/f'{mode+1}-{n["names"][mode].lower()}.png')
 if mode==0:im.convert('RGB').save(P/'UI-preview.png')
contact=Image.new('RGB',(1280,1360),'#10170f')
for mode in range(8):
 im=Image.open(P/'Previews'/f'{mode+1}-{n["names"][mode].lower()}.png');im.thumbnail((636,312));contact.paste(im,(mode%2*640+2,mode//2*340+25))
contact.save(P/'All-eight-modes.png')
print('Approved chrome skin retained; enlarged circuits, compact faders, polished controls and native UI reels.')
