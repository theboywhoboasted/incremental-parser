import numpy as np

class MaxEnt:

	def __init__(self, weights_file, n):
		self.n = n
		self.weights = {}
		with open(weights_file, 'r') as f:
			for line in f.readlines():
				words = line.strip().split()
				self.weights[words[0]] = [float(x) for x in words[1:]]

	def predict(self, feature_list):
		scores = [0.0]*self.n
		feature_list.append('**BIAS**')
		for feature in feature_list:
			try:
				numclasses = len(self.weights[feature])
				for num in range(min(self.n, numclasses)):
					scores[num] += self.weights[feature][num]
					# print num, self.weights[feature][num]
			except KeyError:
					pass
		# print scores
		scores = np.exp(scores)
		norm = np.sum(scores)
		prob = scores/norm
		return prob


# maxent = MaxEnt("wts_wsj", 4)
# with open('long.txt', 'r') as f:
# 	for line in f.readlines():
# 		features = line.strip().split()[1:]
# 		prediction = maxent.predict(features)
# 		maxind = max([(i,p) for (p,i) in enumerate(prediction)])[1]
# 		print str(maxind) + '\t' + ' '.join([('%.20f'%x) for x in prediction])