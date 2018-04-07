import random
import sys
import os
from itertools import groupby

#The depth represents the number of words in the depth of the markov change.
#I plan on changing this later so that it can be any number, but as of now it only works as a tripplet.

#The speech prediciton gets caught in repeating loops.  Set random to how often you want a
#random word form the dictionary thrown in


class Predictor(object):
	def __init__(self, data = 'as long string', depth = 3, random = 15):
		self.depth = depth
		self.data = data.split()

		self.dictionary_tripple= {}
		self.dictionary_doubles = {}
		self.dictionary_single = {}

		self.tripple = []
		self.target = []
		self.get_trip()
		self.pair_dictionary_tripples()

		self.doubles = []
		self.doubles_target = []
		self.get_doubles()
		self.pair_dictionary_doubles()

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
			if self.tripple[i] in self.dictionary_tripple:
				self.dictionary_tripple[self.tripple[i]].append(self.target[i])
			else:
				self.dictionary_tripple[self.tripple[i]] = [self.target[i]]

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
			if self.data[i] in self.dictionary_single:
				self.dictionary_single[self.data[i]].append(self.data[i+1])
			else:
				self.dictionary_single[self.data[i]] = [self.data[i+1]]

	#I couldn't figure out an efficent way of doing this.  This funtion I took from stackoverflow
	def common_word(self, L, noise = False):
		if noise:
			return random.choice(L)
		if len(L) == 1 or len(L) == 2:
			return L[0]
		else:
			return max(groupby(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]


	def predict_word(self, key = 'three word form', noise = False):
		a = key.split()
		temp3 = a[0]+ ' ' + a[1] + ' ' + a[2] 
		temp2 = a[1]+ ' ' + a[2]
		temp1 = a[2]
		if temp3 in self.dictionary_tripple.keys():
			self.error_count[0] += 1
			return self.common_word(self.dictionary_tripple[temp3], noise = noise)
		if temp2 in self.dictionary_doubles.keys():
			self.error_count[1] += 1
			return self.common_word(self.dictionary_doubles[temp2], noise = noise)
		if temp1 in self.dictionary_single.keys():
			self.error_count[2] += 1
			return self.common_word(self.dictionary_single[a[2]], noise = noise)
		self.error_count[3] += 1
		return self.dictionary_tripple[random.choice(self.dictionary_tripple.keys())][0]
			

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
		return sentence, self.error_count
			


with open('moby.txt', 'r') as temp:
	moby = temp.read().replace('\n', '')

Moby_dick = Predictor(moby, random = 10)
print Moby_dick.dictionary_single['Whale']

# c,d = Moby_dick.predict_sentence('a Sperm Whale',parg_length=100)
# print c
# print d


