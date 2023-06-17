#!/usr/bin/python3
# File = ManaaBot.py

import tweepy as tw
from re import match,sub
from os import environ
from logging import getLogger
from newspaper import Article
from ManaaText import *
from googlesearch import search
from statistics import mean
from dotenv import load_dotenv
load_dotenv();

# Twitter API tokens
consumer_key = environ["API_KEY"]
consumer_sec = environ["API_KEY_SECRET"]
access_token = environ["ACCESS_TOKEN"]
access_token_sec = environ["ACCESS_TOKEN_SECRET"]
bearer_token = environ["BEARER_TOKEN"]

# Twitter API authentication credentials
auth = tw.OAuthHandler(consumer_key,consumer_sec)
auth.set_access_token(access_token,access_token_sec)

# Twitter API Client object
client = tw.Client(
    bearer_token= bearer_token,
    consumer_key = auth.consumer_key,
    consumer_secret = auth.consumer_secret,
    access_token = auth.access_token,
    access_token_secret = auth.access_token_secret,
    wait_on_rate_limit = True
)

# Twitter API object
api = tw.API(
    auth,
    wait_on_rate_limit = True
)

def get_tweet_text(status:tw.models.Status) -> tw.models.Status:
	if match(r"^(RT @)",status.full_text):
		sts = status.retweeted_status
	elif status.is_quote_status:
		sts = status
	else:
		if status.truncated:
			sts = api.get_status(
				id = status.id,
				tweet_mode = "extended"
			)
		else:
			sts = status
	return sub(r"(https://t.co/\w+)","",sts.full_text)

def extract_searches(text:str,n:int) -> tuple[str]:
	# Getting Results
	results = search(
		f"\'{text}\' language:en",
		num = n
	)
	return tuple({result for result in results})

def interprete(text:str,A:tuple[str]) -> str:
	C = ();B = ();p = predict_text(text)
	for x in A:# Filtering Results
		try:
			article = Article(url = x)
			article.download()
			article.parse()
			article.nlp()
			tm = article.title
			del article
			c = cos_sim(text,tm)
			s = sem_sen(text,tm)
			# Calculating the Ternary Score
			m = mean((c,s,1.0*p))
			print(f"{(c,s,p)} == {x}")
			if m >= (4*p+5)/12:
				C += (m,)
				B += (x,)
		except:
			continue
	try:# Max value
		p = C.index(max(C))
		print(mn := mean(C))
		verif = f"""Hello 😃
Your claim is ✅TRUE✅
🔎🗒️📰🗞️🔎
You can read access to this link below:
{B[p]}
Thank you 🙏""" if mn >= 0.75 else f"""Hello 😃
Your claim is ❌FAKE❌
🔎🗒️📰🗞️🔎
Bye! Have a great time 🙋️"""
		return verif
	except:
		return f"""Hello 😃
Your claim is ❌FAKE❌
🔎🗒️📰🗞️🔎
Bye! Have a great time 🙋️"""


logger = getLogger()

try:
    api.verify_credentials()
except Exception as e:
    logger.error("Error creating API",exc_info=True)
    raise e

logger.info("API created")
