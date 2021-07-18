from django.utils.text import slugify

from nautobot.dcim.models import Site, Device, Rack, Region, Cable, DeviceRole, DeviceType, Interface
from nautobot.ipam.models import Role, Prefix, IPAddress
from nautobot.extras.models import CustomField, Job, Status
from nautobot.extras.jobs import Job, StringVar, IntegerVar, ObjectVar
from nautobot.circuits.models import Provider, CircuitType, Circuit, CircuitTermination

class CreateAristaPod(Job):
    """Job to create a new site and datacenter pod."""

    class Meta:
        """Meta class for CreateAristaPod."""

        name = "Create a POD"
        description = """
        Create a new Site  with 2 Spine and N leaf switches.
        A new /21 will automatically be allocated from the 'POD Global Pool' Prefix
        """
        label = "POD"
        field_order = [
            "region",
            "pod_code",
            "leaf_count",
        ]

    region = ObjectVar(model=Region)

    pod_code = StringVar(description="Name of the new Pod", label="Pod")

    leaf_count = IntegerVar(description="Number of Leaf Switch", label="Leaf switches count", min_value=1, max_value=4)

    def run(self, data=None, commit=None):
        """Main function for CreatePop."""
        self.devices = {}

        # ----------------------------------------------------------------------------
        # Initialize the database with all required objects
        # ----------------------------------------------------------------------------
        # create_custom_fields()
        # create_relationships()
        # create_prefix_roles()

        # ----------------------------------------------------------------------------
        # Find or Create Site
        # ----------------------------------------------------------------------------
        pod_code = data["pod_code"].lower()
        region = data["region"]
        site_status = Status.objects.get_for_model(Site).get(slug="active")
        self.site, created = Site.objects.get_or_create(name=pod_code, region=region, slug=pod_code, status=site_status)
        self.site.custom_field_data["site_type"] = "POD"
        self.site.save()
        self.log_success(self.site, f"Site {pod_code} successfully created")
        
        # Reference Vars
        TOP_LEVEL_PREFIX_ROLE = "pod"
        SITE_PREFIX_SIZE = "24"    
        RACK_HEIGHT = "42"
        RACK_TYPE = "4-post-frame"
        # ROLES Reference
        ROLES = {}
        # ROLES["spine"]["count"] = "2"
        ROLES["leaf"]["nbr"] = data["leaf_count"]

        # ----------------------------------------------------------------------------
        # Allocate Prefixes for this POP
        # ----------------------------------------------------------------------------
        # Search if there is already a POP prefix associated with this side
        # if not search the Top Level Prefix and create a new one
        pod_role, _ = Role.objects.get_or_create(name=pod_code, slug=pod_code)
        container_status = Status.objects.get_for_model(Prefix).get(slug="container")
        pod_prefix = Prefix.objects.filter(site=self.site, status=container_status, role=pod_role).first()

        if not pod_prefix:
            top_level_prefix = Prefix.objects.filter(
                role__slug=slugify(TOP_LEVEL_PREFIX_ROLE), status=container_status
            ).first()

            if not top_level_prefix:
                raise Exception("Unable to find the top level prefix to allocate a Network for this site")

            first_avail = top_level_prefix.get_first_available_prefix()
            prefix = list(first_avail.subnet(SITE_PREFIX_SIZE))[0]
            pod_prefix = Prefix.objects.create(prefix=prefix, site=self.site, status=container_status, role=pod_role)

        iter_subnet = IPv4Network(str(pod_prefix.prefix)).subnets(new_prefix=21)

        # Allocate the subnet by block of /21
        underlay_p2p = next(iter_subnet)
        overlay_loopback = next(iter_subnet)
        vtep_loopback = next(iter_subnet)
        mlag_leaf_l3 = next(iter_subnet)
        mlag_peer = next(iter_subnet)

        pod_role, _ = Role.objects.get_or_create(name=pod_code, slug=pod_code)

        
        underlay_role, _ = Role.objects.get_or_create(name=f"{pod_code}_underlay", slug=f"{pod_code}_underlay")
        Prefix.objects.get_or_create(
            prefix=str(underlay_p2p), site=self.site, role=underlay_role, status=container_status
        )

        overlay_role, _ = Role.objects.get_or_create(name=f"{pod_code}_overlay", slug=f"{pod_code}_overlay")
        Prefix.objects.get_or_create(prefix=str(overlay_loopback), site=self.site, role=overlay_role, status=container_status)

        vtep_role, _ = Role.objects.get_or_create(name=f"{pod_code}_vtep_loopback", slug=f"{pod_code}_vtep_loopback")
        Prefix.objects.get_or_create(
            prefix=str(vtep_loopback),
            site=self.site,
            role=vtep_role,
        )

        mlag_leaf_l3_role, _ = Role.objects.get_or_create(name=f"{pod_code}_mlag_leaf_l3", slug=f"{pod_code}_mlag_leaf_l3")
        Prefix.objects.get_or_create(
            prefix=str(mlag_leaf_l3),
            site=self.site,
            role=mlag_leaf_l3_role,
        )

        mlag_peer_role, _ = Role.objects.get_or_create(name=f"{pod_code}_mlag_peer", slug=f"{pod_code}_mlag_peer")
        Prefix.objects.get_or_create(
            prefix=str(mlag_peer),
            site=self.site,
            role=mlag_peer_role,
        )

        # ----------------------------------------------------------------------------
        # Create Racks
        # ----------------------------------------------------------------------------
        rack_status = Status.objects.get_for_model(Rack).get(slug="active")
        for i in range(1, ROLES["leaf"]["nbr"] + 1):
            rack_name = f"{pod_code}-{100 + i}"
            rack = Rack.objects.get_or_create(
                name=rack_name, site=self.site, u_height=RACK_HEIGHT, type=RACK_TYPE, status=rack_status
            )

        # ----------------------------------------------------------------------------
        # Create Devices
        # ----------------------------------------------------------------------------
        for role, data in ROLES.items():
            for i in range(1, data.get("nbr", 2) + 1):

                rack_name = f"{pod_code}-{100 + i}"
                rack = Rack.objects.filter(name=rack_name, site=self.site).first()

                device_name = f"{pod_code}-{role}-{i:02}"

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

                # Generate Loopback0 interface and assign Loopback0 address
                loopback0_intf = Interface.objects.create(
                    name="Loopback0", type=InterfaceTypeChoices.TYPE_VIRTUAL, device=device
                )

                loopback0_prefix = Prefix.objects.get(
                    site=self.site,
                    role__name="overlay_role",
                )

                available_ips = loopback0_prefix.get_available_ips()
                lo0_address = list(available_ips)[0]
                loopback0_ip = IPAddress.objects.create(address=str(lo0_address), assigned_object=loopback0_intf)
                

                # Generate Loopback1 interface and assign Loopback1 address
                loopback1_intf = Interface.objects.create(
                    name="Loopback1", type=InterfaceTypeChoices.TYPE_VIRTUAL, device=device
                )

                loopback1_prefix = Prefix.objects.get(
                    site=self.site,
                    role__name="vtep_role",
                )

                available_ips = loopback1_prefix.get_available_ips()
                lo1_address = list(available_ips)[0]
                loopback1_ip = IPAddress.objects.create(address=str(lo1_address), assigned_object=loopback1_intf)

                # Assign Role to Interfaces
                intfs = iter(Interface.objects.filter(device=device))
                for int_role, cnt in data["interfaces"]:
                    for i in range(0, cnt):
                        intf = next(intfs)
                        intf._custom_field_data = {"role": int_role}
                        intf.save()

    def create_p2p_link(self, intf1, intf2):
        """Create a Point to Point link between 2 interfaces.

        This function will:
        - Connect the 2 interfaces with a cable
        - Generate a new Prefix from a "point-to-point" container associated with this site
        - Assign one IP address to each interface from the previous prefix
        """
        P2P_PREFIX_SIZE = "31"
        if intf1.cable or intf2.cable:
            self.log_warning(
                message=f"Unable to create a P2P link between {intf1.device.name}::{intf1} and {intf2.device.name}::{intf2}"
            )
            return False

        status = Status.objects.get_for_model(Cable).get(slug="connected")
        cable = Cable.objects.create(termination_a=intf1, termination_b=intf2, status=status)
        cable.save()

        # Find Next available Network
        prefix = Prefix.objects.filter(site=self.site, role__name="underlay_p2p").first()
        first_avail = prefix.get_first_available_prefix()
        subnet = list(first_avail.subnet(P2P_PREFIX_SIZE))[0]

        Prefix.objects.create(prefix=str(subnet))

        # Create IP Addresses on both sides
        ip1 = IPAddress.objects.create(address=str(subnet[0]), assigned_object=intf1)
        ip2 = IPAddress.objects.create(address=str(subnet[1]), assigned_object=intf2)


