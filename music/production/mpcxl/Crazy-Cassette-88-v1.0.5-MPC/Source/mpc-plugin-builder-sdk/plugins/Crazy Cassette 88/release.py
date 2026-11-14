from pathlib import Path
import zipfile,subprocess,json,hashlib
p=Path(__file__).resolve().parent;sdk=p.parents[1];root=sdk.parent
(root/'output').mkdir(exist_ok=True)
subprocess.run([__import__('sys').executable,str(sdk/'tools/package.py'),str(p)],check=True)
version=json.loads((p/'plugin.json').read_text())['version']
out=root/f'output/Crazy-Cassette-88-v{version}-MPC.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 with zipfile.ZipFile(p/f'dist/crazy-cassette-88-{version}-mpc.zip') as base:
  for f in base.infolist():z.writestr(f,base.read(f.filename))
 z.write(p/'LICENSE-SDK.txt','LICENSE-SDK.txt')
 z.write(p/'UI-preview.png','UI-preview.png')
 z.write(p/'All-eight-modes.png','All-eight-modes.png')
 z.write(p/'REFERENCE-ALIGNMENT.md','REFERENCE-ALIGNMENT.md')
 z.write(p/'SPEED-TEST.txt','SPEED-TEST.txt')
 z.write(p/'Speed-reels-preview.gif','Speed-reels-preview.gif')
 for image in (p/'Previews').glob('*.png'):z.write(image,'Previews/'+image.name)
 for name in ['build-results.txt','host-test-results.txt','host-48k-results.txt','sanitizer-results.txt','spectral-results.txt','feature-test-results.txt','ui-audit-results.txt','speed-fix-results.txt','reel-test-results.txt','native-animation-results.txt','ui-refresh-results.txt','ui-refresh-sanitizer-results.txt']:
  z.write(p/'build'/name,'Verification/'+name)
 z.write(p/'build/release-status.txt',f'Verification/v{version}-STATUS.txt')
 z.write(p/'build/test.wav','Verification/host-test-signal.wav')
 z.writestr('Verification/PRIOR-v1.0.1-STATUS.txt','Compiled ARM32 and ARM64 with official inMusic SDK at febd2ca5bd9eb16c4a412837196e145566bc981b.\nSDK validation: 0 errors, 0 warnings.\nNative host-sim: 20 passes at 44.1k/128 and 20 passes at 48k/32.\nDirect ASan/UBSan tests: PASS; leak checking disabled because tracing prevents LeakSanitizer here.\n44.1/48/96k, blocks 32/127/128/511/512, each effect and stack, parameter extremes, stereo in-place, dry/bypass, mute and stop checks.\nFour varispeed spectral checks: PASS within 10 Hz granular tolerance.\n36 documented settings verified to affect audio. Eight view selectors and all setting/enable/LED/global bindings audited. Legacy 25 parameter IDs and old state restoration checked. No physical MPC tested. UI touch feel and MPC CPU performance are unverified.\n')
 tracked=subprocess.check_output(['git','-C',str(sdk),'ls-files','-z']).decode().split('\0')
 for f in tracked:
  if f and (sdk/f).is_file():z.write(sdk/f,'Source/mpc-plugin-builder-sdk/'+f)
 for f in p.rglob('*'):
  rel=f.relative_to(p)
  if f.is_file() and not any(x in {'build','dist','__pycache__'} for x in rel.parts):z.write(f,'Source/mpc-plugin-builder-sdk/plugins/Crazy Cassette 88/'+str(rel))
 # Hash every deliverable and source file so the extracted bundle can be verified.
 entries=[(x.filename,hashlib.sha256(z.read(x.filename)).hexdigest()) for x in z.infolist()]
 z.writestr('SHA256SUMS.txt',''.join(d+'  '+n+'\n' for n,d in entries))
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 names=z.namelist();assert len(names)==len(set(names))
 assert len([n for n in names if n.endswith('VST/crazy-cassette-88-arm64.so')])==1
 for line in z.read('SHA256SUMS.txt').decode().splitlines():
  digest,name=line.split('  ',1);assert hashlib.sha256(z.read(name)).hexdigest()==digest
 print(f'Verified {len(names)} archive members; {out.stat().st_size:,} bytes')
 print(out)
