#	python 3.5
# 	comparision between stanford ner and spacy ner
import csv 
import nltk
import spacy
import textacy

def spacy_tagger(sentence):

	nlp = spacy.load('en')
	docx = nlp(sentence)
	res = []
	mp = {}
	for entity in docx.ents:
		for x in entity.text.split():
			mp[x] = entity.label_
		
	final = []
	for word in sentence.split():
		if word not in mp:
			final.append((word,'O'))
		else:
			final.append((word,mp[word]))
	return final

print('NTLK Version: %s' % nltk.__version__)
from nltk.tag import StanfordNERTagger
stanford_ner_tagger = StanfordNERTagger(
     'stanford-ner-2018-02-27/classifiers/english.muc.7class.distsim.crf.ser.gz',
    'stanford-ner-2018-02-27/stanford-ner-3.9.1.jar'
)

def is_correct(correct,detected,lib):
	ret = False

	if lib == "STANFORD":
		if 'geo' in  correct and detected == "LOCATION":
			ret = True
		elif 'per' in correct and detected == "PERSON":
			ret = True
		elif ('tim' in correct or 'dat' in correct) and detected == "DATE":
			ret = True
		elif 'org' in correct and detected == "ORGANIZATION":
			ret = True
		elif 'gpe' in correct and detected == "LOCATION":
			ret = True
		elif correct == detected:
			ret = True
	elif lib == "SPACY":
		if 'gpe' in correct and (detected == "GPE" or detected == "NORP"):
			ret = True
		elif 'per' in correct and detected == "PERSON":
			ret = True
		elif ('tim' in correct or 'dat' in correct) and detected == "DATE":
			ret = True
		elif 'org' in correct and detected == "ORG":
			ret = True
		elif 'geo' in correct and detected == "LOC":
			ret = True
		elif 'O' in correct and (detected != "LOC" and detected != "ORG" and detected != "DATE" and detected != "PERSON" and detected != "GPE"):
			ret = True
		elif correct == detected:
			ret = True

	return ret
# csv file name 
filename = "../ner_dataset.csv"

# initializing the titles and rows list 
fields = [] 
rows = [] 
results_stanford = []
results_spacy = []

num_correct = 0
num_total = 0
num_correct_spacy = 0
num_total_spacy = 0
with open(filename, 'r+') as csvfile: 
	data = csv.reader(csvfile)
	sent = ''
	count = 0
	correct = []
	for row in data:
		if count > 70:
			break
		if(row[0] == ''):
			print('ROW1 = '+ row[1] + ' CORRECT = ' + row[3])
			correct.append(row[3])
			sent += (row[1] + ' ')
		else:
			results = stanford_ner_tagger.tag(sent.split())
			results_stanford.append(results)
			results = spacy_tagger(sent)
			results_spacy.append(results)

			print('ANALYSING STANFORD ' + sent)
			for i in range(0,len(sent.split())):
				print(correct[i],end=' ')
				print(results_stanford[len(results_stanford)-1][i][1],end= ' ')
				if is_correct(str(correct[i]), str(results_stanford[len(results_stanford)-1][i][1]),"STANFORD"):
					num_correct+=1
					print('PERFECT')
				else:
					print('IMPERFECT')
				num_total+=1
			print('ANALYSING SPACY ' + sent)
			print((results_spacy[len(results_spacy)-1]))
			#print(results_spacy)
			for i in range(0,len(sent.split())):
				print(correct[i],end=' ')
				print(results_spacy[len(results_spacy)-1][i][1],end= ' ')
				if is_correct(str(correct[i]), str(results_spacy[len(results_spacy)-1][i][1]),"SPACY"):
					num_correct_spacy+=1
					print('PERFECT')
				else:
					print('IMPERFECT')
				num_total_spacy+=1
			
			print('ROW1 = '+ row[1] + ' CORRECT = ' + row[3])
			sent = (row[1] + ' ')
			correct = []
			correct.append(row[3])
			count = count + 1
			print("---------------------------------------------"+str(count))
print("STANFORD NER:")
print('NUM CORRECT = ' + str(num_correct))
print('NUM TOTAL = ' + str(num_total))

	
print("SPACY NER:")
print('NUM CORRECT = ' + str(num_correct_spacy))
print('NUM TOTAL = ' + str(num_total_spacy))
