import unittest

from itglue.resource import Configuration

class TestManager(unittest.TestCase):
    """Test the Manager class and its ManagerMeta metaclass."""

    def setUp(self):
        # Create a fake resource for testing
        class Candy(Resource):
            class Meta:
                resource_type = 'test_config'

            name = Attribute()
            ingredients = Attribute()
            gluten_free = Attribute()

        self.Candy = Candy
