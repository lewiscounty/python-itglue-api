from urllib.parse import urljoin
from .resource import Resource


class Manager:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

class ShowableMixin:
    def get(self, id_):
        url = urljoin(self.base_url, f'/configurations/{id_}')
        res = self.session.get(url)
        return Resource.from_network_dict(res.json())

class ConfigurationManager(Manager, ShowableMixin):
    """Contains methods for reading and writing Configuration resources."""

    pass
