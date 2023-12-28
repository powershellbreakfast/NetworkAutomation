from pprint import pprint
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import logging

logging.basicConfig(filename='netmiko_global.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

USERNAME = "admin"

PASSWORDLIST = [
        "password1",
        "password2"
    ]

SWITCHIPLIST = [
   "1.1.1.1",
   "2.2.2.2",
   "3.3.3.3"
]


def send_show_command(device, commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command, read_timeout=10)
                result[command] = output
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


for IP in SWITCHIPLIST:
    for PASS in PASSWORDLIST:
        device = {
            "device_type": "cisco_s300_telnet",
            "host": IP,
            "username": USERNAME,
            "password": PASS,
            "secret": PASS,
        }
        print(f"IP:{IP}\nPASS:{PASS}")
        result = send_show_command(device, ["show logging"])
        pprint(result, width=120)

print("Done!")
