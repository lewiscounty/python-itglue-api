import unittest

from itglue.resources import *

class TestResource(unittest.TestCase):
    """Test functionality common to all resources."""

    def setUp(self):
        self.init_kwargs = {
            'name': 'My Configuration',
            'hostname': 'desktop-123',
            'primary_ip': '192.168.0.1',
        }

    def test_constructor_noargs(self):
        """Test initialization with no arguments."""

        c = Configuration()
        self.assertEqual(c.id, None, "id is not None when no args passed to constructor")

    def test_constructor_accepts_id(self):
        """Test initialization with an ID."""

        c = Configuration('555')
        self.assertEqual(c.id, '555', "id not initialized (positional arg)")

    def test_constructor_accepts_kwargs(self):
        """Test initialization with keyword args."""

        c = Configuration(**self.init_kwargs)
        self.assertFalse(hasattr(c, '_network_dict'), "_network_dict is defined when resource is initialized without a network dict")

        for (key, val) in self.init_kwargs.items():
            with self.subTest(attr=key):
                self.assertEqual(getattr(c, key), val, "attribute not initialized")

    def test_constructor_accepts_id_and_kwargs(self):
        """Test initialization with an ID and keyword args."""

        c = Configuration('64', **self.init_kwargs)
        self.assertEqual(c.id, '64', "id not initialized")
        self.assertFalse(hasattr(c, '_network_dict'), "_network_dict is defined when resource is initialized without a network dict")

        for (key, val) in self.init_kwargs.items():
            with self.subTest(attr=key):
                self.assertEqual(getattr(c, key), val, "attribute not initialized")

    def test_constructor_raises_exception_on_invalid_kwargs(self):
        """Test that invalid constructor args raise an exception."""

        with self.assertRaises(TypeError, msg="no exception raised on invalid constructor args"):
            Configuration('987', name="My config", invalid_arg="spam")
    
    def test_create_resource_from_network_dict(self):
        """Test creating a resource from a raw network dict."""

        d = {
            'id': '999',
            'type': 'configurations',
            'attributes': {
                'name': 'my config',
                'primary-ip': '10.0.0.2',
                'unknown-attr': 'eggs',
            },
        }

        c = Configuration.from_network_dict(d)

        self.assertEqual(c.id, d['id'], "id attribute not initialized from network dict")
        self.assertEqual(c.name, d['attributes']['name'], "name attribute not initialized from network dict")
        self.assertEqual(c.primary_ip, d['attributes']['primary-ip'], "primary_ip attribute not initialized from network dict")
        self.assertFalse(hasattr(c, 'unknown_attr'), "unknown attribute is defined on resource")
        self.assertEqual(c._network_dict, d, "_network_dict is not initialized")
