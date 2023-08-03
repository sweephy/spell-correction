from collections import Counter


class KeyboardDistanceUtil:
    qwertyKeyboardArray = [
        ['`','1','2','3','4','5','6','7','8','9','0','-','='],
        ['q','w','e','r','t','y','u','i','o','p','[',']','\\'],
        ['a','s','d','f','g','h','j','k','l',';','\''],
        ['z','x','c','v','b','n','m',',','.','/'],
        ['', '', ' ', ' ', ' ', ' ', ' ', '', '']
        ]

    turkish_qwertyKeyboardArray = [
        ['`','1','2','3','4','5','6','7','8','9','0','-','='],
        ['q','w','e','r','t','y','u','i','o','p','ğ','ü','\\'],
        ['a','s','d','f','g','h','j','k','l','ş','i','\''],
        ['z','x','c','v','b','n','m','ö','ç','.'],
        ['', '', ' ', ' ', ' ', ' ', ' ', '', '']
        ]

    qwertyShiftedKeyboardArray = [
        ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+'],
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?'],
        ['', '', ' ', ' ', ' ', ' ', ' ', '', '']
        ]

    layoutDict = {'QWERTY': (qwertyKeyboardArray, qwertyShiftedKeyboardArray)}
    keyboardArray = qwertyKeyboardArray
    shiftedKeyboardArray = qwertyShiftedKeyboardArray

    def array_for_char(self, c):
        if True in [c in r for r in self.keyboardArray]:
            return self.keyboardArray
        elif True in [c in r for r in self.shiftedKeyboardArray]:
            return self.keyboardArray
        else:
            raise ValueError(c + " not found in any keyboard layouts")

    # Finds a 2-tuple representing c's position on the given keyboard array.  If
    # the character is not in the given array, throws a ValueError
    @staticmethod
    def get_character_coord(c, array):
        row = -1
        column = -1
        for r in array:
            if c in r:
                row = array.index(r)
                column = r.index(c)
                return row,column
        raise ValueError(c + " not found in given keyboard layout")

    # Finds the Euclidean distance between two characters, regardless of whether
    # they're shifted or not.
    def euclidean_keyboard_distance(self, c1, c2):
        coord1 = self.get_character_coord(c1, self.array_for_char(c1))
        coord2 = self.get_character_coord(c2, self.array_for_char(c2))
        return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**(0.5)

    @staticmethod
    def typing_distance(keyboard, word):
        a = keyboard.find(word[0][:1])

        res=0
        for i in word:
            position = keyboard.find(i)
            if position != a:
                res += abs(a-position)
            a = position
        return res

    @staticmethod
    def get_char_freq_indexes(str_: str) -> {}:
       str_char_freq = {}
       for index, char in enumerate(str_):
          if str_char_freq[char] not in str_char_freq:
             str_char_freq[char] = {"indexes": [index] , "count": 1}
          elif str_char_freq[char] in str_char_freq:
             str_char_freq[char]["indexes"].append(index)
             str_char_freq[char]["count"] += 1

       return str_char_freq


if __name__ == '__main__':
    util = KeyboardDistanceUtil()
    res = util.euclidean_keyboard_distance('e', 't')
    print(res/10)
