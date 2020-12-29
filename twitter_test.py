from unittest.mock import patch, Mock, MagicMock
import requests

import pytest

from twitter import Twitter


class ResponseGetMock:

    def json(self):
        return {'avatar_url': 'test'}


@pytest.fixture(autouse=True)
def no_request(monkeypatch):
    monkeypatch.delattr('requests.sessions.Session.request')


@pytest.fixture
def backend(tmpdir):
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file


@pytest.fixture(params=[None, 'python'])
def username(request):
    return request.param


@pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, username, request, monkeypatch):
    if request.param == 'list':
        twitter = Twitter(username=username)
    elif request.param == 'backend':
        twitter = Twitter(backend=backend, username=username)

    return twitter

"""
    def monkey_return():
        return 'test'

    monkeypatch.setattr(twitter, 'get', monkey_return)
    return twitter
    
    """


def test_init(twitter):
    """ Initialization test """
    assert twitter


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_single_message(avatar_mock, twitter):
    """ Single message test """

    twitter.tweet('Test message')
    assert twitter.tweet_messages == ['Test message']


def test_tweet_long_message(twitter):
    """Test assert of too long message"""
    # this line check that exception is rised
    with pytest.raises(Exception):
        twitter.tweet('a' * 161)
    assert twitter.tweet_messages == []


def test_init_two_twitter_classes(backend):
    twiter1 = Twitter(backend=backend)
    twiter2 = Twitter(backend=backend)

    twiter1.tweet('test1')
    twiter1.tweet('test2')

    assert twiter2.tweet_messages == ['test1', 'test2']


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


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_username(avatar_mock, twitter):
    if not twitter.username:
        pytest.skip()
    twitter.tweet('Test')
    assert twitter.tweets == [{'message': 'Test', 'avatar': 'test', 'hash': []}]
    avatar_mock.assert_called()

@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_hashtag_mock(avatar_mock, twitter):
    twitter.find_hash = Mock()
    twitter.find_hash.return_value = ['first']
    twitter.tweet('Test #second')
    assert twitter.tweets[0]['hash'] == ['first']

def test_twitter_version(twitter):
    twitter._version = MagicMock()
    twitter._version.__eq__.return_value = '2.0'
    assert twitter._version == '2.0'

