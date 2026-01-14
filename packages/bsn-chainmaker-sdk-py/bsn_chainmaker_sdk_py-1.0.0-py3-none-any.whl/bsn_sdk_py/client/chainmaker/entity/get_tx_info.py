# -*- coding:utf-8 -*-
"""
Chainmaker get transaction info entity
"""
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.chainmaker.entity.bsn_base import BsnBase


class GetTxInfo(BsnBase):
    """
    Get transaction info for Chainmaker
    """
    def __init__(self, txId):
        """
        :param txId: transaction ID
        """
        self.txId = txId

    def req_body(self):
        """
        Build request body
        :return: request body dict
        """
        req_body = {
            "txId": self.txId,
        }
        return req_body

    def sign(self, body):
        """
        Sign the request
        :param body: request body
        :return: signature (mac)
        """
        sign_str = self.config.user_code + self.config.app_code + body['body']["txId"]
        mac = self.config.encrypt_sign.sign(sign_str).decode()
        return mac

    def verify(self, res_data):
        """
        Verify response signature
        :param res_data: response data
        :return: True if signature is valid
        """
        verify_str = str(res_data["header"]["code"]) + res_data["header"]["msg"] + \
                     str(res_data['body']["blockHash"]) + str(res_data['body']["blockHeight"]) + \
                     str(res_data['body']["status"]) + str(res_data['body']["contractAddress"]) + \
                     str(res_data['body']["blockTimestamp"]) + str(res_data['body']["txData"])
        signature = res_data['mac']
        return self.config.encrypt_sign.verify(verify_str, signature)



