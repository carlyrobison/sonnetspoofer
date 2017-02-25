import preprocess
import pronouncing as pron
import random
import representation as rep
import numpy as np

LINES_IN_SONNET = 14


def get_hidden_state(HMM, word, word_dict):
    num = rep.word_to_number(word, word_dict)
    state_probs = [l[num] for l in HMM.O] # get the hidden state distribution
    normalized = [s/sum(state_probs) for s in state_probs]
    return np.random.choice(range(HMM.L), p=normalized)

def prettify_sonnet(sonnet):
    '''Capitalizes the first word of each line, adds punctuation.
    Takes a sonnet as a list of strings/lines.'''
    prettified = []
    for i in range(len(sonnet)):
        em = sonnet[i]
        em = em[0].upper() + em[1:]
        if i != LINES_IN_SONNET - 1:
            em += ','
        else:
            em += '.'
        prettified.append(em)
    return prettified

def make_simple_sonnet(HMM, word_dict):
    '''Generates a sonnet of length 14 with 10 words in each line'''
    emission = []
    for i in range(LINES_IN_SONNET):
        em = HMM.generate_emission(10)
        em = rep.numbers_to_words(em, word_dict)
        em = em.split(' ')
        emission += [' '.join(em)]
    return prettify_sonnet(emission)

def make_ramble_sonnet(HMM, word_dict):
    '''Generates a sonnet of length 14 with 10 words in each line'''
    emission = []
    total_em = HMM.generate_emission(10 * LINES_IN_SONNET)
    for i in range(LINES_IN_SONNET):
        em = total_em[10 * i: 10 * (i + 1)]
        em = rep.numbers_to_words(em, word_dict)
        em = em.split(' ')
        emission += [' '.join(em)]
    return prettify_sonnet(emission)

def make_syllabic_sonnet(HMM, word_dict):
    '''Generates a sonnet of length 14 with 10 /syllables/ in each line'''
    emission = []

    for i in range(LINES_IN_SONNET):
        em = HMM.generate_emission(10) # generate more syllables than we need
        em = rep.numbers_to_words(em, word_dict)
        em = em.split(' ')
        num_syls_left = 10
        line = []
        while (num_syls_left > 0): # tolerate 10+ syllable lines
            line.append(em[0]) # add the next word
            num_syls_left -= preprocess.num_syllables(em[0]) # decrement by the number of syllables of that word
            em = em[1:] # take the word off the queue
        emission += [' '.join(line)]
    return prettify_sonnet(emission)

def get_rhyming_pair(word_dict):
    '''Generates a pair of rhymes for words that exist in these sonnets'''
    while True:
        w = random.choice(word_dict.keys()) # grab a random word
        rhymes = pron.rhymes(w)
        rhymes = [k for k in rhymes if k in word_dict]
        if len(rhymes) > 0:
            return [w, random.choice(rhymes)]

def get_rhymes(word_dict):
    '''Get the last words for rhyming schemes'''
    rhymes = []
    for i in range(7):
        rhymes.append(get_rhyming_pair(word_dict))
    # force it into the quatrain rhyme scheme
    rhyme_scheme = [rhymes[0][0], rhymes[1][0], rhymes[0][1], rhymes[1][1],
                    rhymes[2][0], rhymes[3][0], rhymes[2][1], rhymes[3][1],
                    rhymes[4][0], rhymes[5][0], rhymes[4][1], rhymes[5][1],
                    rhymes[6][0], rhymes[6][1]]
    return rhyme_scheme

def make_rhyming_sonnet(HMM, word_dict):
    '''Just adds the rhyming words to the end of the sonnet'''
    emission = []
    rhymes = get_rhymes(word_dict)
    for i in range(LINES_IN_SONNET):
        em = HMM.generate_emission(10) # more than we need
        em = rep.numbers_to_words(em, word_dict)
        em = em.split(' ')
        rhyme = rhymes[i]
        num_syls_left = 10 - preprocess.num_syllables(rhyme)
        line = []
        while (num_syls_left > 0): # tolerate 10+ syllable lines
            line.append(em[0]) # add the next word
            num_syls_left -= preprocess.num_syllables(em[0]) # decrement by the number of syllables of that word
            em = em[1:] # take the word off the queue
        line.append(rhyme)
        emission += [' '.join(line)]
    return prettify_sonnet(emission)

def make_seeded_sonnet(HMM, word_dict, seed):
    '''Generates a sonnet of length 14 where every line starts with the seed'''
    emission = []

    for i in range(LINES_IN_SONNET):
        em = HMM.generate_seeded_emission(9, get_hidden_state(HMM, seed, word_dict), word_dict) # generate more syllables than we need
        em = rep.numbers_to_words(em, word_dict)
        em = em.split(' ')
        emission += [seed + ' ' + ' '.join(em)]
    return prettify_sonnet(emission)

'''also TODO: generate backwards from rhyming word'''

if __name__ == '__main__':
    HMM_sonnet, word_dict = preprocess.load_model(5, 25, 10)

    gen = HMM_sonnet.generate_seeded_emission(10, get_hidden_state(HMM_sonnet, 'thou', word_dict), word_dict)

    emission = make_seeded_sonnet(HMM_sonnet, word_dict, 'thou')
    for line in emission:
        print line