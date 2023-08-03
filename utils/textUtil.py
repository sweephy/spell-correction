import pandas as pd
from core.preparation.spellCorrection.utils.strDifferenceUtil import StringDifferenceUtil


class TextUtil:
	word_dict = {}
	str_diff_util = StringDifferenceUtil()

	def dataframe_to_word_counts(self, df_: pd.DataFrame, types) -> {}:
		for row in df_.iterrows():
			idx = row[0]
			values = row[1]
			for column_index, val in enumerate(values):
				if types[column_index] == 'text':
					self.save_words_and_row_index(val, idx, column_index)
		return self.word_dict

	def save_words_and_row_index(self, text, index, column_index):
		tokens, tags = self.str_diff_util.get_tokens_tags(text)
		#split_text = text.split()
		for idx, word in enumerate(tokens):
			word_ = word
			tag = tags[idx][1]
			if tag in self.str_diff_util.nltk_plural_tag_dict :
				word_ = self.str_diff_util.singular(word_,tag)

			if word_ not in self.word_dict:
				self.word_dict[word_] = {'tag': tag, 'count': 0, 'row_indexes': [], 'column_indexes': [], 'word_indexes': []}
				self.add_word_frequency(word_, index, column_index, idx)
			else:
				self.add_word_frequency(word_, index, column_index, idx)

	def add_word_frequency(self, word, row_index, column_index, word_index):
		self.word_dict[word]['count'] += 1
		self.word_dict[word]['row_indexes'].append(row_index)
		self.word_dict[word]['column_indexes'].append(column_index)
		self.word_dict[word]['word_indexes'].append(word_index)


if __name__ == '__main__':
	from core.preprocess.detection.cleaning_type import TypeDetection
	csv = pd.read_csv('/Users/ertugdilek/Desktop/Sweephy/deduplication-service/test_datasets/hospital.csv', ';')
	detector = TypeDetection()
	types = detector.type_checker(csv)
	util = TextUtil()
	word_dict = util.dataframe_to_word_counts(csv, types)
	print(word_dict)
