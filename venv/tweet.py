import yaml
import yamlloader
import tweepy
import json

TWITTER_CONFIG_FILE = 'auth.yaml'

with open(TWITTER_CONFIG_FILE, 'r') as config_file:
    config = yaml.load(config_file, Loader=yamlloader.ordereddict.CLoader)

print(config['twitter']['consumer_key'])

def make_Tweet():
    consumer_key = config['twitter']['consumer_key']
    consumer_secret = config['twitter']['consumer_secret']

    # callback_uri = 'oob'
    #
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # redirect_url = auth.get_authorization_url()
    #
    # print(redirect_url)
    #
    # verifier = input('Verifier:')
    # auth.get_access_token(verifier)
    #
    # print(auth.access_token)
    # print(auth.access_token_secret)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(config['twitter']['access_token'], config['twitter']['access_token_secret'])

    tweet = 'On Friday 04/02/22 Their were a total of €14.1M worth of housing sold within Ireland.\n' \
            '#4 - 13 BALLINTEER DRIVE, BALLINTEER, DUBLIN 16 for €€655,000\n' \
            '#5 - 9 FERNCARRIG RISE, FERNLEIGH, SANDYFORD DUBLIN 18 for €625,000\n' \
            '#6 - 6 DANGAN PARK, CRUMLIN, DUBLIN 12 for €610,000'

    api = tweepy.API(auth)
    api.update_status(tweet)
make_Tweet()