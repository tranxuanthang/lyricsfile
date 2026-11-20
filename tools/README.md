# Reading annotation development checker

`check_readings.py` checks the proposed section 5.1 rules. It is not an official
parser, serializer, or full Lyricsfile 1.0 validator. It neither modifies files
nor creates a canonical representation or content hash.

It checks line/word reading lists, scalar-value ranges, ordering, overlap,
nonblank reading text, string language tags, annotation-level conflicts, and
exact word reconstruction for annotated lines. It rejects duplicate YAML keys,
custom tags, aliases, multiple YAML documents, and files larger than 1 MiB.

It does not check timing constraints, every metadata field, complete BCP 47 tag
syntax, grapheme-cluster boundaries, or all YAML nesting/resource limits. It is
for trusted development fixtures, not an untrusted-upload security boundary.

Use Python 3.10+ and install `tools/requirements.txt`. Without positional
arguments the checker reads top-level `examples/*.lyricsfile.yaml` (positive
fixtures). Explicit file arguments can include negative fixtures, which should
exit with an error. Unit tests automatically exercise the negative fixtures.
