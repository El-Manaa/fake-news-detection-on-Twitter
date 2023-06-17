#!/usr/bin/python3
# File = Application.py

from ManaaBot import tw,api,client,interprete,extract_searches,get_tweet_text
import time,logging
from tweepy.errors import NotFound,Forbidden
from ManaaDB import conn_pg

logging.basicConfig(
    level=logging.INFO
)
logger = logging.getLogger()

def check_mentions(api,since_id):
	logger.info("Retrieving mentions")
	new_since_id = since_id
	for tweet in tw.Cursor(
		method = api.mentions_timeline,
		since_id = since_id,
		include_entities = True,
		tweet_mode = "extended"
	).items():
		new_since_id = max(since_id,tweet.id)
		if tweet.in_reply_to_status_id is None: continue
		with conn_pg.cursor() as cur:
			cur.execute("select distinct * from tweet_ids")
			T = cur.fetchall()
			b = ((tweet.in_reply_to_status_id_str,) in T)
		if not b:
			logger.info(f"Answering to {tweet.user.screen_name}")
			client.like(tweet_id = tweet.id)
			tweet_from = api.get_status(
				id = tweet.in_reply_to_status_id,
				tweet_mode = "extended"
			)
			text = get_tweet_text(tweet_from)
			try:
				A = extract_searches(text,n = 20)
				api.update_status(
					status = interprete(text,A),
					in_reply_to_status_id = tweet.id,
					auto_populate_reply_metadata = True
				)
			except Forbidden:
				api.update_status(
					status = f"""Hello 😃
	The claim tweet is interpreted.
	Here is the link:
	https://twitter.com/i/web/status/{tweet.in_reply_to_status_id}
	Thank you 🙏""",
					in_reply_to_status_id = tweet.id,
					auto_populate_reply_metadata = True
				)
			except NotFound:
				api.update_status(
					status = """Hello 😃
	The claim tweet is deleted 🗑️.
	Thank you 🙏""",
					in_reply_to_status_id = tweet.id,
					auto_populate_reply_metadata = True
				)
			with conn_pg.cursor() as cur:
				cur.execute("insert into tweet_ids(t_id) values(%s)",(tweet.in_reply_to_status_id,))
		else:continue
	return new_since_id

def main():
    since_id = 1
    while True:
        since_id = check_mentions(
            api = api,
            since_id = since_id
        )
        logger.info("Waiting...")
        time.sleep(5)

if __name__ == "__main__" : main()
