from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime,date
from textblob import TextBlob

import twitter_credentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


ACCESS_TOKEN="190966353-2JGJYKwW5dyOxqYjfsIFw73GUN0EW2ZU9iwzQhiY"
ACCESS_TOKEN_SECRET="eifop9dvmkNPFI4m70W7fwHuT7kkhEaUSsAAzBLGVMobv"
CONSUMER_KEY="W532jHI4JrqaaTFkd6dyWrNKQ"
CONSUMER_SECRET="DfsLFFvWbERBMBzPlkThQGqa96upxZZxRgNqZYqtfrVBRu7wZV"

'''Authenticating'''

auth = OAuthHandler(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
api = API(auth,wait_on_rate_limit=True)

'''
creating defintions for later use
'''
def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def percentage(part,whole):
	return (part/whole)*100

def sentiment(sentiments):
	sorted_dict = {k:v for k,v in sorted(sentiments.items(), key=lambda item: item[1])}
	print(list(sorted_dict.keys())[-1])


'''
For users to input the term to perform the sentiment analysis on and the number of tweets to analyze
'''
searchTerm = input("Enter keyword to search about: ")
#searchNumber = int(input("Enter how many tweets to analyze: "))
#date_created = datetime.strptime('2020-02-01', '%Y-%m-%d')
#max_date = datetime.strptime('2020-02-02', '%Y-%m-%d')

'''
api.search returns a collection of relevant tweets matching a specific search query
Cursor is required for pagination based on the requests

'''
tweets = Cursor(api.search,q=searchTerm,lang="en").items(500)
sentiment_values = {'positive':0,'negative':0,'neutral':0}
'''
positive = 0
negative = 0
neutral = 0
'''
polarity = 0

'''
looping through every tweet to obtain the sentiment
'''
for tweet in tweets:
	#analysis = TextBlob(clean_tweet(tweet.text))
	analysis = TextBlob(tweet.text)
	polarity += analysis.sentiment.polarity

	if analysis.sentiment.polarity < 0.00:
		sentiment_values['negative'] += 1
	elif analysis.sentiment.polarity > 0.00:
		sentiment_values['positive'] +=1
	elif analysis.sentiment.polarity == 0:
		sentiment_values['neutral'] += 1

'''
obtaining the percentage of positive, negative and neutral sentiments
'''
positive_percentage = format(percentage(sentiment_values['positive'],500),'.2f')
negative_percentage = format(percentage(sentiment_values['negative'],500),'.2f')
neutral_percentage = format(percentage(sentiment_values['neutral'],500),'.2f')

sentiment(sentiment_values)


labels = ['Positive ['+ str(positive_percentage)+ '%]','Neutral ['+ str(neutral_percentage)+ '%]','Negative ['+ str(negative_percentage)+ '%]']
sizes = [positive_percentage,neutral_percentage,negative_percentage]
colors = ['blue','gold','pink']
patches,text = plt.pie(sizes,colors=colors,startangle=90)
plt.legend(patches,labels,loc="upper left")
plt.title("How are people reacting to " + searchTerm + " by analyzing " + str(500) + " tweets")
plt.axis('equal')
plt.tight_layout()
plt.show()


'''
		#df = pd.DataFrame(data=[tweet.text],columns=["Tweets"])
		df=pd.DataFrame(data=[tweet.created_at.date()],columns=["Date"])

		df['Positive Sentiment'] = np.array([positive])
		df['Negative Sentiment'] = np.array([negative])
		df['Neutral Sentiment'] = np.array([neutral])
		df.groupby("Date").sum()
		print(df.head(10))
'''

