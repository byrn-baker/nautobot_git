from django.utils.text import slugify
from nautobot.extras.jobs import Job, StringVar, IntegerVar, ObjectVar
from nautobot.dcim.models import Site, Device, Rack, Region, Cable, DeviceRole, DeviceType, Interface 
from nautobot.ipam.models import Role, Prefix, IPAddress

from pynautobot import api

nb = api(url="https://localhost", token="c7fdc6be609a244bb1e851c5e47b3ccd9d990b58")
nb.http_session.verify = False


class CreateSpineLeafPod(Job):
    """Job to create a new site and datacenter pod."""

    class Meta:
        """Meta class for CreateSpineLeafPod."""

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