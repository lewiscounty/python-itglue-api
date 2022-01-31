import requests

class Client:
    def __init__(self, api_key: str, base_url: str = "https://api.itglue.com", use_session: bool = False):
        self.api_key = api_key
        self.base_url = base_url

        if use_session:
            self.session = requests.Session()
