import json, simplemma, collections, sys
L=lambda w: simplemma.lemmatize(w.lower(),lang='cs')
known=[w['word'].lower() for w in json.load(open(sys.argv[1]))]
cards=json.load(open(sys.argv[2]))
lemcount=collections.Counter()
for l in open('data/cs_50k.txt',encoding='utf8'):
    w,c=l.split(); lemcount[L(w)]+=int(c)
rank={l:i+1 for i,(l,_) in enumerate(lemcount.most_common())}
V={}  # lemma -> status
def put(lem,st):
    order=['new1','familiar','learned','known']
    if lem not in V or order.index(st)>order.index(V[lem]): V[lem]=st
for w in known: put(L(w),'known')
for c in cards:
    if ' ' in c['term']: continue
    st={0:'new1',1:'new1',2:'familiar',3:'learned'}[c['status']]
    put(L(c['term']),st)
def tier(lem):
    st=V.get(lem); r=rank.get(lem,10**6)
    if st in('known','learned') and r<=1500: return 'core'
    if st in('known','learned','familiar'): return 'half'
    if st=='new1': return 'seen'
    return 'new'
out={l:{'status':s,'rank':rank.get(l),'tier':tier(l)} for l,s in V.items()}
json.dump({'vocab':out,'rank':{l:r for l,r in rank.items() if r<=8000}},open('data/vocab.json','w'),ensure_ascii=False)
print(collections.Counter(v['tier'] for v in out.values()))
top=[l for l,_ in lemcount.most_common(1000)]
print('top1000 tiers',collections.Counter(tier(l) for l in top))
