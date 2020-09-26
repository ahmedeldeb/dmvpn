import csv
from jinja2 import Template
from netmiko import ConnectHandler
cisco = {
   'device_type': 'cisco_ios',
   'host': input("router ip add:"),
   'username': 'admin',
   'password': 'cisco',
   }

source_file = "router-ports.csv"
interface_template_file = "router-interface-template.j2"

ch = ConnectHandler(**cisco)
if ch:
   print("success")

interface_configs = ""

s = ch.send_command("show running-config | include hostname ")
s = s.replace("hostname ", "")

with open(interface_template_file) as f:
   interface_template = Template(f.read(), keep_trailing_newline=True)
with open(source_file) as f:
   reader = csv.DictReader(f)

   for row in reader:
      if s in row.values():
         interface_config = interface_template.render(
            Interface=row[ "Interface" ],
            description=row[ "description" ],
            Ipaddress=row[ "ip" ],
            subnetmask=row[ "subnetmask" ],
          )
         interface_configs += interface_config
with open("%s interface_configs.txt" % s.rstrip(), "w") as f:
   f.write(interface_configs)

config_set = interface_configs.split("\n")
output = ch.send_config_set(config_set)
print(output)