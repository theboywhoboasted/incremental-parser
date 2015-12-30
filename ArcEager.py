#!/usr/bin/python

class NonProjectiveParseError(Exception):
	def __init__(self, arg):
		self.arg = arg
	def __str__(self):
		return repr(self.arg)

class ArcEagerState:

	def __init__(self, sentence, func):
		""" initializes the state of the parser 
		stack contains the root node,
		buffer contains the whole sentence,
		index initialized to 0
		arcs is empty
		parent, label and children anre dicts with an element for each buffer item
		log contains the list of (transition, feature set) (initially empty)
		transitions contains the list of transitions (initially empty)
		likelihood is the probability of parse initialized to 1
		get_state is the function that generates features from state 
		"""

		self.stack = [{'index': '0',
						'form': 'ROOT',
						'lemma': 'ROOT_lemma',
						'CPOS': 'ROOT_CPOS',
						'POS': 'ROOT_POS',
						'parent': 'NULL',
						'feats': '',
						'morph': {'chunkId':''}}]
		self.buffer = sentence
		self.get_state = lambda x: func(x.stack, x.buffer, x.arcs, x.index, x.parent, x.children, x.label)
		self.index = 0
		self.arcs = []
		self.parent = {word['index']: None for word in sentence}
		self.label = {word['index']: None for word in sentence}
		self.parent['0'] = None
		self.label['0'] = None
		self.children = {word['index']: [] for word in sentence}
		self.children['0'] = []
		self.log = []
		self.transitions = []
		self.likelihood = 1
		self.gold_trans = 0.0
		self.gold_label = 0.0

	# static variables
	transition_types = [("SHIFT", None), ("REDUCE", None)]
	transition_codes = {j:str(i) for (i,j) in enumerate(transition_types)}

	def possible(self, transition):
		""" indicates if a given transition is possible given the parser state """
		if transition == 'LEFT_ARC':
			return (self.stack[-1]['index'] > '0') and \
					(self.index < len(self.buffer) and \
					(self.parent[self.stack[-1]['index']] == None))
		elif transition == 'RIGHT_ARC':
			return (self.index < len(self.buffer))
		elif transition == 'SHIFT':
			return (self.index < len(self.buffer))
		elif transition == 'REDUCE':
			return (self.parent[self.stack[-1]['index']] != None)
			return False

	def is_incomplete(self):
		""" indicates if the parse is incomplete """
		return (len(self.stack) > 1) or (self.index < len(self.buffer))

	def next_transition_and_label(self):
		""" given the parser state and dependency parse, returns the next transition """
		if not self.stack:
			return ('SHIFT', None)
		stacktop = self.stack[-1]	
		try:
			reducible = (self.parent[stacktop['index']]['index'] == stacktop['parent'])
		except TypeError:
			reducible = False
		for child in self.tree[stacktop['index']]:
			reducible = reducible and (child in [word['index'] for word in self.children[stacktop['index']]])
		if reducible:
			return ('REDUCE', None)
		elif self.index < len(self.buffer):
			buffertop = self.buffer[self.index]
			if stacktop['index'] == buffertop['parent']:
				return ('RIGHT_ARC', buffertop['deprel'])
			elif stacktop['parent'] == buffertop['index']:
				return ('LEFT_ARC', stacktop['deprel'])
			else:
				return ('SHIFT', None)
		else:
			# print "NPPE", [(word['index'], self.parent[word['index']]) for word in self.stack], self.index
			raise NonProjectiveParseError(self.log)

	def make_arc(self, arc, label):
		(parent, child) = arc
		self.arcs.append((parent['index'], child['index'], label))
		self.parent[child['index']] = parent
		self.children[parent['index']].append(child)
		self.label[child['index']] = label

	def make_transition(self, transition, label=None, prob=-1):
		""" given a transition with a probability, makes the transition to the parser state """
		try:
			if self.stack[-1]['parent'] == self.buffer[self.index]['index']:
				self.gold_trans += 1
			if self.stack[-1]['index'] == self.buffer[self.index]['parent']:
				self.gold_trans += 1
		except IndexError:
			pass
		assert self.possible(transition)
		self.log.append(((transition, label),self.get_state(self)))
		if label:
			if (transition, label) not in ArcEagerState.transition_types:
				ArcEagerState.transition_codes[(transition, label)] = str(len(ArcEagerState.transition_types))
				ArcEagerState.transition_types.append((transition,label))
		if transition == 'SHIFT':
			self.stack.append(self.buffer[self.index])
			self.index += 1
		elif transition == 'REDUCE':
			self.stack.pop()
		elif transition == 'LEFT_ARC':
			arc = (self.buffer[self.index], self.stack[-1])
			self.make_arc(arc, label)
			self.stack.pop()
		elif transition == 'RIGHT_ARC':
			arc = (self.stack[-1], self.buffer[self.index])
			self.make_arc(arc, label)
			self.stack.append(self.buffer[self.index])
			self.index += 1
		self.transitions.append(transition)
		if prob > 0:
			self.likelihood *= prob