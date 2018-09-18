from math import log
import operator
from collections import namedtuple
import pickle as p


class model():
	def __init__(self):
		pass
		# Create label classes
		self.lensesLabels = ['age','prescript','astigmatic','tearRate']


	def grabTree(self, filename):
		with open(filename,'rb') as fr:
			return p.load(fr)

	def grabLabel(self):
		return self.lensesLabels


	def classify(self, inputTree, featLabels, testVec):
		# In python 2.x, '.keys()' return a list while in python 3.x, it returns a dict_key which is 
		# similar to a set. So it doesn't support indexing. We could nest it in a list object as below
		# before indexing.

		firstStr = list(inputTree.keys())[0]
		secondDict = inputTree[firstStr]
		featIndex = featLabels.index(firstStr)
		classLabel = str("Unknown")
		#set_trace()
		for key in secondDict.keys():
			if testVec[featIndex] == key:
				if type(secondDict[key]).__name__=='dict':
					classLabel = self.classify(secondDict[key], featLabels, testVec)
				else:
					classLabel = secondDict[key]
		return classLabel