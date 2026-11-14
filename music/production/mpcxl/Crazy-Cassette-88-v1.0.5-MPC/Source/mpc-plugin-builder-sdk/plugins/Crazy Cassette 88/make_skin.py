"""Original cassette-deck MPC skin. Layout follows the reference control roles.
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
colors=['#43d6ee','#e4c458','#e5e4df','#37cf77','#f39836','#368ee1','#ef3e59','#ad78ed']
# Matte, lightly worn metal console.
bg=Image.new('RGB',(1280,628));d=ImageDraw.Draw(bg);rng=random.Random(88)
for y in range(628):
 shade=int(155-20*y/628);d.line((0,y,1279,y),fill=(shade,shade+2,shade+3))
for _ in range(80000):
 x=rng.randrange(1280);y=rng.randrange(628);c=bg.getpixel((x,y));n=rng.randrange(-7,8);d.point((x,y),fill=tuple(max(0,min(255,v+n)) for v in c))
for _ in range(160):
 x=rng.randrange(1280);y=rng.randrange(628);d.line((x,y,x+rng.randint(-18,18),y+rng.randint(-8,8)),fill=(162,165,166),width=1)
d.rectangle((3,3,1276,625),outline='#25292b',width=3);d.line((8,412,1272,412),fill='#555c5f',width=1)
d.rounded_rectangle((371,31,911,411),17,fill='#757c80')
d.rounded_rectangle((373,29,909,407),17,fill='#aeb2b4',outline='#c1c5c5',width=2)
d.rounded_rectangle((414,74,868,365),10,fill='#141a1a',outline='#555b59',width=3)
for x,s in [(87,'NOISE'),(1194,'MIX')]:text(d,(x,32),s,20,b=True)
text(d,(1044,44),'BYPASS',19,b=True)
# Own brand in place of original logo, within familiar retro stripe badge.
for y,c in [(155,'#c75059'),(177,'#53a9bf'),(199,'#cfb56b'),(221,'#ac7547')]:d.rectangle((911,y,1118,y+21),fill=c)
text(d,(1015,169),'TROPIX R!X',19,b=True)
text(d,(1015,197),'CRAZY CASSETTE 88',14,b=True)
text(d,(1015,231),'CRAZY JUNGLE SOUNDS',11,b=True)
bg.save(D/'deck.png')
# Each cassette is an original 454x291 image drawn for native-size display.
def cassette(mode):
 c=ImageColor.getrgb(colors[mode]);im=Image.new('RGB',(454,291));a=ImageDraw.Draw(im)
 for y in range(291):
  f=.8+.22*(1-y/291);a.line((0,y,453,y),fill=tuple(min(255,int(v*f)) for v in c))
 a.rounded_rectangle((3,3,450,287),10,outline='#292c2c',width=3)
 a.rounded_rectangle((30,25,424,207),7,fill='#dbd6c5',outline='#c3c2b3',width=2)
 # Eight distinct familiar tape families, with entirely original graphic details.
 if mode==0:
  for x in range(0,470,58):a.polygon([(x,25),(x+27,25),(x-80,207),(x-108,207)],fill='#60c7d5')
  text(a,(220,53),'SLOW MOTION / C88',18,b=True)
 elif mode==1:
  a.rectangle((31,26,423,206),fill='#202323')
  for j,col in enumerate(['#b59429','#bd7431','#d74932']):a.rectangle((31,112+j*21,423,132+j*21),fill=col)
  a.rectangle((90,41,365,76),fill='#e6dfc8');text(a,(225,58),'JUNGLE CHROME',17,b=True)
 elif mode==2:
  a.rectangle((31,26,423,206),fill='#deded3');text(a,(225,57),'SILENT REEL',17,c='#666d68',b=True)
 elif mode==3:
  a.rectangle((31,26,423,206),fill='#edebd8')
  a.polygon([(65,70),(104,40),(104,59),(160,59),(160,82),(104,82),(104,99)],fill='#189747')
  a.polygon([(380,158),(341,188),(341,169),(285,169),(285,146),(341,146),(341,130)],fill='#189747')
  text(a,(256,53),'BACKSPIN • C88',17,b=True)
 elif mode==4:
  a.rectangle((31,26,423,206),fill='#9b5c37')
  for x in range(24,440,29):
   pts=[(x+9*math.sin(y*.035+x),y) for y in range(27,204,3)];a.line(pts,fill='#75b298',width=2)
  a.rectangle((31,178,423,206),fill='#c65627');text(a,(225,191),'WOW / FLUTTER • TYPE II',14,c='#ecdabe',b=True)
 elif mode==5:
  a.rectangle((31,26,423,206),fill='#1b6fbc');a.rectangle((31,26,290,206),fill='#4badd0')
  for x in range(45,280,19):
   for y in range(37,193,19):a.ellipse((x,y,x+2,y+2),fill='#377fa7')
  text(a,(353,55),'DUST 88',15,c='#d0ed8c',b=True)
 elif mode==6:
  a.rectangle((31,26,423,206),fill='#2c141b')
  for j in range(7):a.rectangle((31,147+j*7,423,149+j*7),fill='#ad414c')
  text(a,(150,55),'MOTOR STOP',20,c='#edcd6b',b=True)
 else:
  a.rectangle((31,26,423,206),fill='#3d2b61')
  for x in range(36,420,30):a.polygon([(x,29),(x+13,29),(x+58,205),(x+45,205)],fill='#71529a')
  text(a,(225,54),'REPEAT / REWIND',20,c='#eee3cd',b=True)
 # Transport mechanics and sculpted lower shell.
 a.polygon([(109,219),(345,219),(373,283),(81,283)],outline='#51534c',fill=tuple(int(v*.84) for v in c))
 a.line((110,221,344,221),fill=tuple(min(255,v+32) for v in c),width=3)
 a.rounded_rectangle((91,89,363,172),4,fill=tuple(int(v*.89) for v in c),outline='#879287',width=2)
 a.rectangle((171,105,283,159),fill='#6b695d',outline='#545449',width=2)
 a.polygon([(173,107),(202,109),(198,153),(173,157)],fill='#4b483d');a.polygon([(281,107),(254,109),(257,154),(281,157)],fill='#4b483d')
 for y in [121,141]:a.line((175,y,279,y),fill='#413e33',width=2)
 for x in [132,321]:
  a.ellipse((x-27,104,x+27,158),fill='#222624',outline='#a4a394',width=3)
  for j in range(6):
   ang=j*math.pi/3;cx=x+20*math.cos(ang);cy=131+20*math.sin(ang);a.ellipse((cx-3,cy-3,cx+3,cy+3),fill='#6b716a')
  a.ellipse((x-5,126,x+5,136),fill='#c3c8bb',outline='#090e0c')
 for x,y,r in [(118,269,9),(163,261,7),(227,239,8),(290,261,7),(335,269,9)]:a.ellipse((x-r,y-r,x+r,y+r),fill='#080f0c')
 for x,y in [(18,18),(435,18),(18,271),(435,271)]:
  a.ellipse((x-7,y-7,x+7,y+7),fill='#111a15',outline='#4b554c',width=2);a.line((x-3,y-3,x+3,y+3),fill='#646d61',width=2)
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
 rgb=ImageColor.getrgb(col)
 for on in [0,1]:
  im=Image.new('RGBA',(w,h));a=ImageDraw.Draw(im)
  a.rounded_rectangle((0,0,w-1,h-1),7,fill='#111817',outline='#5d6561',width=2)
  for y in range(4,h-4):
   if style=='pad':f=.74-.27*y/h if not on else .48+.24*y/h;v=tuple(int(180*f) for _ in range(3))
   else:
    f=(.28 if not on else .66)+.13*(1-y/h);v=tuple(int(v*f) for v in rgb)
   a.line((5,y,w-6,y),fill=v)
  if on and style!='pad':
   glow=Image.new('RGBA',(w,h));gd=ImageDraw.Draw(glow);gd.ellipse((w*.15,h*.2,w*.85,h*.95),fill=rgb+(145,));im=Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(max(4,h*.17))))
  a=ImageDraw.Draw(im);a.rounded_rectangle((8,7,w-9,h-8),5,outline=tuple(min(255,v+40) for v in rgb)+(110,) if on else '#777f7980',width=1)
  im.save(D/f'{name}_{"on" if on else "off"}.png')
for i,c in enumerate(colors):
 button(f'sub{i}',88,78,c);button(f'small{i}',82,74,c);button(f'led{i}',145,19,c);button(f'name{i}',145,43,c)
# Mode captions sit on plain metal when unselected, like the reference layout.
for i,c in enumerate(colors):
 for on in [0,1]:
  im=Image.new('RGBA',(145,43));a=ImageDraw.Draw(im)
  if on:a.rounded_rectangle((1,1,143,41),5,fill=c)
  text(a,(72,22),names[i],19,b=True)
  im.save(D/f'name{i}_{"on" if on else "off"}.png')
button('hold',155,89,'#c6c8c4',style='pad');button('pad',153,107,'#989b97',style='pad')
for on in [0,1]:
 path=D/f'hold_{"on" if on else "off"}.png';im=Image.open(path);text(ImageDraw.Draw(im),(77,44),'HOLD',24,b=True);im.save(path)
# Make unengaged LEDs genuinely black, so selected view is not confused with active audio.
for i in range(8):
 im=Image.new('RGBA',(145,19));a=ImageDraw.Draw(im);a.rounded_rectangle((0,0,144,18),4,fill='#0c100f',outline='#747a75',width=2);im.save(D/f'led{i}_off.png')
# Version badge is baked into the panel as a positive check after the MPC skin cache reloads.
text(d,(1015,258),'v1.0.5 • LIVE REELS',12,b=True);bg.save(D/'deck.png')
# Bypass switch and native-size vertical fader strip.
for on in [0,1]:
 im=Image.new('RGBA',(85,44));a=ImageDraw.Draw(im);a.rounded_rectangle((1,2,83,41),20,fill='#db3a4c' if on else '#7b8281',outline='#b6bcba',width=2);x=63 if on else 22;a.ellipse((x-19,3,x+19,41),fill='#a4aeaa',outline='#717c76',width=2);im.save(D/f'bypass_{"on" if on else "off"}.png')
fader=Image.new('RGBA',(78,307*127))
for n in range(127):
 im=Image.new('RGBA',(78,307));a=ImageDraw.Draw(im);a.rectangle((33,5,44,300),fill='#0b1111');a.line((32,4,32,301),fill='#cad0cd');y=int(289-n*271/126)
 a.rectangle((0,y-13,77,y+13),fill='#596365');a.rectangle((2,y-12,75,y+9),fill='#c4ced0');a.rectangle((1,y-3,76,y+3),fill='#141d20');a.line((3,y+9,74,y+9),fill='#79898c',width=2);fader.paste(im,(0,n*307))
fader.save(D/'deck_fader.png')
E=[entry('Panel','Image',{'version':2,'imageType':'Regular','colour':'0','image':'deck.png'},'0 0 1280 628',focus='No'),entry('Cassette','Image',{'version':2,'imageType':'FilmStrip','colour':'0','image':'cassette_modes.png','numFrames':8,'handleName':'Data'},'414 74 454 291','Parameter 25',focus='No')]
for x in [518,707]:
 E.append(entry('Notified motor reel','Image',{'version':2,'imageType':'FilmStrip','colour':'0','image':'reel_motion.png','numFrames':64,'handleName':'Data','animated':False},f'{x} 177 56 56','Parameter 27',focus='No'))
E.append(label('', '967 267 156 18', 12, param='Parameter 27'))
for x,idx in [(48,1),(1155,2)]:
 E.append(entry('Vertical fader','Knob',{'version':2,'knobType':'FilmStrip','filmStrip':'deck_fader.png','numFrames':127,'invert':False,'handleName':'Data'},f'{x} 57 78 307',f'Parameter {idx}'))
 E.append(label('',f'{x-3} 372 84 27',20,param=f'WithSuffix[%]/Parameter {idx}'))
for idx,name,asset,bounds in [(3,'Bypass','bypass','1001 72 85 44'),(4,'Hold','hold','965 287 155 89')]:
 E.append(entry(name,'Button',g.button_data(asset+'_on.png',asset+'_off.png',1,1),bounds,f'Parameter {idx}'))

# Reference layouts, bound to actual DSP settings. SAT order is Amp, Boost, Drive.
configs={0:(13,4,[(1,'1/4'),(0,'1/2'),(2,'3/4'),(3,'9/10')]),1:(14,3,[(1,'Amp'),(0,'Boost'),(2,'Drive')]),4:(15,7,[(j,str(j+1)) for j in range(7)]),5:(16,8,[(j,str(j+1)) for j in range(8)]),6:(17,4,[(j,str(j+1)) for j in range(4)]),7:(18,9,[(0,'1/2'),(1,'1/4'),(8,'1/4T'),(2,'1/8'),(6,'1/8T'),(3,'1/16'),(4,'1/32'),(5,'1/64')])}
# Store drawing positions for deterministic UI review snapshots.
positions={}
for mode,(param,total,opts) in configs.items():
 inv=[f'IndexedEnabling/{mode}/8/Parameter 25'];cols=2 if len(opts)>4 else 1;h=74 if cols==2 else 78;w=82 if cols==2 else 88;x0=164 if cols==2 else 206;rows=math.ceil(len(opts)/cols);y0=57 if rows==4 else 88
 for j,(buttonId,caption) in enumerate(opts):
  x=x0+(j%cols)*88;y=y0+(j//cols)*(h+3);asset=f'{"small" if cols==2 else "sub"}{mode}'
  base=asset;asset=f'{base}_choice{buttonId}'
  for on in [0,1]:
   im=Image.open(D/f'{base}_{"on" if on else "off"}.png');a=ImageDraw.Draw(im)
   if mode==0:
    top,bottom=caption.split('/');text(a,(29,22),top,23,'#e8fcff');a.line((29,47,54,22),fill='#e8fcff',width=2);text(a,(59,55),bottom,28 if len(bottom)==1 else 22,'#e8fcff')
   else:text(a,(w/2,h/2),caption,23 if len(caption)<4 else 18,'#e6e7d8')
   im.save(D/f'{asset}_{"on" if on else "off"}.png')
  E.append(entry('Setting '+caption,'Button',g.button_data(asset+'_on.png',asset+'_off.png',buttonId,total),f'{x} {y} {w} {h}',f'Parameter {param}',inv))
  positions.setdefault(mode,[]).append((x,y,w,h,asset,caption,buttonId))
for mode,caption in [(2,'MUTE'),(3,'REVERSE')]:
 inv=[f'IndexedEnabling/{mode}/8/Parameter 25']
 E.append(label('×' if mode==2 else '⇄','191 165 118 74',60,c='ff656d6c',invalid=inv))
 E.append(label(caption,'180 242 145 32',17,c='ff656d6c',invalid=inv))
# Mode names select a view. Large pads engage effects independently; LEDs show engagement.
for mode,name in enumerate(names):
 x=26+mode*155
 E.append(entry('View '+name,'Button',g.button_data(f'name{mode}_on.png',f'name{mode}_off.png',mode,8),f'{x} 422 145 43','Parameter 25'))

 E.append(entry('Active '+name,'Indicator',{'version':1,'onImage':f'led{mode}_on.png','offImage':f'led{mode}_off.png','indicatorId':1,'numIndicatorsInGroup':1,'handleName':'Data'},f'{x} 483 145 19',f'Parameter {5+mode}',focus='No'))
 for hold in [0,1]:
  handle=f'Parameter {5+mode}' if hold else f'ResetOnGestureEnd/Parameter {5+mode}';data=g.button_data('pad_on.png','pad_off.png',1,1)
  if not hold:put(data,'gestureBehaviour','Hold')
  E.append(entry('Engage '+name,'Button',data,f'{x-4} 518 153 107',handle,[f'IndexedEnabling/{hold}/2/Parameter 4']))

page=get(T,'pageData');tabs=get(page,'tabs');main=tabs[0]
put(main,'componentDefinition',g.component_definition([],E,'ff969b9c'))
put(main,'qlinkBoundsData',['22 483 614 142','642 483 614 142','40 44 300 358','960 44 280 358'])
(D/'TUI.json').write_text(g.dump_json(T)+'\n')
q=json.loads((D/'Q-Links.json').read_text());mp=[5,6,7,8,9,10,11,12,1,2,25,4,0,19,20,3]
q['Screen Mode Q-Links']['map'][0]['Bank Direction']='Row';q['Screen Mode Q-Links']['map'][0]['Q-Links']={f'Q-Link {i+1}':v for i,v in enumerate(mp)}
(D/'Q-Links.json').write_text(json.dumps(q,indent=2))
# Actual asset previews, not screenshots of physical hardware.
R=P/'Previews';R.mkdir(exist_ok=True)
for mode in range(8):
 im=bg.convert('RGBA');im.alpha_composite(cassettes[mode].convert('RGBA'),(414,74))
 for x,n,t in [(48,0,'0%'),(1155,126,'100%')]:im.alpha_composite(fader.crop((0,n*307,78,(n+1)*307)),(x,57));text(ImageDraw.Draw(im),(x+39,386),t,20)
 im.alpha_composite(Image.open(D/'bypass_off.png'),(1001,72));im.alpha_composite(Image.open(D/'hold_on.png'),(965,287))
 default=2 if mode==6 else 3 if mode==7 else 0
 for x,y,w,h,asset,caption,buttonId in positions.get(mode,[]):
  im.alpha_composite(Image.open(D/f'{asset}_{"on" if buttonId==default else "off"}.png'),(x,y))
 if mode in [2,3]:text(ImageDraw.Draw(im),(250,202),'×' if mode==2 else '⇄',60,'#656d6c');text(ImageDraw.Draw(im),(252,258),'MUTE' if mode==2 else 'REVERSE',17,'#656d6c')
 for j,name in enumerate(names):
  x=26+j*155;im.alpha_composite(Image.open(D/f'name{j}_{"on" if j==mode else "off"}.png'),(x,422))
  im.alpha_composite(Image.open(D/f'led{j}_{"on" if j==mode else "off"}.png'),(x,483));im.alpha_composite(Image.open(D/f'pad_{"on" if j==mode else "off"}.png'),(x-4,518))
 im.convert('RGB').save(R/f'{mode+1}-{names[mode].lower()}.png')
 if mode==0:im.convert('RGB').save(P/'UI-preview.png')
contact=Image.new('RGB',(1280,4*340),'#141d1e');a=ImageDraw.Draw(contact)
for mode in range(8):
 x=mode%2*640;y=mode//2*340;im=Image.open(R/f'{mode+1}-{names[mode].lower()}.png');im.thumbnail((636,312));contact.paste(im,(x+2,y+25));text(a,(x+320,y+12),names[mode],15,'#f3e8cc',True)
contact.save(P/'All-eight-modes.png')
print('Generated eight mode views, native button bindings, and asset previews.')
