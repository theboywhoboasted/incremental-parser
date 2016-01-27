FORM = 'form'
LEMMA = 'lemma'
CPOSTAG = 'CPOS'
POSTAG = 'POS'
FEATS = 'feats'
DEPREL = 'deprel'
	
GENDER = 'gen'
NUMBER = 'num'
PERSON = 'pers'
CASE = 'case'
VIBHAKTI = 'vib'
TAM = 'tam'
CHUNK_ID = 'chunkId'
CHUNK_TYPE = 'chunkType'
STYPE = 'stype'
VOICETYPE = 'voicetype'

def initialise(stack, buffer, arc, index, parent, children, label):
	global Stack, Input, Arc, Index, Parent, Children, Label, Buffer
	# Stack = stack
	# Input = buffer
	Stack = [stack[-1]]
	try:
		Stack.append(stack[-2])
	except IndexError:
		Stack.append(None)
	try:
		Stack.append(stack[-2])
	except IndexError:
		Stack.append(None)
	Input = []
	try:
		Input.append(buffer[index])
	except IndexError:
		Input.append(None)
	Arc = arc
	Index = index
	Parent = parent
	Children = children
	Label = label
	Buffer = buffer


def InputColumn(val, word):
	if word:
		if val in word:
			return word[val]
		elif val in word['morph']:
			return word['morph'][val]
	return ''
def OutputColumn(val, word):
	if word: 
		if val == DEPREL:
			if Label[word['index']]:
				return Label[word['index']]
	return ''


def Split(string, sep):
	return string.split(sep)
def Merge(str1, str2):
	return str1 + '_' + str2


def pred(word):
	if not word:
		return None
	if int(word['index']) < 2:
		return None
	return Buffer[int(word['index']) - 2]
def head(word):
	if not word:
		return None
	return Parent[word['index']]
def ldep(word):
	if not word:
		return None
	try:
		return Children[word['index']][0]
	except IndexError:
		return None
def rdep(word):
	if not word:
		return None
	try:
		return Children[word['index']][-1]
	except IndexError:
		return None
def rdep2(word):
	if not word:
		return None
	try:
		return Children[word['index']][-2]
	except IndexError:
		return None

def combined_all_feature_labelled():
	feature_set=[Split(InputColumn(FEATS, Stack[0]),'|'),
			Split(InputColumn(FEATS, Input[0]),'|'),
			InputColumn(FORM, Stack[0]),
			InputColumn(FORM, Input[0]),
			InputColumn(POSTAG, Stack[0]),
			InputColumn(POSTAG, Input[0]),
			InputColumn(CHUNK_ID, Stack[0]),
			InputColumn(CHUNK_ID, Input[0]),
			InputColumn(POSTAG, Stack[1]),
			InputColumn(POSTAG, pred(Stack[0])),
			InputColumn(POSTAG, head(Stack[0])),
			InputColumn(POSTAG, ldep(Input[0])),
			InputColumn(CPOSTAG, Stack[0]),
			InputColumn(CPOSTAG, Input[0]),
			InputColumn(CPOSTAG, ldep(Input[0])),
			InputColumn(FORM, ldep(Input[0])),
			InputColumn(LEMMA, Stack[0]),
			InputColumn(LEMMA, Input[0]),
			OutputColumn(DEPREL, rdep(Stack[0])),
			OutputColumn(DEPREL, rdep2(Stack[0])),
			Merge(InputColumn(CHUNK_ID, Stack[0]), InputColumn(CHUNK_ID, Input[0])),
			Merge(InputColumn(CPOSTAG, Stack[0]), InputColumn(CPOSTAG, Input[0])),
			Merge(InputColumn(POSTAG, Stack[0]), InputColumn(POSTAG, Input[0])),
			Merge(InputColumn(FEATS, Stack[0]), OutputColumn(DEPREL, Stack[0]))
			]

	split_feat = ['STACK0_FEAT_%s'%feat for feat in feature_set[0]] + ['INPUT0_FEAT_%s'%feat for feat in feature_set[1]]
	return ' '.join(['FEAT_%d_%s'%(ind, val) for (ind, val) in enumerate(feature_set[2:])]) + ' '.join(split_feat)

def combined_all_feature_unlabelled():
	feature_set=[Split(InputColumn(FEATS, Stack[0]),'|'),
			Split(InputColumn(FEATS, Input[0]),'|'),
			InputColumn(FORM, Stack[0]),
			InputColumn(FORM, Input[0]),
			InputColumn(POSTAG, Stack[0]),
			InputColumn(POSTAG, Input[0]),
			InputColumn(CHUNK_ID, Stack[0]),
			InputColumn(CHUNK_ID, Input[0]),
			InputColumn(POSTAG, Stack[1]),
			InputColumn(POSTAG, pred(Stack[0])),
			InputColumn(POSTAG, head(Stack[0])),
			InputColumn(POSTAG, ldep(Input[0])),
			InputColumn(CPOSTAG, Stack[0]),
			InputColumn(CPOSTAG, Input[0]),
			InputColumn(CPOSTAG, ldep(Input[0])),
			InputColumn(FORM, ldep(Input[0])),
			InputColumn(LEMMA, Stack[0]),
			InputColumn(LEMMA, Input[0]),
			Merge(InputColumn(CHUNK_ID, Stack[0]), InputColumn(CHUNK_ID, Input[0])),
			Merge(InputColumn(CPOSTAG, Stack[0]), InputColumn(CPOSTAG, Input[0])),
			Merge(InputColumn(POSTAG, Stack[0]), InputColumn(POSTAG, Input[0])),
			]

	split_feat = ['STACK0_FEAT_%s'%feat for feat in feature_set[0]] + ['INPUT0_FEAT_%s'%feat for feat in feature_set[1]]
	return ' '.join(['FEAT_%d_%s'%(ind, val) for (ind, val) in enumerate(feature_set[2:])]) + ' '.join(split_feat)

def combined_most_features():
	feature_set=[Split(InputColumn(FEATS, Stack[0]),'|'),
			Split(InputColumn(FEATS, Input[0]),'|'),
			InputColumn(FORM, Stack[0]),
			InputColumn(FORM, Input[0]),
			InputColumn(POSTAG, Stack[0]),
			InputColumn(POSTAG, Input[0]),
			InputColumn(CASE, Stack[0]),
			InputColumn(CASE, Input[0]),
			InputColumn(VIBHAKTI, Stack[0]),
			InputColumn(VIBHAKTI, Input[0]),
			InputColumn(TAM, Stack[0]),
			InputColumn(TAM, Input[0]),
			InputColumn(CHUNK_ID, Stack[0]),
			InputColumn(CHUNK_ID, Input[0]),
			InputColumn(CHUNK_ID, Stack[0]),
			InputColumn(CHUNK_ID, Input[0]),
			InputColumn(CHUNK_TYPE, Stack[0]),
			InputColumn(CHUNK_TYPE, Input[0]),
			InputColumn(STYPE, Stack[0]),
			InputColumn(STYPE, Input[0]),
			InputColumn(VOICETYPE, Stack[0]),
			InputColumn(VOICETYPE, Input[0]),
			InputColumn(NUMBER, Stack[0]),
			InputColumn(NUMBER, Input[0]),
			InputColumn(GENDER, Stack[0]),
			InputColumn(GENDER, Input[0]),
			InputColumn(PERSON, Stack[0]),
			InputColumn(PERSON, Input[0]),
			InputColumn(POSTAG, Stack[1]),
			InputColumn(POSTAG, pred(Stack[0])),
			InputColumn(POSTAG, head(Stack[0])),
			InputColumn(POSTAG, ldep(Input[0])),
			InputColumn(CPOSTAG, Stack[0]),
			InputColumn(CPOSTAG, Input[0]),
			InputColumn(CPOSTAG, ldep(Input[0])),
			InputColumn(FORM, ldep(Input[0])),
			InputColumn(LEMMA, Stack[0]),
			InputColumn(LEMMA, Input[0]),
			Merge(InputColumn(CHUNK_ID, Stack[0]), InputColumn(CHUNK_ID, Input[0])),
			Merge(InputColumn(CPOSTAG, Stack[0]), InputColumn(CPOSTAG, Input[0])),
			Merge(InputColumn(POSTAG, Stack[0]), InputColumn(POSTAG, Input[0])),
			]

	split_feat = ['STACK0_FEAT_%s'%feat for feat in feature_set[0]] + ['INPUT0_FEAT_%s'%feat for feat in feature_set[1]]
	return ' '.join(['FEAT_%d_%s'%(ind, val) for (ind, val) in enumerate(feature_set[2:])]) + ' '.join(split_feat)

def construct_stacks1():
	stacktop = "NULL"
	buffertop = ""
	try:
		stacktop = Stack[1:][-1]['POS']
	except IndexError:
		pass
	try:
		buffertop = Buffer[Index]['POS']
	except IndexError:
		pass
	return "STACK1NEXT_" + stacktop + "|**" + buffertop

def construct_stacks2():
	stacktop1 = "NULL"
	stacktop2 = "NULL"
	buffertop = ""
	try:
		stacktop2 = Stack[1:][-2]['POS']
		stacktop1 = Stack[1:][-1]['POS']
	except IndexError:
		try:
			stacktop2 = Stack[1:][-1]['POS']
		except IndexError:
			pass
	try:
		buffertop = Buffer[Index]['POS']
	except IndexError:
		pass
	return "STACK2NEXT_" + stacktop2 + "|" + stacktop1 + "|**" + buffertop

def construct_stacks3():
	stacktop1 = "NULL"
	stacktop2 = "NULL"
	stacktop3 = "NULL"
	buffertop = ""
	try:
		stacktop3 = Stack[1:][-3]['POS']
		stacktop2 = Stack[1:][-2]['POS']
		stacktop1 = Stack[1:][-1]['POS']
	except IndexError:
		try:
			stacktop3 = Stack[1:][-2]['POS']
			stacktop2 = Stack[1:][-1]['POS']
		except IndexError:
			try:
				stacktop3 = Stack[1:][-1]['POS']
			except IndexError:
				pass
	try:
		buffertop = Buffer[Index]['POS']
	except IndexError:
		pass
	return "STACK3NEXT_" + stacktop3 + "|" + stacktop2 + "|" + stacktop1 + "|**" + buffertop

def construct_stacks():
	return ' '.join([construct_stacks1(),
					construct_stacks2(),
					construct_stacks3()])


FEATURE_DICT = {'construct_stacks': construct_stacks,
				'construct_stacks1': construct_stacks1,
				'construct_stacks2': construct_stacks2,
				'construct_stacks3': construct_stacks3,
				'combined_most_features':	combined_most_features}