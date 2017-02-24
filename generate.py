import preprocess
import pronouncing as pron
import random as r

LINES_IN_SONNET = 14


def generate_next_emission(HMM, l, seed):
    '''TODO: actually incorporate the seed'''
    ''' Generates an emission of length l, assuming that
    the starting state is the seed. 

    Arguments:
        HMM:        the model used to generate the emission
        l:          Length of the emission to generate.
        seed: the starting emission

    Returns:
        emission:   The randomly generated emission as a string.
    '''

    emission = []
    state = random.choice(range(self.L))

    for t in range(M):
        # Sample next observation.
        rand_var = random.uniform(0, 1)
        next_obs = 0

        while rand_var > 0:
            rand_var -= self.O[state][next_obs]
            next_obs += 1

        next_obs -= 1
        emission += [next_obs]

        # Sample next state.
        rand_var = random.uniform(0, 1)
        next_state = 0

        while rand_var > 0:
            rand_var -= self.A[state][next_state]
            next_state += 1

        next_state -= 1
        state = next_state

    return emission

def numbers_to_words(line, word_dict):
    '''Converts a generated sonnet of numbers into a sonnet with
    words'''
    ret = ""
    for i in range(len(line)):
        num = line[i]
        for word in word_dict:
            if word_dict[word] == num:
                ret += word
        if i != len(line)-1:
            ret += " "
    return ret

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
        em = HMM_sonnet.generate_emission(10)
        em = numbers_to_words(em, word_dict)
        em = em.split(' ')
        emission += [' '.join(em)]
    return prettify_sonnet(emission)

def make_ramble_sonnet(HMM, word_dict):
    '''Generates a sonnet of length 14 with 10 words in each line'''
    emission = []
    total_em = HMM_sonnet.generate_emission(10 * LINES_IN_SONNET)
    for i in range(LINES_IN_SONNET):
        em = total_em[10 * i: 10 * (i + 1)]
        em = numbers_to_words(em, word_dict)
        em = em.split(' ')
        emission += [' '.join(em)]
    return prettify_sonnet(emission)

def make_syllabic_sonnet(HMM, word_dict):
    '''Generates a sonnet of length 14 with 10 /syllables/ in each line'''
    emission = []

    for i in range(LINES_IN_SONNET):
        em = HMM_sonnet.generate_emission(10) # generate more syllables than we need
        em = numbers_to_words(em, word_dict)
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
        w = r.choice(word_dict.keys()) # grab a random word
        rhymes = pron.rhymes(w)
        rhymes = [k for k in rhymes if k in word_dict]
        if len(rhymes) > 0:
            return [w, r.choice(rhymes)]

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
    emission = []
    rhymes = get_rhymes(word_dict)
    for i in range(LINES_IN_SONNET):
        em = HMM_sonnet.generate_emission(10) # more than we need
        em = numbers_to_words(em, word_dict)
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

if __name__ == '__main__':
    HMM_sonnet, word_dict = preprocess.load_model(10, 50, 10)

    emission = make_rhyming_sonnet(HMM_sonnet, word_dict)
    for line in emission:
        print line