"""Render an illustrative GIF from the real reel and cassette assets (not an MPC capture)."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math
P=Path(__file__).resolve().parent;D=P/'skins'
base=Image.open(D/'cassette-0.png').convert('RGBA');strips={i:Image.open(D/f'reel_native_{i}_0.png') for i in [1,0,2,3]}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',18)
frames=[]
for tick in range(100):
 panel=Image.new('RGB',(800,560),'#172125');d=ImageDraw.Draw(panel)
 for j,(idx,name) in enumerate([(1,'1/4 SPEED'),(0,'1/2 SPEED'),(2,'3/4 SPEED'),(3,'9/10 SPEED')]):
  tape=base.copy();frame=(tick*4)%400
  reel=strips[idx].crop((0,frame*56,56,(frame+1)*56))
  for x in [104,293]:tape.alpha_composite(reel,(x,103))
  tape=tape.resize((396,254),Image.Resampling.LANCZOS);x=j%2*400;y=j//2*280
  panel.paste(tape,(x+2,y+25));d.text((x+200,y+12),name,font=font,fill='#daf4f6',anchor='mm')
 frames.append(panel)
frames[0].save(P/'Speed-reels-preview.gif',save_all=True,append_images=frames[1:],duration=133,loop=0,optimize=True)
