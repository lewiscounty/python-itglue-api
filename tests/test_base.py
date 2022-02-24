import unittest

from itglue.base import Attribute, AttributeCollection

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
