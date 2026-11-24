# Czech Readers

A personal graded-reader course for learning Czech: simplified retellings of real,
public-domain Czech stories (folk tales, Erben, Josef and Karel Čapek, later Švejk),
written against my actual LingQ vocabulary and getting closer to the originals over
time. Plus an Anki deck for the words that haven't stuck yet.

Claude does most of the work. These docs are for me.

## How it works

1. **I read** the readers in LingQ (course *Graded Readers (AI)*) and mark words as I go.
2. **Claude syncs** my LingQ progress: which readers I've read, which words in them are
   still yellow, what I looked up.
3. **Claude writes the next batch** of readers around the words I need - mostly the top
   ~2000 most frequent Czech words - keeping ~95-98% of each reader already known, and
   uploads them to LingQ.
4. **Words that still haven't stuck** go into the Anki deck as cards with new,
   purpose-written sentences, pushed straight into my AnkiWeb account.

The reasons behind the design (coverage, repetition, compelling input, grammar) are in
[`RESEARCH.md`](RESEARCH.md); the long-term plan (stages, past tense → cases → …) is in
[`CURRICULUM.md`](CURRICULUM.md).

## Everyday use

**Get more readers:** open a Claude session with this repo (or `claude --chrome` in this
folder) and say **"next batch"**. Claude syncs LingQ, writes and checks ~5-10 readers,
uploads them, and adds Anki cards. Tell it how the last batch felt; it remembers.

**Get the new Anki cards onto my phone:**

```bash
git pull
uv run scripts/anki_push.py
```

then sync AnkiDroid. (A local Claude Code session runs this itself.)

## Anki setup (once)

1. Have an AnkiWeb account and sign AnkiDroid into it (**Settings → Sync**). Sync the phone.
2. In this folder:
   ```bash
   uv run scripts/anki_push.py --login     # AnkiWeb email + password; only a sync key is saved
   uv run scripts/anki_push.py --dry-run   # shows what would change, uploads nothing
   uv run scripts/anki_push.py             # adds the cards
   ```
3. Sync AnkiDroid - the **Czech Readers** deck appears. Set *New cards/day* to ~8-10.

The script always downloads from AnkiWeb first, only adds or updates cards in the
*Czech Readers* deck, never deletes anything, and asks before any one-way upload.
The sync key lives in `~/.config/czech-readers/` (readable only by me); a private mirror
collection lives in `~/.local/share/czech-readers/`. Delete both to log out.

## Adding cards myself

Cards come from [`anki/notes.json`](anki/notes.json). Each entry:

```json
{
  "id": "čekat",
  "form": "čekám",
  "sentence": "**Čekám** na autobus už hodinu.",
  "en": "I've been waiting for the bus for an hour.",
  "note": "čekám = I wait / I'm waiting (čekat)"
}
```

- `id` - unique and **never changed** (it's what keeps a card's review history).
  For a second card for the same word, use e.g. `čekat2`.
- `sentence` - Czech, with the target word in `**bold**` (shown in red).
- Edit any field and re-run `anki_push.py`: the card updates in place.
- `uv run scripts/make_anki.py --todo` lists words from my readers that still have no card.
- No AnkiWeb? `uv run scripts/make_anki.py` builds `anki/Czech-Readers.apkg` to open in
  AnkiDroid instead.

## Other useful commands

| Command | What it does |
|---|---|
| `uv run scripts/check.py "episodes/s02/001 - ….txt"` | Vocabulary check for one reader |
| `uv run scripts/targets.py 60` | Next high-frequency words to target |
| `uv run scripts/update_ledger.py` | Recount word exposure across all readers |

## Repo layout

| Path | What |
|---|---|
| `episodes/sNN/` | The readers, one folder per stage (LingQ numbers them straight through) |
| `ledger.json` | Course state: stage, feedback notes, roadmap, word exposure, LingQ sync data |
| `anki/notes.json` | The Anki cards |
| `RESEARCH.md`, `CURRICULUM.md` | Why and what |
| `CLAUDE.md` | Working instructions for Claude |
| `scripts/` | Sync, checking, Anki tools |
| `data/` | LingQ snapshots (private - keep this repo private) and frequency list |
