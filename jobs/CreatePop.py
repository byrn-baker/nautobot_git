class CreatePop(Job):
    """Job to create a new site of type POP."""

    class Meta:
        """Meta class for CreatePop."""

        name = "Create a POP"
        description = """
        Create a new Site of Type POP with 2 Edge Routers and N leaf switches.
        A new /16 will automatically be allocated from the 'POP Global Pool' Prefix
        """
        label = "POP"
        field_order = [
            "region",
            "site_code",
            "leaf_count",
        ]

    region = ObjectVar(model=Region)

    site_code = StringVar(description="Name of the new site", label="Site Code")

    leaf_count = IntegerVar(description="Number of Leaf Switch", label="Leaf switches count", min_value=1, max_value=12)

    def create_p2p_link(self, intf1, intf2):
        """Create a Point to Point link between 2 interfaces.

        This function will:
        - Connect the 2 interfaces with a cable
        - Generate a new Prefix from a "point-to-point" container associated with this site
        - Assign one IP address to each interface from the previous prefix
        """
        if intf1.cable or intf2.cable:
            self.log_warning(
                message=f"Unable to create a P2P link between {intf1.device.name}::{intf1} and {intf2.device.name}::{intf2}"
            )
            return False

        status = Status.objects.get_for_model(Cable).get(slug="connected")
        cable = Cable.objects.create(termination_a=intf1, termination_b=intf2, status=status)
        cable.save()

        # Find Next available Network
        prefix = Prefix.objects.filter(site=self.site, role__name="point-to-point").first()
        first_avail = prefix.get_first_available_prefix()
        subnet = list(first_avail.subnet(P2P_PREFIX_SIZE))[0]

        Prefix.objects.create(prefix=str(subnet))

        # Create IP Addresses on both sides
        ip1 = IPAddress.objects.create(address=str(subnet[0]), assigned_object=intf1)
        ip2 = IPAddress.objects.create(address=str(subnet[1]), assigned_object=intf2)

    def run(self, data=None, commit=None):
        """Main function for CreatePop."""
        self.devices = {}

        # ----------------------------------------------------------------------------
        # Initialize the database with all required objects
        # ----------------------------------------------------------------------------
        create_custom_fields()
        create_relationships()
        create_prefix_roles()

        # ----------------------------------------------------------------------------
        # Find or Create Site
        # ----------------------------------------------------------------------------
        site_code = data["site_code"].lower()
        region = data["region"]
        site_status = Status.objects.get_for_model(Site).get(slug="active")
        self.site, created = Site.objects.get_or_create(
            name=site_code, region=region, slug=site_code, status=site_status
        )
        self.site.custom_field_data["site_type"] = "POP"
        self.site.save()
        self.log_success(self.site, f"Site {site_code} successfully created")

        ROLES["leaf"]["nbr"] = data["leaf_count"]

        # ----------------------------------------------------------------------------
        # Allocate Prefixes for this POP
        # ----------------------------------------------------------------------------
        # Search if there is already a POP prefix associated with this side
        # if not search the Top Level Prefix and create a new one
        pop_role, _ = Role.objects.get_or_create(name="pop")
        container_status = Status.objects.get_for_model(Prefix).get(slug="container")
        pop_prefix = Prefix.objects.filter(site=self.site, status=container_status, role=pop_role).first()

        if not pop_prefix:
            top_level_prefix = Prefix.objects.filter(
                role__slug=slugify(TOP_LEVEL_PREFIX_ROLE), status=container_status
            ).first()

            if not top_level_prefix:
                raise Exception("Unable to find the top level prefix to allocate a Network for this site")

            first_avail = top_level_prefix.get_first_available_prefix()
            prefix = list(first_avail.subnet(SITE_PREFIX_SIZE))[0]
            pop_prefix = Prefix.objects.create(prefix=prefix, site=self.site, status=container_status, role=pop_role)

        iter_subnet = IPv4Network(str(pop_prefix.prefix)).subnets(new_prefix=18)

        # Allocate the subnet by block of /18
        server_block = next(iter_subnet)
        mgmt_block = next(iter_subnet)
        loopback_subnet = next(iter_subnet)
        p2p_subnet = next(iter_subnet)

        pop_role, _ = Role.objects.get_or_create(name="pop")

        # Create Server & Mgmt Block
        server_role, _ = Role.objects.get_or_create(name="server")
        Prefix.objects.get_or_create(
            prefix=str(server_block), site=self.site, role=server_role, status=container_status
        )

        mgmt_role, _ = Role.objects.get_or_create(name="mgmt")
        Prefix.objects.get_or_create(prefix=str(mgmt_block), site=self.site, role=mgmt_role, status=container_status)

        loopback_role, _ = Role.objects.get_or_create(name="loopback")
        Prefix.objects.get_or_create(
            prefix=str(loopback_subnet),
            site=self.site,
            role=loopback_role,
        )

        p2p_role, _ = Role.objects.get_or_create(name="point-to-point")
        Prefix.objects.get_or_create(
            prefix=str(p2p_subnet),
            site=self.site,
            role=p2p_role,
        )

        rel_device_vlan = Relationship.objects.get(name="Device to Vlan")
        rel_rack_vlan = Relationship.objects.get(name="Rack to Vlan")

        # ----------------------------------------------------------------------------
        # Create Racks
        # ----------------------------------------------------------------------------
        rack_status = Status.objects.get_for_model(Rack).get(slug="active")
        for i in range(1, ROLES["leaf"]["nbr"] + 1):
            rack_name = f"{site_code}-{100 + i}"
            rack = Rack.objects.get_or_create(
                name=rack_name, site=self.site, u_height=RACK_HEIGHT, type=RACK_TYPE, status=rack_status
            )

        # ----------------------------------------------------------------------------
        # Create Devices
        # ----------------------------------------------------------------------------
        for role, data in ROLES.items():
            for i in range(1, data.get("nbr", 2) + 1):

                rack_name = f"{site_code}-{100 + i}"
                rack = Rack.objects.filter(name=rack_name, site=self.site).first()

                device_name = f"{site_code}-{role}-{i:02}"

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

                # Generate Loopback interface and assign Loopback
                loopback_intf = Interface.objects.create(
                    name="Loopback0", type=InterfaceTypeChoices.TYPE_VIRTUAL, device=device
                )

                loopback_prefix = Prefix.objects.get(
                    site=self.site,
                    role__name="loopback",
                )

                available_ips = loopback_prefix.get_available_ips()
                address = list(available_ips)[0]
                loopback_ip = IPAddress.objects.create(address=str(address), assigned_object=loopback_intf)

                # Assign Role to Interfaces
                intfs = iter(Interface.objects.filter(device=device))
                for int_role, cnt in data["interfaces"]:
                    for i in range(0, cnt):
                        intf = next(intfs)
                        intf._custom_field_data = {"role": int_role}
                        intf.save()

                if role == "leaf":
                    for vlan_name, vlan_data in VLANS.items():
                        prefix_role = Role.objects.get(slug=vlan_name)
                        vlan = VLAN.objects.create(
                            vid=vlan_data["vlan_id"], name=f"{rack_name}-{vlan_name}", site=self.site, role=prefix_role
                        )
                        vlan_block = Prefix.objects.filter(
                            site=self.site, status=container_status, role=prefix_role
                        ).first()

                        # Find Next available Network
                        first_avail = vlan_block.get_first_available_prefix()
                        subnet = list(first_avail.subnet(24))[0]
                        vlan_prefix = Prefix.objects.create(prefix=str(subnet), vlan=vlan)
                        vlan_prefix.save()

                        intf_name = f"vlan{vlan_data['vlan_id']}"
                        intf = Interface.objects.create(
                            name=intf_name, device=device, type=InterfaceTypeChoices.TYPE_VIRTUAL
                        )

                        # Create IP Addresses on both sides
                        vlan_ip = IPAddress.objects.create(address=str(subnet[0]), assigned_object=intf)

                        RelationshipAssociation.objects.create(
                            relationship=rel_device_vlan,
                            source_type=rel_device_vlan.source_type,
                            source_id=device.id,
                            destination_type=rel_device_vlan.destination_type,
                            destination_id=vlan.id,
                        )

                        RelationshipAssociation.objects.create(
                            relationship=rel_rack_vlan,
                            source_type=rel_rack_vlan.source_type,
                            source_id=rack.id,
                            destination_type=rel_rack_vlan.destination_type,
                            destination_id=vlan.id,
                        )

        # ----------------------------------------------------------------------------
        # Cabling
        # ----------------------------------------------------------------------------
        # Connect Edge Routers Together
        edge_01 = self.devices[f"{site_code}-edge-01"]
        edge_02 = self.devices[f"{site_code}-edge-02"]
        peer_intfs_01 = iter(Interface.objects.filter(device=edge_01, _custom_field_data__role="peer"))
        peer_intfs_02 = iter(Interface.objects.filter(device=edge_02, _custom_field_data__role="peer"))

        for link in range(0, 2):
            self.create_p2p_link(next(peer_intfs_01), next(peer_intfs_02))

        # Connect Edge and Leaf Switches together
        leaf_intfs_01 = iter(Interface.objects.filter(device=edge_01, _custom_field_data__role="leaf"))
        leaf_intfs_02 = iter(Interface.objects.filter(device=edge_02, _custom_field_data__role="leaf"))

        for i in range(1, ROLES["leaf"]["nbr"] + 1):
            leaf_name = f"{site_code}-leaf-{i:02}"
            leaf = self.devices[leaf_name]
            edge_intfs = iter(Interface.objects.filter(device=leaf, _custom_field_data__role="edge"))

            self.create_p2p_link(next(leaf_intfs_01), next(edge_intfs))
            self.create_p2p_link(next(leaf_intfs_02), next(edge_intfs))

        # ----------------------------------------------------------------------------
        # Create Circuits and Connect them
        # ----------------------------------------------------------------------------
        external_intfs_01 = iter(Interface.objects.filter(device=edge_01, _custom_field_data__role="external"))
        external_intfs_02 = iter(Interface.objects.filter(device=edge_02, _custom_field_data__role="external"))

        for provider in TRANSIT_PROVIDERS:
            try:
                provider = Provider.objects.get(name=provider)
            except Provider.DoesNotExist:
                self.log_warning(f"Unable to find Circuit Provider {provider}, skipping")
                continue

            try:
                circuit_type = CircuitType.objects.get(name="Transit")
            except CircuitType.DoesNotExist:
                self.log_warning(f"Unable to find CircuitType 'Transit', skipping")
                continue

            for intfs_list in [external_intfs_01, external_intfs_02]:

                intf = next(intfs_list)

                regex = re.compile("[^a-zA-Z0-9]")
                clean_name = regex.sub("", f"{site_code}{intf.device.name[-4:]}{intf.name[-4:]}")
                circuit_id = slugify(f"{provider.name[0:3]}-{int(clean_name, 36)}")
                circuit, created = Circuit.objects.get_or_create(cid=circuit_id, type=circuit_type, provider=provider)

                self.log_success(circuit, f"Circuit {circuit_id} successfully created")

                if circuit.termination_a:
                    circuit.termination_a.delete()

                ct = CircuitTermination(
                    circuit=circuit,
                    site=self.site,
                    term_side="A",
                )
                ct.save()

                status = Status.objects.get(slug="connected")
                cable = Cable.objects.create(termination_a=intf, termination_b=ct, status=status)