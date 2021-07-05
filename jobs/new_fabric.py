from django.utils.text import slugify

from nautobot.dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site, Region
from nautobot.extras.models import Status
from nautobot.extras.jobs import *


class NewDC(Job):

    class Meta:
        name = "New DataCenter"
        description = "Build new vxlan deployment"
        field_order = ['region', 'site_name', 'relay_rack', 'underlay_p2p_network_summary', 'overlay_loopback_network_summary', 'vtep_loopback_network_summary', 'mlag_leaf_peer_l3', 'mlag_peer', '_peer_groups', 'spine_switch_count', 'spine_bgp_as', 'leaf_bgp_as_range', 'leaf_switch_count', 'tor_switch_count']

    region = ObjectVar(
        description="Choose Region",
        model=Region,
        required=False
    )

    site_name = StringVar(
        description = "Name for the new fabric"
    )

    relay_rack = IntegerVar(
        description = "Choice how many Relay Racks"
    )

    underlay_p2p_network_summary = StringVar(
        description = "Underlay P2P network - Assign range larger then total [spines * total potential leafs * 2"
    )

    overlay_loopback_network_summary = StringVar(
        description = "Overlay Loopback network - Assign range larger then total spines + total leafs switches"
    )

    vtep_loopback_network_summary = StringVar(
        description = "Vtep Loopback network - Assign range larger then total leaf switches"
    )

    mlag_leaf_peer_l3 = StringVar(
        description = "Leaf L3 MLAG network - Assign range larger then total spines + total leafs switches"
    )

    mlag_peer = StringVar(
        description = "MLAG Peer network - Assign range larger then total spines + total leafs switches"
    )

    # _peer_groups = Stringvar(
    #     description = "List the names of th BGP Peer Groups - Comma seperated"
    # )

    spine_switch_count = IntegerVar(
        description = "Number of Spines to be deployed"
    )

    spine_bgp_as = IntegerVar(
        description = "Spine BGP ASN"
    )
    
    leaf_bgp_as_range = IntegerVar(
        description = "Define the range of acceptable remote ASNs from leaf switches"
    )

    leaf_switch_count = IntegerVar(
        description = "Number of Leafs to be deployed"
    )

    tor_switch_count = IntegerVar(
        description = "Number of ToR switches to be deployed"
    )
    manufacturer = ObjectVar(
        model=Manufacturer,
        required=False
    )

    spine_model = ObjectVar(
        description="Spine model",
        model=DeviceType,
        query_params={
            'manufacturer_id': '$manufacturer'
        }
    )

    leaf_model = ObjectVar(
        description="Leaf model",
        model=DeviceType,
        query_params={
            'manufacturer_id': '$manufacturer'
        }
    )

    tor_model = ObjectVar(
        description="ToR model",
        model=DeviceType,
        query_params={
            'manufacturer_id': '$manufacturer'
        }
    )

    def run(self, data, commit):
        STATUS_PLANNED = Status.objects.get(slug='planned')

        #  Create the New site
        site = Site(
            name=data['site_name'],
            slug=slugify(data['site_name']),
            asn=data['spine_bgp_as'],
            status=STATUS_PLANNED,
        )
        site.validated_save()
        self.log_success(obj=site, message="Created new site")

        # Create Spine
        spine_role = DeviceRole.objects.get(name='fabric_spine')
        for i in range(1, data['spine_switch_count'] + 1):
            device = Device(
                device_type=data['spine_model'],
                name=f'{site.slug}spine{i}',
                site=site,
                status=STATUS_PLANNED,
                device_role=spine_role
            )
            device.validated_save()
            self.log_success(obj=device, message="Created Spine Switches")

        # Create Leaf
        leaf_role = DeviceRole.objects.get(name='fabric_l3_leaf')
        for i in range(1, data['leaf_switch_count'] + 1):
            device = Device(
                device_type=data['leaf_model'],
                name=f'{site.slug}leaf{i}',
                site=site,
                status=STATUS_PLANNED,
                device_role=leaf_role
            )
            device.validated_save()
            self.log_success(obj=device, message="Created Leaf Switches")

        # Create ToR
        tor_role = DeviceRole.objects.get(name='fabric_l2_leaf')
        for i in range(1, data['tor_switch_count'] + 1):
            device = Device(
                device_type=data['tor_model'],
                name=f'{site.slug}tor{i}',
                site=site,
                status=STATUS_PLANNED,
                device_role=tor_role
            )
            device.validated_save()
            self.log_success(obj=device, message="Created ToR Switches")

        # Generate a CSV table of new devices
        output = [
            'name,make,model'
        ]
        for device in Device.objects.filter(site=site):
            attrs = [
                device.name,
                device.device_type.manufacturer.name,
                device.device_type.model
            ]
            output.append(','.join(attrs))

        return '\n'.join(output)