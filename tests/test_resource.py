import unittest

from itglue.base import Resource
from itglue.resource import Configuration


class TestResource(unittest.TestCase):
    """Test functionality common to all resources."""

    # Uses the Configuration subclass as a concrete instance
    # to test base Resource functionality.

    def setUp(self):
        self.init_kwargs = {
            'name': 'My Configuration',
            'hostname': 'desktop-123',
            'primary_ip': '192.168.0.1',
        }

    def test_subclassing_raises_exception_on_missing_resource_type(self):
        """Test that subclassing Resource without a resource_type attr raises an exception."""

        # No exception expected
        class Subclass(Resource):
            class Meta:
                resource_type = "my_resource"

        no_type_msg = "no exception raised for subclasses without Meta.resource_type defined"

        with self.assertRaises(AttributeError, msg=no_type_msg):
            class Subclass(Resource): pass

        with self.assertRaises(AttributeError, msg=no_type_msg):
            class Subclass(Resource):
                class Meta: pass

    def test_constructor_noargs(self):
        """Test initialization with no arguments."""

        c = Configuration()
        self.assertIsNone(c.id, "id is not None when no args passed to constructor")

    def test_constructor_accepts_id(self):
        """Test initialization with an ID."""

        c = Configuration('555')
        self.assertEqual(c.id, '555', "id attribute not initialized (positional arg)")

    def test_constructor_accepts_kwargs(self):
        """Test initialization with keyword args."""

        c = Configuration(**self.init_kwargs)

        for (key, val) in self.init_kwargs.items():
            with self.subTest(attr=key):
                self.assertEqual(getattr(c, key), val, f"{key} attribute not initialized")

    def test_constructor_accepts_id_and_kwargs(self):
        """Test initialization with an ID and keyword args."""

        c = Configuration('64', **self.init_kwargs)
        self.assertEqual(c.id, '64', "id attribute not initialized")

        for (key, val) in self.init_kwargs.items():
            with self.subTest(attr=key):
                self.assertEqual(getattr(c, key), val, f"{key} attribute not initialized")

    def test_constructor_only_defines_kwargs_as_attrs(self):
        """
        Test that the constructor only defines attributes on the instance that correspond to the passed kwargs.
        Even valid attribute names should be undefined unless they were passed in the constructor.
        """

        c = Configuration(**self.init_kwargs)
        self.assertFalse(hasattr(c, 'installed_at'), "installed_at was not included in the constructor kwargs but it is defined on the instance")

        c = Configuration(installed_at='2010-05-20', **self.init_kwargs)
        self.assertEqual(c.installed_at, '2010-05-20', "installed_at attribute not initialized")

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

        c = Resource.from_network_dict(d)

        self.assertIsInstance(c, Configuration, "Resource constructed from network dict is not an instance of the appropriate subclass")
        self.assertEqual(c.id, d['id'], "id attribute not initialized from network dict")
        self.assertEqual(c.name, d['attributes']['name'], "name attribute not initialized from network dict")
        self.assertEqual(c.primary_ip, d['attributes']['primary-ip'], "primary_ip attribute not initialized from network dict")
        self.assertFalse(hasattr(c, 'unknown_attr'), "unknown attribute is defined on resource")
        self.assertEqual(c.Meta.network_dict, d, "Resource.Meta.network_dict is not initialized")

    def test_subclass_lookup(self):
        """Test finding a subclass by its Meta.resource_type value."""

        class Subclass(Resource):
            class Meta:
                resource_type = 'my_subclass'

        self.assertIs(Resource.lookup_subclass('my_subclass'), Subclass, "Resource.lookup_subclass() didn't return the correct class")
        self.assertIs(Resource.lookup_subclass('configurations'), Configuration, "Resource.lookup_subclass() didn't return the correct class")
