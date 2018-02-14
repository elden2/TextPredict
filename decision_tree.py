import numpy as np
from scipy.optimize import minimize
import math
from scipy.special import expit




iris = np.genfromtxt('iris.csv', delimiter=',', dtype = None)
data = iris[51:, 0:4].astype(float)
labels = iris[51:,4:]

class Node(object):

	def __init__(self, data = None, labels = None):
		self.data = data
		self.labels = labels


	def binary_classifier(self, data, labels):

		def cost(data, labels, threshold = 2):
			# data should be 1D NP array
			# Threshold is cuttof value
			# labels shoukd be converted to 1 or 0
			a = data - threshold
			return expit(a)-labels

		return cost(data, labels)


a = np.array([2,2,3,3])
b = np.array([0,0,1,1])

c = Node()

b = partition(a)
print b.items()







		