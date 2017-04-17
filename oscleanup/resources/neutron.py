from resources.base import NeutronResource
# from neutronclient.v2_0 import client


class Networks(NeutronResource):

    def __init__(self, options):
        super(Networks, self).__init__(options)
        try:
            self.data = self.nc.list_networks(tenant_id=self.options.tenant_id)
            self.data = self.data['networks']

        except Exception, arg:
            print("Exception in listing networks..Exiting %s " % arg)
            exit()

    def delete(self, id):
        try:
            self.nc.delete_network(id)
        except Exception, arg:
            print("Exception in deleting networks..%s " % arg)


class Subnets(NeutronResource):

    def __init__(self, options):
        super(Subnets, self).__init__(options)
        try:
            self.data = self.nc.list_subnets(tenant_id=self.options.tenant_id)
            self.data = self.data['subnets']
        except Exception, arg:
            print("Exception in listing subnets..Exiting %s " % arg)
            exit()

    def delete(self, id):
        try:
            self.nc.delete_subnet(id)
        except Exception, arg:
            print("Exception in deleting router..%s " % arg)


class Ports(NeutronResource):

    def __init__(self, options):
        super(Ports, self).__init__(options)
        try:
            self.data = self.nc.list_ports(tenant_id=self.options.tenant_id)
            self.data = self.data['ports']
            self.ports_not_mapped_with_devices = [n.get("id")
                                                  for n in self.data
                                                  if not n.get("device_owner")]
        except Exception, arg:
            print("Exception in listing ports..Exiting %s " % arg)
            exit()

    def delete(self, id):
        try:
            self.nc.delete_port(id)
        except Exception, arg:
            print("Exception in deleting port..%s " % arg)


class Routers(NeutronResource):

    def __init__(self, options):
        super(Routers, self).__init__(options)
        try:
            self.data = self.nc.list_routers(tenant_id=self.options.tenant_id)
            self.data = self.data['routers']
        except Exception, arg:
            print("Exception in listing routers..Exiting %s " % arg)
            exit()

    def delete(self, id):
        try:
            self.nc.delete_router(id)
        except Exception, arg:
            print("Exception in deleting router..%s " % arg)
