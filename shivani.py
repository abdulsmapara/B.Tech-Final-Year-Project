import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span, Token, Doc  

Doc.set_extension('is_fact', default=False)

def check_verb(doc):
	flag = False
	for token in doc:
		if token.lemma_ == 'swell' or token.lemma_ == 'increase' or token.lemma_ == 'grow':
			flag = True

	if flag == True:
		doc._.is_fact = True
def blackie(object_sentence,word):
	for item in word.children:
		object_sentence.append((item.text,item.i))
		blackie(object_sentence,item)
	

def Sort_Tuple(tup):  
	  
	# getting length of list of tuples 
	lst = len(tup)  
	for i in range(0, lst):  
		  
		for j in range(0, lst-i-1):  
			if (tup[j][1] > tup[j + 1][1]):  
				temp = tup[j]  
				tup[j]= tup[j + 1]  
				tup[j + 1]= temp  
	return tup


	



nlp = spacy.load('en_core_web_sm')
file = open("input_asli.txt", "r",encoding="utf8")
input_text = file.read()
input_sentences = list(input_text.split(". "))
f = open("output_asli.txt", "a")

#print(input_sentences)

facts = ''
for sentence in input_sentences:
	doc = nlp(sentence.lower())
	check_verb(doc)
	sub =''
	obj = '' 
	sub_pos = None
	verb = ''
	object_sentence = []
	if doc._.is_fact == True:
		# for token in doc:
		# 	print(token.text, token.dep_,[child for child in token.children])
		for token in doc:
			# Getting the Verb
			if token.dep_ == 'ROOT':
				verb = token.text
				# Getting the Subject 
				for child in token.children: 
					if child.dep_ == 'nsubj':
						sub_pos = child.i
						positon_compound = child.i - 1
						flag = False
						if doc[positon_compound].dep_ == 'compound':
							sub = doc[positon_compound].text
							flag = True

						if flag == True:
							sub = sub + ' ' + child.text
						else : 
							sub = child.text

				# Gettting the Object
				for child in token.children:
					if child.dep_ != 'nsubj':
						is_object = True
						# Trying to check if it is a verb having other subject
						for child_lvl2 in child.children:
							if child_lvl2.dep_ == 'nsubj': ###Can check for the other three types
								is_object = False

						if is_object == True:
							
							object_sentence.append((child.text,child.i))
							blackie(object_sentence,child)
				if sub_pos is not None:
					for child in doc[sub_pos].children:
						if child.dep_ != 'nsubj':
							is_object = True
							# Trying to check if it is a verb having other subject
							for child_lvl2 in child.children:
								if child_lvl2.dep_ == 'nsubj': ###Can check for the other three types
									is_object = False

							if is_object == True:
								blackie(object_sentence,child)


				# Sorting the objects
				object_sentence = Sort_Tuple(object_sentence)
				# Sentence
				sentence = ''
				for item in object_sentence:
					sentence = sentence + " " + item[0]


		fact = sub+" "+verb+sentence
		facts = facts + fact
		facts = facts +" "+'hadippa '
facts = facts.replace('\n','')		
facts = list(facts.split('hadippa'))
for fact in facts:
	f.write(fact+"\n")

f.close()






