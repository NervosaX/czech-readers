"""Apply a LingQ delta (from make_sync_js.py) to data/lingq/*.json and ledger.json.

Usage: python3 scripts/apply_delta.py /tmp/delta.txt
Then rebuild: python3 scripts/build_vocab.py data/lingq/known_words.json data/lingq/cards.json
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kp_ = os.path.join(ROOT, 'data/lingq/known_words.json'); cp_ = os.path.join(ROOT, 'data/lingq/cards.json')
lp = os.path.join(ROOT, 'ledger.json')
sec = {}
for line in open(sys.argv[1], encoding='utf8').read().splitlines():
    k, _, v = line.partition(' '); sec[k] = v.strip()
split = lambda s: [x for x in s.split(',') if x]
known = json.load(open(kp_, encoding='utf8'))
have = {w['word'] for w in known}
km = set(split(sec.get('K-', '')))
known = [w for w in known if w['word'] not in km] + [{'word': w, 'language': 'cs'} for w in split(sec.get('K+', '')) if w not in have]
json.dump(known, open(kp_, 'w', encoding='utf8'), ensure_ascii=False)
cards = json.load(open(cp_, encoding='utf8'))
idx = {c['term']: c for c in cards}
looked_up = []
for key in ('C', 'N'):
    for item in split(sec.get(key, '')):
        term, _, st = item.rpartition('=')
        if term in idx: idx[term]['status'] = int(st)
        else:
            c = {'term': term, 'status': int(st), 'extended_status': None, 'hint': ''}; cards.append(c); idx[term] = c
        if key == 'N': looked_up.append(term)
json.dump(cards, open(cp_, 'w', encoding='utf8'), ensure_ascii=False)
L = json.load(open(lp, encoding='utf8'))
L['lingq']['max_card_pk'] = int(sec['M']); L['lingq']['last_sync_utc'] = sec['T']; L['lingq']['last_sync'] = sec['T'][:10]
L['lingq']['looked_up_last_sync'] = looked_up
json.dump(L, open(lp, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(f"known +{len(split(sec.get('K+','')))} -{len(km)}; cards changed {len(split(sec.get('C','')))}; "
      f"new lookups {len(looked_up)}: {', '.join(looked_up[:40])}")
