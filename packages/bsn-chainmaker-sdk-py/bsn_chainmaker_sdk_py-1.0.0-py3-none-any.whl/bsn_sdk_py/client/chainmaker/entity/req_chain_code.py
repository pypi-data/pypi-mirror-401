# -*- coding:utf-8 -*-
"""
Chainmaker transaction request entity (Key-Trust Mode)
"""
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.chainmaker.entity.bsn_base import BsnBase
from bsn_sdk_py.until.tools import obj_sort


class ReqChainCode(BsnBase):
    """
    Transaction request for Chainmaker (Key-Trust Mode)
    """
    def __init__(self, userName, contractAddress, funcName, funcParam):
        """
        :param userName: user name
        :param contractAddress: contract address
        :param funcName: function name
        :param funcParam: function parameters (JSON string list format)
        """
        self.userName = userName
        self.contractAddress = contractAddress
        self.funcName = funcName
        self.funcParam = funcParam

    def req_body(self):
        """
        Build request body
        :return: request body dict
        """
        req_body = {
            "userName": self.userName,
            "contractAddress": self.contractAddress,
            "funcName": self.funcName,
            "funcParam": self.funcParam,
        }
        return req_body

    def sign(self, body):
        """
        Sign the request
        :param body: request body
        :return: signature (mac)
        """
        sign_str = self.config.user_code + self.config.app_code + \
                   body['body']["userName"] + body['body']["contractAddress"] + \
                   body['body']["funcName"] + body['body']["funcParam"]
        mac = self.config.encrypt_sign.sign(sign_str).decode()
        return mac

    def verify(self, res_data):
        """
        Verify response signature
        :param res_data: response data
        :return: True if signature is valid
        """
        verify_str = str(res_data["header"]["code"]) + res_data["header"]["msg"] + \
                     obj_sort(res_data['body']["blockInfo"]) + obj_sort(res_data['body']["contractRes"])
        signature = res_data['mac']
        return self.config.encrypt_sign.verify(verify_str, signature)



