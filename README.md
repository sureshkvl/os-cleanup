# os-cleanup
openstack resource cleanup



python oscleanup/main.py -T 5ff3bceb409c48a58aa8c88c4324c4ad  --command list_networks --arg '{"name":"test*"}'
python oscleanup/main.py -T 5ff3bceb409c48a58aa8c88c4324c4ad  --command list_ports --args '{"network_id":" "}'
python oscleanup/main.py -T 5ff3bceb409c48a58aa8c88c4324c4ad  --command list_networks --args '{"subnets":"[]"}'
python oscleanup/main.py -T 5ff3bceb409c48a58aa8c88c4324c4ad  --command list_routers --args '{"name":"test1"}'