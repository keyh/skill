from pathlib import Path
import subprocess, tempfile, json, sys, importlib.util, hashlib
ROOT=Path(__file__).resolve().parents[1]
results=[]
def run(args,expected=0):
 p=subprocess.run([sys.executable,str(ROOT/'scripts/install.py')]+args,text=True,capture_output=True)
 if (expected==0 and p.returncode!=0) or (expected!=0 and p.returncode==0):raise AssertionError(p.stdout+'\n'+p.stderr)
 return p
with tempfile.TemporaryDirectory(prefix='skill-installer-check-') as d:
 t=Path(d);dest=t/'skills'
 run(['--skill','ui-interaction-brief','--dest',str(dest),'--dry-run']);assert not dest.exists();results.append('dry-run writes nothing')
 run(['--skill','ui-interaction-brief','--dest',str(dest)]);assert (dest/'ui-interaction-brief/SKILL.md').is_file();results.append('standalone skill installs')
 digest=hashlib.sha256((dest/'ui-interaction-brief/SKILL.md').read_bytes()).hexdigest()
 run(['--skill','ui-interaction-brief','--dest',str(dest)],1);assert hashlib.sha256((dest/'ui-interaction-brief/SKILL.md').read_bytes()).hexdigest()==digest;results.append('existing destination is not overwritten')
 run(['--skill','design--design-critique','--dest',str(dest)]);assert (dest/'design-critique').is_symlink();assert (dest/'design-critique/../../CONNECTORS.md').is_file();results.append('plugin shared parent references resolve')
 run(['--skill','design--design-handoff','--dest',str(dest)]);assert (dest/'design-handoff/SKILL.md').is_file();results.append('identical plugin bundle is reused')
 run(['--skill','build-web-data-visualization--d3-data-visualization','--dest',str(dest)]);assert (dest/'d3-data-visualization/../../references/foundations/perception-color-and-encoding.md').is_file();results.append('shared visualization references resolve')
 run(['--skill','documents--documents','--dest',str(dest)],1);assert not (dest/'documents').exists();results.append('catalog-only entry refuses installation')
 run(['--skill','image-to-code','product-design--image-to-code','--dest',str(dest)],1);assert not (dest/'image-to-code').exists();results.append('colliding original names rejected')
 run(['--preset','writing','--dest',str(t/'writing'),'--dry-run']);assert not (t/'writing').exists();results.append('preset selection and dry-run work')
 run(['--skill','missing-skill','--dest',str(dest)],1);results.append('unknown identifiers rejected')
 run(['--skill','ppt-master','--dest',str(ROOT/'accidental-install')],1);assert not (ROOT/'accidental-install').exists();results.append('source repository cannot be used as destination')
 (dest/'.skill-bundles/design/CONNECTORS.md').write_text('locally changed')
 run(['--skill','design--design-system','--dest',str(dest)],1);assert not (dest/'design-system').exists();results.append('modified existing bundle rejected')
 spec=importlib.util.spec_from_file_location('check',ROOT/'scripts/verify.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 fixture=t/'corrupt';(fixture/'catalog').mkdir(parents=True);(fixture/'demo.txt').write_text('changed');(fixture/'catalog/files.sha256.json').write_text(json.dumps({'files':{'demo.txt':'0'*64}}));(fixture/'catalog/skills.json').write_text(json.dumps({'skills':[],'count':0}))
 try:module.verify(fixture)
 except RuntimeError:results.append('checksum corruption rejected')
 else:raise AssertionError('corruption accepted')
report={'status':'PASS','test_count':len(results),'checks':results,'environment':'macOS / Python 3.9.6','scope':'File installation and integrity checks only; no skill business operations executed.'}
print(json.dumps(report,ensure_ascii=False,indent=2))
