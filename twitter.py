import re, os, json
from urllib.parse import urljoin

from pip._vendor import requests

USER_API = "https://api.github.com/users"

class Twitter:

    def __init__(self, backend=None, username=None):
        self.backend = backend
        self._tweets = []
        self.username = username

    # property decorator is smt like getter from JS (but not exactly?)
    @property
    def tweets(self):
        if self.backend and not self._tweets:
            backend_text = self.backend.read()
            if backend_text:
                self._tweets = json.loads(backend_text)
        return self._tweets

    @property
    def tweet_messages(self):
        return [tweet['message'] for tweet in self.tweets]

    def get_user_avatar(self):
        if not self.username:
            return None
        url = urljoin(USER_API, self.username)
        resp = requests.get(url)
        return resp.json()['avatar_url']

    def tweet(self, message):
        if len(message) > 160:
            raise Exception("wiadomość za długa ")
        self.tweets.append({'message': message, 'avatar': self.get_user_avatar()})
        if self.backend:
            self.backend.write(json.dumps(self.tweets))

    def find_hash(self, message):
        return [m.lower() for m in re.findall("#(\w+)", message)]
