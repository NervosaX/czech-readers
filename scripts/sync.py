#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["simplemma"]
# ///
"""One-shot LingQ sync: apply a delta, rebuild vocab, update ledger, commit, summarise.

Usage:  python3 scripts/sync.py < /tmp/delta.txt      (or: python3 scripts/sync.py delta.txt)
        add --no-commit to skip git.
The delta string comes from the JS printed by scripts/make_sync_js.py.
"""
import json, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
raw = open(args[0], encoding='utf8').read() if args else sys.stdin.read()
raw = raw.strip().strip('"').replace('\\n', '\n')
if raw.startswith('LONG'): sys.exit('Output was long - read window._syncOut in slices into the file.')
if raw.startswith('NOBASE'):
    sys.exit('Browser baseline missing - see make_sync_js.py docstring.')
tmp = tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, encoding='utf8'); tmp.write(raw); tmp.close()
run = lambda *c: subprocess.run(c, cwd=ROOT, check=True, capture_output=True, text=True).stdout
run(sys.executable, 'scripts/apply_delta.py', tmp.name)
run(sys.executable, 'scripts/build_vocab.py', 'data/lingq/known_words.json', 'data/lingq/cards.json')
run(sys.executable, 'scripts/update_ledger.py')

sec = {}
for line in raw.splitlines():
    k, _, v = line.partition(' '); sec[k] = [x for x in v.strip().split(',') if x]
skip = set(json.load(open(os.path.join(ROOT, 'ledger.json'), encoding='utf8')).get('ignore_tokens', []))
lookups = [x.rpartition('=')[0] for x in sec.get('N', [])]
lookups = [w for w in lookups if w.lower() not in {s.lower() for s in skip}]
print('Newly known: ', ', '.join(sec.get('K+', [])) or '-')
print('Un-known\'d:  ', ', '.join(sec.get('K-', [])) or '-')
print('Looked up:   ', ', '.join(lookups) or '-')
print('Still sticky in read lessons:', ', '.join(x.rpartition('=')[0] for x in sec.get('U', []) if not x.endswith('=-1')) or '-')
print('Reading:     ', ', '.join(r for r in sec.get('R', []) if float(r.split(':')[1]) > 0) or '-')
if '--no-commit' not in sys.argv:
    run('git', 'add', '-A')
    msg = f"LingQ sync {sec.get('T', ['?'])[0][:10]}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
    r = subprocess.run(['git', '-c', 'user.name=NervosaX', '-c', 'user.email=the.nervosax@gmail.com',
                        'commit', '-q', '-m', msg], cwd=ROOT, capture_output=True, text=True)
    if r.returncode == 0:
        subprocess.run(['git', 'push', '-q', 'origin', 'main'], cwd=ROOT, capture_output=True)
        print('Committed and pushed.')
