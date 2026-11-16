"""Generate the JS for a fast LingQ sync (Claude in Chrome), ~2-5 s, one call.

  python3 scripts/make_sync_js.py > /tmp/sync.js
  -> paste into javascript_tool on any lingq.com tab; it returns the delta string.
     If it is longer than ~1500 chars it is also kept in window._syncOut - read slices.
  -> save it to /tmp/delta.txt and run:  python3 scripts/sync.py /tmp/delta.txt
  -> then run  window._syncCommit()  in the tab (moves the known-words baseline on).

What it fetches (all in parallel, nothing proportional to Adam's 19k cards):
  * /api/languages/cs/known-words/         -> diff vs browser baseline (localStorage
    'czr_known_baseline'; LingQ's list has no dates/order). Missing -> 'NOBASE {letter counts}'.
  * /api/v2/cs/cards/?sort=date            -> newest cards first; pages until pk <= last
    max pk = words Adam looked up since last sync (usually 1 page).
  * per course lesson: /api/v3/cs/lessons/<id>/words/ (status of every word in it) and
    /api/v2/cs/lesson-stats/<id>/ (readTimes, lingqsCreated).

Delta format (one line per section):
  K+ / K-  word,...            newly known / no longer known forms
  N  term=status,...           new cards since last sync (= lookups)
  U  term=status,...           words in lessons Adam has READ that are still not known
                               (API status 0-2 = LingQ 1-3) -> the sticky words
  R  NNN:readTimes:lingqs,...  per-lesson reading record for the course
  M  <max card pk>   T <UTC timestamp>
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(ROOT, 'ledger.json'), encoding='utf8'))['lingq']
max_pk = L.get('max_card_pk', 0)
courses = list(L.get('courses', {}).values())
print(f"""(async()=>{{
const MAXPK={max_pk}, COURSES={json.dumps(courses)};
const get=u=>fetch(u,{{credentials:'include'}}).then(r=>r.json());
const kw=(await get('/api/languages/cs/known-words/')).map(x=>x.word);
const base=localStorage.getItem('czr_known_baseline');
if(!base){{const b={{}};for(const w of kw)b[w[0]]=(b[w[0]]||0)+1; return 'NOBASE '+JSON.stringify(b);}}
const PREV=new Set(JSON.parse(base)), NOW=new Set(kw);
const kp=kw.filter(w=>!PREV.has(w)), km=[...PREV].filter(w=>!NOW.has(w));
let nw=[], mx=MAXPK, page=1, more=true;
while(more && page<10){{const d=await get('/api/v2/cs/cards/?page_size=200&sort=date&page='+page);
  for(const c of d.results){{ if(c.pk>mx) mx=c.pk; if(c.pk>MAXPK) nw.push(c.term+'='+c.status); else more=false; }}
  if(!d.next) more=false; page++;}}
const lessons=[]; for(const col of COURSES){{const d=await get('/api/v3/cs/collections/'+col+'/lessons/'); lessons.push(...(d.results||d));}}
const data=await Promise.all(lessons.map(l=>Promise.all([get('/api/v3/cs/lessons/'+l.id+'/words/'),get('/api/v2/cs/lesson-stats/'+l.id+'/')]).then(([w,s])=>({{l,w,s}}))));
const U=new Map(), R=[];
for(const {{l,w,s}} of data){{ const rt=Math.round((s.readTimes||0)*10)/10, read=rt>=0.5;
  R.push(l.title.slice(0,3)+':'+rt+':'+(s.lingqsCreated||0));
  if(!read) continue;
  for(const x of Object.values(w.words||{{}})){{ if(x.status==='card'){{const c=w.cards[x.cardId]; if(c && c.status<3) U.set(c.term,c.status);}}
    else if(x.status==='new') U.set(x.text,-1); }} }}
const T=new Date().toISOString().slice(0,19);
window._syncCommit=()=>{{localStorage.setItem('czr_known_baseline',JSON.stringify(kw));localStorage.setItem('czr_known_baseline_date',T);return 'baseline '+kw.length}};
const out=['K+ '+kp.join(','),'K- '+km.join(','),'N '+nw.join(','),'U '+[...U].map(([t,s])=>t+'='+s).join(','),'R '+R.join(','),'M '+mx,'T '+T].join('\\n');
window._syncOut=out; return out.length>1500 ? 'LONG '+out.length+' - read window._syncOut in slices' : out;
}})()""")
