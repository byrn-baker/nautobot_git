config = """
superspine1:
  interfaces:
    - name: Ethernet1
      type: "1000base-t"
      b_device: spine1
      b_int: Ethernet7
    - name: Ethernet2
      type: "1000base-t"
      b_device: spine2
      b_int: Ethernet7
superspine2: 
  interfaces:
    - name: Ethernet1
      type: "1000base-t"
      b_device: spine1
      b_int: Ethernet8
    - name: Ethernet2
      type: "1000base-t"
      b_device: spine2
      b_int: Ethernet8
spine1:
  device_type: "spine"
  interfaces:
    - name: Ethernet2
      type: "1000base-t"
      b_device: leaf1
      b_int: Ethernet3
    - name: Ethernet3
      type: "1000base-t"
      b_device: leaf2
      b_int: Ethernet3
    - name: Ethernet4
      type: "1000base-t"
      b_device: leaf3
      b_int: Ethernet3
    - name: Ethernet5
      type: "1000base-t"
      b_device: leaf4
      b_int: Ethernet3
    - name: Ethernet6
      type: "1000base-t"
      b_device: leaf5
      b_int: Ethernet3
    - name: Ethernet7 
      type: "1000base-t"
      b_device: superspine1
      b_int: Ethernet1
    - name: Ethernet8
      type: "1000base-t"
      b_device: superspine2
      b_int: Ethernet1
spine2:
  interfaces:
    - name: Ethernet2
      type: "1000base-t"
      b_device: leaf1
      b_int: Ethernet4
    - name: Ethernet3
      type: "1000base-t"
      b_device: leaf2
      b_int: Ethernet4
    - name: Ethernet4
      type: "1000base-t"
      b_device: leaf3
      b_int: Ethernet4
    - name: Ethernet5
      type: "1000base-t"
      b_device: leaf4
      b_int: Ethernet4
    - name: Ethernet6
      type: "1000base-t"
      b_device: leaf5
      b_int: Ethernet3
    - name: Ethernet7 
      type: "1000base-t"
      b_device: superspine1
      b_int: Ethernet1
    - name: Ethernet8
      type: "1000base-t"
      b_device: superspine2
      b_int: Ethernet1
spine3:
  interfaces:
    - name: Ethernet2
      type: "1000base-t"
      b_device: leaf1
      b_int: Ethernet5
    - name: Ethernet3
      type: "1000base-t"
      b_device: leaf2
      b_int: Ethernet5
    - name: Ethernet4
      type: "1000base-t"
      b_device: leaf3
      b_int: Ethernet5
    - name: Ethernet5
      type: "1000base-t"
      b_device: leaf4
      b_int: Ethernet5
    - name: Ethernet6
      type: "1000base-t"
      b_device: leaf5
      b_int: Ethernet3
    - name: Ethernet7 
      type: "1000base-t"
      b_device: superspine1
      b_int: Ethernet1
    - name: Ethernet8
      type: "1000base-t"
      b_device: superspine2
      b_int: Ethernet1
spine4:
  interfaces:
    - name: Ethernet2
      type: "1000base-t"
      b_device: leaf1
      b_int: Ethernet5
    - name: Ethernet3
      type: "1000base-t"
      b_device: leaf2
      b_int: Ethernet5
    - name: Ethernet4
      type: "1000base-t"
      b_device: leaf3
      b_int: Ethernet5
    - name: Ethernet5
      type: "1000base-t"
      b_device: leaf4
      b_int: Ethernet5
    - name: Ethernet6
      type: "1000base-t"
      b_device: leaf5
      b_int: Ethernet3
    - name: Ethernet7 
      type: "1000base-t"
      b_device: superspine1
      b_int: Ethernet1
    - name: Ethernet8
      type: "1000base-t"
      b_device: superspine2
      b_int: Ethernet1
leaf1:
  vlans: 
    - name: Vlan4093
      b_device: leaf2
      b_int: Vlan4093
    - name: Vlan4094
      b_device: leaf2
      b_int: Vlan4094
  interfaces:
    - name: Ethernet1
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf2
      b_int: Ethernet1
    - name: Ethernet2
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf2
      b_int: Ethernet2
    - name: Ethernet3
      type: "1000base-t"
      b_device: spine1
      b_int: Ethernet2
    - name: Ethernet4
      type: "1000base-t"
      b_device: spine2
      b_int: Ethernet3
    - name: Ethernet5
      type: "1000base-t"
      b_device: spine3
      b_int: Ethernet4
    - name: Ethernet6
      type: "1000base-t"
      b_device: spine4
      b_int: Ethernet5
    - name: Ethernet7
      type: "1000base-t"
      mode: "tagged-all"
      b_device: l2leaf1
      b_int: Ethernet3
    - name: Ethernet8
      type: "1000base-t"
      mode: "tagged-all"
      b_device: l2leaf2
      b_int: Ethernet3
leaf2:
  interfaces:
    - name: Ethernet1
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf1
      b_int: Ethernet1
    - name: Ethernet2
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf1
      b_int: Ethernet2
    - name: Ethernet3
      type: "1000base-t"
      b_device: spine1
      b_int: Ethernet2
    - name: Ethernet4
      type: "1000base-t"
      b_device: spine2
      b_int: Ethernet3
    - name: Ethernet5
      type: "1000base-t"
      b_device: spine3
      b_int: Ethernet4
    - name: Ethernet6
      type: "1000base-t"
      b_device: spine4
      b_int: Ethernet5
    - name: Ethernet7
      type: "1000base-t"
      mode: "tagged-all"
      b_device: l2leaf1
      b_int: Ethernet4
    - name: Ethernet8
      type: "1000base-t"
      mode: "tagged-all"
      b_device: l2leaf2
      b_int: Ethernet4
leaf3:
  vlans: 
    - name: Vlan4093
      b_device: leaf4
      b_int: Vlan4093
    - name: Vlan4094
      b_device: leaf4
      b_int: Vlan4094
  interfaces:
    - name: Ethernet1
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf4
      b_int: Ethernet1
    - name: Ethernet2
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf4
      b_int: Ethernet2
    - name: Ethernet3
      type: "1000base-t"
      b_device: spine1
      b_int: Ethernet2
    - name: Ethernet4
      type: "1000base-t"
      b_device: spine2
      b_int: Ethernet3
    - name: Ethernet5
      type: "1000base-t"
      b_device: spine3
      b_int: Ethernet4
    - name: Ethernet6
      type: "1000base-t"
      b_device: spine4
      b_int: Ethernet5
    - name: Ethernet7
      type: "1000base-t"
      mode: "tagged-all"
      b_device: l2leaf3
      b_int: Ethernet3
    - name: Ethernet8
      type: "1000base-t"
      mode: "tagged-all"
      b_device: l2leaf4
      b_int: Ethernet3
leaf4:
  interfaces:
    - name: Ethernet1
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf3
      b_int: Ethernet1
    - name: Ethernet2
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf3
      b_int: Ethernet2
    - name: Ethernet3
      type: "1000base-t"
      b_device: spine1
      b_int: Ethernet2
    - name: Ethernet4
      type: "1000base-t"
      b_device: spine2
      b_int: Ethernet3
    - name: Ethernet5
      type: "1000base-t"
      b_device: spine3
      b_int: Ethernet4
    - name: Ethernet6
      type: "1000base-t"
      b_device: spine4
      b_int: Ethernet5
    - name: Ethernet7
      type: "1000base-t"
      mode: "tagged-all"
      b_device: l2leaf3
      b_int: Ethernet4
    - name: Ethernet8
      type: "1000base-t"
      mode: "tagged-all"
      b_device: l2leaf4
      b_int: Ethernet4
leaf5:
  interfaces:
    - name: Ethernet3
      type: "1000base-t"
      b_device: spine1
      b_int: Ethernet2
    - name: Ethernet4
      type: "1000base-t"
      b_device: spine2
      b_int: Ethernet3
    - name: Ethernet5
      type: "1000base-t"
      b_device: spine3
      b_int: Ethernet4
    - name: Ethernet6
      type: "1000base-t"
      b_device: spine4
      b_int: Ethernet5
l2leaf1:
  interfaces:
    - name: Ethernet1
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf1
      b_int: Ethernet7
    - name: Ethernet2
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf2
      b_int: Ethernet7
l2leaf2:
  interfaces:
    - name: Ethernet1
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf1
      b_int: Ethernet8
    - name: Ethernet2
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf2
      b_int: Ethernet8
l2leaf3:
  interfaces:
    - name: Ethernet1
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf3
      b_int: Ethernet7
    - name: Ethernet2
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf4
      b_int: Ethernet7
l2leaf4:
  interfaces:
    - name: Ethernet1
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf4
      b_int: Ethernet8
    - name: Ethernet2
      type: "1000base-t"
      mode: "tagged-all"
      b_device: leaf4
      b_int: Ethernet8
"""

from django.utils.text import slugify
import yaml
import json
from nautobot.dcim.models import Site, Device, Rack, Region, Cable, DeviceRole, DeviceType, Interface, Manufacturer
from nautobot.ipam.models import Role, Prefix, IPAddress, VLAN, VRF
from nautobot.extras.models import CustomField, Job, Status
from nautobot.extras.models.customfields import ContentType
from nautobot.extras.jobs import Job, StringVar, IntegerVar, ObjectVar, BooleanVar
from nautobot.circuits.models import Provider, CircuitType, Circuit, CircuitTermination
import ipaddress
##########################
# credit to damien @ NTC #
CUSTOM_FIELDS = {
    "role": {"models": [Interface], "label": "Role"},
    "site_type": {"models": [Site], "label": "Type of Site"},
    "fabric_name": {"models": [Site], "label": "Fabric Name"},
    "pod_name": {"models": [Device], "label": "The Pod this device is assigned to"},
    "device_bgp": {"models": [Device], "type": "Integer", "label": "Device BGP ASN"},
    "virtual_router_mac": {"models": [Device], "label": "Virtual Router Mac Address"},
    "virtual_router_ipv4": {"models": [Interface], "label": "Virtual Router IPv4 Address"},
    "vrf_vni": {"models": [VRF], "label": "VxLan VRF VNI"},
    "vxlan_vlan_rt": {"models": [VLAN], "label": "VxLan vLAN Route Target"},
    "vxlan_vlan_vni": {"models": [Interface], "label": "VxLAN SVI VNI"}

}
def create_custom_fields():
    """Create all relationships defined in CUSTOM_FIELDS."""
    for cf_name, field in CUSTOM_FIELDS.items():
        try:
            cf = CustomField.objects.get(name=cf_name)
        except CustomField.DoesNotExist:
            cf = CustomField.objects.create(name=cf_name)
            if "label" in field:
                cf.label = field.get("label")
            cf.validated_save()
        for model in field["models"]:
            ct = ContentType.objects.get_for_model(model)
            cf.content_types.add(ct)
            cf.validated_save()
############################

# Most of this stuff is pretty much pulled from an NTC Job on the demo site. I filled in some of the blanks
IPv4Network = ipaddress.ip_network
class CreateAristaDC(Job):
    """Job to create a new site and datacenter pod."""

    class Meta:
        """Meta class for CreateAristaDC."""

        name = "Create Arista DataCenter Fabric"
        description = """
        Create a new Fabric with N Spine (3 max), N Leaf switches (4 max), N Borderleaf switches (2 max), and a DCI switch if necessary.
        A new /23 will automatically be allocated from the 'Loopback Pool' and split into 2 /24s for the overlay loopback and the vtep loopback.
        A new /24 will automatically be allocated from the 'underlay Pool' and split into /31s to be assigned to each p2p interface in the underlay network.
        A new /26 will automatically be allocated from the 'mlag_peer Pool' and 'leaf_peer Pool' and split into /31s to be assigned to each MLAG SVI and LEAF_PEER SVI.  
        Top level prefixes need to be created and assigned the following roles - loopbacks, underlay_p2p, mlag_peer, and leaf_peer_l3.
        """
        label = "Arista_Fabric"
        field_order = [
            "dc_code",
            "pod_name",
            "fabric_name",
            "dc_bgp",
            "spine_count",
            "l3leaf_count",
            "l2leaf_count",
            "dci",
        ]
    dc_code = StringVar(description="Name of the new DataCenter", label="DataCenter")

    pod_name = StringVar(description="Name of the new Pod", label="Pod Name")

    fabric_name = StringVar(description="Name of the Fabric to assign new pod to", label="Fabirc Name")
    
    spine_count = IntegerVar(description="Number of Spine Switches", label="Spine switches count", min_value=0, max_value=3)

    dc_bgp = IntegerVar(description="BGP AS to Assign to the Spine", label="Spine BGP AS")

    l3leaf_count = IntegerVar(description="Number of Leaf Switches", label="L3 Leaf switch count", min_value=1, max_value=4)

    l2leaf_count = IntegerVar(description="Number of L2 Leaf Switches in this Pod", label="L2 Leaf switch count", min_value=1, max_value=2)
    
    dci = BooleanVar(description="Does this DataCenter require an interconnect?", label="DCI required")
    
    def run(self, data=None, commit=None):
        """Main function for CreateDC."""
        self.devices = {}

        # ----------------------------------------------------------------------------
        # Initialize the database with all required objects
        # ----------------------------------------------------------------------------
        create_custom_fields()
        # create_relationships()
        # create_prefix_roles()

        # ----------------------------------------------------------------------------
        # Create all of the Manufactuers, Models and Roles if they do not exist
        # ----------------------------------------------------------------------------
        arista_man = Manufacturer.objects.get_or_create(name="Arista", slug="arista")
        self.log_success(obj=arista_man, message="Created the Arista Manufacturer")

        arista = Manufacturer.objects.get(name="Arista")

        l2leaf = DeviceType.objects.get_or_create(manufacturer=arista, model="l2leaf", slug="l2leaf", u_height=1)
        # l2leaf.validated_save()
        self.log_success(obj=l2leaf, message="Created new device Type")

        l3leaf = DeviceType.objects.get_or_create(manufacturer=arista, model="l3leaf", slug="l3leaf", u_height=1)
        # l3leaf.validated_save()
        self.log_success(obj=l3leaf, message="Created new device Type")

        spine = DeviceType.objects.get_or_create(manufacturer=arista, model="spine", slug="spine", u_height=1)
        # spine.validated_save()
        self.log_success(obj=spine,message="Created new device Type")

        superspine = DeviceType.objects.get_or_create(manufacturer=arista, model="superspine", slug="superspine", u_height=1)
        self.log_success(obj=superspine,message="Created new device Type")


        # ----------------------------------------------------------------------------
        # Find or Create Site
        # ----------------------------------------------------------------------------
        dc_code = data["dc_code"].lower()
        pod_name = slugify(data["pod_name"])
        fabric_name = slugify(data["fabric_name"])
        p2p_dc_code = f"{dc_code}_underlay"
        mlag_dc_code = f"{dc_code}_mlag_peer"
        leaf_peer_dc_code = f"{dc_code}_leaf_peer"
        # region = data["region"]
        bgp = data["dc_bgp"]
        site_status = Status.objects.get_for_model(Site).get(slug="active")
        self.site, created = Site.objects.get_or_create(name=dc_code.upper(), slug=dc_code, status=site_status)
        self.site.custom_field_data["site_type"] = "fabric"
        self.site.custom_field_data["fabric_name"] = fabric_name
        self.site.save()
        self.log_success(self.site, f"Site {dc_code} successfully created")

        # Creating MLAG VLAN
        vlan = VLAN.objects.get_or_create(
          name="MLAG_PEER_VLAN",
          vid=4094,
          status=site_status,
          site=self.site
        )
        # vlan.validated_save()
        self.log_success(obj=vlan, message="Created MLAG VLAN")

        # vlan_4094_prefix = Prefix.objects.get_or_create(
        #   prefix="10.255.252.0/31",
        #   status=site_status,
        # )
        # # vlan_4094_prefix.validated_save()
        # self.log_success(obj=vlan_4094_prefix, message="Created MLAG Prefix")

        # Creating leaVLAN
        vlan = VLAN.objects.get_or_create(
          name="LEAF_PEER_L3_VLAN",
          vid=4093,
          status=site_status,
          site=self.site
        )
        # vlan.validated_save()
        self.log_success(obj=vlan, message="Created LEAF_PEER VLAN")

        # vlan_4093_prefix = Prefix.objects.get_or_create(
        #   prefix="10.255.254.0/31",
        #   status=site_status,
        # )
        # # vlan_4093_prefix.validated_save()
        # self.log_success(obj=vlan_4093_prefix, message="Created MLAG Prefix")
        
        # Reference Vars
        SWITCHES = yaml.load(config, Loader=yaml.FullLoader)
        TOP_LEVEL_PREFIX_ROLE = "loopbacks"
        TOP_LEVEL_P2P_PREFIX_ROLE = "underlay_p2p"
        TOP_LEVEL_MLAG_PEER_ROLE = "mlag_peer"
        TOP_LEVEL_LEAF_PEER_ROLE = "leaf_peer_l3"
        SITE_PREFIX_SIZE = 23
        P2P_SITE_PREFIX_SIZE = 24
        MLAG_PEER_PREFIX_SIZE = 26
        LEAF_PEER_PREFIX_SIZE = 26
        RACK_HEIGHT = 42
        RACK_TYPE = "4-post-frame"
        ROLES = {
            "spine": {"device_type": "spine"},
            "l3leaf": {"device_type": "l3leaf"},
            "superspine": {"device_type": "superspine"},
            "l2leaf": {"device_type": "l2leaf"},
        }
        # Number of devices to provision
        ROLES["l2leaf"]["nbr"] = data["l2leaf_count"]
        ROLES["l3leaf"]["nbr"] = data["l3leaf_count"]
        ROLES["spine"]["nbr"] = data["spine_count"]
        if data["dci"] == True:
            ROLES["superspine"]["nbr"] = 2
        else:
            ROLES["superspine"]["nbr"] = 0

        
        # ----------------------------------------------------------------------------
        # Allocate Prefixes for this DataCenter
        # ----------------------------------------------------------------------------
        # Search if there is already a datacenter or underlay p2p prefix associated with this side
        # if not search the Top Level Prefix and create a new one

        # Loopback range
        dc_role, _ = Role.objects.get_or_create(name=dc_code, slug=dc_code)
        container_status = Status.objects.get_for_model(Prefix).get(slug="container")
        dc_prefix = Prefix.objects.filter(site=self.site, status=container_status, role=dc_role).first()

        if not dc_prefix:
            top_level_prefix = Prefix.objects.filter(
                role__slug=slugify(TOP_LEVEL_PREFIX_ROLE), status=container_status
            ).first()

            if not top_level_prefix:
                raise Exception("Unable to find the top level Loopback prefix to allocate a Network for this site")

            first_avail = top_level_prefix.get_first_available_prefix()
            prefix = list(first_avail.subnet(SITE_PREFIX_SIZE))[0]
            dc_prefix = Prefix.objects.create(prefix=prefix, site=self.site, status=container_status, role=dc_role)
        
        # Interface P2P range
        dc_p2p_role, _ = Role.objects.get_or_create(name=p2p_dc_code, slug=p2p_dc_code)
        underlay_p2p_prefix = Prefix.objects.filter(site=self.site, status=container_status, role=dc_p2p_role).first()
        if not underlay_p2p_prefix:
          top_level_p2p_prefix = Prefix.objects.filter(
                role__slug=slugify(TOP_LEVEL_P2P_PREFIX_ROLE), status=container_status
            ).first()

          if not top_level_p2p_prefix:
            raise Exception("Unable to find the top level Underlay prefix to allocate a Network for this site")
          
          first_avail_p2p = top_level_p2p_prefix.get_first_available_prefix()
          p2p_prefix = list(first_avail_p2p.subnet(P2P_SITE_PREFIX_SIZE))[0]
          underlay_p2p_prefix = Prefix.objects.create(prefix=p2p_prefix, site=self.site, status=container_status, role=dc_p2p_role)
        
        # MLAG range
        dc_mlag_role, _ = Role.objects.get_or_create(name=mlag_dc_code, slug=mlag_dc_code)
        mlag_p2p_prefix = Prefix.objects.filter(site=self.site, status=container_status, role=dc_mlag_role).first()
        if not mlag_p2p_prefix:
          top_level_mlag_prefix =  Prefix.objects.filter(
                role__slug=slugify(TOP_LEVEL_MLAG_PEER_ROLE), status=container_status
            ).first()

          if not top_level_mlag_prefix:
            raise Exception("Unable to find the top level MLAG prefix to allocate a Network for this site")

          first_avail_mlag = top_level_mlag_prefix.get_first_available_prefix()
          mlag_prefix = list(first_avail_mlag.subnet(MLAG_PEER_PREFIX_SIZE))[0]
          mlag_p2p_prefix = Prefix.objects.create(prefix=mlag_prefix, site=self.site, status=container_status, role=dc_mlag_role)

        # LEAF PEER range
        dc_leaf_peer_role, _ = Role.objects.get_or_create(name=leaf_peer_dc_code, slug=leaf_peer_dc_code)
        leaf_peer_p2p_prefix  = Prefix.objects.filter(site=self.site, status=container_status, role=dc_leaf_peer_role).first()
        if not leaf_peer_p2p_prefix:
          top_level_leaf_peer_prefix = Prefix.objects.filter(
            role__slug=slugify(TOP_LEVEL_LEAF_PEER_ROLE), status=container_status
          ).first()

          if not top_level_leaf_peer_prefix:
            raise Exception("Unable to find the top level Leaf Peer prefix to allocate a Network for this site")

          first_avail_leaf_peer = top_level_leaf_peer_prefix.get_first_available_prefix()
          leaf_peer_prefix = list(first_avail_leaf_peer.subnet(LEAF_PEER_PREFIX_SIZE))[0]
          leaf_peer_p2p_prefix = Prefix.objects.create(prefix=leaf_peer_prefix, site=self.site, status=container_status, role=dc_leaf_peer_role)


        iter_subnet = IPv4Network(str(dc_prefix.prefix)).subnets(new_prefix=24)
        p2p_iter_subnet = IPv4Network(str(underlay_p2p_prefix.prefix)).subnets(new_prefix=24)
        mlag_iter_subnet = IPv4Network(str(mlag_p2p_prefix.prefix)).subnets(new_prefix=27)
        leaf_peer_iter_subnet = IPv4Network(str(leaf_peer_p2p_prefix.prefix)).subnets(new_prefix=27)

        # Allocate the subnet by block of /24
        mlag_peer = next(mlag_iter_subnet)
        leaf_peer_l3 = next(leaf_peer_iter_subnet)
        overlay_loopback = next(iter_subnet)
        vtep_loopback = next(iter_subnet)
        underlay_p2p = next(p2p_iter_subnet)
        # dci_p2p = next(iter_subnet)

        dc_role, _ = Role.objects.get_or_create(name=dc_code, slug=dc_code)

        mlag_role, _ = Role.objects.get_or_create(name=f"{dc_code}_mlag_peer_p2p", slug=f"{dc_code}_mlag_peer_p2p")
        Prefix.objects.get_or_create(
            prefix=str(mlag_peer),
            site=self.site,
            role=mlag_role,
            status=container_status,
        )
        self.log_success(obj=mlag_peer, message="Created new mlag peer prefix")

        leaf_peer_role, _ = Role.objects.get_or_create(name=f"{dc_code}_leaf_peer_p2p", slug=f"{dc_code}_leaf_peer_p2p")
        Prefix.objects.get_or_create(
            prefix=str(leaf_peer_l3),
            site=self.site,
            role=leaf_peer_role,
            status=container_status,
        )
        self.log_success(obj=leaf_peer_l3, message="Created new leaf peer prefix")

        overlay_role, _ = Role.objects.get_or_create(name=f"{dc_code}_overlay", slug=f"{dc_code}_overlay")
        Prefix.objects.get_or_create(
            prefix=str(overlay_loopback),
            site=self.site,
            role=overlay_role,
            status=container_status,
        )
        self.log_success(obj=overlay_loopback, message="Created new overlay prefix")
        

        vtep_role, _ = Role.objects.get_or_create(name=f"{dc_code}_vtep_loopback", slug=f"{dc_code}_vtep_loopback")
        Prefix.objects.get_or_create(
            prefix=str(vtep_loopback),
            site=self.site,
            role=vtep_role,
            status=container_status,
        )
        self.log_success(obj=vtep_loopback, message="Created new vtep prefix")

        underlay_role, _ = Role.objects.get_or_create(name=f"{dc_code}_underlay_p2p", slug=f"{dc_code}_underlay_p2p")
        Prefix.objects.get_or_create(
            prefix=str(underlay_p2p), 
            site=self.site, 
            role=underlay_role, 
            status=container_status,
        )
        self.log_success(obj=underlay_p2p, message="Created new underlay p2p prefix")

        # dci_p2p_role, _ = Role.objects.get_or_create(name=f"{dc_code}_dci_p2p", slug=f"{dc_code}_dci_p2p")
        # Prefix.objects.get_or_create(
        #     prefix=str(dci_p2p),
        #     site=self.site,
        #     role=dci_p2p_role,
        #     status=container_status,
        # )
        # self.log_success(obj=dci_p2p, message="Created new dci p2p prefix")

        # ----------------------------------------------------------------------------
        # Create Racks
        # ----------------------------------------------------------------------------
        rack_status = Status.objects.get_for_model(Rack).get(slug="active")

        rack_name_spine = f"{dc_code}-spine-rr-1"
        rack = Rack.objects.get_or_create(
            name=rack_name_spine, site=self.site, u_height=RACK_HEIGHT, type=RACK_TYPE, status=rack_status
        )
        self.log_success(obj=rack_name_spine, message=f"Created Relay Rack {rack_name_spine}")

        if data["dci"] == True: 
          rack_name_edge = f"{dc_code}-edge-rr-1"
          rack = Rack.objects.get_or_create(
              name=rack_name_edge, site=self.site, u_height=RACK_HEIGHT, type=RACK_TYPE, status=rack_status
          )
          self.log_success(obj=rack_name_edge, message=f"Created Relay Rack {rack_name_edge}")

        for i in range(1, ROLES["l3leaf"]["nbr"] + 1):
          rack_name = f"{dc_code}-leaf-rr-{i}"
          rack = Rack.objects.get_or_create(
              name=rack_name, site=self.site, u_height=RACK_HEIGHT, type=RACK_TYPE, status=rack_status
          )
          self.log_success(obj=rack_name, message=f"Created Relay Rack {rack_name}")
        for i in range(1, ROLES['l2leaf']['nbr'] + 1):
          rack_name_l2leaf = f"{dc_code}-hosts-rr-{i}"
          rack = Rack.objects.get_or_create(
              name=rack_name_l2leaf, site=self.site, u_height=RACK_HEIGHT, type=RACK_TYPE, status=rack_status
          )
          self.log_success(obj=rack_name_l2leaf, message=f"Created Relay Rack {rack_name_l2leaf}")


        # ----------------------------------------------------------------------------
        # Create Devices
        # ----------------------------------------------------------------------------
        for role, data in ROLES.items():
            for i in range(1, data.get("nbr", 2) + 1):
                if 'spine' in role:
                  rack_elevation = i + 1
                  rack_name = f"{dc_code}-spine-rr-1"
                  rack = Rack.objects.filter(name=rack_name, site=self.site).first()
                elif role == 'l3leaf':
                  rack_elevation = i + 1
                  rack_name = f"{dc_code}-l3leaf-rr-{i}"
                  rack = Rack.objects.filter(name=rack_name, site=self.site).first()
                elif 'superspine' in role:
                  rack_elevation = i + 3
                  rack_name = f"{dc_code}-edge-rr-1"
                  rack = Rack.objects.filter(name=rack_name, site=self.site).first()
                elif 'l2leaf' in role:
                  rack_elevation = i + 1
                  rack_name = f"{dc_code}-hosts-rr-{i}"
                  rack = Rack.objects.filter(name=rack_name, site=self.site).first()

                if role == 'l3leaf':
                  device_name = f"{dc_code}-leaf{i}"
                else:
                  device_name = f"{dc_code}-{role}{i}"

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
                    position=rack_elevation,
                    face="front",
                )

                device.clean()
                device.save()
                self.devices[device_name] = device
                self.log_success(device, f"Device {device_name} successfully created")

                # Building local context for various requirements per device
                lo0_prefix = Prefix.objects.get(role=dc_role)
                # global LOCAL_CONTEXT
                LOCAL_CONTEXT = {
                  "prefix_list":[f"{str(lo0_prefix)} eq 32",]
                }
                device.local_context_data = LOCAL_CONTEXT

                # Assigns the device to the Pod described in the Pod_Name survey
                if device_name == f"{dc_code}-spine1" or device_name == f"{dc_code}-spine2" or device_name == f"{dc_code}-spine3" or device_name == f"{dc_code}-spine4" or device_name == f"{dc_code}-leaf1" or device_name == f"{dc_code}-leaf2" or device_name == f"{dc_code}-leaf3" or device_name == f"{dc_code}-leaf4" or device_name == f"{dc_code}-leaf5":
                  device.custom_field_data["pod_name"]=pod_name

                device.validated_save()
                self.log_success(device, f"Added local context on {device_name}")

                # Add the Devices specific BGP assignments
                if device_name == f"{dc_code}-spine1" or device_name == f"{dc_code}-spine2" or device_name == f"{dc_code}-spine3" or device_name == f"{dc_code}-spine4":
                    device._custom_field_data = {"device_bgp": bgp}
                    device.validated_save()
                    self.log_success(device, f"Added AS::{bgp} to Device {device_name}")

                elif device_name == f"{dc_code}-leaf1" or device_name == f"{dc_code}-leaf2":
                    leaf_bgp = bgp + 1
                    device._custom_field_data = {"device_bgp": leaf_bgp}
                    device.validated_save()
                    self.log_success(device, f"Added AS::{leaf_bgp} to Device {device_name}")

                elif device_name == f"{dc_code}-leaf3" or device_name == f"{dc_code}-leaf4":
                    leaf_bgp = bgp + 2
                    device._custom_field_data = {"device_bgp": leaf_bgp}
                    device.validated_save()
                    self.log_success(device, f"Added AS::{leaf_bgp} to Device {device_name}")

                elif device_name == f"{dc_code}-leaf5":
                    borderleaf_bgp = bgp + 3
                    device._custom_field_data = {"device_bgp": borderleaf_bgp}
                    device.validated_save()
                    self.log_success(device, f"Added AS::{borderleaf_bgp} to Device {device_name}")

                elif device_name == f"{dc_code}-superspine1" or device_name == f"{dc_code}-superspine2":
                    superspine_bgp = 65000
                    device._custom_field_data = {"device_bgp":  superspine_bgp}
                    device.validated_save()
                    self.log_success(device, f"Added AS::{superspine_bgp} to Device {device_name}")



                # Create physical interfaces
                dev_name = device_name.replace(f"{dc_code}-","")
                # for iface in SWITCHES[dev_name]['interfaces']:
                #     intf_name = Interface.objects.create(
                #             name=iface['name'],
                #             type="1000base-t",
                #             device=device, 
                #     )
                #     self.log_success(obj=intf_name, message=f"{intf_name} successfully created on {device_name}")
                if device_name == f"{dc_code}-spine1" or device_name == f"{dc_code}-spine2" or device_name == f"{dc_code}-spine3" or device_name == f"{dc_code}-spine4":
                  intf_number =  ROLES["leaf"]["nbr"] + ROLES['superspine']['nbr']
                  for i in range(1, intf_number + 1):
                    if i == 2 or i == 3 or i == 4 or i == 5 or i == 6 or i == 7 or i == 8:
                      int_name = Interface.objects.create(
                        name=f"Ethernet{i}",
                        type="1000base-t",
                        label="Layer3",
                        device=device,

                      )
                      self.log_success(obj=int_name, message=f"{int_name} successfully created on {device_name}")
                      int_name.cf['role'] = "leaf"
                      int_name.validated_save()
                    else:
                      int_name = Interface.objects.create(
                        name=f"Ethernet{i}",
                        type="1000base-t",
                        device=device,
                      )
                      self.log_success(obj=int_name, message=f"{int_name} successfully created on {device_name}")

                elif device_name == f"{dc_code}-leaf1" or device_name == f"{dc_code}-leaf2":
                  intf_number =  ROLES["spine"]["nbr"] + 2
                  for i in range(1, intf_number + 1):
                    if i == 3 or i == 4 or i == 5 or i == 6:
                      int_name = Interface.objects.create(
                      name=f"Ethernet{i}",
                      type="1000base-t",
                      label="Layer3",
                      device=device,

                      )
                      self.log_success(obj=int_name, message=f"{int_name} successfully created on {device_name}")
                      int_name.cf['role'] = "spine"
                      int_name.validated_save()
                    else:
                      int_name = Interface.objects.create(
                      name=f"Ethernet{i}",
                      type="1000base-t",
                      label="trunk",
                      device=device,
                      )
                      self.log_success(obj=int_name, message=f"{int_name} successfully created on {device_name}")
                    
                    if ROLES["l2leaf"]["nbr"] == 1:
                      eth7 = Interface.objects.create(
                        name = "Ethernet7",
                        type = "1000base-t",
                        label = "trunk",
                        device = device,
                      ) 
                      self.log_success(obj=eth7, message=f"{eth7} successfully created on {device_name}")
                      eth7.cf['role'] = "l2leaf_connection"
                      eth7.validated_save()

                    elif ROLES["l2leaf"]["nbr"] == 2:
                      eth7 = Interface.objects.create(
                        name = "Ethernet7",
                        type = "1000base-t",
                        label = "trunk",
                        device = device,
                      ) 
                      self.log_success(obj=eth7, message=f"{eth7} successfully created on {device_name}")
                      eth7.cf['role'] = "l2leaf_connection"
                      eth7.validated_save()

                      eth8 = Interface.objects.create(
                        name = "Ethernet8",
                        type = "1000base-t",
                        label = "trunk",
                        device = device,
                      ) 
                      self.log_success(obj=eth8, message=f"{eth8} successfully created on {device_name}")
                      eth8.cf['role'] = "l2leaf_connection"
                      eth8.validated_save()

                elif device_name == f"{dc_code}-leaf3" or device_name == f"{dc_code}-leaf4" or device_name == f"{dc_code}-leaf5":
                  intf_number =  ROLES["spine"]["nbr"] + 2
                  for i in range(1, intf_number + 1):
                    if i == 3 or i == 4 or i == 5 or i == 6:
                      int_name = Interface.objects.create(
                      name=f"Ethernet{i}",
                      type="1000base-t",
                      label="Layer3",
                      device=device,

                      )
                      self.log_success(obj=int_name, message=f"{int_name} successfully created on {device_name}")
                      int_name.cf['role'] = "spine"
                      int_name.validated_save()
                    else:
                      int_name = Interface.objects.create(
                      name=f"Ethernet{i}",
                      type="1000base-t",
                      label="trunk",
                      device=device,
                      )
                      self.log_success(obj=int_name, message=f"{int_name} successfully created on {device_name}")

                elif device_name == f"{dc_code}-l2leaf1" or device_name == f"{dc_code}-l2leaf2":
                  intf_number = 4
                  for i in range(1, intf_number + 1):
                    int_name = Interface.objects.create(
                      name=f"Ethernet{i}",
                      type="1000base-t",
                      label="trunk",
                      device=device,
                    )
                    self.log_success(obj=int_name, message=f"{int_name} successfully created on {device_name}")

                elif device_name == f"{dc_code}-superspine1" or device_name == f"{dc_code}-superspine2":
                  intf_number =  ROLES["spine"]["nbr"]
                  for i in range(1, intf_number + 1):
                    if i == 1 or i == 2 or i == 3 or i == 4:
                      int_name = Interface.objects.create(
                      name=f"Ethernet{i}",
                      type="1000base-t",
                      label="Layer3",
                      device=device,

                      )
                      self.log_success(obj=int_name, message=f"{int_name} successfully created on {device_name}")
                      int_name.cf['role'] = "spine"
                      int_name.validated_save()
                                
                # LEAF MLAG Port Channel
                if device.device_role.slug == "l3leaf" and ROLES["l3leaf"]["nbr"] >= 2:
                    portchannel_intf = Interface.objects.create(
                        name="Port-Channel1", type="lag", mode="tagged-all", label="trunk", device=device
                    )
                    self.log_success(obj=portchannel_intf, message=f"{portchannel_intf} successfully created on {device_name}")
                    
                    # Thanks mcgoo298
                    eth1 = device.interfaces.get(name="Ethernet1")
                    eth2 = device.interfaces.get(name="Ethernet2")
                    po1 = device.interfaces.get(name="Port-Channel1")
                    eth1.lag = po1
                    eth1.mode = "tagged-all"
                    eth1.label = "trunk"
                    eth1.validated_save()
                    self.log_success(message=f"Moved {eth1} succesfully to {po1}")
                    eth2.lag = po1
                    eth2.mode = "tagged-all"
                    eth2.label = "trunk"
                    eth2.validated_save()
                    self.log_success(message=f"Moved {eth2} succesfully to {po1}")
                    # MLAG SVI
                    mlag_svi = Interface.objects.create(
                        name="Vlan4094", type="virtual", description="MLAG", device=device
                    )
                    self.log_success(obj=mlag_svi, message=f"{mlag_svi} successfully created on {device_name}")

                    #LEAF PEER SVI
                    leaf_peer_svi = Interface.objects.create(
                        name="Vlan4093", type="virtual", description="LEAF_PEER", device=device
                    )
                    self.log_success(obj=leaf_peer_svi, message=f"{leaf_peer_svi} successfully created on {device_name}")
                    #####################################################
                    # Creating IP addresses for MLAG Peer and LEAF Peer #
                    #####################################################
                    # mlag_prefix = Prefix.objects.get(
                    #   site=self.site, role__name=f"{dc_code}_mlag_peer",
                    # )

                    # available_mlag_ips = mlag_prefix.get_available_ips()
                    # mlag_address = list(available_mlag_ips)[0]
                    # mlag_ip = IPAddress.objects.create(address=str(mlag_address), description=f"{device_name}::{mlag_svi}", assigned_object=mlag_svi)

                    # leaf_peer_prefix = Prefix.objects.get(
                    #   site=self.site, role__name=f"{dc_code}_leaf_peer",
                    # )

                    # available_leaf_peer_ips = leaf_peer_prefix.get_available_ips()
                    # leaf_peer_address = list(available_leaf_peer_ips)[0]
                    # leaf_peer_ip = IPAddress.objects.create(address=str(leaf_peer_address), description=f"{device_name}::{leaf_peer_svi}", assigned_object=leaf_peer_svi)



                    # if device_name == f"leaf1-{dc_code}" or device_name == f"leaf3-{dc_code}":
                    #     interface = Interface.objects.get(name="Vlan4094", device=device)
                    #     ip = IPAddress.objects.create(address='192.168.255.1/30', assigned_object=interface)
                    #     self.log_success(message=f"Created MLAG PEER address on {interface.device.name}::{interface}")

                    # elif device_name == f"leaf2-{dc_code}" or device_name == f"leaf4-{dc_code}":
                    #     interface = Interface.objects.get(name="Vlan4094", device=device)
                    #     ip = IPAddress.objects.create(address='192.168.255.2/30', assigned_object=interface)
                    #     self.log_success(message=f"Created MLAG PEER address on {interface.device.name}::{interface}")

                # L3Leaf switch to l2leaf Port Channel
                if device_name == f"{dc_code}-leaf1" or device_name == f"{dc_code}-leaf2" and ROLES["l2leaf"]["nbr"] >= 1:
                  po6_intf = Interface.objects.create(
                    name="Port-Channel6", type="lag", mode="tagged-all", label="trunk",  device=device
                  )  
                  self.log_success(obj=po6_intf, message=f"{po6_intf} successfully created on {device_name}")
                  po6_intf.cf['role'] = "l2leaf_connection"
                  po6_intf.validated_save()
                  try:
                    eth7 = device.interfaces.get(name="Ethernet7")
                    po6 = device.interfaces.get(name="Port-Channel6")
                    eth7.lag = po6
                    eth7.mode = "tagged-all"
                    eth7.label = "trunk"
                    eth7.cf['role'] = "l2leaf_connection"
                    eth7.validated_save()
                    self.log_success(message=f"Moved {eth7} succesfully to {po6}")
                  except Exception:
                    pass
                  
                if device_name == f"{dc_code}-leaf1" or device_name == f"{dc_code}-leaf2" and ROLES["l2leaf"]["nbr"] >= 2:
                  try:
                    eth8 = device.interfaces.get(name="Ethernet8")
                    eth8.lag = po6
                    eth8.mode = "tagged-all"
                    eth8.label = "trunk"
                    eth8.cf['role'] = "l2leaf_connection"
                    eth8.validated_save()
                    self.log_success(message=f"Moved {eth8} succesfully to {po6}")
                  except Exception:
                    pass

                # l2leaf Switch to l3leaf Port Channel
                if device.device_role.slug == "l2leaf" and ROLES["l3leaf"]["nbr"] >= 2:
                  l2leaf_po6_intf = Interface.objects.create(
                    name="Port-Channel6", type="lag", mode="tagged-all", label="trunk", device=device
                  )
                  self.log_success(obj=l2leaf_po6_intf, message=f"{l2leaf_po6_intf} successfully created on {device_name}")

                  try:
                    l2leaf_eth3 = device.interfaces.get(name="Ethernet3")
                    l2leaf_eth4 = device.interfaces.get(name="Ethernet4")
                    l2leaf_po6 = device.interfaces.get(name="Port-Channel6")
                    l2leaf_eth3.lag = l2leaf_po6
                    l2leaf_eth3.mode = "tagged-all"
                    l2leaf_eth3.label = "trunk"
                    l2leaf_eth3.validated_save()
                    self.log_success(message=f"Moved {l2leaf_eth3} succesfully to {l2leaf_po6}")
                    l2leaf_eth4.lag = l2leaf_po6
                    l2leaf_eth4.mode = "tagged-all"
                    l2leaf_eth4.label = "trunk"
                    l2leaf_eth4.validated_save()
                    self.log_success(message=f"Moved {l2leaf_eth4} succesfully to {l2leaf_po6}")
                  except Exception:
                    pass


                # Generate Loopback0 interface and assign Loopback0 address
                if device.device_role.slug == 'spine' or device.device_role.slug == "l3leaf" or device.device_role.slug == 'superspine':
                  loopback0_intf = Interface.objects.create(
                      name="Loopback0", type="virtual", description="EVPN_Overlay_Peering", device=device
                  )
                  self.log_success(obj=loopback0_intf, message=f"{loopback0_intf} successfully created on {device_name}")

                  loopback0_prefix = Prefix.objects.get(
                      site=self.site, role__name=f"{dc_code}_overlay",
                  )

                  available_ips = loopback0_prefix.get_available_ips()
                  lo0_address = list(available_ips)[0]
                  loopback0_ip = IPAddress.objects.create(address=str(lo0_address), description=f"{device_name}::{loopback0_intf}", assigned_object=loopback0_intf)
                

                # Generate Loopback1 interface and assign Loopback1 address
                if device.device_role.slug == "l3leaf":
                    loopback1_intf = Interface.objects.create(
                        name="Loopback1", type="virtual", description="VTEP_VXLAN_Tunnel_Source", device=device
                    )
                    self.log_success(obj=loopback1_intf, message=f"{loopback1_intf} successfully created on {device_name}")

                    loopback1_prefix = Prefix.objects.get(
                        site=self.site,
                        role__name=f"{dc_code}_vtep_loopback",
                    )

                    available_ips = loopback1_prefix.get_available_ips()
                    lo1_address = list(available_ips)[0]
                    loopback1_ip = IPAddress.objects.create(address=str(lo1_address), description=f"{device_name}::{loopback1_intf}", assigned_object=loopback1_intf)

        #######################################
        # Creating Cables between interfaces  #
        #######################################
        for role, data in ROLES.items():
            for i in range(1, data.get("nbr", 2) + 1):
                device_name = f"{dc_code}-{role}{i}"
                device = Device.objects.get(name=device_name)
                dev_name = device_name.replace(f"{dc_code}-","")

                for iface in SWITCHES[dev_name]['interfaces']:
                  try:
                    interface = Interface.objects.get(name=iface['name'], device=device)
                    if interface.cable is None:
                        if "b_device" in iface.keys():
                            b_device = iface['b_device']
                            b_dev_name = f"{dc_code}-{b_device}"
                            bside_device = Device.objects.get(name=b_dev_name)
                            bside_interface = Interface.objects.get(name=iface['b_int'],device=bside_device, )
                            intf1 = interface
                            intf2 = bside_interface
                            status = Status.objects.get_for_model(Cable).get(slug="connected")
                            if intf1.cable or intf2.cable:
                                self.log_warning(
                                    message=f"Unable to create a P2P link between {intf1.device.name}::{intf1} and {intf2.device.name}::{intf2}"
                                )
                                return False
                            cable = Cable.objects.create(termination_a=intf1, termination_b=intf2, status=status)
                            cable.save()
                            self.log_success(message=f"Created a cable between {intf1.device.name}::{intf1} and {intf2.device.name}::{intf2}")
                            # Find Next available Network
                            if "mode" not in iface.keys():
                                P2P_PREFIX_SIZE = 31
                                ip_status = Status.objects.get_for_model(Device).get(slug="active")
                                prefix = Prefix.objects.filter(site=self.site, role__name=f"{dc_code}_underlay_p2p").first()
                                first_avail = prefix.get_first_available_prefix()
                                subnet = list(first_avail.subnet(P2P_PREFIX_SIZE))[0]

                                Prefix.objects.create(prefix=str(subnet))

                                # Create IP Addresses on both sides
                                ip1 = IPAddress.objects.create(address=f"{str(subnet[0])}/31", assigned_object=intf1, status=ip_status)
                                ip2 = IPAddress.objects.create(address=f"{str(subnet[1])}/31", assigned_object=intf2, status=ip_status)
                                self.log_success(message=f"Created a IP Addresses {ip1} & {ip2} between {intf1.device.name}::{intf1} and {intf2.device.name}::{intf2}")
                  except Exception:
                    pass
                
                #####################################
                # Creating /31 assignments for MLAG #
                #####################################
                if "vlans" in SWITCHES[dev_name].keys():
                  for iface in SWITCHES[dev_name]['vlans']:
                    if "Vlan4094" in iface['name']:
                      interface = Interface.objects.get(name=iface['name'], device=device)
                      if "b_device" in iface.keys():
                        b_device = iface['b_device']
                        b_dev_name = f"{dc_code}-{b_device}"
                        bside_device = Device.objects.get(name=b_dev_name)
                        bside_interface = Interface.objects.get(name=iface['b_int'],device=bside_device, )
                        intf1 = interface
                        intf2 = bside_interface
                        P2P_PREFIX_SIZE = 31
                        ip_status = Status.objects.get_for_model(Device).get(slug="active")
                        prefix = Prefix.objects.filter(site=self.site, role__name=f"{dc_code}_mlag_peer_p2p").first()
                        first_avail = prefix.get_first_available_prefix()
                        subnet = list(first_avail.subnet(P2P_PREFIX_SIZE))[0]
                        Prefix.objects.create(prefix=str(subnet))
                        # Create IP Addresses on both sides
                        ip1 = IPAddress.objects.create(address=f"{str(subnet[0])}/31", assigned_object=intf1, status=ip_status)
                        ip2 = IPAddress.objects.create(address=f"{str(subnet[1])}/31", assigned_object=intf2, status=ip_status)
                        self.log_success(message=f"Created a IP Addresses {ip1} & {ip2} between {intf1.device.name}::{intf1} and {intf2.device.name}::{intf2}")
                
                ##########################################
                # Creating /31 assignments for LEAF PEER #
                ##########################################
                  for iface in SWITCHES[dev_name]['vlans']:
                    if "Vlan4093" in iface['name']:
                      interface = Interface.objects.get(name=iface['name'], device=device)
                      if "b_device" in iface.keys():
                        b_device = iface['b_device']
                        b_dev_name = f"{dc_code}-{b_device}"
                        bside_device = Device.objects.get(name=b_dev_name)
                        bside_interface = Interface.objects.get(name=iface['b_int'],device=bside_device, )
                        intf1 = interface
                        intf2 = bside_interface
                        P2P_PREFIX_SIZE = 31
                        ip_status = Status.objects.get_for_model(Device).get(slug="active")
                        prefix = Prefix.objects.filter(site=self.site, role__name=f"{dc_code}_leaf_peer_p2p").first()
                        first_avail = prefix.get_first_available_prefix()
                        subnet = list(first_avail.subnet(P2P_PREFIX_SIZE))[0]
                        Prefix.objects.create(prefix=str(subnet))
                        # Create IP Addresses on both sides
                        ip1 = IPAddress.objects.create(address=f"{str(subnet[0])}/31", assigned_object=intf1, status=ip_status)
                        ip2 = IPAddress.objects.create(address=f"{str(subnet[1])}/31", assigned_object=intf2, status=ip_status)
                        self.log_success(message=f"Created a IP Addresses {ip1} & {ip2} between {intf1.device.name}::{intf1} and {intf2.device.name}::{intf2}")