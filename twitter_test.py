import pytest

from twitter import Twitter


@pytest.fixture
def backend(tmpdir):
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file


@pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, request):
    if request.param == 'list':
        twitter = Twitter()
    elif request.param == 'backend':
        twitter = Twitter(backend=backend)
    return twitter



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


def test_init_two_twitter_classes(backend):
    twiter1 = Twitter(backend=backend)
    twiter2 = Twitter(backend=backend)

    twiter1.tweet('test1')
    twiter1.tweet('test2')

    assert twiter2.tweets == ['test1', 'test2']


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
