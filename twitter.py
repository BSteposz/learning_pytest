import re, os


class Twitter:

    def __init__(self, backend=None):
        self.backend = backend
        self._tweets = []
        if self.backend and not os.path.exists(self.backend):
            with open(self.backend, 'w'):
                pass

    def delete(self):
        if self.backend:
            os.remove(self.backend)

    # property decorator is smt like getter from JS (but not exactly?)
    @property
    def tweets(self):
        if self.backend and not  self._tweets:
            with open(self.backend) as twitter_file:
                self._tweets = [line.rstrip('\n') for line in twitter_file]
        return self._tweets

    def tweet(self, message):
        if len(message) > 160:
            raise Exception("wiadomość za długa ")
        self.tweets.append(message)
        if self.backend:
            with open(self.backend, 'w') as twitter_file:
                twitter_file.write("\n".join(self.tweets))

    def find_hash(self, message):
        return [m.lower() for m in re.findall("#(\w+)", message)]
