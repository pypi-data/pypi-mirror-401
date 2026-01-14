# -*- coding:utf-8 -*-
"""
Chainmaker event register entity
"""
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.chainmaker.entity.bsn_base import BsnBase


class EventRegister(BsnBase):
    """
    Event register for Chainmaker
    """
    def __init__(self, eventType, contractAddress, topic, notifyUrl, attachArgs=''):
        """
        :param eventType: event type (1: block event, 2: contract event)
        :param contractAddress: contract address
        :param topic: event topic
        :param notifyUrl: notification URL
        :param attachArgs: additional arguments
        """
        self.eventType = eventType
        self.contractAddress = contractAddress
        self.topic = topic
        self.notifyUrl = notifyUrl
        self.attachArgs = attachArgs

    def req_body(self):
        """
        Build request body
        :return: request body dict
        """
        req_body = {
            "eventType": self.eventType,
            "contractAddress": self.contractAddress,
            "topic": self.topic,
            "notifyUrl": self.notifyUrl,
            "attachArgs": self.attachArgs,
        }
        return req_body

    def sign(self, body):
        """
        Sign the request
        :param body: request body
        :return: signature (mac)
        """
        sign_str = self.config.user_code + self.config.app_code + \
                   body['body']["eventType"] + body['body']["contractAddress"] + \
                   body['body']["topic"] + body['body']["notifyUrl"] + body['body']["attachArgs"]
        mac = self.config.encrypt_sign.sign(sign_str).decode()
        return mac

    def verify(self, res_data):
        """
        Verify response signature
        :param res_data: response data
        :return: True if signature is valid
        """
        verify_str = str(res_data["header"]["code"]) + res_data["header"]["msg"] + \
                     str(res_data['body']["eventId"])
        signature = res_data['mac']
        return self.config.encrypt_sign.verify(verify_str, signature)



