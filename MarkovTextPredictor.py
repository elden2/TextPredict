import random
import sys
import os
from itertools import groupby
import pickle


#The naming of this as a tree is a bit of a misnomer.  I origionally tried to write
#this as a tree, with each word a branch, bu a dictionary wound up being easier

#The depth represents the number of words in the depth of the markov change.
#I plan on changing this later so that it can be any number, but as of now it only works as a tripplet.

#The speech prediciton gets caught in repeating loops.  Set random to how often you want a
#random word form the dictionary thrown in


class Tree(object):
	def __init__(self, data = 'as long string', depth = 3, random = 15  ):
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

	#I couldn't figure out an efficent way of doing this.  This funtion I took from stackoverflow
	def common_word(self, L, noise = False):
		if noise:
			return random.choice(L)
		if len(L) == 1 or len(L) == 2:
			return L[0]
		else:
			return max(groupby(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]


	def predict_word(self, key = 'three word form', noise = False):
		# if key in self.dictionary.keys():
		# 	# print 'yes three letter'
		# 	self.error_count[0] += 1
		# 	return self.common_word(self.dictionary[key], noise = noise)
		# else:
		a = key.split()
		temp= a[1]+ ' ' + a[2]
		temp2 = a[2]
		# print temp2
		if temp in self.dictionary_doubles.keys():
			# print 'yes two letter'
			self.error_count[1] += 1
			return self.common_word(self.dictionary_doubles[temp], noise = noise)
		if a[2] in self.single_dictionary.keys():
				# print 'single word'
			self.error_count[2] += 1
			return self.common_word(self.single_dictionary[a[2]], noise = noise)
		self.error_count[3] += 1
		return self.dictionary[random.choice(self.dictionary.keys())][0]
			


	def get_promt(self, sentence, length = 3):
		a = sentence.split()
		prompt = ''
		for i in a[-(length):]:
			prompt += i + ' '
		return prompt[:-1]



	def predict_sentence(self, initial = 'who knows what', chain_length = 3, parg_length = 1000):
		sentence = initial
		for i in range(0, parg_length):
			if i%self.random == 0 and i!= 0:
				prompt = self.get_promt(sentence, length= chain_length)
				sentence += ' ' + self.predict_word(prompt, noise = True)
			else:
				prompt = self.get_promt(sentence, length= chain_length)
				sentence += ' ' + self.predict_word(prompt, noise = False)
		return sentence
			


# Moby_Dick
# with open('./Texts/moby.txt', 'r') as temp:
# 	moby = temp.read().replace('\n', '')

# with open('Fitzgerald.txt', 'r') as temp:
# 	fitz = temp.read().replace('\n', '')


with open('Alistair.txt', 'r') as temp:
	fitz = temp.read().replace('\n', '')

Moby_dick = Tree(fitz)
print len(Moby_dick.dictionary)
print Moby_dick.predict_sentence('Alistair was a ')

# print Moby_dick.predict_sentence('Swarth Cheby Gatsby')
# print Moby_dick.error_count

# training_text = ''
# directory = os.path.normpath('./Texts')
# for files in os.walk(directory):
# 	for file in files:
# 		for f in file:
# 			if f.endswith(".txt"):
# 				path = './Texts/'+f
# 				text = open(path, 'r')
# 				a = text.read()
# 				training_text+=a


# Predict = Tree()
# print Predict.predict_sentence('a time it was')


# print len(Predict.dictionary)		


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







# class Predictor2(object):
# 	def __init__(self, data_single = "moby_dick_singles.pickle", data_double = "moby_dick_double.pickle", data_tripple = "moby_dick_tripple.pickle", random = True):
# 		pickle_1 = open(data_single,"rb")
# 		pickle_2 = open(data_double,"rb")
# 		pickle_3 = open(data_tripple,"rb")


# 		self.dictionary = pickle.load(pickle_3)
# 		self.dictionary_doubles = pickle.load(pickle_2)
# 		self.single_dictionary = pickle.load(pickle_1)
# 		self.random = random
# 		self.error_count = [0,0,0,0]

# 	def common_word(self, L):
# 		if len(L) == 1 or len(L) == 2:
# 			return L[0]
# 		else:
# 			return max(groupby(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]


# 	def predict_word(self, key2):
# 		if key2 in self.dictionary.keys():
# 			print key2
# 			print 'yes three letter'
# 			self.error_count[0] += 1
# 			return self.common_word(self.dictionary[key2])
# 		else:
# 			a = key2.split()
# 			temp= a[1]+ ' ' + a[2]
# 			temp2 = a[2]
# 			# print temp2
# 			if temp in self.dictionary_doubles.keys():
# 				# print 'yes two letter'
# 				self.error_count[1] += 1
# 				return self.common_word(self.dictionary_doubles[temp])
# 			if a[2] in self.single_dictionary.keys():
# 					# print 'single word'
# 				self.error_count[2] += 1
# 				return self.common_word(self.single_dictionary[a[2]])
# 			self.error_count[3] += 1
# 			return self.dictionary[random.choice(dictionary.keys())][0]
			



# 	def get_promt(self, sentence, length = 3):
# 		a = sentence.split()
# 		prompt = ''
# 		for i in a[-(length):]:
# 			prompt += i + ' '
# 		return prompt



# 	def predict_sentence(self, initial = 'who knows what', chain_length = 3, parg_length = 200):
# 		sentence = initial
# 		for i in range(0, parg_length):
# 			if self.random:
# 				if i%10 == 0:
# 					sentence += ' ' + self.dictionary[random.choice(self.dictionary.keys())][0]
# 			prompt = self.get_promt(sentence, length= chain_length)
# 			sentence += ' ' + self.predict_word(prompt)
# 		return sentence

# # a = Predictor2()
# # # key = 'same snowy mantle'
# # # print key in a.dictionary.keys()


# # print a.predict_sentence("I'm glad you approve")
# # print a.error_count

