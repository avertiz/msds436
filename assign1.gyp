import tweepy
import pandas as pd
import boto3
from io import StringIO
import numpy as np


def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)

# Using Twitter API to form tabular data set of n = 50

 
# Connect to Twitter API 
consumer_key = ''
consumer_secret = ''
access_key= ''
access_secret = ''

#pass twitter credentials to tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

search_words = 'to:realDonaldTrump'
data_since = "2020-05-1"

tweets = tweepy.Cursor(api.search,
              q=search_words,
              lang="en",
              since=data_since).items(50)

# Past 50 tweets to @Trump
r = [[tweet.text,tweet.user.location,tweet.user.screen_name,tweet.place] for tweet in tweets]

table = pd.DataFrame(data=r,columns=['Text', "User Location","Screen Name","Coordinates"])

table.replace('', 'test', inplace=True)
table.fillna("Test2",inplace=True)
table.replace(',','', regex=True, inplace=True)
table.replace('"','', regex=True, inplace=True)
table.replace('@','', regex=True, inplace=True)
table.replace('\n','', regex=True, inplace=True)
print(table)

aws_access_key_id=''
aws_secret_access_key=''
aws_session_token=''

s3= boto3.client('s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token = aws_session_token)

#table["Text"] = table["Text"].apply(remove_non_ascii)

csv_buffer = StringIO()
table.to_csv(csv_buffer,index=False)

response = s3.put_object(Body =csv_buffer.getvalue(),
                        Bucket = 'msds436assign1',
                        Key = 'twitter_data.csv')
