from django.utils.text import slugify

from nautobot.dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site, Racks, Region
from nautobot.extras.models import Status
from nautobot.extras.jobs import *
import ipaddress

class NewFabric(job):
    class Meta:
        name = "New Fabric"
        description = "Build new vxlan deployment"
        field_order = ['region', 'fabric_name', 'relay_rack', 'underlay_p2p_network_summary', 'overlay_loopback_network_summary', 'vtep_loopback_network_summary', 'mlag_leaf_peer_l3', 'mlag_peer', 'vxlan_vlan_aware_bundles', 'bgp_peer_groups', 'spine_switch_count', 'spine_bgp_as', 'leaf_bgp_as_range', 'leaf_switch_count', 'tor_switch_count']

    region = ObjectVar(model=Region)

    fabric_name = StringVar(
        description = "Name for the new fabric"
    )

    relay_rack = IntegerVar(
        description = "Choice how many Relay Racks"
    )

    underlay_p2p_network_summary = ipaddress.ip_network(
        description = "Underlay P2P network - Assign range larger then total [spines * total potential leafs * 2"
    )

    overlay_loopback_network_summary = ipaddress.ip_network(
        description = "Overlay Loopback network - Assign range larger then total spines + total leafs switches"
    )

    vtep_loopback_network_summary = ipaddress.ip_network(
        description = "Vtep Loopback network - Assign range larger then total leaf switches"
    )

    mlag_leaf_peer_l3 = ipaddress.ip_network(
        description = "Leaf L3 MLAG network - Assign range larger then total spines + total leafs switches"
    )

    mlag_peer = ipaddress.ip_network(
        description = "MLAG Peer network - Assign range larger then total spines + total leafs switches"
    )

    vxlan_vlan_aware_bundles = Bool(
        description = "Should bundles be vxlan vlan aware?"
    )

    bgp_peer_groups = Stringvar(
        description = "List the names of th BGP Peer Groups - Comma seperated 'IPv4_UNDERLAY_PEERS', 'EVPN_OVERLAY_PEERS', 'MLAG_IPv4_UNDERLAY_PEER' "
    )

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
    
    def run(self, data=None, commit=None):
        self.device = {}

        # ----------------------------------------------------------------------------
        # Initialize the database with all required objects
        # ----------------------------------------------------------------------------
        create_custom_fields()
        create_relationships()
        create_prefix_roles()

        # Create the New site
        site_name = data['fabric_name'].lower()
        region = data['region']
        site_status = Status.objects.get_for_model(Site).get(slug="active")
        self.site, created = Site.objects.get_or_create(
            name=site_name, region=region, slug=site_name, status=site_status
        )
        self.site.save()
        self.log_success(self.site, f"Site {site_name} succesfully created")

        ROLES["spine"]["count"] = data['spine_switch_count']
        ROLES["leaf"]["count"] = data['leaf_switch_count']
        ROLES["tor"]["count"] = data['tor_switch_count']

        ROLES["spine"]["role"] = "fabric_spine"
        ROLES["leaf"]["role"] = "fabric_l3_leaf"
        ROLES["tor"]["role"] = "fabric_l2_leaf"

        # prefix_role, _ = Role.object.get_or_create(name="underlay_p2p_network")
        container_status = Status.objects.get_for_model(Prefix).get(slug="container")
        # underlay_prefix = Prefix.objects.filter(site=self.site, status=container_status, role=prefix_role).first()

        # if not underlay_prefix:
        #     top_level_prefix = Prefix.objects.filter(
        #         role__slug=slugify(UNDERLAY_P2P_NETWORK), status=container_status
        #     ).first()

        #     if not top_level_prefix:
        #         raise Exception("Unable to find the top level prefix to allocate a Network for this site")
            
        #     first_avail = top_level_prefix.get_first_available_prefix()
        #     prefix = list(first_avail.subnet(UNDERLAY_PREFIX_SIZE))[0]
        #     underlay_prefix = Prefix.objects.create(prefix=prefix, site=self.site, status=container_status, role=prefix_role)

        # Create underlay p2p block
        underlay_role, _ = Role.objects.get_or_create(name="underlay_p2p")
        Prefix.objects.get_or_create(
            prefix=str(underlay_p2p_network_summary=data['underlay_p2p_network_summary']), site=self.site, role=underlay_role, status=container_status
        )

        overlay_loopback_role, _ = Role.objects.get_or_create(name="overlay_loopback")
        Prefix.objects.get_or_create(
            prefix=str(overlay_loopback_network_summary=data['overlay_loopback_network_summary']), site=self.site, role=overlay_loopback_role, status=container_status
        )

        vtep_loopback_role, _ = Role.objects.get_or_create(name="vtep_loopback")
        Prefix.objects.get_or_create(
            prefix=str(vtep_loopback_network_summary=data['vtep_loopback_network_summary']), site=self.site, role=vtep_loopback_role, status=container_status
        )

        # Create Relay Racks at site
        rack_status = Status.objects.get_for_model(Rack).get(slug="active")
        for i in range(1, ROLE['tor']['count'] + 1):
            rack_name = f"{site_name}-{100 + i}"
            rack = Rack.objects.get_or_create(
                name=rack_name, site=self.site, u_height=RACK_HEIGHT, type=RACK_TYPE, status=rack_status
            )

        # Create Devices

        for role, data in ROLES.items(): 
            for i in range(1, data.get("count", 2) + 1):

                rack_name = f"{site_name}-{100 + i}"
                rack = Rack.objects.filter(name=rack_name, site=self.site).first()
                
                device_name = f"{site_name}-{role}-{i:02}"

                device = Device.objects.filter(name=device_name).first()
                if device:
                    self.devices[device_name] = device
                    self.log_success(obj=device, message=f"Device {device_name} already present")
                    continue

                device_status = Status.objects.get_for_model(Device).get(slug="active")
                device_role, _ = DeviceRole.objects.get_or_create(name=role, slug=slugify(role))
                device = Device.objects.create(
                    device_type=DeviceType.objects.get(slug=data.get("device_type")),
                    name=device_name,
                    site=self.site,
                    status=device_status,
                    device_role=device_role,
                    rack=rack,
                    position=data.get("rack_elevation"),
                    face="front",
                )

                device.clean()
                device.save()
                self.devices[device_name] = device
                self.log_success(device, f"Device {device_name} successfully created")

                # create loopback interface and assign address
                loopback_intf = Interface.objects.create(
                    name="Loopback0", type=InterfaceTypeChoices.TYPE_VIRTUAL, device=device
                )

                loopback0_prefix = Prefix.objects.get(
                    site=self.site,
                    role__name="loopback",
                )

                available_ips = loopback_prefix.get_available_ips()
                address = list(available_ips)[0]
                loopback0_ip = IPAddress.objects.create(address=str(address), assigned_object=loopback_intf)

                # Assign Role to Interfaces
                # intfs = iter(Interface.objects.filter(device=device))
                # for int_role, cnt in data["interfaces"]:
                #     for i in range(0, cnt):
                #         intf = next(intfs)
                #         intf._custom_field_data = {"role": int_role}
                #         intf.save()

                # if role == "fabric_spine":
                #     for vlan_name, vlan_data in VLANS.items():
                #         prefix_role = Role.objects.get(slug=vlan_name)
                #         vlan = VLAN.objects.create(
                #             vid=vlan_data["vlan_id"], name=f"{rack_name}-{vlan_name}", site=self.site, role=prefix_role
                #         )
                #         vlan_block = Prefix.objects.filter(
                #             site=self.site, status=container_status, role=prefix_role
                #         ).first()



