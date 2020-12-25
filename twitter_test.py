import pytest

from twitter import Twitter


def test_init():
    """ Initialization test """
    twitter = Twitter()
    assert  twitter


def test_single_message():
    """ Single message test """
    twitter = Twitter()
    twitter.tweet('Test message')
    assert twitter.tweets == ['Test message']


def test_tweet_long_message():
    """Test assert of too long message"""
    twitter = Twitter()
    # this line check that exception is rised
    with pytest.raises(Exception):
        twitter.tweet('a' * 160)
    assert twitter.tweets == []


def test_find_hash():
    twitter = Twitter()
    message = "Test #hash test"
    twitter.tweet(message)
    assert 'hash' in twitter.find_hash(message)

    