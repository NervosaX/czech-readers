"""Generate the JS that pulls a LingQ *delta* in the browser (Claude in Chrome).

Usage: python3 scripts/make_sync_js.py > /tmp/sync.js
1. Paste /tmp/sync.js into javascript_tool on a lingq.com tab ('started').
2. Poll (cards take ~50 s):  JSON.stringify({done: window._sync.done, len: window._sync.out?.length, err: window._sync.err})
3. Read in slices: window._sync.out.slice(0,1800), slice(1800,3600)... -> save to /tmp/delta.txt
4. python3 scripts/apply_delta.py /tmp/delta.txt   (then rebuild vocab)
5. Only after apply succeeded: run  window._sync.commit()  -> moves the browser baseline forward.

The known-words baseline lives in the browser: localStorage 'czr_known_baseline' on
lingq.com (LingQ's known-words list has no dates and is not in learning order).
If the baseline is missing, the script returns 'NOBASE' + per-letter counts: compare
them with data/lingq/known_words.json, fetch the differing letters, then seed the baseline
(see git history 2026-11-16 for how this was done).

Delta format (one line per section):
  K+ word,...       newly known word forms
  K- word,...       forms no longer known
  C  term=status,...  cards whose status changed since last sync (API status 0-3)
  N  term=status,...  NEW cards since last sync = words Adam looked up while reading
  M  <max card pk>  T <UTC timestamp>
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(ROOT, 'ledger.json'), encoding='utf8'))['lingq']
since = L.get('last_sync_utc', '2026-11-16T06:00:00')
max_pk = L.get('max_card_pk', 0)
print(f"""window._sync={{done:false}};
(async()=>{{try{{
const SINCE='{since}', MAXPK={max_pk};
const kw=(await (await fetch('/api/languages/cs/known-words/',{{credentials:'include'}})).json()).map(x=>x.word);
const base=localStorage.getItem('czr_known_baseline');
if(!base){{const b={{}};for(const w of kw)b[w[0]]=(b[w[0]]||0)+1; window._sync.out='NOBASE '+JSON.stringify(b); window._sync.done=true; return;}}
const PREV=new Set(JSON.parse(base)), NOW=new Set(kw);
const kp=kw.filter(w=>!PREV.has(w)), km=[...PREV].filter(w=>!NOW.has(w));
let url='/api/v2/cs/cards/?page_size=1000', ch=[], nw=[], mx=MAXPK;
while(url){{const d=await (await fetch(url,{{credentials:'include'}})).json();
 for(const c of d.results){{ if(c.pk>mx) mx=c.pk;
  const isNew = MAXPK ? c.pk>MAXPK : (c.srs_due_date && c.srs_due_date>SINCE && !c.status_changed_date);
  if(isNew) nw.push(c.term+'='+c.status);
  else if(c.status_changed_date && c.status_changed_date>SINCE) ch.push(c.term+'='+c.status);}}
 url=d.next;}}
const T=new Date().toISOString().slice(0,19);
window._sync.out=['K+ '+kp.join(','),'K- '+km.join(','),'C '+ch.join(','),'N '+nw.join(','),'M '+mx,'T '+T].join('\\n');
window._sync.commit=()=>{{localStorage.setItem('czr_known_baseline',JSON.stringify(kw));localStorage.setItem('czr_known_baseline_date',T);return 'baseline '+kw.length}};
}}catch(e){{window._sync.err=String(e)}} window._sync.done=true;}})(); 'started'""")
