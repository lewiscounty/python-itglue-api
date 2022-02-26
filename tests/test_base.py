import unittest

from itglue.base import (
    Attribute,
    AttributeCollection,
)
from itglue.resource import Configuration


class TestAttribute(unittest.TestCase):
    """Test the Attribute class."""

    def test_default_constructor(self):
        """Test constructor with no args."""

        a = Attribute()

        self.assertIsNone(a.name, "Attribute.name not initialized to None")
        self.assertIsNone(a.network_key, "Attribute.network_key attr not initialized to None")

    def test_custom_name(self):
        """Test constructor with a name arg."""

        a = Attribute(name='custom_name')

        self.assertEqual(a.name, 'custom_name', "Attribute.name incorrect")
        self.assertEqual(a.network_key, 'custom-name', "Attribute.network_key incorrect")

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

    def test_get_by_name(self):
        """Test retrieving Attribute objects by name."""

        c = AttributeCollection()
        a = Attribute(name='my_attribute')
        c.add(a)

        self.assertIs(c.get_by_name('my_attribute'), a, "failed to retrieve stored Attribute by name")

    def test_get_by_network_key(self):
        """Test retrieving Attribute objects by network_key."""

        c = AttributeCollection()
        a = Attribute(name='my_attr', network_key='my-attribute')
        c.add(a)

        self.assertIs(c.get_by_network_key('my-attribute'), a, "failed to retrieve stored Attribute by network_key")

    def test_raises_exception_when_adding_Attribute_with_no_name(self):
        """Test that an exception is raised when adding an Attribute with a name equal to None."""

        c = AttributeCollection()
        a = Attribute() # No name specified; defaults to None

        with self.assertRaises(ValueError, msg="no exception raised when adding Attribute with Attribute.name == None"):
            c.add(a)

    def test_raises_exception_when_adding_duplicate_name(self):
        """Test that an exception is raised for duplicate name."""

        c = AttributeCollection()
        a1 = Attribute(name='a')
        a2 = Attribute(name='a')
        c.add(a1)

        with self.assertRaises(ValueError, msg="no exception raised when adding Attribute with duplicate name"):
            c.add(a2)

    def test_raises_exception_when_adding_duplicate_network_key(self):
        """Test that an exception is raised for duplicate network_key."""

        c = AttributeCollection()
        a = Attribute(name='a', network_key='dupl')
        b = Attribute(name='b', network_key='dupl')
        c.add(a)

        with self.assertRaises(ValueError, msg="no exception raised when adding Attribute with duplicate network_key"):
            c.add(b)

    def test_len(self):
        """Test that the collection correctly reports its length."""

        c = AttributeCollection()
        c.add(Attribute(name='first'))
        c.add(Attribute(name='second'))
        c.add(Attribute(name='third'))

        self.assertEqual(len(c), 3, "len() of AttributeCollection() incorrect")

    def test_iteration(self):
        """Test that the collection is iterable and supports multiple iterators."""

        ITER_ERR_MSG = "AttributeCollection iterator not working as expected"
        END_ERR_MSG = "AttributeCollection iterator didn't raise StopIteration at end of collection"

        c = AttributeCollection()
        a, b = Attribute(name='a'), Attribute(name='b')
        c.add(a)
        c.add(b)
        iterator1 = iter(c)
        iterator2 = iter(c)

        self.assertIs(next(iterator1), a, ITER_ERR_MSG)
        self.assertIs(next(iterator1), b, ITER_ERR_MSG)
        self.assertIs(next(iterator2), a, ITER_ERR_MSG)
        self.assertIs(next(iterator2), b, ITER_ERR_MSG)

        with self.assertRaises(StopIteration, msg=END_ERR_MSG):
            next(iterator1)

        with self.assertRaises(StopIteration, msg=END_ERR_MSG):
            next(iterator2)

    def test_in_operator(self):
        """Test that the in operator can be used to test if a name is in the AttributeCollection."""

        c = AttributeCollection()
        a, b = Attribute(name='a'), Attribute(name='b')
        outsider = Attribute(name='outsider')
        c.add(a)
        c.add(b)

        self.assertIn(a, c, "membership test with Attribute() instance returned false negative")
        self.assertIn(b, c, "membership test with Attribute() instance returned false negative")
        self.assertIn('a', c, "membership test with str name returned false negative")
        self.assertIn('b', c, "membership test with str name returned false negative")
        self.assertNotIn(outsider, c, "membership test with Attribute() instance returned false positive")
        self.assertNotIn('outsider', c, "membership test with str name returned false positive")
