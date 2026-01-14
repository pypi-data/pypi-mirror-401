# -*- coding:utf-8 -*-
"""
Chainmaker event remove entity
"""
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.chainmaker.entity.bsn_base import BsnBase


class EventRemove(BsnBase):
    """
    Event remove for Chainmaker
    """
    def __init__(self, eventId):
        """
        :param eventId: event ID
        """
        self.eventId = eventId

    def req_body(self):
        """
        Build request body
        :return: request body dict
        """
        req_body = {
            "eventId": self.eventId,
        }
        return req_body

    def sign(self, body):
        """
        Sign the request
        :param body: request body
        :return: signature (mac)
        """
        sign_str = self.config.user_code + self.config.app_code + \
                   body['body']["eventId"]
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



