import requests
from time import sleep
while True:
    response = requests.get("http://pi.afkborn.keenetic.pro/api/v2/altinlar")
    print(response.status_code)
    print(response.elapsed)
    sleep(0.1)