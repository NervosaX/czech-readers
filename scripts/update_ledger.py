"""Rebuild word-exposure counts in ledger.json from every episode file.

Usage: python3 scripts/update_ledger.py
For each lemma that is NOT core in LingQ: first episode it appeared in, total uses,
and uses in each of the last 5 episodes. Words with low recent exposure that are
still status 1-2 in LingQ are flagged 'needs_review' for the next batch.
"""
import json, re, os, glob, collections
import simplemma

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = json.load(open(os.path.join(ROOT, 'data/vocab.json'), encoding='utf8'))['vocab']
lp = os.path.join(ROOT, 'ledger.json')
ledger = json.load(open(lp, encoding='utf8'))
IGN = {w.lower() for w in ledger.get('ignore_tokens', [])}

eps = sorted(glob.glob(os.path.join(ROOT, 'episodes', '*.txt')))
words = {}
per_ep = []
for p in eps:
    eid = os.path.basename(p)[:3]
    c = collections.Counter()
    for t in re.findall(r"[^\W\d_]+", open(p, encoding='utf8').read()):
        if t.lower() in IGN: continue
        c[simplemma.lemmatize(t.lower(), lang='cs')] += 1
    per_ep.append((eid, c))
    for l, n in c.items():
        if V.get(l, {}).get('tier') == 'core': continue
        d = words.setdefault(l, {'first_episode': eid, 'total_uses': 0})
        d['total_uses'] += n

recent = per_ep[-5:]
for l, d in words.items():
    d['recent_uses'] = sum(c.get(l, 0) for _, c in recent)
    d['lingq_status'] = V.get(l, {}).get('status', 'unknown')
    d['needs_review'] = d['lingq_status'] in ('new1', 'unknown') and d['total_uses'] < 12

ledger['words'] = dict(sorted(words.items(), key=lambda kv: (kv[1]['first_episode'], kv[0])))
ledger['episodes'] = [os.path.basename(p) for p in eps]
json.dump(ledger, open(lp, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(f'{len(eps)} episodes, {len(words)} tracked words, '
      f'{sum(d["needs_review"] for d in words.values())} need review')
