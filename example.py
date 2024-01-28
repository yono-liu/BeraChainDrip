# -*- coding: utf-8 -*-
# Time     :2024/1/25 01:21
# Author   :ttty
# File     :example.py

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools

# 创建钱包
account = Account.create()
# account = Account.from_key('')
logger.debug(f'address:{account.address}')
logger.debug(f'key:{account.key.hex()}')

# TODO 填写你的 client key
yes_captcha_client_key = ''
# bera = BeraChainTools(private_key=account.key, client_key=yes_captcha_client_key,solver_provider='yescaptcha',rpc_url='https://rpc.ankr.com/berachain_testnet')
bera = BeraChainTools(private_key=account.key, client_key=yes_captcha_client_key, solver_provider='ez-captcha',rpc_url='https://rpc.ankr.com/berachain_testnet')


# 领水
result = bera.claim_bera()
logger.debug(result.text)
