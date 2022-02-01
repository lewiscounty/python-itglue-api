class Resource:
    def __init__(self, id_=None, **kwargs):
        self.id = id_

        for (key, val) in kwargs.items():
            if key in self.attribute_map:
                setattr(self, key, val)
            else:
                raise TypeError("{} is not a valid keyword argument")

    @classmethod
    def from_network_dict(cls, network_dict):
        inverted_map = {v: k for (k, v) in cls.attribute_map.items()}
        kwargs = {'id_': network_dict['id']}

        for (key, val) in network_dict['attributes'].items():
            if key in inverted_map:
                kwargs[inverted_map[key]] = val

        resource = cls(**kwargs)
        resource._network_dict = network_dict
        return resource

class Configuration(Resource):
    attribute_map = {
        'archived': 'archived',
        'asset_tag': 'asset-tag',
        'configuration_status_id': 'configuration-status-id',
        'configuration_status_name': 'configuration-status-name',
        'configuration_type_id': 'configuration-type-id',
        'configuration_type_kind': 'configuration-type-kind',
        'configuration_type_name': 'configuration-type-name',
        'contact_id': 'contact-id',
        'contact_name': 'contact-name',
        'created_at': 'created-at',
        'default_gateway': 'default-gateway',
        'hostname': 'hostname',
        'installed_at': 'installed-at',
        'installed_by': 'installed-by',
        'location_id': 'location-id',
        'location_name': 'location-name',
        'mac_address': 'mac-address',
        'manufacturer_id': 'manufacturer-id',
        'manufacturer_name': 'manufacturer-name',
        'model_id': 'model-id',
        'model_name': 'model-name',
        'my_glue': 'my-glue',
        'name': 'name',
        'notes': 'notes',
        'operating_system_id': 'operating-system-id',
        'operating_system_name': 'operating-system-name',
        'operating_system_notes': 'operating-system-notes',
        'organization_id': 'organization-id',
        'organization_name': 'organization-name',
        'organization_short_name': 'organization-short-name',
        'position': 'position',
        'primary_ip': 'primary-ip',
        'purchased_at': 'purchased-at',
        'purchased_by': 'purchased-by',
        'psa_integration': 'psa-integration',
        'resource_url': 'resource-url',
        'restricted': 'restricted',
        'serial_number': 'serial-number',
        'updated_at': 'updated-at',
        'warranty_expires_at': 'warranty-expires-at',
    }
