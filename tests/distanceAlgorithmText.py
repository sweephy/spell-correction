import jellyfish as distance
from fastDamerauLevenshtein import damerauLevenshtein

if __name__ == '__main__':
	damerau_score = distance.levenshtein_distance('word', 'wordx')
	print('damerau_score:', damerau_score)

	res = damerauLevenshtein('wodddersx', 'woderdx', similarity= True)
	print(res)
