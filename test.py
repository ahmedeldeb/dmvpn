from netmiko import ConnectHandler
cisco = {
   'device_type': 'cisco_ios',
   'host': input("router ip add:"),
   'username': 'admin',
   'password': 'cisco',
   }
ch = ConnectHandler(**cisco)
if ch:
   print("success")

# s = ch.send_command("show running-config | include hostname ")
# s=output.replace("hostname ", "")
# print(s)