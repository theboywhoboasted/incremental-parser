#!/usr/bin/python

import random
import math
from copy import deepcopy
from ArcEager import ArcEagerState

class IncorrectParseError(Exception):
	def __init__(self):
		pass
	def __str__(self):
		return "IncorrectParseError"


class DependencyParser:

	def __init__(self, sentence):
		""" initializes the state of the parser
		buffer contains the sentence (this does not change through the parse)
		func is the function that computes the features
		tree is dict of nodes with value being the list of children
		"""
		self.buffer = sentence
		self.tree = self.build_tree()

	def build_tree(self):
		""" constructs a tree (dict of nodes with value being the list of children)
		from the parent field in the word as obtained from sentence """
		children = {'0': []}
		for word in self.buffer:
			children[word['index']] = []
		for word in self.buffer:
			children[word['parent']].append(word['index'])
		return children

	def is_correct(self, children):
		""" checks if the parse generated (children) is consistent with the tree """
		correct_parse = True
		for parent in self.tree:
			child_list = [word['index'] for word in children[parent]]
			for child in self.tree[parent]:
				correct_parse = correct_parse and (child in child_list)
		return correct_parse
	
	def get_transitions(self):
		""" gets list of transitions that would correspond to the parse """
		partial_parse = ArcEagerState(self.buffer)
		partial_parse.tree = self.tree
		while partial_parse.is_incomplete():
			transition, label = partial_parse.next_transition_and_label()
			partial_parse.make_transition(transition, label)
		if not self.is_correct(partial_parse.children):
			raise IncorrectParseError
		return partial_parse.log

	def best_parse(self, oracle, k=3):
		""" computes the greedy best parse using the predictions from oracle """
		assert (k > 0)
		partial_parses = []
		root_parse = ArcEagerState(self.buffer)
		root_parse.tree = self.tree
		partial_parses.append((1, 0, 0, root_parse))
		max_buffer_index = 0
		prev_likelihood = 1
		surprisal = []
		word_form = ''
		all_correct = 0
		all_correct_total = 0
		correct_trans_avlbl = []
		for max_buffer_index in range(len(self.buffer)):
			word_form += self.buffer[max_buffer_index]['form']
			while any([parse.index<=max_buffer_index for _,_,_,parse in partial_parses]):
				new_parses = [(l,i,t,p) for l,i,t,p in partial_parses if p.index>max_buffer_index]
				for likelihood, index, prev_retr, partial_parse in [(l,i,t,p) for l,i,t,p in partial_parses if p.index<=max_buffer_index]:
					feature_lists = partial_parse.get_state().split()
					pred = oracle.predict(feature_lists)
					norm_sum = 0
					for index in range(len(partial_parse.transition_types)):
						if not partial_parse.possible(partial_parse.transition_types[index][0]):
							pred[index] = 0
						norm_sum += pred[index]
					prob_vector = [(p/norm_sum, i) for i,p in enumerate(pred)]
					prob_vector.sort(reverse=True)
					prob_vector = prob_vector[:k]
					for prob, index in prob_vector:
						transition, label = ArcEagerState.transition_types[index]
						if partial_parse.possible(transition):
							new_parse = deepcopy(partial_parse)
							new_parse.likelihood = likelihood
							# print new_parse.index, len(new_parse.buffer)
							new_parse.make_transition(transition, label, prob=prob)
							new_parses.append((new_parse.likelihood,new_parse.index,prev_retr,new_parse))
				new_parses.sort(reverse=True)
				partial_parses = new_parses[:10*k]
			if not self.buffer[max_buffer_index].get('to_be_skipped', False):
				partial_parses = partial_parses[:k]
				all_correct += max([p.all_correct for (l,i,t,p) in partial_parses])
				all_correct_total += 1
				for _,_,_,p in partial_parses:
					correct_trans_avlbl += p.gold_trans
				correct_trans_avlbl = list(set(correct_trans_avlbl))
				new_likelihood = sum([l for l,_,_,_ in partial_parses])
				retrieval = max([p.time-t for _,_,t,p in partial_parses])
				surprisal.append((max_buffer_index+1, word_form, '%.5f'%(-math.log(new_likelihood)/math.log(2.0)), retrieval))
				prev_likelihood = new_likelihood
				partial_parses = [(triple[0]/new_likelihood, triple[1], triple[3].time, triple[3]) for triple in partial_parses]
				word_form = ''
		correct_trans_avlbl = set(list(correct_trans_avlbl))		
		correct = 0.0
		correct_label = 0.0
		total = 0.0
		_,_,_,partial_parse = partial_parses[0]
		for word in self.buffer:
			if not partial_parse.parent[word['index']]:
				partial_parse.parent[word['index']] = {'index': '0'}
				partial_parse.label[word['index']] = 'root'
			else:
				if partial_parse.parent[word['index']]['index'] == str(word['parent']):
					correct += 1
					if partial_parse.label[word['index']] == str(word['deprel']):
						correct_label += 1
			total += 1
		# print {x:partial_parse.parent[x]['index'] for x in partial_parse.parent if x!='0'}
		# print {word['index']: word['parent'] for word in self.buffer}
		# print partial_parse.label
		assert (correct <= total)
		assert (correct_label <= total)
		assert (len(correct_trans_avlbl) <= total)
		# print sorted(partial_parse.gold_trans), sorted(correct_trans_avlbl), len(correct_trans_avlbl), correct
		# print correct, correct_label, len(correct_trans_avlbl), total, all_correct, all_correct_total
		# for word in self.buffer:
		# 	print word['index'], partial_parse.parent[word['index']]['index'], word['parent'], (word['index'] in correct_trans_avlbl)
		assert (correct <= len(correct_trans_avlbl))
		assert (all_correct <= all_correct_total)
		assert (all_correct_total <= total)
		return {'surprisal': surprisal,
				'parent': partial_parse.parent,
				'retrieval': sorted([(int(key), partial_parse.decay_list[key]['form'], partial_parse.decay_list[key]['times'][-1]) for key in partial_parse.decay_list]),
				'correct': correct,
				'total': total,
				'correct_trans_avlbl': len(correct_trans_avlbl),
				'all_correct': all_correct,
				'all_correct_total': all_correct_total,
				'correct_label': correct_label}

