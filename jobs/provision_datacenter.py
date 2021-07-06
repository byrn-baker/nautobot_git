from django.utils.text import slugify

from nautobot.dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site, Region, Rack, Interface
from nautobot.ipam.models import VRF, RouteTarget, Prefix, IPAddress
from nautobot.extras.models import Status
from nautobot.extras.jobs import *

class DataCenter(Job):
    class Meta:
        name = "Build New DataCenter"
        description = "Build a new DataCenter with VXLAN"
        field_order = ['region', 'site_name', 'rr_count', 'underlay_p2p_network_summary', 'overlay_loopback_network_summary', 'vtep_loopback_network_summary', 'mlag_leaf_peer_l3', 'mlag_peer', 'vxlan_vlan_aware_bundles', 'spine_switch_count', 'spine_bgp_as', 'leaf_bgp_as_range', 'leaf_switch_count', 'tor_switch_count']

    region = ObjectVar(
        description="Choose Region",
        model=Region
    )

    site_name = StringVar(
        description = "Name for the new fabric"
    )

    rr_count = IntegerVar(
        description = "Number or Relay Racks to build"
    )

    underlay_p2p_network_summary = IPNetworkVar(
        description = "Underlay P2P network - Assign range larger then total [spines * total potential leafs * 2"
    )

    overlay_loopback_network_summary = IPNetworkVar(
        description = "Overlay Loopback network - Assign range larger then total spines + total leafs switches"
    )

    vtep_loopback_network_summary = IPNetworkVar(
        description = "Vtep Loopback network - Assign range larger then total leaf switches"
    )

    mlag_leaf_peer_l3 = IPNetworkVar(
        description = "Leaf L3 MLAG network - Assign range larger then total spines + total leafs switches"
    )

    mlag_peer = IPNetworkVar(
        description = "MLAG Peer network - Assign range larger then total spines + total leafs switches"
    )

    vxlan_vlan_aware_bundles = BooleanVar(
        description = "Should bundles be vxlan vlan aware?"
    )

    spine_switch_count = IntegerVar(
        description = "Number of Spines to be deployed"
    )

    spine_bgp_as = IntegerVar(
        description = "Spine BGP ASN"
    )
    
    leaf_bgp_as_range = StringVar(
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
        self.data = data
        self.commit = commit
        STATUS_PLANNED = Status.objects.get(slug='planned')
        RESERVED = Status.objects.get(slug='reserved')

        #  Create the New site
        site = Site(
            name=data['site_name'],
            slug=slugify(data['site_name']),
            asn=data['spine_bgp_as'],
            status=STATUS_PLANNED,
        )
        site.validated_save()
        self.log_success(obj=site, message="Created new site")

        # Create the Relay Racks
        for i in range(1, data['rr_count'] + 1):
            rack = Rack(
                name=f'{site.slug}_rr_{i}',
                site=site,
                u_height="42",
                width="19",
                status=STATUS_PLANNED
            )
            rack.validated_save()
            self.log_success(obj=rack, message="Created Relay Racks")

        # Create IP Networks
        underlay_pfx = Prefix(
            prefix=data['underlay_p2p_network_summary'],
            site=site,
            status=RESERVED
        )
        underlay_pfx.validated_save()
        self.log_success(obj=underlay_pfx, message="Created new underlay prefix")
        
        overlay_role, _ = Role.objects.get_or_create(name="overlay")
        Prefix.objects.get_or_create(prefix=data['overlay_loopback_network_summary'], site=site, role=overlay_role)

        # overlay_pfx = Prefix(
        #     prefix=data['overlay_loopback_network_summary'],
        #     site=site,
        #     status=RESERVED
        # )
        # overlay_pfx.validated_save()
        # self.log_success(obj=overlay_pfx, message="Created new overlay prefix")

        vtep_pfx = Prefix(
            prefix=data['vtep_loopback_network_summary'],
            site=site,
            status=RESERVED
        )
        vtep_pfx.validated_save()
        self.log_success(obj=vtep_pfx, message="Created new VTEP prefix")

        mlag_leaf_peer_pfx = Prefix(
            prefix=data['mlag_leaf_peer_l3'],
            site=site,
            status=RESERVED
        )
        mlag_leaf_peer_pfx.validated_save()
        self.log_success(obj=mlag_leaf_peer_pfx, message="Created new Leaf mlag peer prefix")

        mlag_peer_pfx = Prefix(
            prefix=data['mlag_peer'],
            site=site,
            status=RESERVED
        )
        mlag_peer_pfx.validated_save()
        self.log_success(obj=mlag_peer_pfx, message="Created new Leaf mlag peer prefix")

        # Create Spine
        spine_role = DeviceRole.objects.get(name='Fabric_Spine')
        for i in range(1, data['spine_switch_count'] + 1):
            device = Device(
                device_type=data['spine_model'],
                name=f'{site.slug}_spine_{i}',
                site=site,
                status=STATUS_PLANNED,
                device_role=spine_role,
                rack=rack,
                position=data.get("rack_elevation"),
                face="front"
            )
            device.validated_save()
            self.log_success(obj=device, message="Created Spine Switches")

        # Generate Loopback interface and Assign address
        loopback_intf = Interface.objects.create(name="Loopback0", type="virtual", device=device)

        loopback_pfx = Prefix.objects.get(site=site, role__name="overlay")

        available_ips = loopback_pfx.get_available_ips()
        address = list(available_ips)[0]
        loopback_ip = IPAddress.objects.create(address=str(address), assigned_object=loopback_intf)

        # Create Leaf
        leaf_role = DeviceRole.objects.get(name='Fabric_l3_leaf')
        for i in range(1, data['leaf_switch_count'] + 1):
            device = Device(
                device_type=data['leaf_model'],
                name=f'{site.slug}_leaf_{i}',
                site=site,
                status=STATUS_PLANNED,
                device_role=leaf_role
            )
            device.validated_save()
            self.log_success(obj=device, message="Created Leaf Switches")

        # Create ToR
        tor_role = DeviceRole.objects.get(name='Fabric_l2_leaf')
        for i in range(1, data['tor_switch_count'] + 1):
            device = Device(
                device_type=data['tor_model'],
                name=f'{site.slug}_tor_{i}',
                site=site,
                status=STATUS_PLANNED,
                device_role=tor_role
            )
            device.validated_save()
            self.log_success(obj=device, message="Created ToR Switches")

