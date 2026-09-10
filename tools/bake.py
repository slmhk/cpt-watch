#!/usr/bin/env python3
"""Validate data/snapshot.json and bake it into index.html (run from the repo root: python3 tools/bake.py)."""
import json, re, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
snap = os.path.join(ROOT, 'data', 'snapshot.json')
d = json.load(open(snap, encoding='utf-8'))
errs = []
if [t['key'] for t in d.get('tiers', [])] != ['cancels','honored','unstated','acknowledged','leads','clear','unresolved']:
    errs.append('tiers must be exactly cancels/honored/unstated/acknowledged/leads/clear/unresolved in that order')
names = [s['name'] for t in d.get('tiers', []) for s in t.get('schools', [])]
dups = sorted({n for n in names if names.count(n) > 1})
if dups: errs.append('duplicate school names: ' + ', '.join(dups))
unc = set(d.get('unchecked', {}).get('lac', [])) | set(d.get('unchecked', {}).get('national', []))
both = sorted(set(names) & unc)
if both: errs.append('both tiered and unchecked: ' + ', '.join(both))
if len(d.get('tripwires', [])) != 4: errs.append('exactly 4 tripwires required')
clear = [t for t in d.get('tiers', []) if t['key'] == 'clear']
if not clear or not clear[0]['schools'] or clear[0]['schools'][-1]['name'] != 'Claremont McKenna':
    errs.append('Claremont McKenna must be the last entry of the clear tier')
if re.search(r'(?i)highest.priority', json.dumps(d, ensure_ascii=False)): errs.append('remove "highest priority" wording')
if not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', d.get('updatedAt', '')): errs.append('updatedAt must be ISO UTC like 2026-09-11T00:12:00Z')
for r in d.get('runs', []):
    if not re.match(r'^\d{4}-\d{2}-\d{2}( \d{2}:\d{2} UTC)?$', r.get('date', '')) and ' to ' not in r.get('date',''):
        errs.append('run date must look like "2026-09-11 00:12 UTC": ' + r.get('date',''))
if len(d.get('runs', [])) > 10: errs.append('keep at most 10 runs (newest first)')
if errs:
    print('SNAPSHOT INVALID:\n - ' + '\n - '.join(errs)); sys.exit(1)
blob = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
tpl = open(os.path.join(ROOT, 'cpt-watch.template.html'), encoding='utf-8').read()
assert tpl.count('__SNAPSHOT__') == 1
page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n</head>\n<body>\n'
        + tpl.replace('__SNAPSHOT__', blob) + '\n</body>\n</html>\n')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page)
hist = os.path.join(ROOT, 'data', 'history', d['updatedAt'].replace(':', '') + '.json')
if not os.path.exists(hist): json.dump(d, open(hist, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('OK: baked index.html — updatedAt', d['updatedAt'], '| tiered', len(names), '| unchecked', len(unc), '| runs', len(d['runs']))
