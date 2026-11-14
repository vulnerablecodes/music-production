"""Roomy native MPC performance UI; reels use the UI clock, not host notifications."""
from pathlib import Path
import runpy,json,math
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
n=runpy.run_path(str(P/'make_skin.py'));D=n['D'];g=n['g'];entry=n['entry'];label=n['label'];get=n['get'];put=n['put'];T=n['T']
names=['SPEED','SATURATION','MUTE','REVERSE','WARBLE','LO-FI','BRAKE','STUTTER']
def text(d,xy,s,size=20,fill='#eee5cb'):
 d.text(xy,s,font=n['font'](size,True),fill=fill,anchor='mm')
def sprite(name,w,h,caption,size=20):
 for on in [0,1]:
  im=Image.new('RGBA',(w,h),'#1b241f');a=ImageDraw.Draw(im)
  a.rounded_rectangle((2,2,w-3,h-3),9,fill='#5b502c' if on else '#26332b',outline='#ffd17e' if on else '#8b9587',width=3 if on else 2)
  text(a,(w/2,h/2),caption,size,'#fff1bf' if on else '#eee5cb');im.save(D/f'{name}_{"on" if on else "off"}.png')
bg=Image.new('RGB',(1280,628),'#202a23');a=ImageDraw.Draw(bg)
a.rounded_rectangle((16,14,868,256),14,fill='#17211b',outline='#727f6c',width=2)
a.rounded_rectangle((892,14,1264,612),14,fill='#151e18',outline='#a99a70',width=2)
text(a,(441,38),'1  SELECT AN EFFECT',20);text(a,(1078,40),'2  ADJUST SETTINGS',20)
text(a,(1078,490),'3  ENGAGE THE SELECTED EFFECT',15)
# Retain the approved recorder artwork in its own uncluttered monitor bay.
art=Image.open(P/'artwork/chrome-neutral.png').convert('RGB')
art=art.resize((1280,628),Image.Resampling.LANCZOS)
bg.paste(art.crop((22,82,510,406)).resize((390,259),Image.Resampling.LANCZOS),(32,270))
text(a,(646,286),'MASTER CONTROLS',18)
for y,s in [(310,'NOISE'),(430,'MIX')]:text(a,(646,y),s,18)
text(a,(128,540),'OUTPUT',16)
text(a,(1078,82),'ACTIVE LEDs show enabled circuits',14,'#b4bfae')
bg.save(D/'deck.png')
E=[entry('Panel','Image',{'version':2,'imageType':'Regular','colour':'0','image':'deck.png'},'0 0 1280 628',focus='No')]
preview=[]
for mode,name in enumerate(names):
 x=32+(mode%4)*208;y=66+(mode//4)*96
 sprite('select'+str(mode),196,76,name,19)
 E.append(entry('Select '+name,'Button',g.button_data(f'select{mode}_on.png',f'select{mode}_off.png',mode,8),f'{x} {y} 196 76','Parameter 25'))
 # Indicator is separate from the selected-view outline.
 for on in [0,1]:
  im=Image.new('RGBA',(12,12));ImageDraw.Draw(im).ellipse((1,1,10,10),fill='#ffcc70' if on else '#090f0b');im.save(D/f'active_{on}.png')
 E.append(entry('Active '+name,'Indicator',{'version':1,'onImage':'active_1.png','offImage':'active_0.png','indicatorId':1,'numIndicatorsInGroup':1,'handleName':'Data'},f'{x+176} {y+7} 12 12',f'Parameter {mode+5}',focus='No'))
 preview.append((x,y,'select'+str(mode),mode))
# Native UI animation continuously cycles even when audio processing is idle.
# Separate reverse strip; no animated parameter writes or cached host callbacks.
for side,cx in enumerate([174,363]):
 disk=art.crop((cx-46,184,cx+46,276)).convert('RGBA');mask=Image.new('L',(92,92));ImageDraw.Draw(mask).ellipse((2,2,89,89),fill=255);disk.putalpha(mask)
 for reverse in [0,1]:
  strip=Image.new('RGBA',(92,92*64))
  for frame in range(64):strip.alpha_composite(disk.rotate((1 if reverse else -1)*frame*360/64,resample=Image.Resampling.BICUBIC),(0,92*frame))
  asset=f'ui_reel_{side}_{reverse}.png';strip.save(D/asset)
  E.append(entry('UI clock reel','Image',{'version':2,'imageType':'FilmStrip','colour':'0','image':asset,'numFrames':64,'handleName':'Data','animated':True},f'{117+side*151} 351 74 74','Parameter 27',[f'IndexedEnabling/{reverse}/2/Parameter 8'],focus='No'))
# Clear, wide choices in the selected effect's settings bay.
options={0:(13,['1/2','1/4','3/4','9/10']),1:(14,['Boost','Amp','Drive']),3:(21,['1/8','1/4','1/2','1 bar']),4:(15,['Gentle','Wow','Flutter','Worn','Seasick','Unstable','Jungle']),5:(16,['Dust','Cassette','Narrow','8-bit','6-bit','4-bit','Broken','Telephone']),6:(17,['1/8 beat','1/2 beat','1 beat','2 beats']),7:(18,['1/2','1/4','1/8','1/16','1/32','1/64','1/8T','1/16T','1/4T'])}
positions={}
for mode,name in enumerate(names):
 inv=[f'IndexedEnabling/{mode}/8/Parameter 25']
 E.append(label(name,'916 98 324 28',23,'ffffd17e',invalid=inv))
 if mode==2:E.append(label('Mutes the wet signal','916 198 324 60',19,'ffeee5cb',invalid=inv))
 if mode in options:
  param,opts=options[mode]
  for j,caption in enumerate(opts):
   x=916+j%2*170;y=142+j//2*60;asset=f'option_{mode}_{j}';sprite(asset,154,50,caption,17)
   E.append(entry(name+' '+caption,'Button',g.button_data(asset+'_on.png',asset+'_off.png',j,len(opts)),f'{x} {y} 154 50',f'Parameter {param}',inv));positions.setdefault(mode,[]).append((x,y,asset,j))
 # Drive/depth are offered directly next to their relevant circuit.
 if mode in [1,4]:
  idx=19 if mode==1 else 20
  E.append(label('DRIVE' if mode==1 else 'DEPTH','916 398 324 24',17,'ffeee5cb',invalid=inv))
  E.append(entry('Selected circuit amount','faderUni',{'version':1,'handleName':'Data'},'916 420 324 62',f'Parameter {idx}',inv))
 sprite('engage',324,72,'ENGAGE',25)
 for hold in [0,1]:
  data=g.button_data('engage_on.png','engage_off.png',1,1)
  if not hold:n['put'](data,'gestureBehaviour','Hold')
  E.append(entry('Engage selected '+name,'Button',data,'916 516 324 72',f'Parameter {mode+5}' if hold else f'ResetOnGestureEnd/Parameter {mode+5}',inv+[f'IndexedEnabling/{hold}/2/Parameter 4']))
for y,idx in [(334,1),(452,2)]:
 E.append(entry('Master horizontal fader','Knob',{'version':3,'knobType':'FilmStrip','filmStrip':'deck_fader.png','numFrames':127,'invert':False,'dragOrientation':'Horizontal','handleName':'Data'},f'452 {y} 388 62',f'Parameter {idx}'))
 E.append(label('',f'578 {y+61} 136 26',16,'ffeee5cb',param=f'WithSuffix[%]/Parameter {idx}'))
E.append(entry('Output','Knob',{'version':3,'knobType':'FilmStrip','filmStrip':'deck_fader.png','numFrames':127,'invert':False,'dragOrientation':'Horizontal','handleName':'Data'},'32 554 192 58','Parameter 0'))
for name,idx,x,w in [('BYPASS',3,244,180),('LATCH',4,452,388)]:
 sprite(name.lower(),w,58,name,20)
 E.append(entry(name,'Button',g.button_data(name.lower()+'_on.png',name.lower()+'_off.png',1,1),f'{x} 554 {w} 58',f'Parameter {idx}'))
main=get(get(T,'pageData'),'tabs')[0];put(main,'componentDefinition',g.component_definition([],E,'ff202a23'));put(main,'qlinkBoundsData',['32 66 404 172','448 66 404 172','452 320 388 292','916 98 324 490'])
(D/'TUI.json').write_text(g.dump_json(T)+'\n')
# Actual asset review previews for each selected circuit.
for mode in range(8):
 im=bg.convert('RGBA')
 for x,y,asset,j in preview:im.alpha_composite(Image.open(D/f'{asset}_{"on" if j==mode else "off"}.png'),(x,y))
 for x,y,asset,j in positions.get(mode,[]):im.alpha_composite(Image.open(D/f'{asset}_{"on" if j==(2 if mode==6 else 3 if mode==7 else 0) else "off"}.png'),(x,y))
 a=ImageDraw.Draw(im);text(a,(1078,112),names[mode],23,'#ffd17e')
 im.alpha_composite(Image.open(D/'engage_off.png'),(916,516))
 for side in range(2):im.alpha_composite(Image.open(D/f'ui_reel_{side}_0.png').crop((0,0,92,92)).resize((74,74)),(117+side*151,351))
 for y,frame,txt in [(334,0,'0%'),(452,126,'100%')]:
  strip=Image.open(D/'deck_fader.png');im.alpha_composite(strip.crop((0,frame*78,307,(frame+1)*78)).resize((388,62)),(452,y));text(a,(646,y+74),txt,16)
 strip=Image.open(D/'deck_fader.png');im.alpha_composite(strip.crop((0,101*78,307,102*78)).resize((192,58)),(32,554))
 for name,x,w,on in [('bypass',244,180,0),('latch',452,388,1)]:im.alpha_composite(Image.open(D/f'{name}_{"on" if on else "off"}.png'),(x,554))
 im.convert('RGB').save(P/'Previews'/f'{mode+1}-{n["names"][mode].lower()}.png')
 if mode==0:im.convert('RGB').save(P/'UI-preview.png')
print('Spacious effect selector, contextual settings and native UI-clock reels generated.')

contact=Image.new('RGB',(1280,1360),'#10170f')
for mode in range(8):
 im=Image.open(P/'Previews'/f'{mode+1}-{n["names"][mode].lower()}.png');im.thumbnail((636,312));contact.paste(im,(mode%2*640+2,mode//2*340+25))
contact.save(P/'All-eight-modes.png')
