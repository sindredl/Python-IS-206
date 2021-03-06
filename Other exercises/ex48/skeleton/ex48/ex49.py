import lexicon
import inputAlgo

class ParserError(Exception):
    pass

class Respond(object):
	def __init__(self, subject, verb, object):
		self.subject = subject[1]
		self.verb = verb[1]
		self.object = object[1]
		
def build_response(sa):
	if sa.is_noun == True:
		print "%s, you cant %s the %s" % (sa.subject, sa.verb, sa.object)
	else:
		print "%s, you cant %s %s" % (sa.subject, sa.verb, sa.object)

class Sentence(object):
	def __init__(self, subject, verb, object,is_noun):
		self.subject = subject[1] #Player
		self.verb = verb[1] #go
		self.object = object[1] #door /north
		self.is_noun = is_noun


def peek(word_list):
	if word_list:
		word = word_list[0]
		return word[0]
	else:
		return None


def match(word_list, expecting):
	if word_list:
		word = word_list.pop(0)
		if word[0] == expecting:
			return word
		else:
			return None
	else:
		return None


def skip(word_list, word_type):
	while peek(word_list) == word_type:
		match(word_list, word_type)


def parse_verb(word_list):
	skip(word_list, 'stop')
	if peek(word_list) == 'verb':
		return match(word_list, 'verb')
	else:
		raise ParserError("Expected a verb next.")


def parse_object(word_list):
	skip(word_list, 'stop')
	next = peek(word_list)
	if next == 'noun':
		return match(word_list, 'noun')
	if next == 'direction':
		return match(word_list, 'direction')
	else:
		raise ParserError("Expected a noun or direction next.")

def parse_object_type(word_list):
	skip(word_list, 'stop')
	next = peek(word_list)
	if next == 'noun':
		return True
	elif next == 'direction':
		return False

def parse_subject(word_list, subj):
	verb = parse_verb(word_list)
	is_noun = parse_object_type(word_list)
	obj = parse_object(word_list)
	return Sentence(subj, verb, obj,is_noun)


def parse_sentence(word_list):
	skip(word_list, 'stop')
	start = peek(word_list)
	if start == 'noun':
		subj = match(word_list, 'noun')
		return parse_subject(word_list, subj)
	elif start == 'verb':
		return parse_subject(word_list, ('noun', 'you'))
	else:
		raise ParserError("Must start with subject, object, or verb not: %s" % start)
		
def starter(user):
	list = user.split()
	if len(list) > 1:
		sent = parse_sentence(lexicon.scan(user))
		build_response(sent)
	else:
		tin = lexicon.scan(user)
		if tin[0][0] == 'verb':
			print "%s is not sufficient. You must also supply a object" % tin[0][1]
		else:
			print "I dont uderstand that"
		
#user = raw_input()
#starter(user)


#Testing the advanced input functionality



	#build_response(sent)



#if sent[0][0] == "error":
#	print "ERrrr"


def valid_sent(input):
	sent = lexicon.scan(input)
	verb_index = 1000
	object_index = 1000
	stop_count = 0
	verb_count = 0
	object_count = 0
	for i, item in enumerate(sent):
		if item[0] == "verb":
			verb_index =  i
			verb_count += 1
		if item[0] == "noun" or item[0] == "direction":
			object_index =  i
			object_count += 1
		if item[0] == "stop" and object_index > i:
			stop_count += 1
	total_count = stop_count + verb_count
	if object_index == verb_index + 1 + stop_count and total_count < 3:
		return True
	else:
		return False

#If for instance the user types a direction two times north north, the function will allow this
def make_valid_sent(input):
	sent = lexicon.scan(input)
	verb = ""
	object =""
	for word in sent:
		if word[0] == "verb":
			verb = word
		elif word[0] == "noun" or word[0] == "direction":
			object = word
			
		
#test case
#while(True):
#	input = raw_input()
#	ignore_case = input.lower()
#	if len(ignore_case.split()) == 1:
#		print inputAlgo.simple_resp(ignore_case, inputAlgo.levels)
#	else:
#		if valid_sent(ignore_case):
	#		sent = parse_sentence(lexicon.scan(ignore_case))
	#		print inputAlgo.respond_dir(sent,inputAlgo.levels,lexicon,0)
	#	else:
	#		print inputAlgo.get_error_message()
			
def process_input(input, lista):
	ignore_case = input.lower()
	if len(ignore_case.split()) == 1:
		return inputAlgo.simple_resp(ignore_case, inputAlgo.levels)
	else:
		if valid_sent(ignore_case):
			sent = parse_sentence(lexicon.scan(ignore_case))
			return inputAlgo.respond_dir(sent,lista,lexicon,0)
		else:
			return inputAlgo.get_error_message()
	