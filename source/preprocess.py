
import HMM
from get_cmudict import read_cmudict
from nltk.corpus import cmudict
from countsyl import count_syllables
import representation as rep

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
    Outputs a list of sonnets, with each sonnet a list of lines; 
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

def read_anything(filename):
    lines = []
    with open(filename) as f:
        while True:
            line = f.readline()
            if line == '':
                break
            if line != '\n':
                # it's a line with text
                line = line.strip()
                line = line.replace('-', ' ')   # split hyphenated words
                line = line.strip()
                # get rid of punctuation
                line = line.replace('.', '')
                line = line.replace(',', '')
                line = line.replace(':', '')
                line = line.replace('(', '')
                line = line.replace(')', '')
                line = line.replace('!', '')
                line = line.replace('?', '')
                line = line.replace('"', '')
                line = line.replace("'", '')
                if line != '':
                    lines += [line.split(' ')]
    return [lines]

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
    '''Returns the number of syllables in a word'''
    if word.lower() in cmu:
        cmu_listing = listing(word)
        return len(stresses(cmu_listing))
    else:
        if len(word) == 0:
            return 0    # temporary fix TODO
        return count_syllables(word)

def listing(cmu_word):
    '''Assumes cmu_word is in cmudict.'''
    return cmu[cmu_word.lower()][0]

def load_model(n_states, n_poems, n_iters, backwards=False):
    '''Loads a model of a sonnet'''
    sonnets = read_shakespeare("../project2data/shakespeare.txt")
    sonnet_nums, word_dict = rep.words_to_numbers(sonnets[:n_poems])
    if backwards:
        sonnet_train = [item[::-1] for sublist in sonnet_nums for item in sublist]
    else:
        sonnet_train = [item for sublist in sonnet_nums for item in sublist]
    return HMM.unsupervised_HMM(sonnet_train, n_states, n_iters), word_dict

def load_any_model(filename, n_states, n_iters, backwards=False):
    '''Loads a model of a sonnet'''
    things = read_anything(filename)
    print things
    thing_nums, word_dict = rep.words_to_numbers(things)
    if backwards:
        thing_train = [item[::-1] for sublist in thing_nums for item in sublist]
    else:
        thing_train = [item for sublist in thing_nums for item in sublist]
    return HMM.unsupervised_HMM(thing_train, n_states, n_iters), word_dict



if __name__ == '__main__':
    # HMM_sonnet = load_model(10, 154, 25)
    print read_anything('../project2data/Alexander_Hamilton.txt')

