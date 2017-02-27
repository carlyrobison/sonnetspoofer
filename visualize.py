import preprocess
import heapq
from collections import defaultdict
import representation as rep


'''
- The next section of this project deals with interpreting and visualizing the learned model. Our goal is to
interpret what the hidden states and transitions capture about the data. Use the learned observation matrix
and transition matrix to determine what words associate most with each hidden state, and how the hidden
states interact with each other. Do the hidden states represent parts of speech, stressed or unstressed words,
number of syllables? What about anything else you can think of? You may use any open source tools to
help you perform some of the analysis such as NLTK.
-In your report, you should explain your interpretation of how a Hidden Markov Model learns patterns
in Shakespeare's texts. You should briefly elaborate on the methods you used to analyze the model. In
addition, for at least 5 hidden states give a list of the top 10 words that associate with this hidden state and
state any common features these groups. Furthermore, try to interpret and visualize the learned transitions
between states. A possible suggestion is to draw a transition diagram of your markov model and give descriptive
names to the sates. Feel free to be creative with your visualizations, but remember that accurately
representing data is still your primary objective. Your figures, tables, and diagrams should contribute to a
discussion about your model.
'''

def get_popular_words(HMM, word_dict):
	for i in range(HMM.L): # for each hidden state
		ordering = HMM.O[i]

		# construct a dictionary of probs
		d = defaultdict(int)
		for j in range(len(ordering)): # for each word
			word = rep.number_to_word(j, word_dict)
			if word is not None:
				d[word] = ordering[j]
		print "state", i, "\t words:", heapq.nlargest(10, d, key=d.__getitem__)

if __name__ == '__main__':
	model, word_dict = preprocess.load_model(5, 25, 10)
    #print HMM_sonnet.A 
    #print HMM_sonnet.O