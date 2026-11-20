# Lyricsfile

Lyricsfile is an open lyrics format based on YAML. It is easy to read and edit,
while supporting plain, line-synced, and word-synced lyrics.

Lyricsfile was introduced in
[LRCGET 2.0.0](https://github.com/tranxuanthang/lrcget/releases/tag/2.0.0)
and is supported by LRCGET and LRCLIB.

> [!WARNING]
> Lyricsfile 1.0 is still a draft and may change.

## Example

Files use the `.lyricsfile.yaml` extension.

```yaml
version: '1.0'

metadata:
  title: 'Song Title'
  artist: 'Artist Name'
  duration_ms: 245000

lines:
  - text: 'A synchronized lyric line'
    start_ms: 12000
    end_ms: 15500
    words:
      - text: 'A '
        start_ms: 12000
        end_ms: 12800
      - text: 'synchronized '
        start_ms: 12800
        end_ms: 14000
      - text: 'lyric '
        start_ms: 14000
        end_ms: 14800
      - text: 'line'
        start_ms: 14800
        end_ms: 15500

plain: |
  A synchronized lyric line
```

## Documentation

- [Draft specification](SPECIFICATION.md)
- [Open design questions](OPEN_QUESTIONS.md)
- [Examples](examples/)
- [Contributing](CONTRIBUTING.md)

The original [`LYRICSFILE_CONCEPT.md`](LYRICSFILE_CONCEPT.md) is kept for
reference. The draft specification is the current source of truth.

## Project Goals

- Keep lyrics files easy to read and edit without special tools.
- Support unsynchronized, line-synchronized, and word-synchronized lyrics.
- Support overlapping vocals.
- Make it practical for different apps and libraries to use the same files.
- Develop the format through open discussion and contributions.

## Proposed Reading Annotations

The draft now describes optional `readings` spans on lines or words: for example,
annotating only `食` in `食べる` with `た`. Base text and timing are unchanged.
This is a proposal for review, not a claim of deployed reader support.

- [Reading rules and Unicode offsets](SPECIFICATION.md#51-optional-reading-annotations)
- [Line-level example](examples/readings-line.lyricsfile.yaml)
- [Word-level example](examples/readings-words.lyricsfile.yaml)
- [Unicode example](examples/readings-unicode.lyricsfile.yaml)
- [Invalid examples](examples/invalid/README.md)

A small development checker covers annotation semantics (not the entire draft):

```sh
python -m pip install -r tools/requirements.txt
python tools/check_readings.py
python -m unittest discover -s tests -v
```

## Current Priorities

1. Review and stabilize the version 1.0 format.
2. Work through the questions in [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md).
3. Add more valid and invalid examples.
4. Add a schema when the main rules are settled.

Packages and converters can come later. For now, the focus is the format and
clear examples.

## Status And Compatibility

LRCGET and LRCLIB may currently accept files that do not follow every rule in
the draft. These differences will be documented as the format develops.

## License

The Lyricsfile specification, documentation, and examples are dedicated to the
public domain under [CC0 1.0 Universal](LICENSE). Contributions are accepted
under the same terms.

Future software packages may use a separate open source software license.
