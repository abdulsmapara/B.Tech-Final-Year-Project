from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from datetime import datetime
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import nltk
import spacy
from spacy.symbols import VERB
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import re
import pickle
import numpy as np
import os
from svo import semi_structured_extraction_all
nlp = spacy.load('en_core_web_sm')
nltk.download('punkt')

'''
	Extracts creation date YYYY-MM-DD of a pdf present at the given path
'''
def getPdfDate(path):
	# Using metadata
	success_metadata = True
	date_metadata = ""
	try:
		def convertPdfDatetime(pdf_date_extracted):
			dtformat = "%Y%m%d%H%M%S"
			clean = pdf_date_extracted.decode("utf-8").replace("D:","").split('+')[0]
			return datetime.strptime(clean,dtformat)
		fp = open(path, 'rb')
		parser = PDFParser(fp)
		doc = PDFDocument(parser)
		date_metadata = str.split(str(convertPdfDatetime(doc.info[0]["CreationDate"])) , " ")[0]
		return date_metadata
	except Exception as e:
		success_metadata = False
		pass
	finally:
		fp.close()

	# Using NER
	rsrcmgr = PDFResourceManager()
	sio = StringIO()
	codec = 'utf-8'
	laparams = LAParams()
	device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
	interpreter = PDFPageInterpreter(rsrcmgr, device)

	# Extract text
	fp = open(path, 'rb')
	for page in PDFPage.get_pages(fp):
	    interpreter.process_page(page)
	    break
	fp.close()

	# Get text from StringIO
	text = sio.getvalue()

	# Cleanup
	device.close()
	sio.close()

	parsed_text = nlp(text)
	for ent in parsed_text.ents:
		if ent.label_ == "DATE":
			date = ent.text
			break
	# Compare the dates

	return date

def get_text_from_pdf(path):
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    # close open handles
    converter.close()
    fake_file_handle.close()
    if text:
        return text

def get_important_sentences(text, keywords):
	facts = []
	for sentence in nltk.tokenize.sent_tokenize(text):
		sent = sentence.replace("\n"," ")
		if len(sent.split(" ")) > 35: # Too long fact
			continue
		for keyword in keywords:
			if keyword in sent.lower():
				parsed_sent = nlp(sent)
				for token in parsed_sent:
					if token.pos == VERB:
						facts.append(sent)
						break
				break
	return facts

def get_facts(files,num,subjects):
	texts = []
	dates = []
	for path in files:
		dates.append(getPdfDate(path))
		texts.append(get_text_from_pdf(path))
	keywords = []

	with open("keywords.txt","r") as f:
		all_keywords = f.read()
		for keyword in all_keywords.split("\n"):
			keywords.append(keyword)
		f.close()

	facts = {}
	for text,date in zip(texts,dates):
		svo = semi_structured_extraction_all(text, subjects)
		fact = get_important_sentences(text, keywords)
		facts[date] = (fact, svo)
		print(svo)
	return facts



def label_sentences(data):
	MAX_SEQUENCE_LENGTH = 100
	def get_tokens(text):
		text = nlp(text)
		tokens = []
		for token in text:
			tokens.append(token.text)
		return tokens

	def preprocessing(text):
		text_nopunct = ''
		text_nopunct = re.sub('['+'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'+']', '', text)
		text = nlp(text_nopunct.lower())
		final_text = ""
		for token in text:
		    if token.is_stop == False:
		        final_text += token.text + " "
		return final_text.strip()
	with open('tokenizer.pickle', 'rb') as handle:
		tokenizer = pickle.load(handle)
		model = load_model("cnn_model_temp.h5")
		sentences = []
		original_sentences = []
		for sentence in data:
			original_sentences.append(sentence)
			sentences.append(preprocessing(sentence))
		test_sequences = tokenizer.texts_to_sequences(sentences)
		test_cnn_data = pad_sequences(test_sequences, maxlen=MAX_SEQUENCE_LENGTH)
		predictions = model.predict(test_cnn_data)
		labels = ['POS','NEG','NEU']
		result = []
		i = 0
		for p in predictions:
			result.append((original_sentences[i],labels[np.argmax(p)]))
			i += 1
		return result
	return None

def deleteDir(dirPath):
	deleteFiles = []
	deleteDirs = []
	for root, dirs, files in os.walk(dirPath):
		for f in files:
			deleteFiles.append(os.path.join(root, f))
		for d in dirs:
			deleteDirs.append(os.path.join(root, d))
	for f in deleteFiles:
		os.remove(f)
	for d in deleteDirs:
		os.rmdir(d)
	os.rmdir(dirPath)

if __name__ == '__main__':
	n = int(input("Number of pdfs\t"))
	texts = []
	dates = []
	for i in range(n):
		path = input("Path of pdf\t")
		dates.append(getPdfDate(path))
		texts.append(get_text_from_pdf(path))

	keywords = []

	with open("keywords.txt","r") as f:
		all_keywords = f.read()
		for keyword in all_keywords.split("\n"):
			keywords.append(keyword)
		f.close()
	facts = []
	import textacy
	nlp = spacy.load('en')
	for content in texts:
		semi_structured_extraction_all(content,["SBI","SBIN", "State Bank of India"])
	# print("FACTS:")
	# for text,date in zip(texts,dates):
	# 	fact = get_important_sentences(text, keywords)
	# 	facts.append((date,fact))
