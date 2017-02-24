
import HMM
from get_cmudict import read_cmudict
from nltk.corpus import cmudict
from countsyl import count_syllables

LINES_IN_SONNET = 14
cmu = cmudict.dict()



'''
TODO:
    syllable processing
    punctuation/capitalization
    emphasis/accent/meter
    rhyming
        Use stresses function but pick up pronunciations as well.
        Rhyme defn: primary stressed vowel and everything after matches.

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
                while True:
                    line = f.readline().strip()
                    if line == '':  # for sonnets with the wrong number of lines
                        break
                    line = line.replace('-', ' ')   # split hyphenated words

                    # get rid of punctuation
                    line = line.replace('.', '')
                    line = line.replace(',', '')
                    line = line.replace(':', '')
                    line = line.replace('(', '')
                    line = line.replace(')', '')

                    # TODO split into syllables/bigrams here? how to do spaces?
                    #       how to choose which pronunciation from cmudict?

                    sonnet += [line.split(' ')]

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

def stresses(cmu_listing):
    '''Some words have multiple pronunciations.  
    The input is which pronuncation.
    E.g. [u'N', u'AE1', u'CH', u'ER0', u'AH0', u'L']
        for 'NATURAL'.
    '''
    stresses = ''
    syllables = []
    syllable = ''
    for item in cmu_listing:
        if item[-1].isdigit():
            stresses += item[-1]
            syllable += item[:-1]
            syllables += [syllable]
            syllable = ''
        else:
            syllable += item

    # At end, if last item did not end in a vowel, 
    # append to last syllable
    if not syllables[-1].isdigit():
        syllables[-1] += syllable

    return stresses

def num_syllables(word):
    if word.lower() in cmu:
        cmu_listing = listing(word)
        return len(stresses(cmu_listing))
    else:
        return count_syllables(word)

def listing(cmu_word):
    '''Assumes cmu_word is in cmudict.'''
    return cmu[cmu_word.lower()][0]



if __name__ == '__main__':
    sonnets = read_shakespeare("project2data/shakespeare.txt")
    for sonnet in sonnets:
        for line in sonnet:
            for item in line:
                print item, num_syllables(item)

    '''
    sonnet_nums, word_dict = words_to_numbers(sonnets)
    HMM_sonnet = HMM.unsupervised_HMM(sonnet_nums[0], 10, 200)
    em = HMM_sonnet.generate_emission(50)
    print em
    print len(em)
    print numbers_to_words(em, word_dict)
    '''