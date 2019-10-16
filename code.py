from module import *

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

if __name__ == '__main__':
	'''Training'''
	custom_train_NER(model=None, TRAIN_DATA=TRAIN_DATA, model_file='../ner_model/spacy_ner_custom_1', no_iteration=100)
	print()
	'''Testing'''
	model = "../ner_model/spacy_ner_custom_1"
	test_NER("test_data.txt", model=model)
	print()