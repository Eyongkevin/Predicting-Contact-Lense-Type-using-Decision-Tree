from math import log
import operator
from collections import namedtuple
import saveDT 
from pdb import set_trace



def calcShannonEnt(dataset):   
	"""
	This calculates the Shannon Entropy which is the measure of the amount of uncertainty in the data
	or the expected value of an information.
	This tells us how the data is distributed through out some classes. 
	if the entropy result is 0, then it shows that 
	all the information belong in the same class. and vise vesa. But if 1,
	then it is uniformly distributed whithin a set of classes.However, the higher the entropy(>1), 
	the more mixed up the data is.
	-----------------------
	
	It formula is #p(xi)log2p(xi) where p(xi) is the probability of the occourance of that piece of info in the dataset.
	We do that for all pieces of info in the dataset."""                      
	numEntries = len(dataset)                         #get length
	labelCounts = {}
	#here we get the frequency of the data label
	#set_trace()

	for featVec in dataset:
		currentLabel = featVec[-1]                    #get the last value in the list. which is the label. eg [1,1, 'yes']
		'''
		if currentLabel not in labelCounts.keys():    #check if the label is not yet in the dictionary
			labelCounts[currentLabel] = 0             #add it with an initial value of zero
		labelCounts[currentLabel] += 1                #This will increment each time it sees the label.
		'''
		labelCounts[currentLabel] = labelCounts.get(currentLabel,0) + 1
	shannonEnt = 0.0	
	#here we calculate the log
	for key in labelCounts:
		prob = float(labelCounts[key])/numEntries     #calculate the probability [each label frequency/dataset length]
		shannonEnt -= prob * log(prob,2)              #This is where the entropy formula is been applied P(xi)log2P(xi)
	return shannonEnt
    	
	
def createDataset():
	dataset = [	[1, 1, 'yes'],
				[1, 1, 'yes'],
				[1,1, 'yes'],
				[1,0, 'no'],
				[0,1, 'no'],
				[0,1, 'no']]
				
	labels = ['no surfacing','flippers']
	dataset_created = namedtuple('data',['dataset','labels'])
	return dataset_created(dataset, labels)
	
	
def splitDataSet(dataSet, axis, value):
	'''
	Decision tree consist of seperating data, calculating the entropy change, and over and over
	This function provides the spliting feature of this system.
	--------------------
	@param:
		- dataSet[list] : list of the data set
		- axis[int]     : the axis(index) to split on
		- value[int]    : The value of the axis feature to split on.
	@Hint:
		- This fxn will be called recursively, so we need to create an array for each call.
		which will hold the split result, since list are mutable.
	----------------------Example------------------
	data = [[1, 1, 'yes'], [1, 1, 'yes'], [1, 0, 'no'], [0, 1, 'no'], [0, 1, 'no']]
			* for axis = 1, value = 1.
			for dataFeature in data:
				if dataFeature[axis] == value:
				        ====[[1, 1, 'yes'], [1, 1, 'yes'], [1, 0, 'no']]
				reducedFeatVec = dataFeature[:axis] ------(1)
				        ==== [1],[1],[1],[1]
				dataFeature[axis+1:] 
				        ==== ['yes'],['yes'],['no']-----(2)
				when we extend (1) and (2), we have 
				       ====  [1,'yes'],[1,'yes'],[1,'no']
	-------------------------------------------------
	                  		
	'''
	retDataSet = []
	for featVec in dataSet:
		if featVec[axis] == value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis+1:])
			retDataSet.append(reducedFeatVec)
	return retDataSet
	
def chooseBestFeatureToSplit(dataSet):
	'''
	We combine the Shannon entropy calculation and the splitDataSet() function
	to cycle through the dataset and decide which feature is the best to split on.
	Entropy tells us which split best organise the data.
	--------------------
	@Hint:
		- Here we asume all the data set of the same size, and 
		the lable is the last item in the data set.
	'''
	numFeatures = len(dataSet[0]) - 1		# Get the size of the features(exclude the lable) = 2
	baseEntropy = calcShannonEnt(dataSet)   # get entropy for all the dataset
	bestInfoGain = 0.0
	bestFeature = -1
	for i in range(numFeatures):            # loop through the features.
		featList = [example[i] for example in dataSet]    # Get list of index 0 items in the dataset
		uniqueVals = set(featList)          # make them unique and sorted , for [1,1,0,1], we have [0,1]
		newEntropy = 0.0
		
		for value in uniqueVals:            # split and find entropy when index value is in [0,1]
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob * calcShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy
		
		if (infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = i
	return bestFeature

def majorityCnt(classList):
	'''
	It takes a list of names and creates a dictionary whose keys are unique values in classList
	and the object of the dictionary is the frequency of occurance of each class label from classList.
	--------------
	@Hint:
	    - We use the operator class to sort the dictionary by the keys and return the class that 
	    occurs with the greatest frequency.
	    
	'''
	classCount={}
	for vote in classList:
		#if vote not in classCount.keys(): classCount[vote] = 0
		#classCount[vote] += 1
		classCount[vote] = classCount.get(vote,0)+1

	# In python 3.x, iteritems() is been replaced by items().
	sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1), reverse=True)
	return sortedClassCount[0][0]
	
def createTree(dataSet,labelList):
	labels = labelList.copy()

	# create list of all the label in the dataset.
	# For each feature of the dataset, the label is the last column, so we use index (-1)
	classList = [example[-1] for example in dataSet]

	# check the frequency of an item at any index(in this case 0) of the list, if its frequency equals
	# the total size of the list, then the list is compose of only that item.
	if classList.count(classList[0]) == len(classList):
		return classList[0]

	# When no more features to split, return majority.
	if len(dataSet[0]) == 1:
		return majorityCnt(classList)
	bestFeat = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeat]
	myTree = {bestFeatLabel:{}}
	del(labels[bestFeat])
	featValues = [example[bestFeat] for example in dataSet]

	# this eliminate redundancy(repatitive data), return each item once
	# e.g. for ['yes','yes','no','mayb','mayb'], it set will return ['yes','no','mayb']
	uniqueVals = set(featValues)
	for value in uniqueVals: 

		# create a shallow copy of a list. this is bc by default list are past by
		# reference(a change in one affects the other), so a shallow or deep copy won't affect the other
		# this can also be accomplished using 'copy' of the copy model.
		subLabels = labels[:] 
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)
	return myTree

def classify(inputTree, featLabels, testVec):
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
				classLabel = classify(secondDict[key], featLabels, testVec)
			else:
				classLabel = secondDict[key]
	return classLabel


if __name__ == '__main__':
		data = createDataset()
		print(data.dataset)
		#shannonEnt = calcShannonEnt(data.dataset)
		#print(shannonEnt)
		#split = splitDataSet(data.dataset,0,1)
		#print(split)

		chose = createTree(data.dataset, data.labels)
		saveDT.storeTree(chose, 'storage.txt')
		getTree = saveDT.grabTree('storage.txt')
		print(getTree)

		#print(chose)

		
		
		
		
		
		
		
		
		
		
		
		
		