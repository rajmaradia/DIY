import requests
import random
import tweepy
import os
import smtplib
from datetime import datetime

def main():
    raw_headlines, tw_api=initialize()
    headlines=data_parsing(raw_headlines)
    tweet(tw_api, headlines)

def initialize():
    nyt_api = 'https://api.nytimes.com/svc/topstories/v2/home.json?api-key='+os.getenv("NYT_API_KEY")
    response = requests.get(nyt_api)
    if response.status_code !=200:
        print('Bad response, please check NYT', response.status_code)
        raise Exception
    else:
        raw_headlines = response.json()
    auth = tweepy.OAuthHandler(os.getenv("TW_CONSUMER_KEY"), os.getenv("TW_CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("TW_ACCESS_TOKEN"), os.getenv("TW_ACCESS_TOKEN_SECRET"))
    tw_api = tweepy.API(auth)
    print('1)Initialization successful')
    return raw_headlines, tw_api


def data_parsing(raw_headlines):
    i=int(0)
    rand = random.randint(1, raw_headlines['num_results'])
    for result in raw_headlines['results']:
        headlines_nyt = result['abstract']
        i+=1
        if (len(headlines_nyt) < 250) & (i==rand):         #todo need logic to consider cornercase(rand headlines which >250)
            break
    print('2)Headlines extracted from NYT')
    return headlines_nyt


def tweet(tw_api, headlines):
    try:
        tw_api.update_status(headlines)
        print('3)Tweet Success')
        send_email()
    except:
        print('Tweet failed, email failed')


def send_email():
    email_id=os.getenv('EMAIL_ID')
    email_pw=os.getenv('EMAIL_PW')
    email_to=os.getenv('EMAIL_ID')
    subject='Success'
    body='Tweet posted at '+(datetime.today().strftime('%Y-%b-%d;  %H:%M')) +'\n...sent by app1-API'

    email_text = 'Subject: {}\n\n{}'.format(subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com','465')
        server.ehlo()
        server.login(email_id,email_pw)
        server.sendmail(email_id,email_to,email_text)
        server.close()
        print('4)Email sent, successfully\n\n Goodbye...')
    except:
        print('Something went wrong with SMTP server')


main()