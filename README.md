# os-cleanup
openstack resource cleanup



python oscleanup/main.py -T 5ff3bceb409c48a58aa8c88c4324c4ad  --command list_networks --arg '{"name":"test*"}'
python oscleanup/main.py -T 5ff3bceb409c48a58aa8c88c4324c4ad  --command list_ports --args '{"network_id":" "}'
python oscleanup/main.py -T 5ff3bceb409c48a58aa8c88c4324c4ad  --command list_networks --args '{"subnets":"[]"}'
python oscleanup/main.py -T 5ff3bceb409c48a58aa8c88c4324c4ad  --command list_routers --args '{"name":"test1"}'

(oscleanup) cloud@dev2:~/oscleanup/os-cleanup$ nova show vm1
+--------------------------------------+----------------------------------------------------------------+
| Property                             | Value                                                          |
+--------------------------------------+----------------------------------------------------------------+
| Net1 network                         | 192.168.1.3                                                    |
| OS-DCF:diskConfig                    | AUTO                                                           |
| OS-EXT-AZ:availability_zone          | nova                                                           |
| OS-EXT-STS:power_state               | 1                                                              |
| OS-EXT-STS:task_state                | -                                                              |
| OS-EXT-STS:vm_state                  | active                                                         |
| OS-SRV-USG:launched_at               | 2017-04-15T13:45:59.000000                                     |
| OS-SRV-USG:terminated_at             | -                                                              |
| accessIPv4                           |                                                                |
| accessIPv6                           |                                                                |
| config_drive                         | True                                                           |
| created                              | 2017-04-15T13:45:50Z                                           |
| description                          | vm1                                                            |
| flavor                               | m1.tiny (1)                                                    |
| hostId                               | cd7380871845dc53ae1a15e2065e10dca926bd5b7df991e8bdcfa258       |
| id                                   | 38a56b74-87a7-4c5d-84cd-22e8280788f3                           |
| image                                | cirros-0.3.4-x86_64-uec (6121a5c3-e761-41e2-aac1-6f99051d2b84) |
| key_name                             | -                                                              |
| locked                               | False                                                          |
| metadata                             | {}                                                             |
| name                                 | vm1                                                            |
| os-extended-volumes:volumes_attached | []                                                             |
| progress                             | 0                                                              |
| security_groups                      | default                                                        |
| status                               | ACTIVE                                                         |
| tenant_id                            | e4874d7f84eb462097f055ceb0d02dbf                               |
| updated                              | 2017-04-15T13:45:59Z                                           |
| user_id                              | 5216e1b8f5a44ff180c504d35e552ad4                               |
+--------------------------------------+----------------------------------------------------------------+


Purge Networks:

1. Delete the VMs associated to the ports(networks)
    - when we delete the VM, the associated ports also removed
If the VM is associated with more than one networks, more than one ports ????????????????

2. Delete the Router:
   remove the interfaces from the router
   neutron router-interface-delete <routerid>  <subnetid>

   neutron clear

If the router is associated with more than one subnets/networks...??????????????????????
   clear the router gateway?
   neutron router-gateway-clear 5358f9b1-be3d-4f87-8a70-0b53632700a2

   remove the router
3. Delete the network
neutron net-delete 3414765a-21f8-4715-8624-03010592adc

4. floating ip ??