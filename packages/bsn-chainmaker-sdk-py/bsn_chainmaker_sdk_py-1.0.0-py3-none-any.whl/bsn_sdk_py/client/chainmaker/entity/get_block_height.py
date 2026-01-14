# -*- coding:utf-8 -*-
"""
Chainmaker get block height entity
"""
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.chainmaker.entity.bsn_base import BsnBase


class GetBlockHeight(BsnBase):
    """
    Get block height for Chainmaker
    """
    def __init__(self):
        pass

    def req_body(self):
        """
        Build request body
        :return: request body dict (empty for this request)
        """
        req_body = {}
        return req_body

    def sign(self, body):
        """
        Sign the request
        :param body: request body
        :return: signature (mac)
        """
        sign_str = self.config.user_code + self.config.app_code
        mac = self.config.encrypt_sign.sign(sign_str).decode()
        return mac

    def verify(self, res_data):
        """
        Verify response signature
        :param res_data: response data
        :return: True if signature is valid
        """
        verify_str = str(res_data["header"]["code"]) + res_data["header"]["msg"] + \
                     str(res_data['body']["blockHeight"])
        signature = res_data['mac']
        return self.config.encrypt_sign.verify(verify_str, signature)



