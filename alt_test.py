from faker import Faker
import requests
import json
import random
import time
from typing import Union
from requests import Response


user_agent = Faker().chrome()
url = "https://airdrop.altlayer.io/"
headers = {
    # 'content-type': 'text/plain;charset=UTF-8',
        'next-action': '6817e8f24aae7e8aed1d5226e9b368ab8c1ded5d', 
        'user-agent': user_agent}
wallet_address = "0x8e0524B9960112351c9680C3346aFfDC5b19052a"
params = f'["{wallet_address}"]'
# if proxies is not None:
#     proxies = {"http": f"http://{proxies}", "https": f"http://{proxies}"}
response = requests.post(url, params=params,
                            headers=headers, data=params, proxies=None)

print(response.status_code)
print(response.text)
print(response.request.body)