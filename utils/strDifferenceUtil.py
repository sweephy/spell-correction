from core.preparation.spellCorrection.serializers import TypoSerializer, DifferenceSerializer, DifferenceEnum
import nltk
import time


class StringDifferenceUtil:

	nltk_plural_tag_dict = [
		'NNS',
		'NNPS',
	]
	str1 = ''
	str2 = ''

	def singularize_strings(self, str1: str, str2: str, tag1: str, tag2: str):
		self.str1 = self.singular(str1, tag1)
		self.str2 = self.singular(str2, tag2)

	@staticmethod
	def get_tokens_tags(value):
		# Tags & Tokens
		tokens = nltk.word_tokenize(value)
		tags = nltk.pos_tag(tokens)

		return tokens, tags

	def get_strings(self):
		return self.str1, self.str2

	def singular(self, str_: str, tag: str):
		if tag in self.nltk_plural_tag_dict:
			'''
			if str_[len(str_) - 3: -1] == 'ies':
				str_ = str_.rstrip('ies')
				str_ = str_ + 'y'
			'''
			
			str_ = str_.rstrip('s')
			return str_

	@staticmethod
	def find_lcs(str1: str, str2: str) -> str:
		m = len(str1)
		n = len(str2)
		matrix = [[0] * (n + 1) for x in range(m + 1)]

		# Building the mtrix in bottom-up way
		for i in range(m + 1):
			for j in range(n + 1):
				if i == 0 or j == 0:
					matrix[i][j] = 0
				elif str1[i - 1] == str2[j - 1]:
					matrix[i][j] = matrix[i - 1][j - 1] + 1
				else:
					matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1])

		index = matrix[m][n]

		lcs_algo = [""] * (index + 1)
		lcs_algo[index] = ""

		i = m
		j = n
		while i > 0 and j > 0:

			if str1[i - 1] == str2[j - 1]:
				lcs_algo[index - 1] = str1[i - 1]
				i -= 1
				j -= 1
				index -= 1

			elif matrix[i - 1][j] > matrix[i][j - 1]:
				i -= 1
			else:
				j -= 1

		lcs = "".join(lcs_algo)
		return lcs

	def get_differences_between_left_right(self, str1: str, str2: str):
		differences = []
		start_lcs = time.time()
		lcs = self.find_lcs(str1, str2)
		print('lcs:', time.time() - start_lcs)
		str1_len = len(str1)
		str2_len = len(str2)

		processed = []
		lcs_ptr = str_ptr = 0
		while str_ptr < str1_len:
			if lcs_ptr == len(lcs):
				break

			if lcs[lcs_ptr] == str2[str_ptr]:
				lcs_ptr += 1
				str_ptr += 1
				continue
			elif lcs[lcs_ptr] != str2[str_ptr]:
				if lcs_ptr == 0:
					wrong_letter = str2[str_ptr]
					wrong_index = str_ptr
					difference = DifferenceSerializer(cause=DifferenceEnum.extra, wrong_index=wrong_index,
						wrong_letter=wrong_letter, current=str1[lcs_ptr], previous= str1[lcs_ptr - 1])
					differences.append(difference)
					str_ptr += 1
					continue
				else:
					wrong_letter = str2[str_ptr]
					wrong_index = str_ptr
					difference = DifferenceSerializer(cause=DifferenceEnum.wrong, wrong_index=wrong_index,
						wrong_letter=wrong_letter, current=str1[lcs_ptr], previous= str1[lcs_ptr - 1])
					differences.append(difference)
					processed.append(wrong_index)
					str_ptr += 1
					continue

		return differences


if __name__ == '__main__':
	util = StringDifferenceUtil()
	#util.singularize_strings('deneme', 'denrme', )
	#str1, str2 = util.get_strings()
	differences = util.get_differences_between_left_right('deneme', 'denrme')
	print(differences[0])











