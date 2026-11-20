import copy
from pathlib import Path
import unittest
from tools.check_readings import ReadingError,check_file,validate_readings

ROOT=Path(__file__).resolve().parents[1]


class Readings(unittest.TestCase):
    def test_valid_examples_and_existing_examples(self):
        for path in sorted((ROOT/'examples').glob('*.lyricsfile.yaml')):
            with self.subTest(path=path.name):check_file(path)

    def test_invalid_examples_fail(self):
        paths=list((ROOT/'examples/invalid').glob('*.lyricsfile.yaml'))
        self.assertGreaterEqual(len(paths),6)
        for path in paths:
            with self.subTest(path=path.name),self.assertRaises(ReadingError):check_file(path)

    def test_scalar_offsets_preserve_text_and_timing(self):
        document=check_file(ROOT/'examples/readings-unicode.lyricsfile.yaml')
        before=copy.deepcopy(document)
        validate_readings(document)
        self.assertEqual(document,before)
        self.assertEqual([line['text'][line['readings'][0]['start']:line['readings'][0]['end']] for line in document['lines']],['食','風','𠮷'])

    def test_word_offsets_are_local_and_leave_okurigana_untouched(self):
        document=check_file(ROOT/'examples/readings-words.lyricsfile.yaml')
        line=document['lines'][0]
        self.assertEqual(''.join(word['text'] for word in line['words']),line['text'])
        self.assertEqual(line['words'][1]['text'][0:1],'食')
        self.assertEqual(line['words'][1]['text'][1:],'べる')

    def test_adjoining_spans_and_custom_non_dictionary_readings_are_allowed(self):
        validate_readings({'lines':[{'text':'東京','readings':[
            {'start':0,'end':1,'text':'ひがし'}, {'start':1,'end':2,'text':'capital','language':'en'}]}]})

    def test_empty_and_missing_annotations_are_optional(self):
        validate_readings({'lines':[{'text':'Example','readings':[],'words':[{'text':'Example','readings':[]}]}]})
        validate_readings({'plain':'Plain text'})

    def test_reader_does_not_normalize_text_before_indexing(self):
        validate_readings({'lines':[{'text':'e\u0301風','readings':[{'start':2,'end':3,'text':'かぜ'}]}]})
        with self.assertRaises(ReadingError):
            validate_readings({'lines':[{'text':'é風','readings':[{'start':2,'end':3,'text':'かぜ'}]}]})

    def test_boolean_negative_string_null_and_surrogate_offsets_rejected(self):
        for start,end in [(True,2),(-1,1),('0',1),(0,None),(2,1)]:
            with self.subTest(start=start,end=end),self.assertRaises(ReadingError):
                validate_readings({'lines':[{'text':'食べる','readings':[{'start':start,'end':end,'text':'た'}]}]})
        with self.assertRaises(ReadingError):
            validate_readings({'lines':[{'text':'\ud800','readings':[{'start':0,'end':1,'text':'x'}]}]})
