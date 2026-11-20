# Invalid reading annotations

These documents are parseable YAML, but violate the proposed reading rules.
They are negative fixtures, not examples to copy into lyric collections.

| File | Expected error |
| --- | --- |
| `empty-range.lyricsfile.yaml` | `start` must be less than `end`. |
| `negative-offset.lyricsfile.yaml` | Offsets must be nonnegative. |
| `blank-reading.lyricsfile.yaml` | A pronunciation cannot be blank. |
| `boolean-offset.lyricsfile.yaml` | YAML booleans are not integer offsets. |
| `out-of-bounds.lyricsfile.yaml` | The range exceeds the three scalar values in `食べる`. |
| `overlapping-spans.lyricsfile.yaml` | Reading spans cannot overlap. |
| `conflicting-levels.lyricsfile.yaml` | A line cannot supply both line and word readings. |
| `inconsistent-word-text.lyricsfile.yaml` | Annotated words must reconstruct line text exactly. |

Run `python -m unittest discover -s tests -v` to confirm that these are rejected.
Passing an invalid file explicitly to `tools/check_readings.py` also returns a
nonzero exit status and identifies the erroneous field.
