import requests


DEFAULT_BASE_URL = 'https://api.itglue.com'


class ITGlueAuth(requests.auth.AuthBase):
    """Attach authentication info to the given Request."""

    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, req):
        req.headers['x-api-key'] = self.api_key
        return req


class Client:
    def __init__(self, api_key, base_url=DEFAULT_BASE_URL):
        session = requests.Session()
        session.auth = ITGlueAuth(api_key)
        session.headers.update({'Content-Type': 'application/vnd.api+json'})
        self.session = session
        self.base_url = base_url
