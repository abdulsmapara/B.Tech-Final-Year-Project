import spacy

nlp = spacy.load('en', disable=['parser', 'ner'])

file = open('semi_facts.txt', 'r', encoding='utf8')
i_verbs = open('inc_verbs.txt', 'r', encoding='utf8')
d_verbs = open('dec_verbs.txt', 'r', encoding='utf8')
inc_verbs = i_verbs.read().split("\n")
dec_verbs = d_verbs.read().split("\n")
f2 = open('neg_words.txt', 'r', encoding='utf8')
neg = f2.read().split("\n")
facts = file.read().split('\n')
pos_facts = []
neg_facts = []
i = 0
d = 0 
n = 0
for f in facts:
	parts = f.split('|')
	word = nlp(parts[1])
	for token in word:
		base_verb = token.lemma_
		#print(base_verb)
	if base_verb in inc_verbs:
		i=i+1
		pos_facts.append(f)
	elif base_verb in dec_verbs:
		d=d+1
		neg_facts.append(f)
	else:
		n=n+1



'''
if i<d:
	print("More negative facts")
elif i>d:
	print("More positive facts")
else:
	print("Equal number of positive and negative facts")
'''


print("Positive facts")
for f in pos_facts:
	print(f)


print("Negative facts")
for f in neg_facts:
	print(f)