import requests
import urllib3
from requests.exceptions import ReadTimeout,ConnectTimeout,ConnectionError


urllib3.disable_warnings()


ip_addresses = [
    "1.1.1.1",
    "8.8.8.8",
    "4.4.4.4"

]



username = "admin"
password = "1stPass2Try"
password2 = "2ndPass2Try"
password3 = "3rdPass2Try"

ip_change = []
ip_reboot = []
ip_timeout = []

def login(ip_address):
    url = f"https://{ip_address}/logincheck"
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = f'username={username}&secretkey={password}'
    response = requests.request("POST", url, headers=headers, data=payload, verify=False, timeout=2)

    if response.status_code == 401:
        payload = f'username={username}&secretkey={password2}'
        response = requests.request("POST", url, headers=headers, data=payload, verify=False, timeout=2)

    if response.status_code == 401:
        payload = f'username={username}&secretkey={password3}'
        response = requests.request("POST", url, headers=headers, data=payload, verify=False, timeout=2)

    print(response.text)

    if response.json()["message"] == "Password force change":
            ip_change.append(ip_address)
            return

    return response.headers["set-cookie"]


    

def reboot(ip_address,cookie):
    url = f"https://{ip_address}/api/v1/reboot"
    headers = {
        'Content-Type': 'application/json',
        'Cookie': cookie 
    }
    response = requests.request("POST", url, headers=headers, data={}, verify=False)
    print(response.text)
    return response.status_code

for ip in ip_addresses:
    print("--------------")
    print(ip)
    try:
        cookie = login(ip)
    except ConnectTimeout as error:
        print(error)
        ip_timeout.append(ip)
    except ReadTimeout as error:
        print(error)
        ip_timeout.append(ip)
    else:
        status = reboot(ip,cookie)
        print(status)

print("###############")
print("IP Addresses that need a change of password")
for ip in ip_change:
    print(ip_change)

print("###############")
print("IP Addresses that timed out")
for ip in ip_timeout:
    print(ip_timeout)

print("###############")
print("IP Addresses that were rebooted")
for ip in ip_reboot:
    print(ip_reboot)