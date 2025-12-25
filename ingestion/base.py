import time
import requests

class BaseIngestor:
    def __init__(self, rate_limit=1):
        self.rate_limit = rate_limit

    def fetch(self):
        raise NotImplementedError

    def backoff(self, attempt):
        time.sleep(2 ** attempt)
