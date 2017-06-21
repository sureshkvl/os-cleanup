# os-cleanup (openstack resource cleanup)

OS Cleanup project helps to view/remove the resources.


## Usecases:
1. User wants to view or remove all the Resources for a specific type.
    Example : Remove all the Networks for a given tenant.
2. User wants to view remove the subset of the Resources  for a specific type.
    Example:  Remove the Networks which has subnet field is empty. or name contains "test"
3. User want to view or remove the Specific Resource with the dependent resources.
    Example:  Network Resource -> subnet  -> Ports  -> Routers/VMS etc
4. Remove all the resources in the tenant.



## Installation:

Install it using virtual environment
Prerequisties:  Python 2.7

1. setup virtualenv
2. clone the os-cleanup repo from github
3. Install it


```
cloud@devstack1:~$ virtualenv os-c
New python executable in /home/cloud/os-c/bin/python
Installing setuptools, pip, wheel...done.
cloud@devstack1:~$ cd os-c/
cloud@devstack1:~/os-c$ . bin/activate
(os-c) cloud@devstack1:~/os-c$ 
(os-c) cloud@devstack1:~/os-c$ git clone https://github.com/sureshkvl/os-cleanup
Cloning into 'os-cleanup'...
remote: Counting objects: 58, done.
remote: Total 58 (delta 0), reused 0 (delta 0), pack-reused 58
Unpacking objects: 100% (58/58), done.
Checking connectivity... done.
(os-c) cloud@devstack1:~/os-c$ cd os-cleanup/
(os-c) cloud@devstack1:~/os-c/os-cleanup$ ls
LICENSE  README.md  oscleanup  requirements.txt  setup.py  tox.ini
(os-c) cloud@devstack1:~/os-c/os-cleanup$ pip install .
Processing /home/cloud/os-c/os-cleanup
....................skipped
(os-c) cloud@devstack1:~/os-c/os-cleanup$
(os-c) cloud@devstack1:~/os-c/os-cleanup$ python oscleanup/main.py 
usage: Neutron Resource Cleanup script [-h] -T TENANT_ID --command
                                       {list_networks,list_subnets,list_ports,list_routers,delete_networks,delete_subnets,delete_ports,delete_routers,inspect_networks,purge_networks,inspect_routers,list_servers}
                                       [--args ARGS]
Neutron Resource Cleanup script: error: argument -T/--tenant-id is required
(os-c) cloud@devstack1:~/os-c/os-cleanup$ 

```

## How to use:

1. Source your openstack creds file(openrc)
2. Run the program as below
    python oscleanup/main.py -T <Tenant ID> --command <command> [--args <args>]
```
(os-c) cloud@devstack1:~/os-c/os-cleanup$ python oscleanup/main.py -T 4f32991ec8c44a4198d5218abd5ba9c7 --command list_networks
INFO:__main__:Neutron script starts with the arguments Namespace(args=None, command='list_networks', tenant_id='4f32991ec8c44a4198d5218abd5ba9c7')
+--------------------------------------+---------------------------------------------------------------------------------------------+--------+-----------------+-------------------------------------------+--------+
| id                                   | name                                                                                        | status | router:external | subnets                                   | shared |
+--------------------------------------+---------------------------------------------------------------------------------------------+--------+-----------------+-------------------------------------------+--------+
| e68c04f1-56f9-4411-991d-5434487002b7 | N1                                                                                          | ACTIVE | False           | [u'1acb3c2b-879c-455f-a4a0-28ddb5278c9d'] | False  |
| 1a2361d4-a78b-4fca-adad-77ea8399506f | snat-si-left_snat_1bb507e8-4d73-4229-9b48-7091e4f02eb0_71466b30-2cda-4730-a076-da31275ef06e | ACTIVE | False           | [u'dfacb593-89e1-46de-ba9c-83c40d7bb4f4'] | False  |
+--------------------------------------+---------------------------------------------------------------------------------------------+--------+-----------------+-------------------------------------------+--------+
```




