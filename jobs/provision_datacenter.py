from django.utils.text import slugify

from nautobot.dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site, Region
from nautobot.extras.models import Status
from nautobot.extras.jobs import *

class DataCenter(Job):
    class Meta:
        name = "Build New DataCenter"
        description = "Build a new DataCenter with VXLAN"
        field_order = ['region', 'site_name', 'underlay_p2p_network_summary', 'overlay_loopback_network_summary', 'vtep_loopback_network_summary', 'mlag_leaf_peer_l3', 'mlag_peer', 'spine_switch_count', 'spine_bgp_as', 'leaf_bgp_as_range', 'leaf_switch_count', 'tor_switch_count']

    region = ObjectVar(
        description="Choose Region",
        model=Region
    )

    site_name = StringVar(
        description = "Name for the new fabric"
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
    
    # leaf_bgp_as_range = IntegerVar(
    #     description = "Define the range of acceptable remote ASNs from leaf switches"
    # )

    # leaf_switch_count = IntegerVar(
    #     description = "Number of Leafs to be deployed"
    # )

    # tor_switch_count = IntegerVar(
    #     description = "Number of ToR switches to be deployed"
    # )
    # manufacturer = ObjectVar(
    #     model=Manufacturer,
    #     required=False
    # )

    # spine_model = ObjectVar(
    #     description="Spine model",
    #     model=DeviceType,
    #     query_params={
    #         'manufacturer_id': '$manufacturer'
    #     }
    # )

    # leaf_model = ObjectVar(
    #     description="Leaf model",
    #     model=DeviceType,
    #     query_params={
    #         'manufacturer_id': '$manufacturer'
    #     }
    # )

    # tor_model = ObjectVar(
    #     description="ToR model",
    #     model=DeviceType,
    #     query_params={
    #         'manufacturer_id': '$manufacturer'
    #     }
    # )