# -*- coding:utf-8 -*-
"""
Chainmaker get block info entity
"""
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.chainmaker.entity.bsn_base import BsnBase
from bsn_sdk_py.until.tools import array_sort


class GetBlockInfo(BsnBase):
    """
    Get block info for Chainmaker
    """
    def __init__(self, blockHeight=0, blockHash=''):
        """
        :param blockHeight: block height (cannot be empty if blockHash is empty)
        :param blockHash: block hash (cannot be empty if blockHeight is empty)
        """
        self.blockHeight = blockHeight
        self.blockHash = blockHash

    def req_body(self):
        """
        Build request body
        :return: request body dict
        """
        req_body = {
            "blockHeight": self.blockHeight,
            "blockHash": self.blockHash,
        }
        return req_body

    def sign(self, body):
        """
        Sign the request
        :param body: request body
        :return: signature (mac)
        """
        sign_str = self.config.user_code + self.config.app_code + \
                   str(body['body']["blockHeight"]) + body['body']["blockHash"]
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
                     str(res_data['body']["preBlockHash"]) + str(res_data['body']["blockSize"]) + \
                     str(res_data['body']["blockTxCount"]) + array_sort(res_data['body']["transactions"]) + \
                     str(res_data['body']["blockData"])
        signature = res_data['mac']
        return self.config.encrypt_sign.verify(verify_str, signature)



