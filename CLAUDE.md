# Czech graded reader — working instructions

Adam is learning Czech by reading in LingQ. This repo is a graded comprehensible-input
course: simplified retellings of public-domain Czech stories, written against his
actual LingQ vocabulary, getting closer to the originals over time.

## Principles
- **Coverage: >=95% of tokens core / taught / half-known, aiming for ~98%** (`scripts/check.py`).
  Research: 95% = minimal comprehension, 98% = comfortable reading (Laufer & Ravenhorst-
  Kalovski 2010; Hu & Nation 2000). So 'new' tokens <=5% of a reader.
- New lemmas per reader: see CURRICULUM (8-10 in Stage 1, mostly top-2000). Each new word
  3-5 uses in its first reader, then recycled to **~10-20 total encounters spread over the
  next ~10 readers** in varied contexts (words are reliably learned after ~7-10 encounters;
  gains flatten after ~20). `needs_review` words in ledger.json get those extra uses.
- LingQ status 1-2 = NEW (he looked it up once; it did not stick). Status 3 = half.
  Status 4 / known (API status 3) = known.
- **`CURRICULUM.md` is the plan.** Follow its stages, phases (introduce → saturate →
  consolidate → gate) and per-reader rules. Hundreds of readers per stage; never
  advance without passing the gate. Log gate decisions in `ledger.levels.notes`.
- Sources are public domain only (folk tales, Erben, Němcová, Čapek, Hašek).
  Retell in our own simplified words; later versions move toward the original text.
- Run 2-3 story threads at once (a short folk tale + a longer Čapek thread) for variety.
- Readers live in `episodes/sNN/NNN - Title.txt` (stage folder, 3-digit number within
  the stage), title on line 1. No "(1)" in titles. Length grows by stage (see CURRICULUM).
- Dialogue: Czech quotation marks „…“ (never a straight " to close). Write dialogue the
  natural way; don't restructure sentences just to suit LingQ's sentence splitter
  (it splits after ?/! inside quotes - Adam accepts that).
- Keep the folk tales' original darkness (wolves drowned, foxes beaten, etc.) when it's in
  the source and the vocabulary is easy - it's part of the culture. Don't add gore that
  isn't in the original, and don't soften it.
- Doubling for effect ("jí a jí", "spí a spí", "rychle, rychle") only where the original
  tale has it or for real emphasis - at most once in a reader, not as a habit.
- Adam's messages are concise; give him trade-offs, not specs.
- Stories should get richer as he improves: longer, more complex sentences, more
  literary texture - not just more vocabulary.

## Batch routine ("next batch")
1. **Sync LingQ** (~3 s) via Claude in Chrome, on any lingq.com tab:
   `python3 scripts/make_sync_js.py > /tmp/sync.js`, paste it into javascript_tool (it
   awaits and returns the delta; if it says LONG, read `window._syncOut` in slices),
   save to `/tmp/delta.txt`, run `python3 scripts/sync.py /tmp/delta.txt` (applies,
   rebuilds vocab + ledger, commits, prints a summary), then `window._syncCommit()`.
   It reads per-lesson word statuses for the course (`/api/v3/cs/lessons/<id>/words/`,
   `/api/v2/cs/lesson-stats/<id>/`) - 'sticky' = words in READ readers still at
   LingQ 1-3: give them extra repetitions. Details in the script docstring.
2. (`pip install --break-system-packages simplemma` first if missing - sync.py needs it.)
3. Read `ledger.json` (difficulty notes, grammar stage, roadmap, needs_review words,
   `open_items` - pick up anything pending there first).
4. Run `python3 scripts/targets.py 80` and plan the batch around those words. Write ~5-10 readers. Check each with `python3 scripts/check.py "episodes/sNN/NNN - ....txt"`,
   revise until it meets the targets. Add character names to `ignore_tokens`.
5. `python3 scripts/update_ledger.py`; update roadmap/grammar notes; commit + push.
6. Upload to the stage's LingQ course (`ledger.lingq.courses`; Stage 1 = 2972731,
   "Graded Readers (AI)") via Chrome. Delete a lesson: DELETE /api/v3/cs/lessons/<id>/
   with the same CSRF header (only with Adam's OK). Working method (2026-11-16): in a tab on lingq.com, run JS:
   `fetch('/api/v3/cs/lessons/import/', {method:'POST', credentials:'include',
   headers:{'X-CSRFToken': <csrftoken cookie>}, body: FormData{title, text,
   collection: 2972731, status:'private', save:'true'}})` → 201 with lesson id.
   Title format: `NNN Title` (e.g. "002 Zlatá hruška"); text = file minus title line.
   v2 /lessons/ is dead ("API is obsolete"). Check the course list first
   (`/api/v3/cs/collections/2972731/lessons/`) to avoid duplicates. Never upload a
   test fragment - upload the real episode. Fallback: hand Adam the files for Bulk Import.
7. Ask Adam how the batch felt; record his answer in `ledger.levels.notes`.

## Local tooling
Adam uses **uv**: scripts carry inline dependency headers, so locally prefer
`uv run scripts/<name>.py` (no pip installs needed).

## Keeping docs lean
- `CURRICULUM.md` and `CLAUDE.md` are the plan and the method: no progress logs, word
  lists or per-batch notes in them.
- Progress lives only in `ledger.json`. `levels.notes` holds decisions and feedback that
  change how readers are written (one line each); when it passes ~10 lines, fold older
  ones into a short summary line. Roadmap entries: one line per story, drop finished
  ones once they're in `episodes/`.

## Files
- `CURRICULUM.md` — stages, phases, gates, story sources
- `episodes/sNN/` — the readers, one folder per stage
- `ledger.json` — course state: current stage/phase, notes, roadmap, word exposure
- `data/lingq/` — latest LingQ snapshots (private data, keep repo private)
- `data/cs_50k.txt` — Czech subtitle frequency list (hermitdave/FrequencyWords)
- `data/vocab.json` — generated lemma tiers (rebuild after each sync)
