from commands.base import BaseCommand
from resources.neutron import Networks, Subnets, Ports, Routers
from resources.nova import Servers
import json


class ListServers(BaseCommand):

    FIELDS = ['id', 'name']
    name = "list_servers"

    def __init__(self, options):
        m = Servers(options)
        if not options.args:
            self.result = m.list()
        else:
            self.result = m.find(**json.loads(options.args))
        self.print_table(self.result, self.FIELDS)
        self.write_json_file(self.result)
