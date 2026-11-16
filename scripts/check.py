"""Check an episode's vocabulary against Adam's LingQ data and the course ledger.

Usage: python3 scripts/check.py "episodes/s01/004 - ....txt"

Tiers:
  core    known/status-4+ in LingQ AND in top ~1500 lemmas
  taught  introduced in an earlier episode of this course (from ledger.json)
  half    LingQ status 3, or known but rarer
  new     everything else (incl. LingQ status 1-2: "seen once" = new)
Target per episode: <=6-8 new lemmas, each used 3+ times; core+taught+half >= ~90% of tokens.
"""
import json, re, sys, collections, os
import simplemma

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = json.load(open(os.path.join(ROOT, 'data/vocab.json'), encoding='utf8'))['vocab']
ledger = json.load(open(os.path.join(ROOT, 'ledger.json'), encoding='utf8'))
IGN = {w.lower() for w in ledger.get('ignore_tokens', [])}

path = sys.argv[1]
ep_id = os.path.basename(os.path.dirname(os.path.abspath(path))) + '/' + os.path.basename(path)[:3]  # e.g. s01/004
taught = {l for l, d in ledger['words'].items() if d['first_episode'] < ep_id}

txt = open(path, encoding='utf8').read()
c = collections.Counter(); forms = collections.defaultdict(set)
for t in re.findall(r"[^\W\d_]+", txt):
    if t.lower() in IGN:
        continue
    l = simplemma.lemmatize(t.lower(), lang='cs'); c[l] += 1; forms[l].add(t.lower())

def tier(l):
    t = V.get(l, {}).get('tier', 'new')
    if t == 'core': return 'core'
    if l in taught: return 'taught'
    if t == 'half': return 'half'
    return 'new'

groups = collections.defaultdict(list)
for l, n in c.items(): groups[tier(l)].append((l, n))
tot = sum(c.values())
print('tokens', tot)
for t in ('core', 'taught', 'half', 'new'):
    n = sum(x for _, x in groups[t])
    print(f'{t:6}: {len(groups[t]):3} lemmas, {n:4} tokens ({100*n/tot:.1f}%)')
RANK = json.load(open(os.path.join(ROOT, 'data/vocab.json'), encoding='utf8'))['rank']
rk = lambda l: RANK.get(l, 99999)
for t in ('taught', 'half', 'new'):
    print(t.upper(), sorted([(l, n, rk(l)) for l, n in groups[t]], key=lambda x: -x[1]))
fresh = [l for l, _ in groups['new'] + groups['half']]
print(f"FREQUENCY: new/half lemmas in top 2000: {sum(rk(l) <= 2000 for l in fresh)}/{len(fresh)}; "
      f"story-specific (rank >3000): {[l for l in fresh if rk(l) > 3000]}")
