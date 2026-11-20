# Lyricsfile 1.0 Draft Specification

**Status:** Draft

This is an early draft and may change. In this document, **must** means a rule
is required, while **should** means it is recommended.

## 1. File Representation

A Lyricsfile should use the `.lyricsfile.yaml` extension.

The file must:

- use UTF-8 encoding;
- contain one YAML document;
- contain a mapping at the top level; and
- use only mappings, sequences, strings, integers, booleans, and null.

Files must not contain duplicate keys or custom YAML tags. Writers should also
avoid YAML anchors and aliases for now.

## 2. Top-Level Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `version` | string | Yes | Lyricsfile format version. This draft uses `"1.0"`. |
| `metadata` | mapping | Yes | Information about the track and lyrics. |
| `lines` | sequence | No | Synchronized lyric lines. |
| `plain` | string | No | Unsynchronized lyrics with preserved line breaks. |

A non-instrumental file should contain at least one of `lines` or `plain`.
An empty `lines` sequence is equivalent to having no synchronized lines.

## 3. Metadata

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `title` | string | Yes | Track title. |
| `artist` | string | Yes | Primary artist name. |
| `album` | string | No | Album name. |
| `duration_ms` | integer | No | Track duration in milliseconds. |
| `offset_ms` | integer | No | Global timing offset; exact application is unresolved. |
| `language` | string | No | Primary lyrics language as an ISO 639-1 code. |
| `instrumental` | boolean | No | Whether the track has no vocal lyrics. Defaults to `false`. |

`duration_ms` must not be negative.

The meaning of `offset_ms` is not settled yet. Writers should leave it out for
now unless the writer and reader already agree on how to use it.

When `instrumental` is `true`, `lines` and `plain` must be omitted or empty.

## 4. Synchronized Lines

Each item in `lines` must be a mapping with these fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `text` | string | Yes | Complete text of the line. |
| `start_ms` | integer | Yes | Start time in milliseconds. |
| `end_ms` | integer | No | End time in milliseconds. |
| `words` | sequence | No | Word- or segment-level synchronization. |
| `readings` | sequence | No | Optional pronunciation spans relative to this line’s `text`; see section 5.1. |

`start_ms` must not be negative. When present, `end_ms` must be greater than or
equal to `start_ms`.

Writers should order lines by `start_ms`, from earliest to latest. Equal start
times and overlapping lines are allowed. Readers must not assume that one line
ends when another starts.

There is no standard rule for a missing `end_ms` yet. Readers may choose a
sensible display time, but should not save an invented end time back to the
file without user input.

## 5. Synchronized Words

Each item in `words` must be a mapping with these fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `text` | string | Yes | Text of the word or segment, including relevant whitespace. |
| `readings` | sequence | No | Optional pronunciation spans relative to this word’s `text`; see section 5.1. |
| `start_ms` | integer | Yes | Start time in milliseconds. |
| `end_ms` | integer | No | End time in milliseconds. |

Word `start_ms` values must not be negative. When present, a word's `end_ms`
must be greater than or equal to its `start_ms`.

Writers should order words by `start_ms`. Words may overlap, but writers should
only do this when the overlap is intentional.

Joining every `word.text` value should produce the line's `text`. Spaces needed
to rebuild the line should be included in word text. Languages that do not use
spaces do not need to add them.

When `words` is not empty, readers should use it for timed highlighting.
`line.text` remains the fallback for readers without word-sync support.

## 5.1. Optional Reading Annotations

This addition is proposed as part of the draft. It is not a statement that
existing Lyricsfile applications already support it. See the compatibility
and version questions in [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md).

A line or word may include a `readings` sequence. An omitted or empty sequence
means no supplied reading annotations. A reader may generate its own readings
when none are supplied, but generated readings must not silently overwrite
supplied annotations when saving.

Each reading must be a mapping with these fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `start` | integer | Yes | Zero-based start offset in the containing `text`. |
| `end` | integer | Yes | End-exclusive offset in that same `text`. |
| `text` | string | Yes | Nonblank, contributor-supplied pronunciation. |
| `language` | string | No | BCP 47 language tag for the reading, such as `ja` or `ja-Latn`. |

Offsets count Unicode scalar values (code points excluding surrogates), not
UTF-8 bytes, UTF-16 code units, or grapheme clusters. Count the exact decoded
YAML `text` value, including whitespace and line breaks. Do not trim, case-fold,
or normalize Unicode before counting. Writers should place span boundaries at
grapheme-cluster boundaries, so combining marks are not separated from their
base characters.

For example, `🍀食べる` has four scalar values. The span `[1, 2)` selects `食`,
even though its UTF-8 byte offset and JavaScript string index differ. In Rust,
count `.chars()`; in JavaScript, use `Array.from(text)` rather than indexing UTF-16
code units. A decomposed accent counts separately from its base character.

For each annotation:

- `0 <= start < end <=` the scalar-value count of the containing `text`.
- The base substring is the containing `text[start:end]`; it must not be
  duplicated into the annotation or replaced with the reading.
- The reading's `text` must contain at least one non-whitespace character.
- The reading is authoritative for this lyric version. It may differ from a
  dictionary reading, and is not restricted to Japanese, kana, or one script.
- `language`, when supplied, must be a nonblank BCP 47 tag. Omission makes no
  assertion about the reading's language; do not infer it from the base text.

Annotations in a sequence must be ordered by `start` and must not overlap.
Adjacent spans are allowed. At most one reading may annotate a given base
character; alternate pronunciations need a separate lyric version.

A word's offsets are local to that word, not the complete line. A line may
instead supply line-relative readings, even when it has timed words. A line
must not have nonempty `readings` if any of its words also has nonempty
`readings`; this avoids conflicting or duplicate annotations. A reader maps
line-relative readings across word boundaries using the concatenated word
text. Annotated lines with words must satisfy the exact text-concatenation
rule in section 5; otherwise the document is invalid for this extension.

```yaml
# Only 食 receives a reading. べる remains ordinary text (okurigana).
text: '食べる'
start_ms: 12000
end_ms: 14000
readings:
  - start: 0
    end: 1
    text: 'た'
    language: 'ja'
```

Readings have no timestamps and do not change line or word timing. They are
annotations over a timed unit, not independently sung units. A player may
render them as ruby, a pronunciation aid, or hide them. Styling and animation
remain application decisions.

Inline editing notation such as `{食|た}べる` is an editor convention, not part
of this format: store `食べる` as `text` and its reading as structured data.
Unannotated text is not a request to delete or translate the original lyrics.

When exporting plain text or LRC, emit only the base lyric text. Do not insert
furigana, braces, HTML, or pronunciation into `plain`, `line.text`, or
`word.text`. A lossy exporter should warn that reading annotations will be
lost, and retain the source Lyricsfile when possible. Reading-aware editors
must preserve untouched annotations; if base text changes, validate or update
the offsets instead of carrying them over unchanged. Invalid annotations
should produce an actionable error; a viewer may still show the base lyrics.

Annotations belong to the exact text in a particular Lyricsfile revision, not
to a track title or a global dictionary. External correction overlays should
identify both the lyric version and its content (for example, an immutable
revision ID and SHA-256 of the original file bytes), and reject a changed base
revision. This does not introduce an LRCLIB-specific ID or canonical hashing
scheme into the file format. Changes to an audio/video offset do not change
these text-relative positions.

## 6. Plain Lyrics

`plain` is a separate unsynchronized version of the lyrics. It may include
section labels, blank lines, annotations, or other text not present in
`lines`.

Writers should use YAML's literal block style (`|`) for multiline lyrics.
Readers must still accept `plain` as a string written in another valid YAML
style.

Readers must not assume that `plain` and `lines` contain exactly the same text.

## 7. Timing And Rendering

All timestamps are integer milliseconds from the start of the audio track.

Lines may overlap. A player may display and highlight several active lines at
the same time.

Rendering layout, animation, colors, and end-time inference are outside the
scope of this draft.

## 8. Version Handling

For this draft, `version` must be the exact string `"1.0"`.

Readers must not treat an unknown version as version 1.0. They may reject the
file or preserve it without displaying it.

How version 1.0 can grow without breaking readers is still being discussed.

## 9. Example

```yaml
version: '1.0'

metadata:
  title: 'Example Song'
  artist: 'Example Artist'
  language: 'en'
  instrumental: false

lines:
  - text: 'Hello world'
    start_ms: 1200
    end_ms: 2800
    words:
      - text: 'Hello '
        start_ms: 1200
        end_ms: 1900
      - text: 'world'
        start_ms: 1900
        end_ms: 2800

plain: |
  Hello world
```

Additional examples are available in [`examples/`](examples/).

## 10. Implementation Notes

- Parse YAML with safe loading enabled.
- Reject duplicate keys rather than choosing one value silently.
- Apply reasonable limits to document size, nesting depth, and alias expansion.
- Keep the original document when lossless editing is not possible.
- Report structural errors separately from semantic timing warnings.
