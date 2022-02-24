import requests

DEFAULT_BASE_URL = 'https://api.itglue.com'

class Client:
    def __init__(self, api_key, base_url=DEFAULT_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
