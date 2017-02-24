def word_to_number(word, word_dict):
    return word_dict[word]

def words_to_numbers(sonnets):
    '''Converts a sonnet to a list of lists
    with each word represented as a number'''
    word_dict = {}
    counter = 0
    sonnet_nums = []
    for sonnet in sonnets:
        sonnet_num = []
        for line in sonnet:
            sonnet_line = []
            for word in line:
                l_word = word.lower()
                if l_word not in word_dict:
                    word_dict[l_word] = counter
                    counter += 1
                sonnet_line += [word_dict[l_word]]
            sonnet_num += [sonnet_line]
        sonnet_nums += [sonnet_num]
    return sonnet_nums, word_dict

def number_to_word(num, word_dict):
    '''Converts a number to a word'''
    for word in word_dict:
        if word_dict[word] == num:
            return word
    return None

def numbers_to_words(line, word_dict):
    '''Converts a generated sonnet of numbers into a sonnet with
    words'''
    ret = ""
    for i in range(len(line)):
        num = line[i]
        ret += number_to_word(num, word_dict)
        if i != len(line)-1:
            ret += " "
    return ret