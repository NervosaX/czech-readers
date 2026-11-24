# Czech graded reader — working instructions

Adam is learning Czech by reading in LingQ. This repo is a graded comprehensible-input
course: simplified retellings of public-domain Czech stories, written against his
actual LingQ vocabulary, getting closer to the originals over time.

## Principles
- **`RESEARCH.md` is the evidence base.** Every batch must pass its checklist (section 6):
  compelling stories, Adam chooses what's next, 95-98% coverage, 10-20 encounters per
  new word, short grammar notes kept OUT of the reader text, low pressure.
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
  (with proper „…“ quotes LingQ keeps „…?“ řekl X. together - checked 2026-11-23).
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
6. Upload to the ONE LingQ course, "Graded Readers (AI)" (2972731), for all stages, via
   Chrome. LingQ titles use a running number across stages (s01/001-016 = 001-016,
   s02/001 = 017, ...): next number = lesson count in the course + 1. Move/rename a lesson:
   PATCH /api/v3/cs/lessons/<id>/ JSON {title, collection} (keeps progress). Delete a lesson: DELETE /api/v3/cs/lessons/<id>/
   with the same CSRF header (only with Adam's OK). Working method (2026-11-16): in a tab on lingq.com, run JS:
   `fetch('/api/v3/cs/lessons/import/', {method:'POST', credentials:'include',
   headers:{'X-CSRFToken': <csrftoken cookie>}, body: FormData{title, text,
   collection: 2972731, status:'private', save:'true'}})` → 201 with lesson id.
   Title format: `NNN Title` with the running number; text = file minus title line.
   v2 /lessons/ is dead ("API is obsolete"). Check the course list first
   (`/api/v3/cs/collections/2972731/lessons/`) to avoid duplicates. Never upload a
   test fragment - upload the real episode. Fallback: hand Adam the files for Bulk Import.
7. **Anki:** `python3 scripts/make_anki.py --todo` lists eligible words (in read readers,
   not known in LingQ) without a card. Write notes for the most useful ones in
   `anki/notes.json` - new sentences with intent (memorable, funny, vivid or about Adam's
   life), known words only, target form in **bold**; never copy reader sentences unless
   it's genuinely the best example; never change an existing note's `id`. Then
   commit + push. Delivery: Adam runs `uv run scripts/anki_push.py` locally (pushes notes
   straight into his AnkiWeb, updates in place, keeps progress; his password never goes
   through Claude). In a LOCAL Claude Code session, run that yourself after the batch. In
   the cloud workspace (no AnkiWeb access) remind him to run it. Fallback:
   `python3 scripts/make_anki.py` builds `anki/Czech-Readers.apkg` to open in AnkiDroid.
8. Ask Adam how the batch felt; record his answer in `ledger.levels.notes`. Offer him 2-3
   options for the next story or thread (self-selected reading, RESEARCH.md section 1).

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
- `README.md` — Adam's own docs (how it works, setup, adding cards). Keep it in step when
  workflows or commands change.
- `RESEARCH.md` — the evidence behind the method, with sources and a per-batch checklist
- `CURRICULUM.md` — stages, phases, gates, story sources
- `episodes/sNN/` — the readers, one folder per stage
- `ledger.json` — course state: current stage/phase, notes, roadmap, word exposure
- `data/lingq/` — latest LingQ snapshots (private data, keep repo private)
- `data/cs_50k.txt` — Czech subtitle frequency list (hermitdave/FrequencyWords)
- `data/vocab.json` — generated lemma tiers (rebuild after each sync)
- `anki/notes.json` — hand-written Anki sentence notes (source of truth for the deck)
- `scripts/anki_push.py` — pushes notes.json into AnkiWeb (local only); `scripts/make_anki.py` — .apkg fallback
