"""Original FIELD / CIPHER skin. Fictional field-recorder and cipher-instrument styling.
No manufacturer artwork is copied. Pillow is needed only to redraw assets.
"""
from pathlib import Path
import sys,json,math,random
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageColor
P=Path(__file__).resolve().parent;SDK=P.parents[1];sys.path.insert(0,str(SDK/'tools'))
import gen_ui as g
D=P/'skins';D.mkdir(exist_ok=True)
result=g.main(['--params',str(P/'build/params.json'),'--ui',str(P/'ui.json'),'--out',str(D),'--kit-cache',str(P/'build')])
if result:raise SystemExit(result)
T=json.loads((D/'TUI.json').read_text(),object_pairs_hook=g.Obj)
def get(o,k):return next(v for a,v in o if a==k)
def put(o,k,v):
 for i,(a,_) in enumerate(o):
  if a==k:o[i]=(k,v);return
 o.append((k,v))
def font(n,b=False):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf',n)
def text(d,xy,s,n=20,c='#242729',b=False):d.text(xy,s,font=font(n,b),fill=c,anchor='mm')
def entry(name,typ,data,bounds,param=None,invalid=None,focus='Yes'):
 return g.entry(name,typ,data,bounds,focus,'Show' if param is None else 'Hide','Always',remap=() if param is None else [('Data',param)],invalidating=invalid)
def label(s,bounds,n=20,c='ff202326',param=None,invalid=None):
 a={'version':1,'textStyle':{'version':1,'font':{'version':1,'name':'Roboto','style':'Bold','height':float(n)},'colour':c,'justification':'horizontallyCentred verticallyCentred','case':'Original'},'type':'Text' if param is None else 'Value','handleName':'Parameter 0' if param is None else 'Data'}
 if param is None:a['text']=s
 return entry(s,'Label',a,bounds,param,invalid,'No')
names=['SPEED','SAT','MUTE','REV','WARBLE','LO-FI','BRAKE','STUTTER']
colors=['#e0ae50']*8
# Fictional instrument: original geometry, no reproduction of a historical product.
bg=Image.new('RGB',(1280,628),'#242b26');d=ImageDraw.Draw(bg);rng=random.Random(88)
for y in range(628):
 v=int(49-14*y/628);d.line((0,y,1279,y),fill=(v,v+9,v+2))
for _ in range(16000):
 x=rng.randrange(1280);y=rng.randrange(628);v=rng.choice(['#354034','#293329','#3c4536']);d.point((x,y),fill=v)
d.rounded_rectangle((5,5,1274,622),16,outline='#a2966c',width=2)
d.rectangle((18,18,1262,68),fill='#171e19')
text(d,(220,41),'VINTAGE MILITARY RADIO',27,'#f0e5bb',True)
text(d,(620,41),'FIELD / CIPHER',20,'#d4b870',True)
text(d,(1020,41),'TROPIX R!X',23,'#eee1b7',True)
text(d,(1020,61),'CRAZY JUNGLE SOUNDS',10,'#a7b49d',True)
# Main recorder chassis and setting bay.
d.rounded_rectangle((22,82,510,406),12,fill='#121b17',outline='#7c8060',width=2)
d.rounded_rectangle((521,82,755,406),10,fill='#20291f',outline='#686f50',width=2)
text(d,(638,99),'ROTOR SETTINGS',13,'#d6cba5',True)
text(d,(269,419),'SIGNAL TRANSPORT / C88',12,'#b7bd9f',True)
for x,s in [(188,'NOISE'),(534,'MIX')]:text(d,(x,449),s,17,'#e6ddbc',True)
text(d,(191,590),'BYPASS',16,'#ded7ba',True)
text(d,(407,590),'v1.0.8 / FIELD-CIPHER',12,'#a6b399',True)
for x,y in [(16,16),(1263,16),(16,611),(1263,611)]:
 d.ellipse((x-5,y-5,x+5,y+5),fill='#151c18',outline='#8c9372');d.line((x-3,y+2,x+3,y-2),fill='#a1a58d',width=2)
text(d,(1015,80),'EFFECT CIRCUITS',12,'#bfc7a8',True)
bg.save(D/'deck.png')
def cassette(mode):
 im=Image.new('RGB',(454,291),'#151d18');a=ImageDraw.Draw(im)
 a.rounded_rectangle((1,1,452,289),8,fill='#344334',outline='#b2a47a',width=2)
 # Cream instrument plate, brass inspection windows and olive enclosure.
 a.rectangle((17,13,437,66),fill='#dad2ae')
 text(a,(227,32),'C88 / FIELD RECORDER',19,'#202b23',True)
 text(a,(227,54),'CIRCUIT %02d / %s'%(mode+1,names[mode]),12,'#344132',True)
 a.rounded_rectangle((37,82,417,178),7,fill='#090f0c',outline='#9b8956',width=3)
 for x in [132,321]:
  a.ellipse((x-39,92,x+39,170),fill='#353b2d',outline='#c1ac73',width=2)
  a.ellipse((x-27,104,x+27,158),fill='#171c1a',outline='#929b90',width=3)
  for j in range(6):
   ang=j*math.pi/3;cx=x+19*math.cos(ang);cy=131+19*math.sin(ang)
   a.ellipse((cx-3,cy-3,cx+3,cy+3),fill='#e8d6a0' if j==0 else '#778269')
  a.ellipse((x-5,126,x+5,136),fill='#bdc8ba')
 a.rectangle((172,112,280,149),fill='#393c28',outline='#9d915f',width=2)
 for y in [120,140]:a.line((172,y,280,y),fill='#d0ac62',width=2)
 # Cipher-inspired thumbwheels: decorative, never advertised as audio controls.
 for j,x in enumerate([92,182,272,362]):
  a.rounded_rectangle((x-29,194,x+29,245),5,fill='#171c17',outline='#7c7956',width=2)
  for dx in range(-22,25,6):a.line((x+dx,198,x+dx,241),fill='#505b43')
  a.rectangle((x-13,205,x+13,234),fill='#ddd4b2')
  text(a,(x,220),str((mode*7+j*3+8)%10),21,'#253126',True)
 text(a,(227,270),'TRANSPORT  /  MONITOR',12,'#d0c7a0',True)
 for x,y in [(12,12),(442,12),(12,278),(442,278)]:
  a.ellipse((x-4,y-4,x+4,y+4),fill='#151c15',outline='#8f9272');a.line((x-2,y+1,x+2,y-1),fill='#a8ad8a')
 return im
cassettes=[cassette(i) for i in range(8)]
strip=Image.new('RGB',(454,291*8))
for i,im in enumerate(cassettes):strip.paste(im,(0,i*291));im.save(D/f'cassette-{i}.png')
strip.save(D/'cassette_modes.png')
# 64-frame reel strips are driven by DSP telemetry, not the UI's fixed-rate animation.
# A single bright marker makes speed/direction unambiguous even with six reel spokes.
reels=Image.new('RGBA',(56,56*64))
for frame in range(64):
 im=Image.new('RGBA',(56,56));a=ImageDraw.Draw(im)
 a.ellipse((1,1,54,54),fill='#171c1a',outline='#929b90',width=3)
 for spoke in range(6):
  angle=frame*2*math.pi/64+spoke*math.pi/3
  cx=28+19*math.cos(angle);cy=28+19*math.sin(angle)
  a.ellipse((cx-3,cy-3,cx+3,cy+3),fill='#f2e9c3' if spoke==0 else '#69766c')
 a.ellipse((23,23,33,33),fill='#bdc8ba',outline='#080e0b')
 reels.alpha_composite(im,(0,56*frame))
reels.save(D/'reel_motion.png')
# Native animated Images have their own UI clock; no audio telemetry repaint required.
# All strips have the SAME 400 frames. Closed cycles 5/10/15/18 give exact relative
# quarter/half/three-quarter/nine-tenths motion regardless of the MPC UI tick rate.
reels.crop((0,0,56,56)).save(D/'reel_still.png')
for index,turns in [(1,5),(0,10),(2,15),(3,18)]:
 for reverse in [0,1]:
  strip=Image.new('RGBA',(56,56*400))
  for frame in range(400):
   im=Image.new('RGBA',(56,56));a=ImageDraw.Draw(im)
   a.ellipse((1,1,54,54),fill='#171c1a',outline='#929b90',width=3)
   for spoke in range(6):
    angle=(1 if not reverse else -1)*frame*2*math.pi*turns/400+spoke*math.pi/3
    cx=28+19*math.cos(angle);cy=28+19*math.sin(angle)
    a.ellipse((cx-3,cy-3,cx+3,cy+3),fill='#f2e9c3' if spoke==0 else '#69766c')
   a.ellipse((23,23,33,33),fill='#bdc8ba',outline='#080e0b');strip.alpha_composite(im,(0,frame*56))
  strip.save(D/f'reel_native_{index}_{reverse}.png')


def button(name,w,h,col,style='glass'):
 for on in [0,1]:
  im=Image.new('RGBA',(w,h));a=ImageDraw.Draw(im)
  a.rounded_rectangle((0,0,w-1,h-1),6,fill='#11170f',outline='#747a58',width=2)
  face='#c6a969' if on else '#313c2b'
  if style=='pad':face='#d1bd83' if on else '#c7c7aa'
  a.rounded_rectangle((5,4,w-6,h-6),4,fill=face,outline='#e1d6aa' if on else '#879176',width=2)
  a.line((9,h-9,w-10,h-9),fill='#5e654b',width=2)
  im.save(D/f'{name}_{"on" if on else "off"}.png')
for i,c in enumerate(colors):
 button(f'sub{i}',88,64,c);button(f'small{i}',82,64,c)
 for on in [0,1]:
  im=Image.new('RGBA',(217,30));a=ImageDraw.Draw(im)
  a.rounded_rectangle((0,0,216,29),4,fill='#6b633c' if on else '#1b241b',outline='#a5a078' if on else '#59674e')
  text(a,(108,15),f'{i+1:02d} / {names[i]}',16,'#fff0b8' if on else '#b6bea3',True)
  im.save(D/f'name{i}_{"on" if on else "off"}.png')
  im=Image.new('RGBA',(217,8));a=ImageDraw.Draw(im)
  a.rounded_rectangle((0,0,216,7),3,fill='#eab65b' if on else '#0b110d',outline='#716744')
  im.save(D/f'led{i}_{"on" if on else "off"}.png')
button('hold',155,58,'#d2bd80',style='pad');button('pad',217,67,'#d2bd80',style='pad')
for on in [0,1]:
 path=D/f'hold_{"on" if on else "off"}.png';im=Image.open(path);text(ImageDraw.Draw(im),(77,29),'HOLD',21,'#182217',True);im.save(path)
 path=D/f'pad_{"on" if on else "off"}.png';im=Image.open(path);text(ImageDraw.Draw(im),(108,33),'ENGAGE',14,'#263122',True);im.save(path)
for on in [0,1]:
 im=Image.new('RGBA',(85,44));a=ImageDraw.Draw(im)
 a.rounded_rectangle((1,2,83,41),5,fill='#141b14',outline='#7c8664',width=2)
 x=63 if on else 22;a.rounded_rectangle((x-18,5,x+18,38),4,fill='#e0b46b' if on else '#b9bca3',outline='#e9e3bc',width=2)
 im.save(D/f'bypass_{"on" if on else "off"}.png')
# Horizontal native filmstrip: no scaled artwork or changed parameter semantics.
fader=Image.new('RGBA',(307,78*127))
for n in range(127):
 im=Image.new('RGBA',(307,78));a=ImageDraw.Draw(im)
 for x in range(15,298,18):a.line((x,8,x,17),fill='#a5ae8c')
 a.rounded_rectangle((10,31,296,44),4,fill='#080e09',outline='#7b8663')
 x=int(15+n*275/126)
 a.rounded_rectangle((x-13,22,x+13,55),3,fill='#d4c49a',outline='#f1e6bd',width=2)
 a.line((x,26,x,51),fill='#303b24',width=3)
 fader.paste(im,(0,n*78))
fader.save(D/'deck_fader.png')
E=[entry('Panel','Image',{'version':2,'imageType':'Regular','colour':'0','image':'deck.png'},'0 0 1280 628',focus='No'),entry('Cassette','Image',{'version':2,'imageType':'FilmStrip','colour':'0','image':'cassette_modes.png','numFrames':8,'handleName':'Data'},'40 100 454 291','Parameter 25',focus='No')]
for x in [144,333]:
 E.append(entry('Notified motor reel','Image',{'version':2,'imageType':'FilmStrip','colour':'0','image':'reel_motion.png','numFrames':64,'handleName':'Data','animated':False},f'{x} 203 56 56','Parameter 27',focus='No'))
E.append(label('', '540 381 156 18', 12, param='Parameter 27'))
for x,idx in [(35,1),(380,2)]:
 E.append(entry('Vertical fader','Knob',{'version':2,'knobType':'FilmStrip','filmStrip':'deck_fader.png','numFrames':127,'invert':False,'handleName':'Data'},f'{x} 464 307 78',f'Parameter {idx}'))
 E.append(label('',f'{x+111} 530 84 27',16,c='ffe3d6ad',param=f'WithSuffix[%]/Parameter {idx}'))
for idx,name,asset,bounds in [(3,'Bypass','bypass','40 565 85 44'),(4,'Hold','hold','550 553 155 58')]:
 E.append(entry(name,'Button',g.button_data(asset+'_on.png',asset+'_off.png',1,1),bounds,f'Parameter {idx}'))

# Existing DSP setting values; visual positions are independent of other products. SAT order is Amp, Boost, Drive.
configs={0:(13,4,[(1,'1/4'),(0,'1/2'),(2,'3/4'),(3,'9/10')]),1:(14,3,[(1,'Amp'),(0,'Boost'),(2,'Drive')]),4:(15,7,[(j,str(j+1)) for j in range(7)]),5:(16,8,[(j,str(j+1)) for j in range(8)]),6:(17,4,[(j,str(j+1)) for j in range(4)]),7:(18,9,[(0,'1/2'),(1,'1/4'),(8,'1/4T'),(2,'1/8'),(6,'1/8T'),(3,'1/16'),(4,'1/32'),(5,'1/64')])}
# Store drawing positions for deterministic UI review snapshots.
positions={}
for mode,(param,total,opts) in configs.items():
 inv=[f'IndexedEnabling/{mode}/8/Parameter 25'];cols=2 if len(opts)>4 else 1;h=64;w=82 if cols==2 else 88;x0=550 if cols==2 else 591;rows=math.ceil(len(opts)/cols);y0=121 if rows==4 else 154
 for j,(buttonId,caption) in enumerate(opts):
  x=x0+(j%cols)*88;y=y0+(j//cols)*(h+3);asset=f'{"small" if cols==2 else "sub"}{mode}'
  base=asset;asset=f'{base}_choice{buttonId}'
  for on in [0,1]:
   im=Image.open(D/f'{base}_{"on" if on else "off"}.png');a=ImageDraw.Draw(im)
   if mode==0:
    top,bottom=caption.split('/');text(a,(29,17),top,21,'#e8fcff');a.line((29,42,54,19),fill='#e8fcff',width=2);text(a,(59,47),bottom,24 if len(bottom)==1 else 19,'#e8fcff')
   else:text(a,(w/2,h/2),caption,23 if len(caption)<4 else 18,'#e6e7d8')
   im.save(D/f'{asset}_{"on" if on else "off"}.png')
  E.append(entry('Setting '+caption,'Button',g.button_data(asset+'_on.png',asset+'_off.png',buttonId,total),f'{x} {y} {w} {h}',f'Parameter {param}',inv))
  positions.setdefault(mode,[]).append((x,y,w,h,asset,caption,buttonId))
for mode,caption in [(2,'MUTE'),(3,'REVERSE')]:
 inv=[f'IndexedEnabling/{mode}/8/Parameter 25']
 E.append(label('×' if mode==2 else '⇄','579 178 118 74',60,c='ffd4c595',invalid=inv))
 E.append(label(caption,'566 259 145 32',17,c='ffd4c595',invalid=inv))
# Mode names select a view. Large pads engage effects independently; LEDs show engagement.
for mode,name in enumerate(names):
 x=790+(mode%2)*235; y=95+(mode//2)*128
 E.append(entry('View '+name,'Button',g.button_data(f'name{mode}_on.png',f'name{mode}_off.png',mode,8),f'{x} {y} 217 30','Parameter 25'))

 E.append(entry('Active '+name,'Indicator',{'version':1,'onImage':f'led{mode}_on.png','offImage':f'led{mode}_off.png','indicatorId':1,'numIndicatorsInGroup':1,'handleName':'Data'},f'{x} {y+35} 217 8',f'Parameter {5+mode}',focus='No'))
 for hold in [0,1]:
  handle=f'Parameter {5+mode}' if hold else f'ResetOnGestureEnd/Parameter {5+mode}';data=g.button_data('pad_on.png','pad_off.png',1,1)
  if not hold:put(data,'gestureBehaviour','Hold')
  E.append(entry('Engage '+name,'Button',data,f'{x} {y+48} 217 67',handle,[f'IndexedEnabling/{hold}/2/Parameter 4']))

page=get(T,'pageData');tabs=get(page,'tabs');main=tabs[0]
put(main,'componentDefinition',g.component_definition([],E,'ff303b2b'))
put(main,'qlinkBoundsData',['784 88 462 254','784 345 462 254','29 435 683 177','521 82 234 324'])
(D/'TUI.json').write_text(g.dump_json(T)+'\n')
q=json.loads((D/'Q-Links.json').read_text());mp=[5,6,7,8,9,10,11,12,1,2,25,4,0,19,20,3]
q['Screen Mode Q-Links']['map'][0]['Bank Direction']='Row';q['Screen Mode Q-Links']['map'][0]['Q-Links']={f'Q-Link {i+1}':v for i,v in enumerate(mp)}
(D/'Q-Links.json').write_text(json.dumps(q,indent=2))
# Actual asset previews, not screenshots of physical hardware.
R=P/'Previews';R.mkdir(exist_ok=True)
for mode in range(8):
 im=bg.convert('RGBA');im.alpha_composite(cassettes[mode].convert('RGBA'),(40,100))
 for x,n,t in [(35,0,'0%'),(380,126,'100%')]:im.alpha_composite(fader.crop((0,n*78,307,(n+1)*78)),(x,464));text(ImageDraw.Draw(im),(x+153,542),t,16,'#e3d6ad')
 im.alpha_composite(Image.open(D/'bypass_off.png'),(40,565));im.alpha_composite(Image.open(D/'hold_on.png'),(550,553))
 default=2 if mode==6 else 3 if mode==7 else 0
 for x,y,w,h,asset,caption,buttonId in positions.get(mode,[]):
  im.alpha_composite(Image.open(D/f'{asset}_{"on" if buttonId==default else "off"}.png'),(x,y))
 if mode in [2,3]:text(ImageDraw.Draw(im),(638,215),'×' if mode==2 else '⇄',60,'#d4c595');text(ImageDraw.Draw(im),(638,275),'MUTE' if mode==2 else 'REVERSE',17,'#d4c595')
 for j,name in enumerate(names):
  x=790+(j%2)*235;y=95+(j//2)*128;im.alpha_composite(Image.open(D/f'name{j}_{"on" if j==mode else "off"}.png'),(x,y))
  im.alpha_composite(Image.open(D/f'led{j}_{"on" if j==mode else "off"}.png'),(x,y+35));im.alpha_composite(Image.open(D/f'pad_{"on" if j==mode else "off"}.png'),(x,y+48))
 im.convert('RGB').save(R/f'{mode+1}-{names[mode].lower()}.png')
 if mode==0:im.convert('RGB').save(P/'UI-preview.png')
contact=Image.new('RGB',(1280,4*340),'#141d1e');a=ImageDraw.Draw(contact)
for mode in range(8):
 x=mode%2*640;y=mode//2*340;im=Image.open(R/f'{mode+1}-{names[mode].lower()}.png');im.thumbnail((636,312));contact.paste(im,(x+2,y+25));text(a,(x+320,y+12),names[mode],15,'#f3e8cc',True)
contact.save(P/'All-eight-modes.png')
print('Generated eight mode views, native button bindings, and asset previews.')
