#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["genanki", "simplemma"]
# ///
"""Build the Anki deck anki/Czech-Readers.apkg from anki/notes.json.

Which words: words in readers Adam has READ that are not known in LingQ
(ledger.lingq.sticky_in_read_lessons, refreshed by every sync). A word only gets a card
once someone has written a note for it in anki/notes.json.

Notes are hand-written, not copied from the readers: a short, memorable sentence with
intent (humour, a vivid picture, something from Adam's life), using only words he knows
plus the target form in **bold**. Fields: id (stable key - never change it), form,
sentence, en (translation), note (one-line meaning / form hint).

Usage:
  python3 scripts/make_anki.py           # build the .apkg
  python3 scripts/make_anki.py --todo    # list eligible words that have no note yet

Re-importing the .apkg into Anki/AnkiDroid adds new cards and keeps progress on old ones
(stable note GUIDs). Adam syncs via AnkiWeb.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES = os.path.join(ROOT, 'anki', 'notes.json')
OUT = os.path.join(ROOT, 'anki', 'Czech-Readers.apkg')
notes = json.load(open(NOTES, encoding='utf8'))

if '--todo' in sys.argv:
    L = json.load(open(os.path.join(ROOT, 'ledger.json'), encoding='utf8'))
    rank = json.load(open(os.path.join(ROOT, 'data', 'vocab.json'), encoding='utf8'))['rank']
    skip = {s.lower() for s in L.get('ignore_tokens', [])}
    have = {n['id'].rstrip('0123456789') for n in notes}
    todo = [w for w in L['lingq'].get('sticky_in_read_lessons', []) if w.lower() not in skip and w not in have]
    todo.sort(key=lambda w: rank.get(w, 99999))
    print(f'{len(todo)} eligible words without a note (frequency order):')
    print(' '.join(todo))
    sys.exit()

import genanki
MODEL = genanki.Model(
    1607392319, 'Czech Readers sentence',
    fields=[{'name': 'Sentence'}, {'name': 'Translation'}, {'name': 'Form'}, {'name': 'Note'}],
    templates=[{
        'name': 'Read',
        'qfmt': '<div class="cz">{{Sentence}}</div>',
        'afmt': '<div class="cz">{{Sentence}}</div><hr id="answer">'
                '<div class="en">{{Translation}}</div><div class="note">{{Note}}</div>',
    }],
    css='.card{font-family:system-ui,sans-serif;text-align:center;padding:1em}'
        '.cz{font-size:1.5em;line-height:1.4}.cz b{color:#c0392b}'
        '.en{font-size:1.1em;margin-top:.6em}.note{color:#777;margin-top:.8em;font-size:.95em}')
deck = genanki.Deck(2059400110, 'Czech Readers')
bold = lambda s: re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
for n in notes:
    deck.add_note(genanki.Note(model=MODEL, fields=[bold(n['sentence']), n['en'], n['form'], n['note']],
                               guid=genanki.guid_for('czech-readers', n['id'])))
genanki.Package(deck).write_to_file(OUT)
print(f'{len(notes)} cards -> {os.path.relpath(OUT, ROOT)}')
