import spacy
import textacy
import textacy.keyterms
import textacy.preprocessing
import sys
import warnings
import random


TRAIN_DATA = [('SBI is the largest bank in India.', {'entities': [(0, 3, 'ORG')]}),
			  ('Axis Bank is the second largest bank in India.', {'entities': [(0, 9, 'ORG')]}),
			  ('Bank of Baroda is the third largest bank in India.', {'entities': [(0, 14, 'ORG')]}),
			  ('Bank of Maharashtra is the fourth largest bank in India.', {'entities': [(0, 19, 'ORG')]}),
			  ('Bank of India is the fifth largest bank in India.', {'entities': [(0, 13, 'ORG')]}),
			  ('Canara Bank is the sixth largest bank in India.', {'entities': [(0, 11, 'ORG')]}),
			  ('Central Bank of India is the seventh largest bank in India.', {'entities': [(0, 21, 'ORG')]}),
			  ('Indian Overseas Bank is the eighth largest bank in India.', {'entities': [(0, 20, 'ORG')]}),
			  ('Union Bank of India is the ninth largest bank in India.', {'entities': [(0, 19, 'ORG')]}),
			  ('HDFC is the tenth largest bank in India.', {'entities': [(0, 4, 'ORG')]}),
			  ('ICICI is the eleventh largest bank in India.', {'entities': [(0, 5, 'ORG')]}),
			  ('Kotak Mahindra Bank is the twelfth largest bank in India.', {'entities': [(0, 19, 'ORG')]}),
			  ('Yes Bank is the thirteenth largest bank in India.', {'entities': [(0, 8, 'ORG')]})]


def train_spacy(data,iterations):
    TRAIN_DATA = data
    nlp = spacy.blank('en')  # create blank Language class
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
       

    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Statring iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)
    return nlp






if __name__ == '__main__':
	warnings.filterwarnings("ignore")

	prdnlp = train_spacy(TRAIN_DATA, 20)
	# Save our trained Model
	modelfile = 'spacy_tm_1'				# one
	prdnlp.to_disk(modelfile)
	
	#file = textacy.io.read_text("Virat.txt",lines=True)
	file = textacy.io.read_text("doc2.txt",lines=True)
	prdnlp = spacy.load('spacy_tm_1')
	#nlp = spacy.load("en_core_web_sm")
	content = ""
	for line in file:
		line = textacy.preprocessing.remove_punctuation(line)
		docx = textacy.doc.make_spacy_doc(line)
		content += str(docx)
	docx = prdnlp(content)
	print(list(textacy.extract.entities(docx)))
	mp = {}
	for entity in docx.ents:
		if entity.label_ == 'ORG':
			mp[entity.text] = entity.sent
	print('')
	print('NAMED ENTITY RECOGNITION:')
	print([(entity.text,entity.label_) for entity in docx.ents])
	for i in mp:
		print("{}: {}".format(i,mp[i]))
		print('\n')