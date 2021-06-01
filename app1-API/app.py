import requests
import random
import tweepy
import os
# from dotenv import load_dotenv


def main():
    raw_headlines, tw_api=initialize()
    headlines=data_parsing(raw_headlines)
    tweet(tw_api, headlines)


def initialize():
    nyt_api = 'https://api.nytimes.com/svc/topstories/v2/home.json?api-key=lQwZxNJFBYcpRAEZPp9s92tK2FhK3bmM'
    response = requests.get(nyt_api)

    if response.status_code !=200:
        print('Bad response', response.status_code)
        raise Exception
    else:
        raw_headlines = response.json()

    auth = tweepy.OAuthHandler(os.getenv("TW_CONSUMER_KEY"), os.getenv("TW_CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("TW_ACCESS_TOKEN"), os.getenv("TW_ACCESS_TOKEN_SECRET"))
    tw_api = tweepy.API(auth)

    return raw_headlines, tw_api

def data_parsing(raw_headlines):

    i=0
    rand = random.randint(1, raw_headlines['num_results'])

    for result in raw_headlines['results']:
        headlines_nyt = result['abstract']
        i+=1
        if (len(headlines_nyt) < 250) & (int(i)==rand):         #todo need logic to consider cornercase(rand headlines which >250)
            break

    return headlines_nyt


def tweet(tw_api, headlines):
    tw_api.update_status(headlines)
    print('Success')

main()