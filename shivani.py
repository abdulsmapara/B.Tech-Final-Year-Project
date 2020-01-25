import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span, Token, Doc  

Doc.set_extension('is_fact', default=False)

def check_verb(doc):
	flag = False
	for token in doc:
		if token.lemma_ == 'increase' or token.lemma_ == 'swell':
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

input_text = "State Bank of India’s (SBIN) Q1FY20 PAT of Rs 23bn was in line with our estimate. Asset quality was a miss with the stressed book swelling to Rs 274bn (vs Rs 77.6bn in Q4) as SBIN is resolving standard accounts worth Rs 191.4bn post RBI’s 7 June circular. Fresh slippages at Rs 162bn (vs Rs 75bn in Q4FY19) included (1) a Maharatna PSU account worth Rs 20bn that saw a delays in signing the inter-creditor agreement, (2) agri slippages worth Rs 20bn from one state in the wake of the farm loan waiver, and (c) SME slippages of Rs 40bn  (Rs 70bn in Q1FY19) as RBI’s restructuring dispensation was withdrawn. Loan growth at 14% YoY was steady, underpinned by a ~12%/19% increase in corporate/retail credit. Retail loan growth was fuelled by a ~28% rise in home loans. Domestic NIM increased 6bps QoQ to 3% (FY20 guidance at 3.15%). Interest reversals stood at Rs 27.9bn as interest accrued was reversed on agriculture loan slippage in Q1."
input_sentences = list(input_text.split(". "))
#print(input_sentences)

obj = ''
for sentence in input_sentences:
	doc = nlp(sentence.lower())
	check_verb(doc)
	sub ='' 
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



		print (sub+" "+verb+sentence) 








