"""List the next high-frequency target words for upcoming readers.

Usage: python3 scripts/targets.py [N=60] [MAX_RANK=2000]
Prints top-frequency lemmas that are not yet core for Adam, in frequency order, marked:
  T = already introduced by the course (needs more reps)   L = looked up / still unknown in a read lesson
  h = LingQ status 3 (half-known)   s = seen once in LingQ   . = never seen
Pick most of each reader's new words from the top of this list, then write a story
that needs them. Skip-list (swearing, filler, lemmatizer noise) is ledger.target_skip.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = json.load(open(os.path.join(ROOT, 'data/vocab.json'), encoding='utf8'))
L = json.load(open(os.path.join(ROOT, 'ledger.json'), encoding='utf8'))
n = int(sys.argv[1]) if len(sys.argv) > 1 else 60
max_rank = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
skip = set(L.get('target_skip', []))
taught = L.get('words', {})
looked = set(L.get('lingq', {}).get('looked_up_last_sync', [])) | set(L.get('lingq', {}).get('sticky_in_read_lessons', []))
out = []
for lem, r in sorted(V['rank'].items(), key=lambda kv: kv[1]):
    if r > max_rank or lem in skip: continue
    tier = V['vocab'].get(lem, {}).get('tier', 'new')
    if tier == 'core': continue
    mark = 'L' if lem in looked else 'T' if lem in taught else {'half': 'h', 'seen': 's'}.get(tier, '.')
    out.append(f"{lem}({r}{mark})")
    if len(out) >= n: break
print(' '.join(out))
