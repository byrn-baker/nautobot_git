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
        tenant = Tenant.objects.get_or_create(
            name=data['tenant_name'],
            slug=slugify(data['tenant_name'])
        )
        if not tenant:
            tenant.validated_save()
            self.log_success(obj=tenant, message=f"Created {data['tenant_name']} as new tenant")

        # Create Route Target for VRF
        route_target = RouteTarget.object.get_or_create(
            name=data['vrf_rt'],
            tenant=tenant,
        )
        route_target.validated_save()
        self.log_success(obj=route_target, message=f"Created new Route Target {data['vrf_rt']}")
        
        # Create the VRF
        vrf = VRF.objects.get_or_create(
            name=data['tenant_name'],
            rd=data['vrf_rd'],
            import_targets=route_target,
            export_targets=route_target,
        )
        vrf.validated_save()
        self.log_success(obj=vrf, message=f"Created new VRF {data['tenant_name']}")

        # Create VLAN Role
        vxlan_role = Role.objects.get_or_create(
            name="VXLAN",
            slug=slugify("VXLAN"),
        )
        vxlan_role.validated_save()

        # Create VLAN
        vlan_name = data['tenant_name']
        vlan = VLAN.objects.get_or_create(
            name=f"{vlan_name.upper}_VLAN_{data['vlan_vid']}",
            vid=data['vlan_vid'],
            role=vxlan_role,
            _custom_field_data={"vxlan_vlan_rt": data['vlan_rt']},
            # tenant=tenant,
            status=STATUS_ACTIVE,
            site=site,
        )
        vlan.validated_save()
        self.log_success(obj=vlan, message=f"Created new vlan {vlan_name.upper}_VLAN_{data['vlan_vid']}")



