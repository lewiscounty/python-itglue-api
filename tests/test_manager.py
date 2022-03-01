import unittest

from itglue.manager import *
from unittest.mock import Mock, patch, sentinel


FAKE_ID = '555'


@patch('itglue.manager.urljoin')
class TestConfigurationManager(unittest.TestCase):
    """Test the ConfigurationManager class."""

    @patch('itglue.manager.Resource.from_network_dict')
    def test_get(self, from_network_dict_mock, urljoin_mock):
        """Test getting a single Configuration."""

        session_mock = Mock()
        session_mock.get.return_value.status_code = 200
        session_mock.get.return_value.json.return_value = sentinel.json
        configurations = ConfigurationManager(session_mock, sentinel.base_url)
        from_network_dict_mock.return_value = sentinel.configuration_obj
        urljoin_mock.return_value = sentinel.url

        res = configurations.get(FAKE_ID)

        urljoin_mock.assert_called_once_with(sentinel.base_url, f'/configurations/{FAKE_ID}')
        session_mock.get.assert_called_once_with(sentinel.url)
        from_network_dict_mock.assert_called_once_with(sentinel.json)
        self.assertEqual(res, sentinel.configuration_obj, "ConfigurationManager.get() didn't return the expected Configuration instance")
