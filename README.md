# fake_news_det
A graduation project about detecting Fake News on the Twitter Platform.

The application consists of seven files:

1) Dotenv file:
    contains the Twitter Bot account's tokens and the ElephantSQL (PostgreSQL as a Service) API tokens.
    Here is the Twitter Bot account: https://twitter.com/ManaaBot

2) Application.py: 
    is the main file that assembles all the other files.

3) ManaaBot.py:
    consists of Twitter API and Client objects and other functions like extracting the tweets' texts and interpreting the claim truthfulness.
    It also uses the Google Search API to get many results that are related to the claim.

4) ManaaDB.py:
    consists of PostgreSQL database connection object.

5) ManaaText.py:
    where the claim is analyzed with many methods (sentiments, meanings and structures of the sentences).

6) pa_clf.pkl:
    is a Pickle file of the Passive Aggressive Classifier used for the classification of the News.

7) tfidf_vect.pkl:
    is a TFIDF transformer used for the conversion of a sentence to a numerical vector.


I hope this helps to clarify my Project. It is the first time that I upload an official Project for myself.