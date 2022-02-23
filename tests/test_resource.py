import unittest

from itglue.resource import *

class TestAttribute(unittest.TestCase):
    """Test the Attribute class."""

    def test_default_constructor(self):
        """Test constructor with no args."""

        a = Attribute()

        self.assertIsNone(a.name, "name attr not initialized to None")
        self.assertIsNone(a.network_key, "network_key attr not initialized to None")

    def test_custom_network_key(self):
        """Test constructor with custom network_key."""

        a = Attribute(network_key='spam')

        self.assertEqual(a.network_key, 'spam', "network_key incorrect")
        self.assertIsNone(a.name, "name attr not initialized to None")

    def test_set_name(self):
        """Test setting name after initialization."""

        a = Attribute()
        a.set_name('attr_name')

        self.assertEqual(a.name, 'attr_name', "name incorrect")
        self.assertEqual(a.network_key, 'attr-name', "network_key incorrect")

    def test_set_name_with_custom_network_key(self):
        """Test setting name after initialization with custom network_key."""

        a = Attribute(network_key="custom network key")
        a.set_name('new_name')

        self.assertEqual(a.name, 'new_name', "name incorrect")
        self.assertEqual(a.network_key, 'custom network key', "network_key incorrect")


class TestAttributeCollection(unittest.TestCase):
    """Test the AttributeCollection class."""

    def setUp(self):
        self.a = Attribute()
        self.a.set_name('my_attribute')
        self.b = Attribute(network_key='custom network key')
        self.b.set_name('b_attr')

    def test_attr_collection_basic_functionality(self):
        """Test adding and retrieving Attribute objects."""

        c = AttributeCollection()
        c.add(self.a)
        c.add(self.b)

        self.assertIs(c.get_by_name('my_attribute'), self.a, "failed to retrieve stored Attribute by name")
        self.assertIs(c.get_by_name('b_attr'), self.b, "failed to retrieve stored Attribute by name")
        self.assertIs(c.get_by_network_key('my-attribute'), self.a, "failed to retrieve stored Attribute by network key")
        self.assertIs(c.get_by_network_key('custom network key'), self.b, "failed to retrieve stored Attribute by network key")

    def test_raises_exception_when_adding_invalid_Attribute(self):
        """Test that an exception is raised when adding an Attribute with an invalid name."""

        c = AttributeCollection()
        a = Attribute() # No name specified

        with self.assertRaises(ValueError, msg="no exception raised when adding Attribute with no name attr defined"):
            c.add(a)

    def test_raises_exception_when_adding_duplicate_name(self):
        """Test that an exception is raised for duplicate name."""

        c = AttributeCollection()
        a1 = Attribute()
        a1.set_name('a')
        a2 = Attribute()
        a2.set_name('a')
        c.add(a1)

        with self.assertRaises(ValueError, msg="no exception raised when adding Attribute with duplicate name"):
            c.add(a2)

    def test_raises_exception_when_adding_duplicate_network_key(self):
        """Test that an exception is raised for duplicate network_key."""

        c = AttributeCollection()
        a = Attribute(network_key='dupl')
        a.set_name('a')
        b = Attribute(network_key='dupl')
        b.set_name('b')
        c.add(a)

        with self.assertRaises(ValueError, msg="no exception raised when adding Attribute with duplicate network_key"):
            c.add(b)

    def test_iteration(self):
        """Test that the collection is iterable."""

        c = AttributeCollection()
        c.add(self.a)
        c.add(self.b)
        iterator1 = iter(c)
        iterator2 = iter(c)

        self.assertEqual(len(c), 2, "AttributeCollection length incorrect")
        self.assertIs(next(iterator1), self.a, "AttributeCollection iterator not working as expected")
        self.assertIs(next(iterator1), self.b, "AttributeCollection iterator not working as expected")
        self.assertIs(next(iterator2), self.a, "AttributeCollection iterator not working as expected")
        self.assertIs(next(iterator2), self.b, "AttributeCollection iterator not working as expected")

        with self.assertRaises(StopIteration):
            next(iterator1)

        with self.assertRaises(StopIteration):
            next(iterator2)

    def test_in_operator(self):
        """Test that the in operator can be used to test if a name is in the AttributeCollection."""

        c = AttributeCollection()
        c.add(self.a)
        c.add(self.b)

        self.assertIn(self.a, c, "membership test with Attribute() instance returned false negative")
        self.assertIn('my_attribute', c, "membership test with str name returned false negative")
        self.assertIn(self.b, c, "membership test with Attribute() instance returned false negative")
        self.assertIn('b_attr', c, "membership test with str name returned false negative")
        self.assertNotIn(Attribute(), c, "membership test with Attribute() instance returned false positive")
        self.assertNotIn('definitely missing', c, "membership test with str name returned false positive")


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
