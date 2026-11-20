"""Development checks for the proposed reading extension, not a full validator."""
import argparse
from pathlib import Path
import sys
import yaml


class ReadingError(ValueError):
    pass


class SafeLoader(yaml.SafeLoader):
    def compose_node(self, parent, index):
        if self.check_event(yaml.AliasEvent):
            raise ReadingError('YAML aliases are not supported by this checker')
        return super().compose_node(parent, index)

    def construct_mapping(self, node, deep=False):
        keys=set()
        for key_node, _ in node.value:
            key=self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ReadingError('Mapping keys must be strings')
            if key in keys:
                raise ReadingError(f'Duplicate YAML key: {key}')
            keys.add(key)
        return super().construct_mapping(node, deep=deep)


def _sequence(value, where):
    if not isinstance(value, list):
        raise ReadingError(f'{where} must be a sequence')
    return value


def _unicode(value, where):
    if not isinstance(value, str) or any(0xD800 <= ord(c) <= 0xDFFF for c in value):
        raise ReadingError(f'{where} must be a Unicode string without surrogates')
    return value


def _readings(unit, where):
    if not isinstance(unit, dict):
        raise ReadingError(f'{where} must be a mapping')
    readings=_sequence(unit.get('readings', []), where+'.readings')
    if not readings:
        return False
    base=_unicode(unit.get('text'), where+'.text')
    previous_end=0
    for index, reading in enumerate(readings):
        label=f'{where}.readings[{index}]'
        if not isinstance(reading, dict):
            raise ReadingError(f'{label} must be a mapping')
        start,end=reading.get('start'),reading.get('end')
        if type(start) is not int or type(end) is not int:
            raise ReadingError(f'{label}: start/end must be integers, not booleans or strings')
        if not 0 <= start < end <= len(base):
            raise ReadingError(f'{label}: expected 0 <= start < end <= {len(base)} Unicode scalar values')
        if start < previous_end:
            raise ReadingError(f'{label}: reading spans must be ordered and nonoverlapping')
        previous_end=end
        if not _unicode(reading.get('text'),label+'.text').strip():
            raise ReadingError(f'{label}.text must not be blank')
        if 'language' in reading and not _unicode(reading['language'],label+'.language').strip():
            raise ReadingError(f'{label}.language must not be blank')
    return True


def validate_readings(document):
    if not isinstance(document,dict):
        raise ReadingError('Document must be a mapping')
    for index,line in enumerate(_sequence(document.get('lines',[]),'lines')):
        label=f'lines[{index}]'
        line_readings=_readings(line,label)
        words=_sequence(line.get('words',[]),label+'.words')
        word_readings=False
        for j,word in enumerate(words):
            word_readings=_readings(word,f'{label}.words[{j}]') or word_readings
        if line_readings and word_readings:
            raise ReadingError(f'{label}: use line readings or word readings, not both')
        if (line_readings or word_readings) and words:
            base=_unicode(line.get('text'),label+'.text')
            joined=''.join(_unicode(word.get('text'),label+'.words.text') for word in words)
            if joined != base:
                raise ReadingError(f'{label}: annotated word text must concatenate exactly to line text')


def check_file(path):
    data=Path(path).read_bytes()
    if len(data)>1024*1024:
        raise ReadingError('Example exceeds the 1 MiB checker limit')
    document=yaml.load(data.decode('utf-8'),Loader=SafeLoader)
    validate_readings(document)
    return document


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files',nargs='*',type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    files=args.files or sorted((root/'examples').glob('*.lyricsfile.yaml'))
    failed=False
    for path in files:
        try:check_file(path)
        except (ReadingError,yaml.YAMLError,UnicodeError,OSError) as error:
            print(f'{path}: {error}',file=sys.stderr);failed=True
    if not failed:print(f'Checked reading annotations in {len(files)} files (not full draft validation).')
    return int(failed)


if __name__=='__main__':
    raise SystemExit(main())
