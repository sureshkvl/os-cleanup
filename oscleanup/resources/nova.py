from resources.base import NovaResource
from novaclient import client


class Servers(NovaResource):

    def __init__(self, options):
        super(Servers, self).__init__(options)
        try:
            self.servers = self.nc.servers.list(
                search_opts={"all_tenants": 1,
                             "project_id": self.options.tenant_id}
                )
            for server in self.servers:
                self.data.append({"id": server.id, "name": server.name})

        except Exception, arg:
            print("Exception in listing servers..Exiting %s " % arg)
            exit()

    def delete(self, id):
        pass
