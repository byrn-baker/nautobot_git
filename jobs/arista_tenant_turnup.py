from django.utils.text import slugify
from nautobot.dcim.models import Site, Device, Rack, Region, Cable, DeviceRole, DeviceType, Interface
from nautobot.ipam.models import Role, Prefix, IPAddress, VLAN, VRF
from nautobot.extras.models import CustomField, Job, Status
from nautobot.extras.models.customfields import ContentType
from nautobot.extras.jobs import Job, StringVar, IntegerVar, ObjectVar, BooleanVar, MultiObjectVar
from nautobot.circuits.models import Provider, CircuitType, Circuit, CircuitTermination

class VxLan_Tenant_Turnup(Job):

    class Meta:
        name = "Provision new VxLan Tenant"
        description = "Creates New Tenant with VRFs, RDs, RTs, and vLans"


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



    def run(self, data, commit):
        STATUS_ACTIVE = Status.objects.get(slug='active')

        # Create the New tenant