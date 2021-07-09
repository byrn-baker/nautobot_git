from django.utils.text import slugify

from nautobot.dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site, Region, Rack, Interface
from nautobot.ipam.models import VRF, RouteTarget, Prefix, IPAddress, Role
from nautobot.extras.models import Status
from nautobot.extras.jobs import *

class DataCenter(Job):
    class Meta:
        name = "Build New DataCenter"
        description = "Build a new DataCenter with VXLAN"
        field_order = ['region', 'site_name', 'pod_name', 'relay_rack_count', 'underlay_p2p_network_summary', 'overlay_loopback_network_summary', 'vtep_loopback_network_summary', 'mlag_leaf_peer_l3', 'mlag_peer', 'vxlan_vlan_aware_bundles', 'spine_switch_count', 'spine_bgp_as', 'leaf_bgp_as_range', 'leaf_switch_count', 'tor_switch_count']

    region = ObjectVar(
        description="Choose Region",
        model=Region
    )

    site_name = StringVar(
        description = "Name for the new fabric"
    )

    pod_name = StringVar(
        description = "Pod number for this deployment"
    )

    relay_rack_count = IntegerVar(
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
    
    def create_p2p_link(self, intf1, intf2):
        # Creating a point to point link between 2 interfaces
        # Connects 2 interfaces with a cable and uses the underlay prefix assigning one IP to each interface
        if intf1.cable or intf2.cable:
            self.log_warning(
                essage=f"Unable to create a P2P link between {intf1.device.name}::{intf1} and {intf2.device.name}::{intf2}"
            )
            return False

        status = Status.objects.get_for_model(Cable).get(slug="connected")
        cable = Cable.objects.create(termination_a=intf1, termination_b=intf2, status=status)
        cable.save()

        # Find Next available Network
        prefix = Prefix.objects.filter(site=self.site, role__name="p2p_underlay").first()
        first_avail = prefix.get_first_available_prefix()
        subnet = list(first_avail.subnet(P2P_PREFIX_SIZE))[0]

        Prefix.objects.create(prefix=str(subnet))

        # Create IP Addresses on both sides
        ip1 = IPAddress.objects.create(address=str(subnet[0]), assigned_object=intf1)
        ip2 = IPAddress.objects.create(address=str(subnet[1]), assigned_object=intf2)

    def run(self, data, commit):
        self.data = data
        self.commit = commit
        STATUS_PLANNED = Status.objects.get(slug='planned')
        RESERVED = Status.objects.get(slug='reserved')
        ACTIVE = Status.objects.get(slug='active')
        self.devices = {}

        #  Create the New site
        self.site, created = Site.objects.get_or_create(
            name=data['site_name'],
            slug=slugify(data['site_name']),
            asn=data['spine_bgp_as'],
            status=STATUS_PLANNED
        )
        self.site.validated_save()
        self.log_success(obj=self.site, message="Created new site")
        # site = Site(
        #     name=data['site_name'],
        #     slug=slugify(data['site_name']),
        #     asn=data['spine_bgp_as'],
        #     status=STATUS_PLANNED,
        # )
        # site.validated_save()
        # self.log_success(obj=site, message="Created new site")

        # Create IP Networks
        underlay_role, _ = Role.objects.get_or_create(name="p2p_underlay", slug="p2p_underlay")
        underlay_pfx = Prefix(
            prefix=str(data['underlay_p2p_network_summary']),
            site=self.site,
            role=underlay_role,
            status=RESERVED 
        )
        underlay_pfx.validated_save()
        self.log_success(obj=underlay_pfx, message="Created new underlay prefix")
        
        overlay_role, _ = Role.objects.get_or_create(name="bgp_overlay", slug="bgp_overlay")
        overlay_pfx = Prefix(
            prefix=str(data['overlay_loopback_network_summary']),
            site=self.site,
            role=overlay_role,
            status=RESERVED
        )
        overlay_pfx.validated_save()
        self.log_success(obj=overlay_pfx, message="Created new overlay prefix")

        vtep_role, _ = Role.objects.get_or_create(name="vtep_loopback", slug="vtep_loopback")
        vtep_pfx = Prefix(
            prefix=str(data['vtep_loopback_network_summary']),
            site=self.site,
            role=vtep_role,
            status=RESERVED
        )
        vtep_pfx.validated_save()
        self.log_success(obj=vtep_pfx, message="Created new VTEP prefix")

        leaf_role, _ = Role.objects.get_or_create(name="mlag_l3", slug="mlag_l3")
        mlag_leaf_peer_pfx = Prefix(
            prefix=str(data['mlag_leaf_peer_l3']),
            site=self.site,
            role=leaf_role,
            status=RESERVED
        )
        mlag_leaf_peer_pfx.validated_save()
        self.log_success(obj=mlag_leaf_peer_pfx, message="Created new Leaf mlag peer prefix")

        mlag_role, _ = Role.objects.get_or_create(name="mlag_l2", slug="mlag_l2")
        mlag_peer_pfx = Prefix(
            prefix=str(data['mlag_peer']),
            site=self.site,
            role=mlag_role,
            status=RESERVED
        )
        mlag_peer_pfx.validated_save()
        self.log_success(obj=mlag_peer_pfx, message="Created new Leaf mlag peer prefix") 

        # Create the Relay Racks
        pod = data['pod_name'].lower()
        for i in range(1, data['relay_rack_count'] + 1):
            rack = Rack(
                name=f'{self.site.slug}_{pod}_rr_{i}',
                site=self.site,
                u_height="42",
                width="19",
                status=STATUS_PLANNED
            )
            rack.validated_save()
            self.log_success(obj=rack, message="Created Relay Racks")

        # Create Spine
        spine_role = DeviceRole.objects.get(name='Fabric_Spine')
        device_intf = ['Ethernet1', 'Ethernet2', 'Ethernet3', 'Ethernet4', 'Ethernet5', 'Ethernet6', 'Ethernet7', 'Ethernet8', 'Management1' ]
        for i in range(1, data['spine_switch_count'] + 1):
            rack_name = f'{self.site.slug}_{pod}_rr_{i}'
            rack = Rack.objects.filter(name=rack_name, site=self.site).first()

            device_name = f'{self.site.slug}_spine_{i}'
            device = Device.objects.filter(name=device_name).first()
            if device:
                self.devices[device_name] = device
                self.log_success(obj=device, message=f"Device {device_name} already present")
                continue

            device = Device(
                device_type=data['spine_model'],
                name=f'{self.site.slug}_{pod}_spine_{i}',
                site=self.site,
                status=STATUS_PLANNED,
                device_role=spine_role,
                rack=rack,
                position=data.get("rack_elevation"),
                face="front"
            )
            device.validated_save()
            self.devices[device_name] = device
            self.log_success(device, f"Device {device_name} successfully created")

            # Create physical interfaces
            for intf in device_intf:
                Interface.objects.create(name=intf, type='1000base-t', device=device)

            # Generate BGP Overlay interface and Assign address
            loopback_intf = Interface.objects.create(name="Loopback0", type="virtual", description="BGP Overlay", device=device)
            loopback_intf.validated_save()
            self.log_success(obj=loopback_intf, message="Created Loopback Interfaces")

            loopback_pfx = Prefix.objects.get(site=self.site, role__name="bgp_overlay")

            overlay_ips = loopback_pfx.get_available_ips()
            overlay_address = list(overlay_ips)[0]
            overlay_ip = IPAddress.objects.create(address=str(overlay_address), status=RESERVED, assigned_object=loopback_intf)
            overlay_ip.validated_save()
            self.log_success(obj=overlay_ip, message="Assigned Available IP to Loopback")

            # Generate VTEP Loopback interface and assign addresses
            vtep_intf = Interface.objects.create(name="Loopback1", type="virtual", description="VTEP Loopback", device=device)
            vtep_intf.validated_save()
            self.log_success(obj=vtep_intf, message="Created vtep Interfaces")

            vtep_pfx = Prefix.objects.get(site=self.site, role__name="vtep_loopback")

            vtep_ips = vtep_pfx.get_available_ips()
            vtep_address = list(vtep_ips)[0]
            vtep_ip = IPAddress.objects.create(address=str(vtep_address), status=RESERVED, assigned_object=vtep_intf)
            vtep_ip.validated_save()
            self.log_success(obj=vtep_ip, message="Assigned Available IP to Loopback")

        # Create Leaf
        leaf_role = DeviceRole.objects.get(name='Fabric_l3_leaf')
        for i in range(1, data['leaf_switch_count'] + 1):
            rack_name = f'{self.site.slug}_{pod}_rr_{i}'
            rack = Rack.objects.filter(name=rack_name, site=self.site).first()

            device_name = f'{self.site.slug}_{pod}_leaf_{i}'
            device = Device.objects.filter(name=device_name).first()
            if device:
                self.devices[device_name] = device
                self.log_success(obj=device, message=f"Device {device_name} already present")
                continue

            device = Device(
                device_type=data['leaf_model'],
                name=f'{self.site.slug}_{pod}_leaf_{i}',
                site=self.site,
                status=STATUS_PLANNED,
                device_role=leaf_role,
                rack=rack,
                position=data.get("rack_elevation"),
                face="front"
            )
            device.validated_save()
            self.devices[device_name] = device
            self.log_success(obj=device, message="Created Leaf Switches")

            # Generate BGP Overlay interface and Assign address
            loopback_intf = Interface.objects.create(name="Loopback0", type="virtual", description="BGP Overlay", device=device)
            loopback_intf.validated_save()
            self.log_success(obj=loopback_intf, message="Created Loopback Interfaces")

            loopback_pfx = Prefix.objects.get(site=self.site, role__name="bgp_overlay")

            overlay_ips = loopback_pfx.get_available_ips()
            overlay_address = list(overlay_ips)[0]
            overlay_ip = IPAddress.objects.create(address=str(overlay_address), status=RESERVED, assigned_object=loopback_intf)
            overlay_ip.validated_save()
            self.log_success(obj=overlay_ip, message="Assigned Available IP to Loopback")

            # Generate VTEP Loopback interface and assign addresses
            vtep_intf = Interface.objects.create(name="Loopback1", type="virtual", description="VTEP Loopback", device=device)
            vtep_intf.validated_save()
            self.log_success(obj=vtep_intf, message="Created vtep Interfaces")

            vtep_pfx = Prefix.objects.get(site=self.site, role__name="vtep_loopback")

            vtep_ips = vtep_pfx.get_available_ips()
            vtep_address = list(vtep_ips)[0]
            vtep_ip = IPAddress.objects.create(address=str(vtep_address), status=RESERVED, assigned_object=vtep_intf)
            vtep_ip.validated_save()
            self.log_success(obj=vtep_ip, message="Assigned Available IP to Loopback")


        # # Create ToR
        # tor_role = DeviceRole.objects.get(name='Fabric_l2_leaf')
        # for i in range(1, data['tor_switch_count'] + 1):
        #     device = Device(
        #         device_type=data['tor_model'],
        #         name=f'{self.site.slug}_tor_{i}',
        #         site=self.site,
        #         status=STATUS_PLANNED,
        #         device_role=tor_role,
        #         rack=rack,
        #         position=data.get("rack_elevation"),
        #         face="front"
        #     )
        #     device.validated_save()
        #     self.log_success(obj=device, message="Created ToR Switches")