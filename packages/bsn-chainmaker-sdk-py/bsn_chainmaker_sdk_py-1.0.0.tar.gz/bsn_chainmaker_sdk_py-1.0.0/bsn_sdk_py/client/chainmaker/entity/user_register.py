# -*- coding:utf-8 -*-
"""
Chainmaker user registration entity (Key-Trust Mode)
"""
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.chainmaker.entity.bsn_base import BsnBase


class UserRegister(BsnBase):
    """
    User registration for Chainmaker (Key-Trust Mode)
    """
    def __init__(self, config: Config, userName):
        """
        :param userName: user name
        """
        self.userName = userName
        self.config = config

    def req_body(self):
        """
        Build request body
        :return: request body dict
        """
        req_body = {
            "userName": self.userName,
        }
        return req_body

    def sign(self):
        """
        Sign the request
        :return: signature (mac)
        """
        sign_str = self.config.user_code + self.config.app_code + self.userName
        mac = self.config.encrypt_sign.sign(sign_str).decode()
        return mac

    def verify(self, res_data):
        """
        Verify response signature
        :param res_data: response data
        :return: True if signature is valid
        """
        verify_str = str(res_data["header"]["code"]) + res_data["header"]["msg"]
        signature = res_data['mac']
        return self.config.encrypt_sign.verify(verify_str, signature)



