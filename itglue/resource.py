from collections.abc import Collection
from types import SimpleNamespace


class Attribute:
    """Represents a single IT Glue resource attribute."""

    def __init__(self, network_key=None):
        """
        Initialize an Attribute instance with optional custom network_key.

        When Attribute instances are assigned to attributes of Resource
        subclasses, Attribute.set_name() will be called automatically with
        the name of the attribute that the instance was assigned to.

        If network_key is omitted, set_name() will also initialize network_key
        to be the same as the name except with underscores replaced with hyphens.
        """

        self.name = None
        self.network_key = network_key

    def set_name(self, name):
        """
        Set the Attribute instance name.

        If self.network_key is None, set_name() also sets a default network_key
        by replacing underscores in the new name with hyphens and assigning
        the result to self.network_key.
        """

        self.name = name
        if self.network_key is None:
            self.network_key = name.replace('_', '-')


class AttributeCollection(Collection):
    """Store a collection of Attribute instances."""

    def __init__(self):
        self.__attributes = {}

    def add(self, attr):
        if attr.name is None:
            raise ValueError("Cannot add attribute with a name of None: call Attribute.set_name() first")
        if self.get_by_name(attr.name):
            raise ValueError(f"Another attribute with the name \"{attr.name}\" already exists")
        if self.get_by_network_key(attr.network_key):
            raise ValueError(f"Another attribute with the network key \"{attr.network_key}\" already exists")

        self.__attributes[attr.name] = attr

    def get_by_name(self, name):
        if name in self.__attributes:
            return self.__attributes[name]
        return None

    def get_by_network_key(self, network_key):
        for val in self.__attributes.values():
            if val.network_key == network_key:
                return val

        return None

    def __contains__(self, item):
        if isinstance(item, Attribute):
            return item in self.__attributes.values()
        return item in self.__attributes

    def __iter__(self):
        return iter(self.__attributes.values())

    def __len__(self):
        return len(self.__attributes)


class ResourceMeta(type):
    """Metaclass for all Resource subclasses."""

    resource_classes = {}

    def __new__(metaclass, classname, bases, namespace_dict, **kwargs):
        # Only use custom initialization for subclasses of Resource
        # (exclude Resource itself)
        parents = [b for b in bases if isinstance(b, ResourceMeta)]
        if not parents:
            # Run default type() constructor
            return super().__new__(metaclass, classname, bases, namespace_dict, **kwargs)

        attrs = {'Meta': namespace_dict.pop('Meta', SimpleNamespace())}
        attrs['Meta'].attributes = AttributeCollection()

        for (key, val) in namespace_dict.items():
            if isinstance(val, Attribute):
                val.set_name(key)
                attrs['Meta'].attributes.add(val)
            else:
                attrs[key] = val

        # Call type() to create the class and then register it
        # in the resource_classes list
        cls = super().__new__(metaclass, classname, bases, attrs, **kwargs)
        metaclass.resource_classes[attrs['Meta'].resource_type] = cls
        return cls

    def lookup_subclass(cls, resource_type):
        """Get the Resource subclass associated with the specified resource_type."""

        return cls.resource_classes[resource_type]


class Resource(metaclass=ResourceMeta):
    """Base class representing an IT Glue resource."""

    def __init__(self, id_=None, **kwargs):
        """
        Initialize an instance representing an IT Glue resource.

        The id_ positional arg is optional and defaults to None
        (useful for resources that don't yet have an ID). All other
        args are keyword-only and specify resource attributes to set.
        Each Resource subclass defines its own list of valid attributes.
        """

        self.id = id_

        for (key, val) in kwargs.items():
            if key in self.Meta.attributes:
                setattr(self, key, val)
            else:
                raise TypeError(f"\"{key}\" is not a valid keyword argument")

    @staticmethod
    def from_network_dict(network_dict):
        """
        Create a Resource instance from a network dict parsed from a raw
        IT Glue API JSON response.

        The network_dict must have a 'type' key that matches a Resource subclass's
        declared resource_type. This value is used to ensure that the resulting Resource
        instance is an instance of the correct Resource subclass.
        """

        cls = Resource.resource_classes[network_dict['type']]
        kwargs = {'id_': network_dict['id']}

        for (key, val) in network_dict['attributes'].items():
            attr = cls.Meta.attributes.get_by_network_key(key)
            if attr:
                kwargs[attr.name] = val

        resource = cls(**kwargs)
        resource.Meta.network_dict = network_dict
        return resource


class Configuration(Resource):
    """
    Represents an IT Glue Configuration.
    """

    class Meta:
        resource_type = 'configurations'

    archived = Attribute()
    asset_tag = Attribute()
    configuration_status_id = Attribute()
    configuration_status_name = Attribute()
    configuration_type_id = Attribute()
    configuration_type_kind = Attribute()
    configuration_type_name = Attribute()
    contact_id = Attribute()
    contact_name = Attribute()
    created_at = Attribute()
    default_gateway = Attribute()
    hostname = Attribute()
    installed_at = Attribute()
    installed_by = Attribute()
    location_id = Attribute()
    location_name = Attribute()
    mac_address = Attribute()
    manufacturer_id = Attribute()
    manufacturer_name = Attribute()
    model_id = Attribute()
    model_name = Attribute()
    my_glue = Attribute()
    name = Attribute()
    notes = Attribute()
    operating_system_id = Attribute()
    operating_system_name = Attribute()
    operating_system_notes = Attribute()
    organization_id = Attribute()
    organization_name = Attribute()
    organization_short_name = Attribute()
    position = Attribute()
    primary_ip = Attribute()
    purchased_at = Attribute()
    purchased_by = Attribute()
    psa_integration = Attribute()
    resource_url = Attribute()
    restricted = Attribute()
    serial_number = Attribute()
    updated_at = Attribute()
    warranty_expires_at = Attribute()
