"""Build assets and compile until references stabilise; no latexmk/Perl required."""
from pathlib import Path
import argparse
import hashlib
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def run_script(name):
    subprocess.run([sys.executable,str(ROOT/'scripts'/name)],cwd=ROOT,check=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--skip-figures',action='store_true',help='Use already generated vector figures')
    args=parser.parse_args()
    (ROOT/'build').mkdir(exist_ok=True);(ROOT/'output').mkdir(exist_ok=True)
    run_script('generate_appendices.py')
    if not args.skip_figures:run_script('draw_figures.py')
    run_script('verify_math.py')
    engine=shutil.which('xelatex')
    if not engine:raise SystemExit('XeLaTeX not found. Install MiKTeX/TeX Live and add it to PATH.')
    previous=None;stable=False
    for i in range(1,7):
        cmd=[engine,'-interaction=nonstopmode','-halt-on-error','-file-line-error','-no-shell-escape','-output-directory=build','main.tex']
        process=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        log=process.stdout.decode('utf-8',errors='replace')
        (ROOT/'build'/f'pass-{i}.txt').write_text(log,encoding='utf-8')
        if process.returncode:
            print(log[-10000:]);raise SystemExit(f'XeLaTeX pass {i} failed; see build/pass-{i}.txt')
        state=hashlib.sha256(b''.join((ROOT/'build'/f'main.{ext}').read_bytes() if (ROOT/'build'/f'main.{ext}').exists() else b'' for ext in ['aux','toc','out'])).hexdigest()
        print(f'XeLaTeX pass {i} completed')
        if i>=3 and state==previous:stable=True;break
        previous=state
    if not stable:raise SystemExit('References did not stabilise after six passes.')
    texlog=(ROOT/'build'/'main.log').read_text(encoding='utf-8',errors='replace')
    if 'Missing character:' in texlog or 'There were undefined references' in texlog:
        raise SystemExit('Missing glyphs or undefined references remain. Inspect build/main.log.')
    dst=ROOT/'Econometrics中文版笔记.pdf'
    shutil.copy2(ROOT/'build'/'main.pdf',dst)
    run_script('verify_delivery.py')
    run_script('verify_translation.py')
    print('BUILT:',dst)

if __name__=='__main__':main()
