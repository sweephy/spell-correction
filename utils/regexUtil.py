import re
import pandas as pd
import time


class RegexUtil:
    def prepare(self, df_: pd.DataFrame = None, texts: [str] = None, ):
        start_time = time.time()
        if df_ is None and texts is None:
            raise ValueError('Parameters emtpy')

        if df_ is not None:
            prepared_df = self.prepare_dataframe(df_)
            return prepared_df
        elif texts is not None:
            prepared_texts = self.prepare_texts(texts)
            return prepared_texts

        end_time = time.time() - start_time
        print(end_time)

    def prepare_dataframe(self, df_: pd.DataFrame, types):
        for idx, column in enumerate(df_.columns):
            if types[idx] == 'text':
                df_[column] = df_[column].apply(lambda x: self.text_regex_v2(x))
        return df_

    def prepare_texts(self, texts: [str]):
        prepared_texts = []
        for text in texts:
            res = self.text_regex_v2(text)
            prepared_texts.append(res)
        return prepared_texts

    @staticmethod
    def remove_link(text: str):
        return re.sub(r'http\S+', '', text)

    def text_regex(self, text):
        if isinstance(text, str):
            try:
                text_ = self.remove_link(text)
                text_ = re.sub(r'()#\w+', r'\1', text_)
                text_ = re.sub(r'()\'\w+', r'\1', text_)
                # new_text = re.sub(r'()@\'\w+', r'\1', new_text) #removing @ symbol from user tags
                text_ = re.sub(r'\w*\d\w*', '', text_)
                text_ = re.sub('[^a-zA-Zğüşoöçı@]+', ' ', text_)
                return text_.lstrip()
            except Exception as error:
                raise error

    def text_regex_v2(self, text: str):
        if isinstance(text, str):
            try:
                text_ = self.remove_link(text)
                text_ = re.sub(r'[-a - zA - Z0–9 @: %._\+~  # =]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)', '', text_)
                text_ = self.deEmojify(text_)
                text_ = re.sub('[^a-zA-Zğüşoöçı@]+', ' ', text_)
                return self.remove_unnecessary_blanks(text_)
            except Exception as error:
                raise error

    @staticmethod
    def remove_unnecessary_blanks(text: str):
        text_ = text.strip()
        return text_

    @staticmethod
    def deEmojify(text):
        return text.encode('ascii', 'ignore').decode('ascii')

'''
if __name__ == '__main__':
    path_ = 'D:\sweephy\core\test_datasets\bankcustomer.csv'
    df = pd.read_csv(path_)
    util_ = RegexUtil()
    util_.prepare(df)
    '''

