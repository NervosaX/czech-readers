# Curriculum — how the readers grow

## The core idea: wide plateaus, small steps

Adam wants to read **a lot**: hundreds of readers on each new concept before moving on.
So the course is a series of **stages**. Each stage adds one main grammar idea and one
vocabulary band, then stays on that plateau for a long time:

```
Stage N:   introduce ─▶ saturate ─────────────────────────────▶ consolidate ─▶ gate
           (~10 rdrs)   (bulk of the stage: 80-200 readers)     (~20 rdrs)     (check)
```

- **Introduce (~10 readers):** the new grammar point shows up constantly, in very
  simple, familiar contexts. These readers hold back on new vocabulary (2-4 new
  lemmas) so all the effort goes into the grammar.
- **Saturate (most of the stage):** the new point is simply *normal*. Stories vary
  (new tales, genres, narrators, dialogue-heavy vs. descriptive), the vocabulary
  band widens at the usual rate (5-8 new lemmas per reader), and everything from
  earlier stages keeps getting used. This is where the hundreds of readers live.
- **Consolidate (~20 readers):** retell stories from earlier in the stage (or from
  earlier stages) at the current level. They're familiar plots with richer language. Almost
  no new words: these should feel easy, a "victory lap".
- **Gate:** move on only when all three hold:
  1. Adam says the current readers feel easy (comfortable, few lookups).
  2. LingQ sync: ≥80% of the stage's taught words are at status 4/known.
  3. The minimum reader count for the stage is reached.
  If the gate fails, keep reading at this stage. More plateau is never a problem.

**Nothing is ever dropped.** Every stage's grammar and vocabulary stay in use in every
later stage. A reader in Stage 9 is still full of Stage 1-8 material; only ~5% of
it is new.

**The stories grow too, not just the words.** As the stages go up, so does:
- reader length: ~250 words → ~600 → ~1,500 (a short chapter)
- sentence length and number of clauses
- narrative texture: description, inner thoughts, humour, real dialogue rhythms
- closeness to the source text: from simplified retelling → abridged
  original → the original

## Stages

Minimum reader counts are a floor, not a target; the gate decides.

| Stage | Grammar focus | Vocab band (lemmas) | Min readers | Story sources |
|---|---|---|---|---|
| **1** Present tense | být/mít, present tense of common verbs, nominative + accusative singular, negation (ne-), questions, imperative as fixed phrases | ~1,000 | 60 | Short repetitive folk tales: Budulínek, O veliké řepě, Kohoutek a slepička, Koza a kůzlátka, O Smolíčkovi, Perníková chaloupka |
| **2** Past tense | Past tense (byl, šel, řekl, -l/-la/-li), storytelling voice ("Byl jednou…") | ~1,300 | 100 | Same tales retold in past tense, then Hloupý Honza stories, Němcová's simpler tales |
| **3** Locative | v/na/o + locative singular; where things are and what people talk about | ~1,600 | 100 | Němcová & Erben tales with travel/places; Dášeňka (simplified) |
| **4** Genitive | u/do/z/od/bez/kolem + genitive sg; "nemá…" + genitive; quantity (trochu, hodně, kousek) | ~2,000 | 120 | Erben's *Sto prostonárodních pohádek* (100 tales = huge supply) |
| **5** Plurals | Nominative/accusative plural, all genders; numbers 1-4 | ~2,400 | 100 | Erben, Němcová; animal fables; Jirásek *Staré pověsti české* (simplified) |
| **6** Future & first aspect | budu + infinitive; perfective present = future; introducing aspect pairs (dělat/udělat) | ~2,800 | 120 | Jirásek legends (Libuše, Bruncvík, Golem); Čapek *Devatero pohádek* |
| **7** Instrumental | s/za/před/pod/nad/mezi + instrumental; být + profession (je učitelem) | ~3,300 | 120 | Čapek *Devatero pohádek*, *Dášeňka* (closer to original) |
| **8** Dative | k/proti/díky + dative; pronouns mi/ti/mu/jí; "líbí se mi", "je mi zima" | ~3,800 | 120 | Neruda *Povídky malostranské* (simplified); Čapek fairy tales |
| **9** Verbs of motion & prefixes | jít/chodit, jet/jezdit, nést/nosit…; prefixes při-/od-/vy-/za-/pře- | ~4,500 | 150 | Čapek *Povídky z jedné kapsy* (detective stories) |
| **10** Plural cases | Genitive/locative/instrumental/dative plural; numbers 5+ with genitive plural | ~5,200 | 150 | Čapek *Povídky z druhé kapsy*; Erben *Kytice* retold as prose |
| **11** Complex sentences | Conditional (by), kdyby/aby, relative který/jenž, reported speech | ~6,000 | 150 | Němcová *Babička* (abridged); Čapek *Krakatit* (abridged) |
| **12** Literary & spoken Czech | Participles/passive, older literary forms (recognition only), obecná čeština (-ej-, -ý → -ej, dělaj) | ~7,000+ | 150+ | *Švejk*: simplified → abridged → original; originals of earlier stories |

Total: roughly **1,500+ readers** before the originals. At 3-5 readers a day, that's
about a year of reading.

## Retelling: the spiral

Stories come back. Budulínek in Stage 1 (present tense, ~300 words) can return in
Stage 4 (past tense, genitive, ~600 words, more detail and dialogue) and again late
(close to a real folk-tale text). Rereading a familiar plot at a higher level is
cheap comprehension, and it shows Adam how far he's come. Aim for ~1 in 8 readers to
be a retelling.

## Variety inside a stage

To keep hundreds of readers on one plateau from going stale, rotate:
- **2-3 story threads at once:** one short tale (resolves in 2-5 readers) plus one
  longer serial (10-30 readers).
- **Narrative modes:** third-person tale, first-person ("Jmenuji se Honza…"), letters,
  diary entries, mostly-dialogue scenes, short descriptive "pictures" of a place.
- **Tone:** comic tales (Hloupý Honza), spooky (Erben), legends (Jirásek), modern
  humour (Čapek, Švejk).

## Per-reader rules (all stages)

- ≥90% of tokens are core / taught / half-known (`scripts/check.py`); in the
  Introduce phase aim for ≥95%.
- 5-8 genuinely new lemmas per reader (2-4 in the Introduce phase), each used 3+ times.
- Words flagged `needs_review` in `ledger.json` get worked into the next readers.
- Only grammar from the current stage or earlier. A later-stage form may appear as a
  fixed phrase (e.g. "Byl jednou jeden…" in Stage 1) but is never relied on.

## Repo layout for stages

- `episodes/s01/`, `episodes/s02/`, … one folder per stage, numbered 001-999 inside.
- One LingQ course per stage (Stage 1 = course 2972731, "Graded Readers (AI)").
  Create the next stage's course when its first reader is ready.
- `ledger.json → current_stage` and `readers_per_stage` track where we are;
  `levels.notes` records Adam's feedback and every gate decision.

## Where we are now

Stage 1, Introduce phase. Readers s01/001-003: Budulínek (apple, pear, fox takes him).
Already introduced: liška, dědeček, hodný, trochu, hloupý, jenom, otevřít/neotvírej,
kaše, hruška, hlad, zase, míč, běžet, díra, rychle, křičet, plakat.
Next: s01/004 Budulínek rescue → then Kohoutek a slepička, O veliké řepě,
Koza a kůzlátka, alongside a longer serial of Hloupý Honza episodes.
