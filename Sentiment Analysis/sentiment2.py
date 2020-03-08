import pandas as pd
import nltk
import numpy as np




'''
	Returns labelled data for sentiment analysis
	Classes: ['POS','NEG','NEU']
	https://medium.com/@b.terryjack/nlp-pre-trained-sentiment-analysis-1eb52a9d742c
'''
def get_labelled_data(unlabelled_data, tag):
	news_data = unlabelled_data
	count_pos = 0
	count_neg = 0
	count_neu = 0
	statements = []
	labels = []	
	for ind in news_data.index:
		statement = news_data[tag][ind]
		scores = sid.polarity_scores(statement)
		maximum = max(scores['neu'], scores['pos'], scores['neg'])
		label = "POS"
		if maximum == scores['neu']:
			label = "NEU"
			random_val = np.random.rand(1,1)
			if random_val[0][0] >= 0.98:
				statements.append(statement)
				labels.append(label)
				print(ind,' ' ,label)
				count_neu += 1
		elif maximum == scores['neg']:
			label = "NEG"
			random_val = np.random.rand(1,1)
			print(random_val[0][0])
			if random_val[0][0] >= 0.85:
				statements.append(statement)
				labels.append(label)
				print(ind,' ' ,label)
				count_neg += 1
		else:
			statements.append(statement)
			labels.append(label)
			print(ind,' ' ,label)
			count_pos += 1
		
	print(statements,'\n',labels)
	final_data = {'SENTENCE': statements, 'LABEL': labels}
	df = pd.DataFrame(final_data, columns= ['SENTENCE', 'LABEL']) 
	df.to_csv('labelled_news.csv') 
	print(count_pos, ' ',count_neg, ' ',count_neu)
	return df

if __name__ == '__main__':
	nltk.download('vader_lexicon')
	from nltk.sentiment.vader import SentimentIntensityAnalyzer
	sid = SentimentIntensityAnalyzer()
	unlabelled_data = pd.read_csv("RedditNews.csv")
	tag = 'News'
	df = get_labelled_data(unlabelled_data, tag)