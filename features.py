def construct_stacks1(stack, buffer, arc, index):
	stacktop = "NULL"
	buffertop = ""
	try:
		stacktop = stack[1:][-1]['CPOS']
	except IndexError:
		pass
	try:
		buffertop = buffer[index]['CPOS']
	except IndexError:
		pass
	return "STACK1NEXT_" + stacktop + "|**" + buffertop

def construct_stacks2(stack, buffer, arc, index):
	stacktop1 = "NULL"
	stacktop2 = "NULL"
	buffertop = ""
	try:
		stacktop2 = stack[1:][-2]['CPOS']
		stacktop1 = stack[1:][-1]['CPOS']
	except IndexError:
		try:
			stacktop2 = stack[1:][-1]['CPOS']
		except IndexError:
			pass
	try:
		buffertop = buffer[index]['CPOS']
	except IndexError:
		pass
	return "STACK2NEXT_" + stacktop2 + "|" + stacktop1 + "|**" + buffertop

def construct_stacks3(stack, buffer, arc, index):
	stacktop1 = "NULL"
	stacktop2 = "NULL"
	stacktop3 = "NULL"
	buffertop = ""
	try:
		stacktop3 = stack[1:][-3]['CPOS']
		stacktop2 = stack[1:][-2]['CPOS']
		stacktop1 = stack[1:][-1]['CPOS']
	except IndexError:
		try:
			stacktop3 = stack[1:][-2]['CPOS']
			stacktop2 = stack[1:][-1]['CPOS']
		except IndexError:
			try:
				stacktop3 = stack[1:][-1]['CPOS']
			except IndexError:
				pass
	try:
		buffertop = buffer[index]['CPOS']
	except IndexError:
		pass
	return "STACK3NEXT_" + stacktop3 + "|" + stacktop2 + "|" + stacktop1 + "|**" + buffertop

def construct_stacks(stack, buffer, arc, index, parent, children, label):
	return ' '.join([construct_stacks1(stack, buffer, arc, index),
					construct_stacks2(stack, buffer, arc, index),
					construct_stacks3(stack, buffer, arc, index)])

def combined_feature(stack, buffer, arc, index, parent, children, label):
	Stack = [stack[-1]]
	try:
		Stack.append(stack[-2])
	except IndexError:
		Stack.append(None)
	FORM = 'form'
	LEMMA = 'lemma'
	POSTAG = 'POS'
	CPOSTAG = 'CPOS'
	FEATS = 'feats'
	DEPREL = 'deprel'
	CHUNK_ID = 'chunkId'
	NUMBER = 'num'
	PERSON = 'pers'
	Input = []
	try:
		Input.append(buffer[index])
	except IndexError:
		Input.append(None)
	
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
				if label[word['index']]:
					return label[word['index']]
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
		return buffer[int(word['index']) - 2]
	def head(word):
		if not word:
			return None
		return parent[word['index']]
	def ldep(word):
		if not word:
			return None
		try:
			return children[word['index']][0]
		except IndexError:
			return None
	def rdep(word):
		if not word:
			return None
		try:
			return children[word['index']][-1]
		except IndexError:
			return None
	def rdep2(word):
		if not word:
			return None
		try:
			return children[word['index']][-2]
		except IndexError:
			return None

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
			Merge(InputColumn(FEATS, Stack[0]), OutputColumn(DEPREL, Stack[0]))]

	split_feat = ['STACK0_FEAT_%s'%feat for feat in feature_set[0]] + ['INPUT0_FEAT_%s'%feat for feat in feature_set[1]]
	return ' '.join(['FEAT_%d_%s'%(ind, val) for (ind, val) in enumerate(feature_set[2:])]) + ' '.join(split_feat)
