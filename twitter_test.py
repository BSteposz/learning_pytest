import pytest

from twitter import Twitter


@pytest.fixture(params=[None, 'test.txt'], name='twitter')
def fixture_twitter(request):
    twitter = Twitter(backend=request.param)
    yield twitter
    twitter.delete()

def test_init(twitter):
    """ Initialization test """
    assert twitter


def test_single_message(twitter):
    """ Single message test """
    twitter.tweet('Test message')
    assert twitter.tweets == ['Test message']


def test_tweet_long_message(twitter):
    """Test assert of too long message"""
    # this line check that exception is rised
    with pytest.raises(Exception):
        twitter.tweet('a' * 161)
    assert twitter.tweets == []


@pytest.mark.parametrize("message, expected", (
        ('Test #first message', ['first']),
        ('#first Test  message', ['first']),
        ('Test #FIRST message', ['first']),
        ('Test  message #FIRST', ['first']),
        ('Test  message #FIRST #second', ['first', "second"])

))
def test_find_hash(twitter, message, expected):
    """ Test find hashtag function """
    assert twitter.find_hash(message) == expected
