"""This module handles the streaming of data from Twitter."""


import logging
import tweepy

from collections import namedtuple

from streamlistener import KeywordStreamListener

CONFIG = 'keys.txt'


def start_stream(keyword, queue):
    """Runs the tweepy stream to pull tweets containing the given keyword from Twitter."""

    stream = _get_stream(queue)

    logging.debug('Starting stream')

    while True:
        try:
            stream.filter(track=[keyword], stall_warnings=True)
        except Exception as e:
            logging.error(e)


def _get_stream(queue):
    """Returns a configured tweepy.Stream object."""

    api = _get_tweepy_api()

    stream_listener = KeywordStreamListener(queue)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

    return stream


def _get_tweepy_api():
    """Returns a tweepy.API object with the necessary OAuth configs."""

    keys = _get_keys_and_tokens()

    auth = tweepy.OAuthHandler(keys.consumer, keys.consumer_secret)
    auth.set_access_token(keys.access, keys.access_secret)

    return tweepy.API(auth)


def _get_keys_and_tokens():
    """Returns a namedtuple of Twitter keys and access tokens read from the config file."""

    KeysTuple = namedtuple('Keys', ['consumer', 'consumer_secret',
                                    'access', 'access_secret'])

    with open(CONFIG) as file:
        logging.debug('Reading Twitter keys from file')
        keys_list = [line.strip() for line in file]

    return KeysTuple(*keys_list)
