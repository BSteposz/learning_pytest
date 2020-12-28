import re, os


class Twitter:

    def __init__(self, backend=None):
        self.backend = backend
        self._tweets = []

    # property decorator is smt like getter from JS (but not exactly?)
    @property
    def tweets(self):
        if self.backend and not self._tweets:
            self._tweets = [line.rstrip('\n') for line in self.backend.readlines()]
        return self._tweets

    def tweet(self, message):
        if len(message) > 160:
            raise Exception("wiadomość za długa ")
        self.tweets.append(message)
        if self.backend:
            self.backend.write("\n".join(self.tweets))

    def find_hash(self, message):
        return [m.lower() for m in re.findall("#(\w+)", message)]
