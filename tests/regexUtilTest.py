import pandas as pd
import sys
sys.path.append('../../../../')
from core.preparation.spellCorrection.utils.regexUtil import RegexUtil

util = RegexUtil()
poc_texts_wrong_format = [
    '@nguyenthanhtamz @cctip io @cctip io draw eeth @ @ @ @ @ smart chain address🥺',
    '私も頑張らなきゃ！！！！ https://t.co/link", follow your dream',
    '**86,"Feeling crafty** 🛠️🧶⚒',
    '🔗 Check price: [https://t.co/test](https://t.co/test2)**',
    '@nguyenthanhtamz @cctip io @cctip io draw eeth @ @ @ @ @ smart chain address🥺',
]

poc_texts_correct_format = [
    '@nguyenthanhtamz @cctip io @cctip io draw eeth @ @ @ @ @ smart chain address',
    'follow your dream',
    'Feeling crafty',
    'Check price',
    '@nguyenthanhtamz @cctip io @cctip io draw eeth @ @ @ @ @ smart chain address',
]


def test_text_regex_method():
    for idx, test_text in enumerate(poc_texts_wrong_format):
        res = util.text_regex_v2(test_text)
        assert res == poc_texts_correct_format[idx]
    print('Regex test success!')

if __name__ == '__main__':
    test_text_regex_method()
