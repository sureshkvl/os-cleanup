from commands.base import BaseCommand
from resources.neutron import Networks, Subnets, Ports, Routers
from resources.nova import Servers
import json


class ListNetworks(BaseCommand):

    FIELDS = ['id', 'name', 'status', 'router:external', 'subnets', 'shared']
    name = "list_networks"

    def __init__(self, options):
        m = Networks(options)
        if not options.args:
            self.result = m.list()
        else:
            self.result = m.find(**json.loads(options.args))
        self.print_table(self.result, self.FIELDS)
        self.write_json_file(self.result)


class ListSubnets(BaseCommand):
    FIELDS = ['id', 'name', 'network_id', 'cidr']
    name = "list_subnets"

    def __init__(self, options):
        m = Subnets(options)
        if not options.args:
            self.result = m.list()
        else:
            self.result = m.find(**json.loads(options.args))
        self.print_table(self.result, self.FIELDS)
        self.write_json_file(self.result)


class ListPorts(BaseCommand):
    FIELDS = ['id', 'network_id', 'fixed_ips', 'device_owner', 'device_id']
    name = "list_ports"

    def __init__(self, options):
        m = Ports(options)
        if not options.args:
            self.result = m.list()
        else:
            self.result = m.find(**json.loads(options.args))
        self.print_table(self.result, self.FIELDS)
        self.write_json_file(self.result)


class ListRouters(BaseCommand):
    FIELDS = ['id', 'name', 'status', 'external_gateway_info']
    name = "list_routers"

    def __init__(self, options):
        m = Routers(options)
        if not options.args:
            self.result = m.list()
        else:
            self.result = m.find(**json.loads(options.args))
        self.print_table(self.result, self.FIELDS)
        self.write_json_file(self.result)


class DeleteNetworks(BaseCommand):

    name = "delete_networks"

    def __init__(self, options):
        m = Networks(options)
        if not options.args:
            self.result = m.list()
        else:
            self.result = m.find(**json.loads(options.args))
        # delete
        for net in self.result:
            m.delete(net.get('id'))
            print 'Deleting Network {} ID {}'.format(
                net.get('name'), net.get('id'))


class DeleteSubnets(BaseCommand):

    name = "delete_subnets"

    def __init__(self, options):
        m = Subnets(options)
        if not options.args:
            self.result = m.list()
        else:
            self.result = m.find(**json.loads(options.args))
            # delete
        for snet in self.result:
            m.delete(snet.get('id'))
            print 'Deleting Subnet {} ID {}'.format(
                snet.get('name'), snet.get('id'))


class DeletePorts(BaseCommand):

    name = "delete_ports"

    def __init__(self, options):
        m = Ports(options)
        if not options.args:
            self.result = m.list()
        else:
            self.result = m.find(**json.loads(options.args))

        for port in self.result:
            m.delete(port.get('id'))
            print 'Deleting Port {} ID {}'.format(
                port.get('name'), port.get('id'))


class DeleteRouters(BaseCommand):
    FIELDS = ['id', 'name', 'status', 'external_gateway_info']
    name = "delete_routers"

    def __init__(self, options):
        m = Routers(options)
        if not options.args:
            self.result = m.list()
        else:
            self.result = m.find(**json.loads(options.args))

        # delete
        for rtr in self.result:
            m.delete(rtr.get('id'))
            print 'Deleting Router {} ID {}'.format(
                rtr.get('name'), rtr.get('id'))


class InspectNetworks(BaseCommand):

    FIELDS = ['id', 'name', 'status', 'router:external', 'subnets', 'shared']
    name = "inspect_networks"

    def __init__(self, options):
        m = Networks(options)
        s = Subnets(options)
        p = Ports(options)
        r = Routers(options)
        v = Servers(options)
        result = []
        if not options.args:
            self.netlist = m.list()
        else:
            self.netlist = m.find(**json.loads(options.args))
        self.print_table(self.netlist, self.FIELDS)
        # Iterate network list
        for net in self.netlist:
            s_node, p_node, r_node = None, None, None
            net_node = self.populate_net_node(net)
            # find the subnets associated for the network, and iterate it
            for subnet in s.find(**{"network_id": net.get('id')}):
                s_node = self.populate_subnet_node(subnet)
                # find the ports associated for the subnet , and iterate it
                for port in p.find(**{"fixed_ips": subnet.get('id')+"*"}):
                    p_node = self.populate_port_node(port)
                    if "router" in port.get('device_owner'):
                        # find the routers associated for the ports
                        for rtr in r.find(**{"id": port.get('device_id')}):
                            r_node = self.populate_router_node(rtr)
                            self.add_child_node(p_node, r_node)
                    elif "nova" in port.get('device_owner'):
                        # find the vms associated for the ports
                        for server in v.find(**{"id": port.get('device_id')}):
                            v_node = self.populate_server_node(server)
                            self.add_child_node(p_node, v_node)
                        # pass
                    else:
                        pass
                    self.add_child_node(s_node, p_node)
                self.add_child_node(net_node, s_node)
            if s_node and p_node and r_node:
                net_node["details"] = "subnets, ports, routers associated"
                net_node["status"] = "complete"
                self.print_info_tree(net_node)
            else:
                net_node["status"] = "incomplete"
                net_node["details"] = "subnets or ports or routers not associated"
                self.print_warn_tree(net_node)
            print "\n"
            result.append(net_node)
        self.write_json_file(result)


class PurgeNetworks(BaseCommand):
    name = "purge_networks"

    def __init__(self, options):
        m = Networks(options)
        s = Subnets(options)
        p = Ports(options)
        r = Routers(options)
        v = Servers(options)
        result = []
        if not options.args:
            self.netlist = m.list()
        else:
            self.netlist = m.find(**json.loads(options.args))
        # Iterate network list
        for net in self.netlist:
            s_node, p_node, r_node = None, None, None
            # find the subnets associated for the network, and iterate it
            for subnet in s.find(**{"network_id": net.get('id')}):
                # find the ports associated for the subnet , and iterate it
                for port in p.find(**{"fixed_ips": subnet.get('id')+"*"}):
                    if "router" in port.get('device_owner'):
                        # find the routers associated for the ports
                        for rtr in r.find(**{"id": port.get('device_id')}):
                            r.remove_interface(rtr.get('id'),port.get('id'))
                            r.delete(rtr.get('id'))
                    elif "nova" in port.get('device_owner'):
                        # find the vms associated for the ports
                        for server in v.find(**{"id": port.get('device_id')}):
                            v.delete(server.get('id'))
                    else:
                        pass
            m.delete(net.get('id'))




class InspectRouters(BaseCommand):

    FIELDS = ['id', 'name', 'status', 'external_gateway_info']
    name = "inspect_routers"

    def populate_subnet_node(self, port):
        params = port.get("fixed_ips")
        return self.populate_node(self.format_node("Subnet", **params[0]))

    def populate_port_node(self, port):
        params = {
                  "id": port.get('id'),
                  "device_owner": port.get('device_owner')
                  }
        return self.populate_node(self.format_node("Port", **params))

    def __init__(self, options):
        m = Networks(options)
        s = Subnets(options)
        p = Ports(options)
        r = Routers(options)
        v = Servers(options)
        result = []
        if not options.args:
            self.rtrlist = r.list()
        else:
            self.rtrlist = r.find(**json.loads(options.args))

        self.print_table(self.rtrlist, self.FIELDS)
        self.portlist = p.list()
        # Iterate Router List
        for rtr in self.rtrlist:
            s_node, p_node, r_node = None, None, None
            r_node = self.populate_router_node(rtr)
            # find the directly connected ports in this router
            for port in p.find(**{"device_id": rtr.get('id')}):
                p_node = self.populate_port_node(port)
                s_node = self.populate_subnet_node(port)
                # Networks
                for net in m.find(**{"id": port.get('network_id')}):
                    n_node = self.populate_net_node(net)
                    self.add_child_node(s_node, n_node)
                self.add_child_node(p_node, s_node)
                self.add_child_node(r_node, p_node)
            self.print_info_tree(r_node)
