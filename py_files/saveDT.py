import pickle as p

def storeTree(inputTree, filename):
	'''
	We should make sure we open file as 'wb' ie writable and as byte. And also, 
	we should use the protocol
	'''
	with open(filename, 'wb') as fw:
		p.dump(inputTree, fw, protocol=p.HIGHEST_PROTOCOL)


def grabTree(filename):
	with open(filename,'rb') as fr:
		return p.load(fr)
