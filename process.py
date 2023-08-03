import nltk
import ssl
from neuspell import BertChecker, CnnlstmChecker
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from core.preparation.basicClean.process import BasicCleaning
from core.preprocess.detection.cleaning_type import TypeDetection
from utils.strDifferenceUtil import StringDifferenceUtil
import os
import warnings
from spacy.vocab import Vocab
import spacy

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


class TypoWordObject:
    index: str
    wrong: str
    correct: str

    def __init__(self, index, wrong_word, correct_word):
        self.index = index
        self.wrong = wrong_word
        self.correct = correct_word


class TypoFixWithTransformers:
    nlp = spacy.load("en_core_web_lg")
    words = set(nlp.vocab.strings)
    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-large-finetuned-conll03-english")
    model = AutoModelForTokenClassification.from_pretrained("xlm-roberta-large-finetuned-conll03-english")
    ner_tagger = pipeline("ner", model=model, tokenizer=tokenizer)
    checker_bert = BertChecker()
    checker_bert.from_pretrained()
    found_typos = {}

    def __init__(self, _data: pd.DataFrame = None, col_types_dict=None):
        if _data is not None and col_types_dict is not None:
            null_cleaner = BasicCleaning()
            _data, dropped_null_values, dropped_rows, dropped_cols = null_cleaner.drop_null_and_invalid(_data)
            self.df = _data
            self.col_dict = self.get_col_types()

    def fix(self):
        for idx, column in enumerate(self.df.columns):
            if self.col_dict[column] == 'text':
                for row in self.df.values:
                    value = row[idx]
                    starts = self.start_indexes_of_tokens(value=value)
                    typos = self.detect_typo(value=value, starts=starts)
                    self.found_typos[idx] = typos

        return self.found_typos

    def detect_typo(self, value, starts):
        typos = []
        str_diff_util = StringDifferenceUtil()
        w_tokens, w_tags = str_diff_util.get_tokens_tags(value)
        ner_df, correct = self.correct(value)
        c_tokens, c_tags = str_diff_util.get_tokens_tags(correct)
        tags = self.get_tags_spacy(value)
        for idx, token in enumerate(w_tokens):
            if not ner_df.empty:
                starts_ = [starts[idx]]  # [0]
                found_ = ner_df[ner_df['start'].isin(starts_)]
                total_rows = found_.shape[1]
                if token != c_tokens[idx]:
                    tag = w_tags[idx][1]
                    if (tag == 'NN' or tag == 'NNS' or tag == 'NNP' or tag == 'NNPS') and total_rows > 0:
                        typo = TypoWordObject(index=idx, wrong_word=token, correct_word=c_tokens[idx])
                        typos.append(typo)
                    elif self.check_vocab(token):
                        c_tokens[idx] = token
                    else:
                        typo = TypoWordObject(index=idx, wrong_word=token, correct_word=c_tokens[idx])
                        print('typo:', typo.correct, typo.wrong)
                        typos.append(typo)
        return typos

    @staticmethod
    def start_indexes_of_tokens(value):
        span_generator = nltk.WhitespaceTokenizer().span_tokenize(value)
        spans = [span for span in span_generator]
        starts = [span[0] for span in spans]
        return starts

    def correct(self, wrong):
        correct = self.checker_bert.correct(wrong)
        outputs = self.ner_tagger(wrong)
        ner_df = pd.DataFrame(outputs)
        return ner_df, correct

    def get_col_types(self):
        type_checker_obj = TypeDetection()
        col_types = type_checker_obj.type_checker(df=self.df)
        col_dict = dict(zip(self.df.columns, col_types))
        return col_dict

    def check_vocab(self, word):
        if word in self.words:
            return True
        else:
            return False

    def get_tags_spacy(self, text):
        doc = self.nlp(text)
        tags = []
        for token in doc:
            tags.append((token.pos_, token.tag_))
        tag_df = pd.DataFrame(tags)
        return tag_df


'''
#df = pd.read_csv('/Users/ertugdilek/Desktop/Sweephy/deduplication-service/test_datasets/hospital.csv', ';')
df = pd.read_csv('/Users/ertugdilek/Desktop/Sweephy/POC/juphy_prepared.csv', ',')
df = df.loc[df['lang'] == 'en']

types = TypeDetection()
fixer = TypoFixWithTransformers(_data=df)
found_typos = fixer.fix()
print(found_typos)
'''
