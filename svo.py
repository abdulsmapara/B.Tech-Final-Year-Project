import spacy
nlp = spacy.load('en')
import nltk
from spacy import displacy

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

def svo(sentences, subjects):
	svo_list = []
	for sentence in sentences:
		doc = nlp(sentence)
		prev_token_1 = ''
		prev_token_2 = ''
		# displacy.serve(doc, 'dep')
		prev_sub = ""
		is_noun_1 = False
		is_noun_2 = False
		for token in doc:
			if token.pos_ == "VERB" and token.dep_ != "aux":
				verb = token.lemma_
				subject = ""
				obj = ""
				extra_sub_text = ''
				extra_sub = ''
				new_sub = ''
				for child in token.children:
					if child.dep_ == "nsubj":
						subject = child.text
						for further_child in child.children:
							if further_child.dep_ == "prep":
								if further_child.pos_ == "NOUN" or further_child.pos_ == "PROPN":
									extra_sub = further_child.text
						for chunk in doc.noun_chunks:
							if chunk.root.text == subject:
								new_sub = chunk.text
							if chunk.root.head.text == extra_sub:
								extra_sub_text = chunk.text
					elif child.dep_ == "attr" or child.dep_ == "pobj" or child.dep_ == "dobj" or child.dep_ == "acomp" or child.dep_ == "xcomp":
						obj = child.text + " " + obj
						while True:
							loops = False
							for further_child in child.children:
								if further_child.dep_ == "amod" or further_child.dep_ == "compound":
									obj = further_child.text + " " + obj
									break
									loops = True
							child = further_child
							if not loops:
								break
					elif child.dep_ == "prep":
						obj = obj + " " + child.text
						for more_child in child.children:
							if more_child.dep_ == 'pobj' or more_child.dep_ == 'dobj':
								for another_child in more_child.children:
									another_child_string = ''
									for new_child in another_child.children:
										another_child_string = new_child.text + ' ' + another_child_string
									another_child_string = another_child_string + ' ' + another_child.text
									if more_child.text not in obj:
										obj = obj + ' ' + another_child_string + ' ' + more_child.text
									else:
										obj += ' ' + another_child_string
				
				subject = new_sub + ' ' + extra_sub + ' ' + extra_sub_text

				if len(subject.strip()) == 0:
					# Window approach
					if is_noun_1 and is_noun_2:
						subject = prev_token_2 + ' ' + prev_token_1
					elif prev_token_1 in subjects or (is_noun_1):
						subject = prev_token_1
					elif prev_token_2 in subjects or (is_noun_2):
						subject = prev_token_2
					# for conjunctions
					elif prev_token_1 in ["but", "and"]:
							subject = prev_sub
				else:
					prev_sub = subject
				if (len(subject.strip()) > 0 and len(verb.strip()) >0 and len(obj.strip()) > 0):
					svo_list.append(subject.strip() + "|" + verb.strip()+"|" + obj.strip())
			if is_noun_1:
				is_noun_2 = True
				is_noun_1 = False
			else:
				is_noun_2 = False
			if token.pos_ == "NOUN":
				is_noun_1 = True
			else:
				is_noun_1 = False
			prev_token_2 = prev_token_1
			prev_token_1 = token.text
	print(svo_list)
	return svo_list

def semi_structured_extraction_all(content, subjects):
	# for each sentence
	sentences_to_consider = []
	# displacy.serve(nlp(content), 'dep')
	for sentence in nltk.tokenize.sent_tokenize(content):
		sent = sentence.replace("\n"," ")
		if len(sent.split(" ")) > 35:
			continue
		doc = nlp(sent)
		for token in doc:
			if (token.pos_ == "PROPN" and str(token) in subjects) or (token.pos_ == "NOUN" and str(token).lower() == "bank"):
				sentences_to_consider.append(sent)
	return svo(sentences_to_consider, subjects)

# def semi_structured_extraction(content):
#     doc = nlp(content)
#     chunks_dict = dict()
#     for chunk in doc.noun_chunks:
#         chunks_dict[chunk.root.text] = chunk.text

#     sub = ''
#     obj = ''
#     new_sub = ''
#     fact_list = []
#     flag = 0
#     for token in doc:
#         if token.dep_ == 'ROOT':
#             comp_obj = ''
#             prep_obj = ''
#             extra_sub = ''
#             for child in token.children:
#                 if child.dep_ == 'nsubj':
#                     sub = child.text
#                     for more_child in child.children:
#                         if more_child.dep_ == 'prep':
#                             extra_sub = more_child.text
#                     for chunk in doc.noun_chunks:
#                         if chunk.root.text == sub:
#                             new_sub = chunk.text
#                         if chunk.root.head.text == extra_sub:
#                             extra_sub_text = chunk.text
#                             flag = 1
#                     if flag == 1:
#                         new_sub = new_sub + ' ' + extra_sub + ' ' + extra_sub_text
#                         flag = 0
#                         extra_sub = ''
#                         extra_sub_text = ''
#                 if child.dep_ == 'prep':
#                     for more_child in child.children:
#                         if more_child.dep_ == 'pobj' or more_child.dep_ == 'dobj':
#                             obj = more_child.text
#                             for another_child in more_child.children:
#                                 another_child_string = ''
#                                 for new_child in another_child.children:
#                                         another_child_string = new_child.text + ' ' + another_child_string
#                                 another_child_string = another_child_string + ' ' + another_child.text
#                                 obj = another_child_string + ' ' + obj
#                         prep_obj = prep_obj + ' ' + obj
#                 if child.dep_ == 'dobj' or child.dep_ == 'pobj' or child.dep_ == 'attr':
#                     obj = child.text
#                     for chunk in doc.noun_chunks:
#                         if chunk.root.head.text == token.text and chunk.root.text == child.text:
#                             obj = chunk.text
#                     comp_obj = comp_obj + ' ' +obj

#                 if child.dep_ == 'xcomp':
#                     more_verb = child.text
#                     for more_child in child.children:
#                         if more_child.dep_ == 'ccomp':
#                             for chunk in doc.noun_chunks:
#                                 if chunk.root.head.text == more_child.text:
#                                     obj = chunk.text
#                     comp_obj = more_verb + ' ' + obj



#             if new_sub != '' and token.text != '' and (prep_obj != '' or comp_obj != ''):
#                 if prep_obj != '':
#                     prep_obj = prep_obj.replace('\n', '')
#                 if comp_obj != '':
#                     comp_obj = comp_obj.replace('\n', '')
#                 if '\n' in new_sub:
#                     index = new_sub.find('\n')
#                     if index != -1:
#                         new_sub = new_sub[index+1:]
#                     for c in new_sub:
#                         if ord(c) > 256:
#                             new_sub = new_sub.replace(c,'')
#                     while new_sub[0] == ' ':
#                         new_sub = new_sub[1:]
#                 new_str = new_sub + ' | ' + token.text + ' | ' + prep_obj +  comp_obj
#                 if new_str not in fact_list:
#                     fact_list.append(new_str)
#                     new_sub = ''
#                     comp_obj = ''
#                     extra_sub = ''
#                     extra_sub_text = ''

#     return fact_list

if __name__ == '__main__':
	n = 2
	texts = []
	dates = []
	path = "uploads/127.0.0.1/StateBankofIndia-2Aug.pdf"
	# path = input("Path of pdf\t")
	texts.append(get_text_from_pdf(path))
	texts.append(get_text_from_pdf("uploads/127.0.0.1/SBI_DEC_19.pdf"))

	import textacy
	nlp = spacy.load('en')
	for content in texts:
		semi_structured_extraction_all(content,["SBI","SBIN", "State Bank of India"])
