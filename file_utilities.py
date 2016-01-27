#!/usr/bin/python

from ArcEager import NonProjectiveParseError, ArcEagerState
from DependencyParser import DependencyParser
# from features import construct_stacks, combined_feature
from MaxEnt import MaxEnt
import random

def get_word_from_conllu(split_line):

	morph = split_line[5] + '|' + split_line[9]
	tokens = [(token.split('=')[0],token.split('=')[1]) for token in morph.split('|')if len(token.split('=')) == 2]
	morph_dict = {key: value for (key,value) in tokens}
	word = {'index': split_line[0],
			'form': split_line[1],
			'lemma':split_line[2],
			'CPOS': split_line[3],
			'POS': split_line[4],
			'feats': '|'.join([key+'-'+value for (key, value) in tokens]),
			'parent': split_line[6],
			'deprel': split_line[7],
			'morph': morph_dict,
			'phead': '_',
			'pdeprel': '_'}
	return word

def get_word_from_conll(split_line):

	# CONLL format:
	# <column name="ID" category="INPUT" type="INTEGER"/>
	# <column name="FORM" category="INPUT" type="STRING"/>
	# <column name="LEMMA" category="INPUT" type="STRING"/>
	# <column name="CPOSTAG" category="INPUT" type="STRING"/>
	# <column name="POSTAG" category="INPUT" type="STRING"/>
	# <column name="FEATS" category="INPUT" type="STRING"/>
	# <column name="HEAD" category="HEAD" type="INTEGER"/>
	# <column name="DEPREL" category="DEPENDENCY_EDGE_LABEL" type="STRING"/>
	# <column name="PHEAD" category="IGNORE" type="INTEGER" default="_"/>
	# <column name="PDEPREL" category="IGNORE" type="STRING" default="_"/>

	morph_dict = {token.split('-')[0]:token.split('-')[1] for token in split_line[5].split('|') }
	word = {'index': split_line[0],
			'form': split_line[1],
			'lemma': split_line[2],
			'CPOS': split_line[3],
			'POS': split_line[4],
			'feats': split_line[5],
			'parent': split_line[6],
			'deprel': split_line[7],
			'phead': split_line[8],
			'pdeprel': split_line[9],
			'morph': morph_dict}
	return word

def write_to_conll(word):
	return '\t'.join([word['index'], word['form'], word['lemma'],
						word['CPOS'], word['POS'], word['feats'],
						word['parent'], word['deprel'], word['phead'],
						word['pdeprel']])

def train_from_file(ifile, file_type):

	dictionaries = []
	sentences = []
	with open(ifile, 'r') as fr:
		sentence_index = 0
		sentence = []
		nonprojs = []
		for line in fr.readlines():
			split_line = line.split()
			if len(split_line) == 10:
				if file_type == 'conll':
					word = get_word_from_conll(split_line)
				if file_type == 'conllu':
					if split_line[0] == '#':
						continue
					word = get_word_from_conllu(split_line)
				word['deprel'] = 'dep'
				sentence.append(word)
			else:
				if sentence_index >= 0:
					parser = DependencyParser(sentence)
					try:
						log = parser.get_transitions()
						dictionaries.append(log)
						sentences.append(sentence)
					except NonProjectiveParseError as nppe:
						nonprojs.append((sentence_index, str(nppe)))
				sentence_index += 1
				sentence = []
				# break
	return dictionaries, sentences

def parse_dp(dp_file, wts_file, surp_file, k, ofile, num_sent=None):
	correct = 0
	correct_label = 0
	total = 0
	gold_trans = 0.0
	maxent = MaxEnt(wts_file, len(ArcEagerState.transition_types))
	with open(dp_file, 'r') as fr:
		with open(surp_file, 'w') as fw:
			with open(ofile, 'w') as fo:
				sentence_index = 0
				sentence = []
				nonprojs = []
				for line in fr.readlines()+['\n']:
					split_line = line.split()
					if len(split_line) == 10:
						word = get_word_from_conll(split_line)
						sentence.append(word)
					else:
						if sentence_index % 50 == 0:	print "Sent %s"%sentence_index
						if sentence_index >= 0:
							parser = DependencyParser(sentence)
							parse = parser.best_parse(maxent,k)
							correct += parse['correct']
							total += parse['total']
							gold_trans += parse['gold_trans']
							correct_label += parse['correct_label']
							for pair in parse['surprisal']:
								fw.write(' '.join([str(x) for x in pair]) + '\n')
							fw.write('\n')
							if len(sentence):
								for w in sentence:
									w['parent'] = parse['parent'][w['index']]['index']
									fo.write(write_to_conll(w)+'\n')
								fo.write('\n')
						sentence_index += 1
						sentence = []
						if num_sent and (sentence_index >= num_sent): break
	return correct, total, gold_trans, correct_label

def save_whole(ofile, logs, labelled, feature_set):
	with open (ofile, 'w') as fw:
		for transitions in logs:
			for trans, state in transitions:
				fw.write(ArcEagerState.transition_codes[trans])
				fw.write(' ' + state + '\n')
		for tr in range(len(ArcEagerState.transition_types)):
			fw.write(str(tr) + ' DUMMY_FEAT\n')
	with open ('meta_' + ofile, 'w') as fw:
		fw.write(labelled + '\n')
		fw.write(feature_set + '\n')
		for (transition, label) in ArcEagerState.transition_types:
			fw.write(transition + ', ' + repr(label) + '\n')

def save_parts(ofile, n, logs, sentences):
	train = {i:[] for i in range(n)}
	test = {i:[] for i in range(n)}
	sent_indices = range(len(sentences))
	random.shuffle(sent_indices)
	for ind in sent_indices:
		for k in range(n):
			if k == ind % n:
				test[k].append(ind)
			else:
				train[k].append(ind)
	for i in range(n):
		print i, len(train[i]), len(test[i])
		with open(str(i) + '_train_' + ofile, 'w') as fw:
			for ind in train[i]:
				for trans, state in logs[ind]:
					fw.write(ArcEagerState.transition_codes[trans])
					fw.write(' ' + state + '\n')
			for tr in range(len(ArcEagerState.transition_types)):
				fw.write(str(tr) + ' DUMMY_FEAT\n')
		with open(str(i) + '_test_' + ofile, 'w') as fw:
			for ind in test[i]:
				for trans, state in logs[ind]:
					fw.write(ArcEagerState.transition_codes[trans])
					fw.write(' ' + state + '\n')
		with open(str(i) + '_dp_' + ofile, 'w') as fw:
			for ind in test[i]:
				for word in sentences[ind]:
					fw.write(write_to_conll(word) + '\n')
				fw.write('\n')
