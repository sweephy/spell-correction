import jellyfish as distance
from fastDamerauLevenshtein import damerauLevenshtein

from core.preparation.spellCorrection.serializers import DifferenceEnum
from core.preparation.spellCorrection.utils.keyboardDistanceUtil import KeyboardDistanceUtil
from core.preparation.spellCorrection.utils.strDifferenceUtil import StringDifferenceUtil
from core.preparation.spellCorrection.utils.textUtil import TextUtil
from core.preparation.spellCorrection.utils.regexUtil import RegexUtil
from core.preparation.spellCorrection.process import TypoFixWithTransformers


class WordSimilarity:
	keyboard_util = KeyboardDistanceUtil()
	str_difference_util = StringDifferenceUtil()

	def create_candid_groups(self, word_dict: {}):
		"""
		@:param word_dict: generally coming from TextUtil class
		Example format: word_dict = {word: { count: 0 , row_indexes: [] }}

		@:return
		"""


		all_scores = {}
		for word in word_dict:
			scores = self.get_similar_word_groups(word, word_dict)

			# Score filtering could be unnecessary
			copy_scores = scores.copy()
			for key in copy_scores:
				if scores[key] < 0.5:
					del scores[key]

			self.scores = scores
			start = time.time()
			#normalized_scores = self.normalize_scores(self.scores, word)
			new_scores = self.optimize_scores(word,scores)
			for key in new_scores.copy():
				if new_scores[key] < 0.5:
					del new_scores[key]

			all_scores[word] = new_scores
			end = time.time() - start
			print(end)

		return all_scores

	def check_result(self, value, min, max):
		#(value - min) / (max - min)
		if value > 0.8:
			return value
		else:
			return None

	def normalize_scores(self, scores, word):
		values = scores.values()
		min_ = min(values)
		max_ = max(values)

		normalized_d = {key: self.check_result(v,  min_, max_) for (key, v) in scores.copy().items()}
		filtered = {k: v for k, v in normalized_d.items() if v is not None}
		return filtered

	def optimize_scores(self, word, scores):
		for score_key in scores:
			score_ = scores[score_key]
			start_difference = time.time()
			print('last word optimization:', word, score_key)
			differences = self.str_difference_util.get_differences_between_left_right(word, score_key)
			print('diff:', time.time() - start_difference)

			for difference in differences:
				if difference.cause != DifferenceEnum.extra:
					word_char = difference.current
					different_char = difference.wrong_letter
					start_kd = time.time()
					print('last difference:', word_char,different_char)
					res = self.keyboard_util.euclidean_keyboard_distance(word_char, different_char)/10 # Keyboard distance divided by 10 to normalize result
					print('kd:', time.time() - start_kd)
					scores[score_key] = score_ - res
		return scores


	def get_similar_word_groups(self, word, word_dict):
		"""
		:param word:
		:param word_dict:

		Variable scores:{} -> scores variable includes similarity scores for each word in word_dict for current word


		:return:
		"""

		scores = {}
		for w in word_dict:
			if w is not word:
				#jaro_winkler_score = distance.jaro_winkler_similarity(word, w)
				#damerau_score = distance.damerau_levenshtein_distance(word, w)
				res = damerauLevenshtein(word, w, similarity=True)
				scores[w] = res

		return scores


if __name__ == '__main__':
	from core.preprocess.detection.cleaning_type import TypeDetection
	import pandas as pd
	import time
	main_start = time.time()

	start = time.time()
	csv = pd.read_csv('/Users/ertugdilek/Desktop/Sweephy/deduplication-service/test_datasets/hospital.csv', ';')

	detector = TypeDetection()
	types = detector.type_checker(csv)

	regex_util = RegexUtil()
	regex_util.prepare_dataframe(csv, types)

	end = time.time() - start


	start = time.time()
	text_util = TextUtil()
	word_dict = text_util.dataframe_to_word_counts(csv, types)
	end = time.time() - start

	similarity = WordSimilarity()
	all_scores = similarity.create_candid_groups(word_dict=word_dict)
	print(all_scores)

	# key: Row index, value: [Column Indexes]
	possible_data_points = {}

	for score in all_scores:
		for word in all_scores[score]:
			row_indexes = word_dict[word]['row_indexes']
			column_indexes = word_dict[word]['column_indexes']
			word_indexes = word_dict[word]['word_indexes']
			for row in row_indexes:
				possible_data_points[row] = {'columns': set(column_indexes), 'target': score, 'word': word, 'word_indexes': set(word_indexes)}

	typo_fixer = TypoFixWithTransformers()
	for row in possible_data_points:
		possible_mistake = possible_data_points[row]
		for column_index in possible_data_points[row]['columns']:
			value = csv.iloc[row][column_index]
			starts = typo_fixer.start_indexes_of_tokens(value)
			typos = typo_fixer.detect_typo(value,starts)
			if len(typos) > 0:
				for typo in typos:
					if typo.index in possible_mistake['word_indexes'] and typo.correct == possible_mistake['target']:
						print(typos)


	#TypoFixWithTransformers()
	main_end = time.time() - start
	print(main_end)
	print('finished')
