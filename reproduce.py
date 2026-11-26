"""Entry points for model evaluation, personalization, figures, and ANOVA."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
TABLES=ROOT/'main_pvrnn/data/processed_epp_v6_20261020_131548_599411'
MAINRUN=ROOT/'main_pvrnn/results/epp_v6/20261020T142629_112453Z'
FORMAL=ROOT/'personalization/results/formal_20261028_180424_097163'
SIMULATION=ROOT/'personalization/results/formal_fourphase_20261125'

def need(*paths):
    missing=[str(p.relative_to(ROOT)) for p in paths if not p.exists()]
    if missing:
        raise SystemExit('Companion files are required: '+', '.join(missing)+
            '\nMerge the matching reproduction companion into this repository; see docs/RUN_GUIDE_zh.md.')

def run(args,cwd=ROOT):
    env=os.environ.copy()
    env.update(MPLBACKEND='Agg',PYTHONIOENCODING='utf-8',MKL_THREADING_LAYER='SEQUENTIAL')
    env.pop('KMP_DUPLICATE_LIB_OK',None)
    print('RUN:', ' '.join(map(str,args)),flush=True)
    subprocess.run([sys.executable,*map(str,args)],cwd=cwd,env=env,check=True)

def verify():
    for name in ['provenance/scientific_source_checks.json','SHA256SUMS.json']:
        manifest=json.loads((ROOT/name).read_text())
        entries=manifest if isinstance(manifest,list) else [dict(path=k,expected_sha256=v) for k,v in manifest.items()]
        for row in entries:
            p=ROOT/row['path']
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['expected_sha256']:
                raise SystemExit('File differs/missing: '+row['path'])
    print('PASS: release files and scientific source hashes.')
    private=ROOT/'COMPANION_SHA256SUMS.json'
    if private.is_file():
        entries=json.loads(private.read_text())
        for name,h in entries.items():
            p=ROOT/name
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:
                raise SystemExit('Companion file differs/missing: '+name)
        print(f'PASS: {len(entries)} companion files.')
    else:
        print('Code-only snapshot: research inputs and individual outputs are in the separate companion.')

def statistics():
    need(MAINRUN,FORMAL,SIMULATION,ROOT/'personalization/data/minutes.csv')
    out=ROOT/'reproduced/statistics'
    run(['analysis/audit_main_and_scope.py','--repro-root',ROOT,'--formal-run',FORMAL,'--out',out/'main'])
    run(['analysis/audit_personalization_fourphase.py','--simulation-run',SIMULATION,'--validation-run',FORMAL,
         '--source',ROOT/'personalization','--output',out/'personalization'])
    run(['analysis/audit_personalization_offsets_and_contrasts.py','--run',FORMAL,
         '--simulation-run',SIMULATION,'--output',out/'offsets'])
    run(['analysis/check_offset_correspondence.py','--stage-pairs',out/'offsets/training_vs_recalibrated_A.csv',
         '--training22',out/'offsets/training_offsets_22_participants.csv','--output',out/'correspondence'])
    run(['supplementary/anova/run_anova.py','--output',out/'anova'])

def figure_data():
    need(MAINRUN,TABLES,SIMULATION/'simulation/trajectories_seed_mean.csv')
    run(['figures/main/prepare_data.py','--output',ROOT/'figures/main/data'])
    target=ROOT/'figures/common_environment/data';target.mkdir(parents=True,exist_ok=True)
    for src,dst in [(SIMULATION/'simulation/trajectories_seed_mean.csv','simulation_trajectories_seed_mean.csv'),
                    (SIMULATION/'protocol/scenarios.csv','simulation_scenarios.csv')]:
        shutil.copyfile(src,target/dst)
    print('Prepared Figure 5 and four-phase Figure 6 tables.')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['verify','statistics','figure-data','figures','check-inputs','train-main',
        'personalization-check','personalization-simulate','personalization-all','personalization-retrain','anova','tests'])
    a=p.parse_args()
    if a.command=='verify':return verify()
    if a.command=='statistics':return statistics()
    if a.command=='figure-data':return figure_data()
    if a.command=='anova':
        return run(['supplementary/anova/run_anova.py','--output',ROOT/'reproduced/statistics/anova'])
    if a.command=='figures':
        need(ROOT/'figures/main/data/LOO_seed_metrics.csv',ROOT/'figures/common_environment/data/simulation_trajectories_seed_mean.csv')
        run(['figures/main/plot_main.py']);run(['figures/common_environment/plot_figure6.py']);return
    if a.command in ['check-inputs','train-main']:
        need(TABLES)
        stage='check' if a.command=='check-inputs' else 'behavior'
        return run([ROOT/'main_pvrnn/run_epp_v6.py','--table-dir',TABLES,'--config',ROOT/'main_pvrnn/config/epp_v6.json',
            '--stage',stage,'--cohorts','11' if stage=='behavior' else '22,11','--output-dir',ROOT/'reproduced/main_training'])
    if a.command.startswith('personalization-'):
        need(ROOT/'personalization/data/minutes.csv')
        args=[ROOT/'personalization/run_project.py']
        if a.command=='personalization-check': args+=['--check-only']
        else:
            args+=['--mode','formal','--phase','simulate' if a.command=='personalization-simulate' else 'all']
            if a.command=='personalization-retrain':args+=['--force-train']
        return run(args,cwd=ROOT/'personalization')
    if a.command=='tests':
        run(['-m','unittest','discover','-s','tests','-p','test_epp_v6.py'],cwd=ROOT/'main_pvrnn')
        run(['-m','unittest','discover','-s','tests','-p','test_epp_timefix.py'],cwd=ROOT/'main_pvrnn')
        need(ROOT/'personalization/data/minutes.csv',ROOT/'personalization/bundled/manifest.json')
        return run(['-m','unittest','test_mechanism'],cwd=ROOT/'personalization')

if __name__=='__main__':main()
