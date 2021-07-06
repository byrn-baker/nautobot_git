from django.utils.text import slugify

from nautobot.dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site, Region, Racks
from nautobot.extras.models import Status
from nautobot.extras.jobs import *


class NewBranch(Job):

    class Meta:
        name = "New Pod"
        description = "Provision a new pod"
        field_order = ['region', 'site_name', 'relay_rack', 'underlay_p2p_network_summary', 'overlay_loopback_network_summary', 'vtep_loopback_network_summary', 'mlag_leaf_peer_l3', 'mlag_peer', '_peer_groups', 'spine_switch_count', 'spine_bgp_as', 'leaf_bgp_as_range', 'leaf_switch_count', 'tor_switch_count']
    
    region = ObjectVar(
        description="Choose Region",
        model=Region,
        query_params={
            'region_id': '$region'
        }
        required=False
    )

    site_name = StringVar(
        description="Name of the new pod"
    )

    site_asn = StringVar(
        description="BGP Autonomous System Number (ASN)"
    )
    router_count = IntegerVar(
        description="Number of routers to create"
    )
    core_switch_count = IntegerVar(
        description="Number of core switches to create"
    )
    access_switch_count = IntegerVar(
        description="Number of access switches to create"
    )
    manufacturer = ObjectVar(
        model=Manufacturer,
        required=False
    )
    router_model = ObjectVar(
        description="vios_router",
        model=DeviceType,
        query_params={
            'manufacturer_id': '$manufacturer'
        }
    )
    switch_model = ObjectVar(
        description="vios_switch",
        model=DeviceType,
        query_params={
            'manufacturer_id': '$manufacturer'
        }
    )

    def run(self, data, commit):
        STATUS_PLANNED = Status.objects.get(slug='planned')

        # Create the new site
        site = Site(
            name=data['site_name'],
            slug=slugify(data['site_name']),
            asn=data['site_asn'],
            status=STATUS_PLANNED,
        )
        site.validated_save()
        self.log_success(obj=site, message="Created new site")
        
        # Create router
        router_role = DeviceRole.objects.get(name='pod_router')
        for i in range(1, data['router_count'] + 1):
            switch = Device(
                device_type=data['router_model'],
                name=f'{site.slug}r{i}',
                site=site,
                status=STATUS_PLANNED,
                device_role=router_role
            )
            switch.validated_save()
            self.log_success(obj=switch, message="Created new Router")

        # Create core switches
        core_switch_role = DeviceRole.objects.get(name='pod_core_switch')
        for i in range(1, data['core_switch_count'] + 1):
            switch = Device(
                device_type=data['switch_model'],
                name=f'{site.slug}csw{i}',
                site=site,
                status=STATUS_PLANNED,
                device_role=core_switch_role
            )
            switch.validated_save()
            self.log_success(obj=switch, message="Created new core switch")

        # Create access switches
        access_switch_role = DeviceRole.objects.get(name='pod_access_switch')
        for i in range(1, data['access_switch_count'] + 1):
            switch = Device(
                device_type=data['switch_model'],
                name=f'{site.slug}asw{i}',
                site=site,
                status=STATUS_PLANNED,
                device_role=access_switch_role
            )
            switch.validated_save()
            self.log_success(obj=switch, message="Created new access switch")

        # Generate a CSV table of new devices
        output = [
            'name,make,model'
        ]
        for switch in Device.objects.filter(site=site):
            attrs = [
                switch.name,
                switch.device_type.manufacturer.name,
                switch.device_type.model
            ]
            output.append(','.join(attrs))

        return '\n'.join(output)