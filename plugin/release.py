"""Package the current build, source, previews and verification without other plugins."""
from pathlib import Path
import subprocess, sys, json, zipfile, hashlib
p=Path(__file__).resolve().parent
sdk=p.parents[1]
version=json.loads((p/'plugin.json').read_text())['version']
subprocess.run([sys.executable,str(sdk/'tools/package.py'),str(p)],check=True)
out=p/'dist'/f'Vintage-Military-Radio-{version}-source-and-both-architectures.zip'
folder=p/'build'/'Tropix R!X Crazy Jungle Sounds - VST - Vintage Military Radio'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for f in folder.rglob('*'):
  if f.is_file():z.write(f,folder.name+'/'+str(f.relative_to(folder)))
 for f in p.rglob('*'):
  if f.is_file() and not any(a in {'build','dist','__pycache__'} for a in f.relative_to(p).parts):z.write(f,'Source/mpc-plugin-builder-sdk/plugins/Vintage Military Radio/'+str(f.relative_to(p)))
 for root in ['framework','tools','docs','schemas','ui-kit']:
  for f in (sdk/root).rglob('*'):
   if f.is_file() and '__pycache__' not in f.parts:z.write(f,'Source/mpc-plugin-builder-sdk/'+str(f.relative_to(sdk)))
 for f in (p/'build/verification').glob('*'):
  if f.is_file():z.write(f,'Verification/'+f.name)
 for name in ['README.md','revisions.txt']:z.write(p/name,name)
 entries=[(i.filename,hashlib.sha256(z.read(i.filename)).hexdigest()) for i in z.infolist()]
 z.writestr('SHA256SUMS.txt',''.join(h+'  '+n+'\n' for n,h in entries))
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(set(z.namelist()))
print(out)
