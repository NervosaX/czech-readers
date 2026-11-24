#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["anki", "genanki"]
# ///
"""Push anki/notes.json straight into Adam's AnkiWeb account - no manual import.

Runs on Adam's own machine (needs AnkiWeb; the Claude workspace can't reach it, and his
password must never pass through Claude). Uses Anki's official Python library and the
same sync protocol as the Anki apps.

  uv run scripts/anki_push.py --login     # once: asks for AnkiWeb email + password,
                                          # stores only the sync key (not the password)
  uv run scripts/anki_push.py --dry-run   # download + show what would change, upload nothing
  uv run scripts/anki_push.py             # download, add new / update changed cards, sync up

What it does, every run:
  1. Syncs a private mirror collection (~/.local/share/czech-readers/) DOWN from AnkiWeb.
     The mirror is never studied, so AnkiWeb always wins: if Anki asks for a full sync,
     the script downloads. It never does a one-way upload without asking you.
  2. Adds/updates notes in the "Czech Readers" deck from anki/notes.json. Notes are keyed
     by a stable GUID (same as the .apkg builder), so cards you already have - imported or
     pushed - are updated in place and keep all their review history.
  3. Syncs the changes back UP. Then sync your phone and the new cards are there.

Never deletes cards. Never touches other decks.
"""
import argparse, getpass, json, os, re, stat, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.expanduser('~/.config/czech-readers/anki-sync.json')
COLDIR = os.path.expanduser('~/.local/share/czech-readers')
COLPATH = os.path.join(COLDIR, 'collection.anki2')
DECK = 'Czech Readers'
NOTETYPE = 'Czech Readers sentence'
FIELDS = ['Sentence', 'Translation', 'Form', 'Note']
QFMT = '<div class="cz">{{Sentence}}</div>'
AFMT = ('<div class="cz">{{Sentence}}</div><hr id="answer">'
        '<div class="en">{{Translation}}</div><div class="note">{{Note}}</div>')
CSS = ('.card{font-family:system-ui,sans-serif;text-align:center;padding:1em}'
       '.cz{font-size:1.5em;line-height:1.4}.cz b{color:#c0392b}'
       '.en{font-size:1.1em;margin-top:.6em}.note{color:#777;margin-top:.8em;font-size:.95em}')

from anki.collection import Collection
from anki.sync import SyncAuth, SyncOutput
import genanki

NO, NORMAL, FULL, FULL_DOWN, FULL_UP = (SyncOutput.NO_CHANGES, SyncOutput.NORMAL_SYNC,
    SyncOutput.FULL_SYNC, SyncOutput.FULL_DOWNLOAD, SyncOutput.FULL_UPLOAD)


def save_cfg(d):
    os.makedirs(os.path.dirname(CFG), exist_ok=True)
    with open(CFG, 'w') as f: json.dump(d, f)
    os.chmod(CFG, stat.S_IRUSR | stat.S_IWUSR)


def login():
    os.makedirs(COLDIR, exist_ok=True)
    user = input('AnkiWeb email: ').strip()
    pw = getpass.getpass('AnkiWeb password (not stored): ')
    col = Collection(COLPATH)
    try:
        auth = col.sync_login(username=user, password=pw, endpoint=None)
    finally:
        col.close()
    save_cfg({'hkey': auth.hkey, 'endpoint': auth.endpoint or '', 'user': user})
    print(f'Logged in. Sync key saved to {CFG} (your password was not saved).')


def get_auth():
    if not os.path.exists(CFG):
        sys.exit('Not logged in yet. Run:  uv run scripts/anki_push.py --login')
    c = json.load(open(CFG))
    return SyncAuth(hkey=c['hkey'], endpoint=c.get('endpoint') or None), c


def sync(col, auth, cfg, label):
    out = col.sync_collection(auth=auth, sync_media=False)
    if out.new_endpoint:
        auth = SyncAuth(hkey=auth.hkey, endpoint=out.new_endpoint)
        cfg['endpoint'] = out.new_endpoint; save_cfg(cfg)
    if out.server_message: print('AnkiWeb says:', out.server_message)
    return out.required, auth


def full_download(col, auth):
    print('  AnkiWeb asked for a full sync - downloading (AnkiWeb wins; the mirror is never studied).')
    col.close_for_full_sync()
    col.full_upload_or_download(auth=auth, server_usn=None, upload=False)
    col.reopen(after_full_sync=True)


def ensure_notetype(col):
    mm = col.models
    m = mm.by_name(NOTETYPE)
    if m: return m, False
    m = mm.new(NOTETYPE)
    for f in FIELDS: mm.add_field(m, mm.new_field(f))
    t = mm.new_template('Read'); t['qfmt'] = QFMT; t['afmt'] = AFMT
    mm.add_template(m, t); m['css'] = CSS
    mm.add(m)
    return mm.by_name(NOTETYPE), True


def apply_notes(col, dry):
    notes = json.load(open(os.path.join(ROOT, 'anki', 'notes.json'), encoding='utf8'))
    m, created = ensure_notetype(col) if not dry else (col.models.by_name(NOTETYPE), False)
    did = col.decks.id(DECK) if not dry else None
    bold = lambda s: re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    added = updated = same = 0
    for n in notes:
        guid = genanki.guid_for('czech-readers', n['id'])
        vals = [bold(n['sentence']), n['en'], n['form'], n['note']]
        nid = col.db.scalar('select id from notes where guid=?', guid)
        if nid:
            note = col.get_note(nid)
            cur = [note[f] if f in note else '' for f in FIELDS]
            if cur == vals: same += 1; continue
            updated += 1
            if not dry:
                for f, v in zip(FIELDS, vals):
                    if f in note: note[f] = v
                col.update_note(note)
        else:
            added += 1
            if not dry:
                note = col.new_note(m); note.guid = guid
                for f, v in zip(FIELDS, vals): note[f] = v
                col.add_note(note, did)
    return added, updated, same, created


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--login', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    if a.login: return login()

    auth, cfg = get_auth()
    os.makedirs(COLDIR, exist_ok=True)
    col = Collection(COLPATH)
    try:
        print('1. Syncing down from AnkiWeb...')
        req, auth = sync(col, auth, cfg, 'down')
        if req in (FULL, FULL_DOWN):
            full_download(col, auth)
        elif req == FULL_UP:
            sys.exit('AnkiWeb has no collection yet (or asked for a one-way upload). Sync your phone '
                     'to AnkiWeb first, then run this again. Nothing was changed.')

        print('2. Applying anki/notes.json...')
        added, updated, same, created = apply_notes(col, a.dry_run)
        print(f'   new cards: {added}   updated: {updated}   unchanged: {same}'
              + ('   (created the card type)' if created else ''))
        if a.dry_run:
            print('Dry run - nothing uploaded.'); return
        if not (added or updated or created):
            print('Nothing to upload. Done.'); return

        print('3. Syncing up to AnkiWeb...')
        req, auth = sync(col, auth, cfg, 'up')
        if req in (FULL, FULL_UP):
            print('\n   Anki needs a ONE-WAY UPLOAD to apply this (usually only the very first time,\n'
                  '   when the card type is created). This replaces AnkiWeb with the mirror, which\n'
                  '   was downloaded seconds ago - safe ONLY if your phone has no unsynced reviews.')
            if input('   Sync your phone first, then type "upload" to continue: ').strip() != 'upload':
                sys.exit('   Cancelled - nothing uploaded. Run again any time.')
            col.close_for_full_sync()
            col.full_upload_or_download(auth=auth, server_usn=None, upload=True)
            col.reopen(after_full_sync=True)
        elif req == FULL_DOWN:
            sys.exit('   AnkiWeb changed during the run - run the script again.')
        print('Done. Sync AnkiDroid and the cards will be there.')
    finally:
        col.close()


if __name__ == '__main__':
    main()
