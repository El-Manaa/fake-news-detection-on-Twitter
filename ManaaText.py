#!/usr/bin/python3
# File = ManaaText.py

from re import sub
from spacy import load as spacy_load
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from pickle import load as pkl_load
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from newspaper import Article
from math import exp

nlp = spacy_load("en_core_web_md") # Load medium-sized trained english pipeline model
ps = PorterStemmer() # Word Stemmer : change,changes,changement,changing --> chang
analyzer = SentimentIntensityAnalyzer() # Sentiment Analyzer

cor = lambda text:(
	review := sub(
		pattern = r"[^a-zA-Z]",
		repl = " ",
		string = text
	).lower().split(),
	" ".join([
		ps.stem(W)
		for W in review
		if W not in stopwords.words("english")
	])
)[1] # Text preprocessing & stemming function

with open("tfidf_vect.pkl","rb") as t,open("pa_clf.pkl","rb") as p:
	tfidf_vect = pkl_load(t) # TFIDF algorithm Vectorizer
	pa_clf = pkl_load(p) # Passive Aggressive Classifier algorithm

# Vectorize the article's text/title
def article_vect(text:str):
	c = cor(text)
	v = tfidf_vect.transform([c]).toarray()
	return v

# Cosine Similarity between the two texts' structures : S_C
def cos_sim(text1:str,text2:str) -> float:
	v1 = article_vect(text1)
	v2 = article_vect(text2)
	return round(cosine_similarity(v1,v2)[0][0],3)

# Logistic-like function
logis_sen = lambda x : isinstance(x,float|int) and 1 / (1 + exp(x))

# Semantic & Sentimental Similarity (Semanto-sentiment similarity) : S_S
def sem_sen(text1:str,text2:str) -> float:
	# Sentiment Similarity
	sentiment1 = analyzer.polarity_scores(text1)["compound"]
	sentiment2 = analyzer.polarity_scores(text2)["compound"]
	sen = logis_sen(abs(sentiment1 - sentiment2))
	# Semantic Similarity
	nlp1 = nlp(text1)
	nlp2 = nlp(text2)
	if nlp1 and nlp2:
		sem = nlp1.similarity(nlp2)
		# Semanto-sentiment similarity
		return round(2*sem*sen,3)
	else:
		return 0

# Model's prediction of the text : S_P
def predict_text(text:str) -> int:
	c = cor(text)
	v = tfidf_vect.transform([c]).toarray()
	return pa_clf.predict(v)[0]
