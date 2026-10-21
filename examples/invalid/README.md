# Invalid Examples

These files intentionally violate requirements in the
[draft specification](../../SPECIFICATION.md). They are negative examples for
format reviewers and implementers, not lyrics files to import or copy as valid
templates. The valid examples remain in the parent [`examples/`](../) directory.

Each file isolates one problem. Correcting the problem described below gives a
valid example under the current draft.

| File | Problem | Specification | Correction |
| --- | --- | --- | --- |
| [duplicate-keys.lyricsfile.yaml](duplicate-keys.lyricsfile.yaml) | `metadata` contains two `title` keys. Readers must not silently choose one. | Section 1: duplicate keys are forbidden. | Remove one of the `title` entries. |
| [numeric-version.lyricsfile.yaml](numeric-version.lyricsfile.yaml) | Unquoted `1.0` is a YAML number, not a string. | Sections 2 and 8: `version` must be the exact string `"1.0"`. | Quote the value: `version: '1.0'`. |
| [multiple-documents.lyricsfile.yaml](multiple-documents.lyricsfile.yaml) | `---` starts a second YAML document in the same file. | Section 1: a file must contain one YAML document. | Store each document in its own file. |
| [negative-line-start.lyricsfile.yaml](negative-line-start.lyricsfile.yaml) | The line starts at `-1` milliseconds. | Section 4: `start_ms` must not be negative. | Change the start to `0` or another non-negative integer no later than `end_ms`. |
| [reversed-line-interval.lyricsfile.yaml](reversed-line-interval.lyricsfile.yaml) | The line ends before it starts. | Section 4: `end_ms` must be greater than or equal to `start_ms`. | Change the end to `1000` or a later integer. |
| [reversed-word-interval.lyricsfile.yaml](reversed-word-interval.lyricsfile.yaml) | The word ends before it starts, although its containing line has a valid interval. | Section 5: a word's `end_ms` must be greater than or equal to its `start_ms`. | Change the word's end to `1200` or a later integer. |
| [instrumental-with-lyrics.lyricsfile.yaml](instrumental-with-lyrics.lyricsfile.yaml) | An instrumental track supplies non-empty `plain` lyrics. | Section 3: when `instrumental` is `true`, `lines` and `plain` must be omitted or empty. | Remove `plain`, or change `instrumental` to `false` if the track has vocals. |

Some examples are valid YAML but invalid Lyricsfiles; successful YAML parsing
alone is not enough. The duplicate-key and multiple-document examples also need
the file-representation checks required by the draft.

These examples cover existing **must** requirements. They do not classify
unresolved questions such as unknown fields, word containment, or timing beyond
`metadata.duration_ms`. They also do not turn **should** recommendations, such
as word-text consistency or timestamp ordering, into rejection rules. See
[`OPEN_QUESTIONS.md`](../../OPEN_QUESTIONS.md) for those discussions.
