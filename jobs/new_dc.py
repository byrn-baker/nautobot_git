class NewDataCenter(Job, FormEntry):
    """Job to build out a new Datacenter"""

    region = FormEntry.region
    site_name = FormEntry.site
    rack = FormEntry.rack