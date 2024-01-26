# -*- coding: utf-8 -*-
# Time     :2024/1/25 01:21
# Author   :ttty
# File     :example.py
import json
import random
import time
from typing import Union

import requests
from eth_account import Account
from faker import Faker
from requests import Response


class BeraChainTools(object):
    def __init__(self, private_key, client_key='', solver_provider='', rpc_url='https://artio.rpc.berachain.com/'):
        if solver_provider not in ["ez-captcha", ""]:
            raise ValueError("solver_provider must be 'ez-captcha' ")
        self.solver_provider = solver_provider
        self.private_key = private_key
        self.client_key = client_key
        self.rpc_url = rpc_url
        self.fake = Faker()
        self.account = Account.from_key(self.private_key)
        self.session = requests.session()


    def get_ez_captcha_google_token(self) -> Union[bool, str]:
        if self.client_key == '':
            raise ValueError('ez-captcha is null ')
        json_data = {
            "clientKey": self.client_key,
            "task": {"websiteURL": "https://artio.faucet.berachain.com/",
                     "websiteKey": "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH",
                     "type": "ReCaptchaV3TaskProxyless", }, 'appId': '34119'}
        response = self.session.post(url='https://api.ez-captcha.com/createTask', json=json_data).json()
        if response['errorId'] != 0:
            raise ValueError(response)
        task_id = response['taskId']
        time.sleep(5)
        for _ in range(30):
            data = {"clientKey": self.client_key, "taskId": task_id}
            response = requests.post(url='https://api.ez-captcha.com/getTaskResult', json=data).json()
            if response['status'] == 'ready':
                return response['solution']['gRecaptchaResponse']
            else:
                time.sleep(2)
        return False

    def get_solver_provider(self):
        provider_dict = {
            'ez-captcha': self.get_ez_captcha_google_token,
        }
        if self.solver_provider not in list(provider_dict.keys()):
            raise ValueError("solver_provider must be 'yescaptcha' or '2captcha' or 'ez-captcha' ")
        return provider_dict[self.solver_provider]()

    def claim_bera(self, proxies=None) -> Response:
        """
        bera领水
        :param proxies: http代理
        :return: object
        """
        google_token = self.get_solver_provider()
        if not google_token:
            raise ValueError('获取google token 出错')
        user_agent = self.fake.chrome()
        headers = {'authority': 'artio-80085-ts-faucet-api-2.berachain.com', 'accept': '*/*',
                   'accept-language': 'zh-CN,zh;q=0.9', 'authorization': f'Bearer {google_token}',
                   'cache-control': 'no-cache', 'content-type': 'text/plain;charset=UTF-8',
                   'origin': 'https://artio.faucet.berachain.com', 'pragma': 'no-cache',
                   'referer': 'https://artio.faucet.berachain.com/', 'user-agent': user_agent}
        params = {'address': self.account.address}
        # if proxies is not None:
        #     proxies = {"http": f"http://{proxies}", "https": f"http://{proxies}"}
        response = requests.post('https://artio-80085-ts-faucet-api-2.berachain.com/api/claim', params=params,
                                 headers=headers, data=json.dumps(params), proxies=proxies)
        return response

    
