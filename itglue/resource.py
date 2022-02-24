from itglue.base import Attribute, Resource

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
