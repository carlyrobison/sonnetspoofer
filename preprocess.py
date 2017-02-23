
import HMM

LINES_IN_SONNET = 14



'''
TODO:
    syllable processing
    punctuation/capitalization
    emphasis/accent/meter
    rhyming

Apparently there are a couple sonnets which don't have exactly 14 lines...
'''



def read_shakespeare(filename):
    '''
    Outputs a list of sonnets, with each sonnet a list of 14 lines; 
    and each line a list of words.
    '''
    sonnets = []
    with open(filename) as f:
        while True:
            line = f.readline()
            if line == '':
                break
            if line.strip().isdigit():
                # read the sonnet, putting it into a data structure
                sonnet = []
                for i in range(LINES_IN_SONNET):
                    sonnet += [f.readline().strip().split(' ')]
                    # TODO split into syllables here
                    #    got stuck on how to read from nltk cmudict
                sonnets += [sonnet]
    return sonnets

def words_to_numbers(sonnets):
    word_dict = {}
    counter = 0
    sonnet_nums = []
    for sonnet in sonnets:
        sonnet_num = []
        for line in sonnet:
            sonnet_line = []
            for word in line:
                if word not in word_dict:
                    word_dict[word] = counter
                    counter += 1
                sonnet_line += [word_dict[word]]
            sonnet_num += [sonnet_line]
        sonnet_nums += [sonnet_num]
    return sonnet_nums, word_dict

def numbers_to_words(line, word_dict):
    ret = ""
    for i in range(len(line)):
        num = line[i]
        for word in word_dict:
            if word_dict[word] == num:
                ret += word
        if i != len(line)-1:
            ret += " "
    return ret



if __name__ == '__main__':
    sonnets = read_shakespeare("project2data/shakespeare.txt")
    sonnet_nums, word_dict = words_to_numbers(sonnets)
    HMM_sonnet = HMM.unsupervised_HMM(sonnet_nums[0], 10, 200)
    em = HMM_sonnet.generate_emission(50)
    print em
    print len(em)
    print numbers_to_words(em, word_dict)