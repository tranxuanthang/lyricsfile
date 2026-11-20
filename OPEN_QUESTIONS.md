# Open Design Questions

Lyricsfile 1.0 is still a draft. These questions are listed here so we can work
through them over time. They do not all need answers right away.

## Highest Priority

These questions matter most for a stable 1.0 release.

1. **Unknown fields:** Should apps preserve fields they do not understand when
   saving a file?
2. **Required identity:** Should `metadata.title` and `metadata.artist` remain
   required when a Lyricsfile is already associated with an audio file?
3. **Global offset:** Is `offset_ms` added to timestamps, subtracted from them,
   or only used while editing?
4. **Missing end times:** Should a missing line or word `end_ms` be inferred
   from the next start time, the containing interval, or left entirely to the
   renderer?
5. **Word consistency:** Must concatenated word text exactly equal
   `line.text`, and what should happen when it does not?
6. **Version changes:** What can be added to version 1.0, and what requires a
   new version?
7. **YAML features:** Should aliases and anchors be forbidden? Should editing
   tools preserve comments?

## Timing And Rendering

- Must every word interval fit inside its containing line interval?
- Are overlapping words valid within one line?
- Are equal timestamps valid for zero-duration cues?
- Should timestamps be bounded by `metadata.duration_ms`?
- Should line order carry meaning when lines have equal start times?
- Is there a standard fallback for rendering a missing `end_ms`?

## Lyrics Model

- Should `lines` support non-vocal events such as section markers?
- How should multiple vocalists or simultaneous vocal parts be identified?
- Should translations and romanizations be first-class fields or extensions?
- Is `language` sufficient, and should it use BCP 47 instead of ISO 639-1?
- Can an instrumental track contain descriptive or structural text?
- Should empty strings and whitespace-only lyric lines be treated differently?

## Serialization And Distribution

- Should Lyricsfile define a media type?
- Are byte order marks permitted?
- Are line endings normalized when a file is rewritten?
- Is there a canonical serialization for hashing, signing, or fixtures?

## Conversion

- How should word synchronization be degraded when exporting to LRC?
- How should overlapping lines be represented in formats that do not support
  them?
- Should conversion use `plain` or derive text from synchronized lines?
- How should timestamp precision loss be reported?

## Discussing A Question

Use a separate GitHub Discussion or issue for each question. A small example
is often the clearest way to explain a problem or suggestion.
