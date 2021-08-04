from django.utils.text import slugify
from nautobot.tenancy.models import Tenant
from nautobot.dcim.models import Site, Device, Interface
from nautobot.ipam.models import Role, Prefix, IPAddress, VLAN, VRF, RouteTarget
from nautobot.extras.models import CustomField, Job, Status
from nautobot.extras.jobs import Job, StringVar, IntegerVar, ObjectVar, BooleanVar, MultiObjectVar

class VxLan_Tenant_Turnup(Job):

    class Meta:
        name = "Provision new VxLan Tenant"
        description = "Creates New Tenant with VRFs, RDs, RTs, and vLans"
        field_order = ['site_name", "leaf_switches', 'tenant_name', 'vrf_rd', 'vrf_rt', 'vlan_vid', 'vlan_rt', 'svi_description', 'virtual_ip']


    site_name = ObjectVar(
        description = "Choose the site to turn up new Tenant",
        model = Site,
        query_params = {
            'site_name': '$site'
        }
    )

    leaf_switches = MultiObjectVar(
        description = "Select the Leaf switches to provision SVI interfaces for VxLan",
        model = Device,
        query_params={
            'device_id': '$device'
        }
    )

    tenant_name = StringVar(
        description = "New Tenant name"
    )

    vrf_rd = IntegerVar(
        description = "VRF Route Distinguisher"
    )

    vrf_rt = StringVar(
        description = "Route target value (formatted in accordance with RFC 4360)"
    )

    vlan_vid = IntegerVar(
        description = "vLan number for new Tenant"
    )

    vlan_rt = IntegerVar(
        description = "Route Target to be assigned to this vLan"
    )

    svi_description = StringVar(
        description = "SVI interface description"
    )

    virtual_ip = StringVar(
        description = "SVI Virtual IP address"
    )

    def run(self, data, commit):
        STATUS_ACTIVE = Status.objects.get(slug='active')

        site = Site.objects.get(name=data['site_name'])
        # Create the New tenant
        try:
            tenant = Tenant.objects.get(name=data['tenant_name'])
            if not tenant:
                tenant = Tenant.objects.get_or_create(
                    name=data['tenant_name'],
                    slug=slugify(data['tenant_name'])
                )
                tenant.validated_save()
                self.log_success(obj=tenant, message=f"Created {data['tenant_name']} as new tenant")
        except Exception:
            pass

        # Create Route Target for VRF
        try:
            route_target = RouteTarget.objects.get(name=data['vrf_rt'])

            if not route_target:
                route_target = RouteTarget.objects.get_or_create(
                    name=data['vrf_rt'],
                    tenant=tenant,
                )
                route_target.validated_save()
                self.log_success(obj=route_target, message=f"Created new Route Target {data['vrf_rt']}")
        except Exception:
            pass
        
        # Create the VRF
        try:
            vrf = VRF.objects.create(
                name=data['tenant_name'],
                rd=data['vrf_rd'],
            )
            vrf.import_targets.set([route_target])
            vrf.export_targets.set([route_target])
            vrf.validated_save()
            self.log_success(obj=vrf, message=f"Created new VRF {data['tenant_name']}")
        except Exception:
            vrf = VRF.objects.get(name=data['tenant_name'])

        # Create VLAN Role
        try:
            vxlan_role = Role.objects.get_or_create(
                name="VXLAN",
                slug=slugify("VXLAN"),
            )
            vxlan_role.validated_save()
        except Exception:
            vxlan_role = Role.objects.get(name="VXLAN")

        # Create VLAN
        try:
            vlan_name = data['tenant_name'].upper()
            vlan = VLAN.objects.get_or_create(
                name=f"{vlan_name}_VLAN_{data['vlan_vid']}",
                vid=data['vlan_vid'],
                role=vxlan_role,
                _custom_field_data={"vxlan_vlan_rt": data['vlan_rt']},
                tenant=tenant,
                status=STATUS_ACTIVE,
                site=site,
            )
            vlan.validated_save()
            self.log_success(obj=vlan, message=f"Created new vlan {vlan_name}_VLAN_{data['vlan_vid']}")
        except Exception:
            vlan = VLAN.objects.get(name=f"{vlan_name}_VLAN_{data['vlan_vid']}")

        # Create SVI on Devices
        for dev in data['leaf_switches']:
            device = Device.objects.get(name=dev)

            svi = Interface.objects.get_or_create(
                name=f"Vlan{data['vlan_vid']}",
                type="virtual",
                enabled=True,
                label="Layer3",
                description=data['svi_description'],
                _custom_field_data={"role": "vxlan", "vxlan_vlan_vni": data['vlan_rt']},
                device=device,
            )
            self.log_success(obj=svi, message=f"Created new SVI Interface Vlan{data['vlan_vid']} on {dev}")
        
            # Create Virtual IP address and assign it to the SVI
            interface = Interface.objects.get(name=f"Vlan{data['vlan_vid']}", device=device)
            virtual_ip = IPAddress.objects.create(
                address=data['virtual_ip'],
                assigned_object=interface,
                vrf=vrf,
                role="anycast",
                description=f"{dev}::{interface}",
                status=STATUS_ACTIVE
            )
            self.log_success(message=f"Assigned IP::{data['virtual_ip']} to {interface} on {dev}")