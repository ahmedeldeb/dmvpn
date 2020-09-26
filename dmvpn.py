import csv
from jinja2 import Template
from netmiko import ConnectHandler
def network (l):
   interface_configs = ""
   source_file = "router-ports.csv"
   interface_template_file = "router-interface-template.j2"
   with open(interface_template_file) as f:
      interface_template = Template(f.read(), keep_trailing_newline=True)
   with open(source_file) as f:
      reader = csv.DictReader(f)
      for row in reader:
         if l in row.values():
            interface_config = interface_template.render(
               Interface=row[ "Interface" ],
               description=row[ "description" ],
               Ipaddress=row[ "ip" ],
               subnetmask=row[ "subnetmask" ],
            )
            interface_configs += interface_config
   with open("%s interface_configs.txt" % l.rstrip(), "w") as f:
      f.write(interface_configs)
   return  interface_configs

def sroute(l):
   internet_configs = ""
   source_file = "book1.csv"
   internet_template_file = "sroute.j2"
   with open(internet_template_file) as f:
      internet_template = Template(f.read(), keep_trailing_newline=True)
   with open(source_file) as f:
      reader = csv.DictReader(f)
      for row in reader:
         if l in row.values():
            internet_config = internet_template.render(
               ip=row[ "ip" ],
               nip=row[ "nip" ],
            )
            internet_configs += internet_config
   with open("%s interface_configs.txt" % l.rstrip(), "a") as f:
      f.write(internet_configs)
   return  internet_configs

def tunnel(l):
   if l == 'Cbtme-Hub':
      b = [
            'int tunnel 1',
            'ip add 192.168.200.1 255.255.255.0',
            'tunnel source 110.110.110.1',
            'tunnel mode gre multipoint',
            'ip nhrp network 111',
            'ip nhrp map multicast dynamic',
            'no ip split-horizon eigrp 100',
            'no ip next-hop-self eigrp 100',
            'exi',
            'Router eigrp 100',
            'No au',
            'Net 192.168.200.1 0.0.0.0',
            'Net 1.1.1.1 0.0.0.0',
            'Net 11.11.11.11 0.0.0.0'
           ]
   elif l == 'Cbtme-Spoke1':
      b = [
         'int tunnel 1',
         'ip add 192.168.200.2 255.255.255.0',
         'tunnel source 120.120.120.1',
         'tunnel mode gre multipoint',
         'ip nhrp network 111',
         'ip nhrp map 192.168.200.1 110.110.110.1',
         'ip nhrp nhs 192.168.200.1',
         'ip nhrp map multicast 110.110.110.1',
         'exi',
         'Router eigrp 100',
         'No au',
         'Net 192.168.200.2 0.0.0.0',
         'Net 2.2.2.2 0.0.0.0',
         'Net 22.22.22.22 0.0.0.0'
          ]
   elif l == 'Cbtme-Spoke2':
      b = [
         'int tunnel 1',
         'ip add 192.168.200.3 255.255.255.0',
         'tunnel source 130.130.130.1',
         'tunnel mode gre multipoint',
         'ip nhrp network 111',
         'ip nhrp map 192.168.200.1 110.110.110.1',
         'ip nhrp nhs 192.168.200.1',
         'ip nhrp map multicast 110.110.110.1',
         'exi',
         'Router eigrp 100',
         'No au',
         'Net 192.168.200.3 0.0.0.0',
         'Net 3.3.3.3 0.0.0.0',
         'Net 33.33.33.33 0.0.0.0',
         ]
   with open("%s interface_configs.txt" % l.rstrip(), "a") as f:
      f.writelines(["%s\n" % item  for item in b])
   return b




cisco = {
   'device_type': 'cisco_ios',
   'host': input("router ip add:"),
   'username': 'admin',
   'password': 'cisco',
   }
ch = ConnectHandler(**cisco)
if ch:
   print("success")
s = ch.send_command("show running-config | include hostname ")
s = s.replace(" ","")
s = s.replace("hostname", "")
m = [ network(s), sroute(s) ]
for a in m:
   config_set = a.split("\n")
   output = ch.send_config_set(config_set)
   print(output)
o = ch.send_config_set(tunnel(s))
print(o)




