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
    manufacturer = ObjectVar(
        model=Manufacturer,
        required=False
    )
    
    spine = ObjectVar(
        description="Spine model",
        model=DeviceType,
        query_params={
            'manufacturer_id': '$manufacturer'
        }
    )

    leaf = ObjectVar(
        description="Leaf model",
        model=DeviceType,
        query_params={
            'manufacturer_id': '$manufacturer'
        }
    )

    tor = ObjectVar(
        description="ToR model",
        model=DeviceType,
        query_params={
            'manufacturer_id': '$manufacturer'
        }
    )