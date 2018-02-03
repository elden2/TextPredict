import random
import sys
from itertools import groupby
import pickle



#data
test = 'potato santa this is a test that I am using just to see if this works.  If this works.  If this works.  If This does not work not work not work not oh'

#Moby Dick
with open('Fitzgerald.txt', 'r') as temp:
	Fitz = temp.read().replace('\n', '')

# with open('moby.txt', 'r') as temp:
# 	Moby = temp.read().replace('\n', '')

# text = Fitz + Moby



class Tree(object):
	def __init__(self, data = 'as string', depth = 3, random = True):
		self.depth = depth
		self.data = data.split()
		self.dictionary = {}
		self.tripple = []
		self.target = []
		self.get_trip()
		self.pair_dictionary_tripples()
		self.doubles = []
		self.doubles_target = []
		self.dictionary_doubles = {}
		self.get_doubles()
		self.pair_dictionary_doubles()
		self.single_dictionary = {}
		self.single_pair()
		self.random = random
		self.error_count = [0,0,0,0] ##Number of tripples, doubles, singles, none used

	def get_trip(self):
		a = len(self.data)
		for i in range(0, a-self.depth):
			self.tripple.append(self.data[i]+' '+self.data[i+1]+' ' + self.data[i+2])
			self.target.append(self.data[i+3])

	def get_doubles(self):
		a = len(self.data)
		for i in range(0,a-2):
			self.doubles.append(self.data[i]+' '+self.data[i+1])
			self.doubles_target.append(self.data[i+2])

	def pair_dictionary_tripples(self):
		a = len(self.target)
		for i in range(0,a):
			if self.tripple[i] in self.dictionary:
				self.dictionary[self.tripple[i]].append(self.target[i])
			else:
				self.dictionary[self.tripple[i]] = [self.target[i]]

	def pair_dictionary_doubles(self):
		a = len(self.doubles_target)
		for i in range(0,a):
			if self.doubles[i] in self.dictionary_doubles:
				self.dictionary_doubles[self.doubles[i]].append(self.doubles_target[i])
			else:
				self.dictionary_doubles[self.doubles[i]] = [self.doubles_target[i]]


	def single_pair(self):
		a = len(self.data)
		for i in range(0, a-1):
			if self.data[i] in self.single_dictionary:
				self.single_dictionary[self.data[i]].append(self.data[i+1])
			else:
				self.single_dictionary[self.data[i]] = [self.data[i+1]]





	def common_word(self, L):
		if len(L) == 1 or len(L) == 2:
			return L[0]
		else:
			return max(groupby(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]


	def predict_word(self, key = 'three word form'):
		if key in self.dictionary.keys():
			# print 'yes three letter'
			self.error_count[0] += 1
			return self.common_word(self.dictionary[key])
		else:
			a = key.split()
			temp= a[1]+ ' ' + a[2]
			temp2 = a[2]
			# print temp2
			if temp in self.dictionary_doubles.keys():
				# print 'yes two letter'
				self.error_count[1] += 1
				return self.common_word(self.dictionary_doubles[temp])
			if a[2] in self.single_dictionary.keys():
					# print 'single word'
				self.error_count[2] += 1
				return self.common_word(self.single_dictionary[a[2]])
			self.error_count[3] += 1
			return self.dictionary[random.choice(dictionary.keys())][0]
			



	def get_promt(self, sentence, length = 3):
		a = sentence.split()
		prompt = ''
		for i in a[-(length):]:
			prompt += i + ' '
		return prompt



	def predict_sentence(self, initial = 'who knows what', chain_length = 3, parg_length = 100):
		sentence = initial
		for i in range(0, parg_length):
			if self.random:
				if i%15:
					sentence += ' ' + self.dictionary[random.choice(self.dictionary.keys())][0]
			prompt = self.get_promt(sentence, length= chain_length)
			sentence += ' ' + self.predict_word(prompt)
		return sentence
			


test = Tree(Fitz)



# pickle_out = open("moby_dick_tripple.pickle", "wb")
# pickle.dump(a.dictionary, pickle_out)
# pickle_out.close()

# pickle_out = open("moby_dick_double.pickle", "wb")
# pickle.dump(a.dictionary_doubles, pickle_out)
# pickle_out.close()

# pickle_out = open("moby_dick_singles.pickle", "wb")
# pickle.dump(a.single_dictionary, pickle_out)
# pickle_out.close()

# print len(a.dictionary_doubles)
# print len(a.dictionary)

print test.predict_sentence('Once upon a time')
print test.error_count





class Predictor2(object):
	def __init__(self, data_single = "moby_dick_singles.pickle", data_double = "moby_dick_double.pickle", data_tripple = "moby_dick_tripple.pickle", random = True):
		pickle_1 = open(data_single,"rb")
		pickle_2 = open(data_double,"rb")
		pickle_3 = open(data_tripple,"rb")


		self.dictionary = pickle.load(pickle_3)
		self.dictionary_doubles = pickle.load(pickle_2)
		self.single_dictionary = pickle.load(pickle_1)
		self.random = random
		self.error_count = [0,0,0,0]

	def common_word(self, L):
		if len(L) == 1 or len(L) == 2:
			return L[0]
		else:
			return max(groupby(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]


	def predict_word(self, key2):
		if key2 in self.dictionary.keys():
			print key2
			print 'yes three letter'
			self.error_count[0] += 1
			return self.common_word(self.dictionary[key2])
		else:
			a = key2.split()
			temp= a[1]+ ' ' + a[2]
			temp2 = a[2]
			# print temp2
			if temp in self.dictionary_doubles.keys():
				# print 'yes two letter'
				self.error_count[1] += 1
				return self.common_word(self.dictionary_doubles[temp])
			if a[2] in self.single_dictionary.keys():
					# print 'single word'
				self.error_count[2] += 1
				return self.common_word(self.single_dictionary[a[2]])
			self.error_count[3] += 1
			return self.dictionary[random.choice(dictionary.keys())][0]
			



	def get_promt(self, sentence, length = 3):
		a = sentence.split()
		prompt = ''
		for i in a[-(length):]:
			prompt += i + ' '
		return prompt



	def predict_sentence(self, initial = 'who knows what', chain_length = 3, parg_length = 200):
		sentence = initial
		for i in range(0, parg_length):
			if self.random:
				if i%10 == 0:
					sentence += ' ' + self.dictionary[random.choice(self.dictionary.keys())][0]
			prompt = self.get_promt(sentence, length= chain_length)
			sentence += ' ' + self.predict_word(prompt)
		return sentence

# a = Predictor2()
# # key = 'same snowy mantle'
# # print key in a.dictionary.keys()


# print a.predict_sentence("I'm glad you approve")
# print a.error_count

