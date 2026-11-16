# Czech graded reader — working instructions

Adam is learning Czech by reading in LingQ. This repo is a graded comprehensible-input
course: simplified retellings of public-domain Czech stories, written against his
actual LingQ vocabulary, getting closer to the originals over time.

## Principles
- ~90%+ of tokens must be core / taught / half-known (`scripts/check.py`).
- 5-8 genuinely new lemmas per episode; each new word used 3+ times in its episode
  and recycled in the next few. `needs_review` words in ledger.json get extra uses.
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
- Adam's messages are concise; give him trade-offs, not specs.
- Stories should get richer as he improves: longer, more complex sentences, more
  literary texture - not just more vocabulary.

## Batch routine ("next batch")
1. **Sync LingQ** via Claude in Chrome (he is signed in): open a tab on
   `https://www.lingq.com/api/v2/cs/cards/?page_size=1`, run JS that fetches all pages
   of `/api/v2/cs/cards/?page_size=1000` in the background (store on `window`, poll),
   and `/api/languages/cs/known-words/`. The tool output is ~2k chars max, so save
   the results via a Blob download (`lingq_cards_cs.json`, `known.json`) and ask Adam
   to attach them. Save to `data/lingq/cards.json` and `data/lingq/known_words.json`.
2. `pip install --break-system-packages simplemma`, then
   `python3 scripts/build_vocab.py data/lingq/known_words.json data/lingq/cards.json`
   and `python3 scripts/update_ledger.py`.
3. Read `ledger.json` (difficulty notes, grammar stage, roadmap, needs_review words).
4. Write ~5-10 readers. Check each with `python3 scripts/check.py "episodes/sNN/NNN - ....txt"`,
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

## Files
- `CURRICULUM.md` — stages, phases, gates, story sources
- `episodes/sNN/` — the readers, one folder per stage
- `ledger.json` — course state: current stage/phase, notes, roadmap, word exposure
- `data/lingq/` — latest LingQ snapshots (private data, keep repo private)
- `data/cs_50k.txt` — Czech subtitle frequency list (hermitdave/FrequencyWords)
- `data/vocab.json` — generated lemma tiers (rebuild after each sync)
