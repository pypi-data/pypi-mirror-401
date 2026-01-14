# -*- coding:utf-8 -*-
"""
Chainmaker client for Chainmaker framework
"""
from bsn_sdk_py.client.base_client import BaseClient
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.bsn_enum import AppCaType
from bsn_sdk_py.until.bsn_logger import log_info
from bsn_sdk_py.client.chainmaker.entity import (
    UserRegister, UserEnroll, ReqChainCode, SdkTrans,
    GetTxInfo, GetBlockInfo, GetBlockHeight,
    EventRegister, EventQuery, EventRemove
)


class ChainmakerClient(BaseClient):
    """
    Chainmaker app requests client
    """

    def __init__(self):
        super().__init__()
        self.framework_type = "chainmaker"

    def get_api_base_path(self):
        """
        Get API base path for Chainmaker
        :return: API base path
        """
        return "/api/chainmaker/v1"

    def build_req_data(self, req_body, reqInfo=None):
        """
        Uniformly create the request message for Chainmaker
        According to proto definition, all Chainmaker requests include reqInfo field
        :param req_body: request body
        :param reqInfo: optional request info data (for syschainService.RequestInfoData)
        :return: build result
        """
        data = {
            "header": {
                "userCode": self.config.user_code,
                "appCode": self.config.app_code,
            },
            "body": req_body,
            "mac": "",
        }
        # Add reqInfo if provided (according to proto definition: syschainService.RequestInfoData reqInfo =4)
        if reqInfo is not None:
            data["reqInfo"] = reqInfo
        return data

    def user_register(self, userName):
        """
        User registration (Key-Trust Mode)
        :param userName: user name
        :return: response data
        """
        req_url = self.config.nodeApi + self.get_api_base_path() + "/user/register"
        user_register_obj = UserRegister(self.config, userName)
        req_data = self.build_req_data(user_register_obj.req_body())
        mac = user_register_obj.sign()
        req_data["mac"] = mac
        res_data = self.common_request(req_url, req_data)
        assert user_register_obj.verify(res_data)
        return res_data

    def user_enroll(self, userName):
        """
        User enrollment (Public-Key-Upload Mode)
        :param userName: user name
        :return: response data
        """
        assert self.config.app_info[
            "caType"] == AppCaType.AppCaType_NoTrust.value, "only allow to enroll user under Public-Key-Upload Mode"
        req_url = self.config.nodeApi + self.get_api_base_path() + "/user/enroll"
        user_enroll_obj = UserEnroll(userName)
        user_enroll_obj.set_config(self.config)
        req_data = self.build_req_data(user_enroll_obj.req_body())
        mac = user_enroll_obj.sign()
        req_data["mac"] = mac
        res_data = self.common_request(req_url, req_data)
        assert user_enroll_obj.verify(res_data)
        return res_data

    def req_chain_code(self, userName, contractAddress, funcName, funcParam):
        """
        Transaction processing under Key-Trust Mode
        :param userName: user name
        :param contractAddress: contract address
        :param funcName: function name
        :param funcParam: function parameters (JSON string list format)
        :return: response data
        """
        req_url = self.config.nodeApi + self.get_api_base_path() + "/node/reqChainCode"
        req_chain_code_obj = ReqChainCode(userName, contractAddress, funcName, funcParam)
        req_chain_code_obj.set_config(self.config)
        req_data = self.build_req_data(req_chain_code_obj.req_body())
        mac = req_chain_code_obj.sign(req_data)
        req_data["mac"] = mac
        res_data = self.common_request(req_url, req_data)
        assert req_chain_code_obj.verify(res_data)
        return res_data

    def sdk_trans(self, contractAddress: str, funcName: str, funcParam: list = None, userName: str = None, isQuery: bool=False):
        """
        Transaction under Public-Key-Upload Mode
        :param contractAddress: contract address
        :param funcName: function name
        :param funcParam: function parameters (list format)
        :param userName: user name (required for Public-Key-Upload Mode)
        :return: response data
        """
        req_url = self.config.nodeApi + self.get_api_base_path() + "/node/sdkTrans"
        if userName is None:
            userName = self.config.user_code
        sdk_trans_obj = SdkTrans(contractAddress, funcName, funcParam, userName, isQuery)
        sdk_trans_obj.set_config(self.config)
        req_data = self.build_req_data(sdk_trans_obj.req_body())
        mac = sdk_trans_obj.sign(req_data)
        req_data["mac"] = mac
        # return req_data
        res_data = self.common_request(req_url, req_data)
        assert sdk_trans_obj.verify(res_data)
        return res_data

    def get_tx_info(self, txId):
        """
        Get transaction info
        :param txId: transaction ID
        :return: response transaction information
        """
        req_url = self.config.nodeApi + self.get_api_base_path() + "/node/getTxInfo"
        get_tx_info_obj = GetTxInfo(txId)
        get_tx_info_obj.set_config(self.config)
        req_data = self.build_req_data(get_tx_info_obj.req_body())
        log_info(req_data)
        mac = get_tx_info_obj.sign(req_data)
        req_data["mac"] = mac
        res_data = self.common_request(req_url, req_data)
        log_info(res_data)
        assert get_tx_info_obj.verify(res_data)
        return res_data

    def get_block_info(self, blockHeight=0, blockHash=''):
        """
        Get block info
        :param blockHeight: block height (cannot be empty if blockHash is empty)
        :param blockHash: block hash (cannot be empty if blockHeight is empty)
        :return: response block information
        """
        assert any((
            blockHeight,
            blockHash,
        )), "blockHeight or blockHash cannot be empty at the same time"
        req_url = self.config.nodeApi + self.get_api_base_path() + "/node/getBlockInfo"
        get_block_info_obj = GetBlockInfo(blockHeight, blockHash)
        get_block_info_obj.set_config(self.config)
        req_data = self.build_req_data(get_block_info_obj.req_body())
        mac = get_block_info_obj.sign(req_data)
        req_data["mac"] = mac
        res_data = self.common_request(req_url, req_data)
        assert get_block_info_obj.verify(res_data), "verification failure"
        return res_data

    def get_block_height(self):
        """
        Get the latest block height
        :return: response block height information
        """
        req_url = self.config.nodeApi + self.get_api_base_path() + "/node/getBlockHeight"
        get_block_height_obj = GetBlockHeight()
        get_block_height_obj.set_config(self.config)
        req_data = self.build_req_data(get_block_height_obj.req_body())
        mac = get_block_height_obj.sign(req_data)
        req_data["mac"] = mac
        res_data = self.common_request(req_url, req_data)
        assert get_block_height_obj.verify(res_data), "verification failure"
        return res_data

    def event_register(self, eventType, contractAddress, topic, notifyUrl, attachArgs=''):
        """
        Event registration
        :param eventType: event type (1: block event, 2: contract event)
        :param contractAddress: contract address
        :param topic: event topic
        :param notifyUrl: notification URL
        :param attachArgs: additional arguments
        :return: response data
        """
        req_url = self.config.nodeApi + self.get_api_base_path() + "/chainCode/event/register"
        event_register_obj = EventRegister(eventType, contractAddress, topic, notifyUrl, attachArgs)
        event_register_obj.set_config(self.config)
        req_data = self.build_req_data(event_register_obj.req_body())
        mac = event_register_obj.sign(req_data)
        req_data["mac"] = mac
        res_data = self.common_request(req_url, req_data)
        assert event_register_obj.verify(res_data), "verification failure"
        return res_data

    def event_query(self):
        """
        Event query
        :return: response data
        """
        req_url = self.config.nodeApi + self.get_api_base_path() + "/chainCode/event/query"
        event_query_obj = EventQuery()
        event_query_obj.set_config(self.config)
        # For Chainmaker, body is a string, not a dict
        req_body = event_query_obj.req_body()
        req_data = {
            "header": {
                "userCode": self.config.user_code,
                "appCode": self.config.app_code,
            },
            "body": req_body,
            "mac": "",
        }
        mac = event_query_obj.sign(req_data)
        req_data["mac"] = mac
        res_data = self.common_request(req_url, req_data)
        assert event_query_obj.verify(res_data), "verification failure"
        return res_data

    def event_remove(self, eventId):
        """
        Event remove
        :param eventId: event ID
        :return: response data
        """
        req_url = self.config.nodeApi + self.get_api_base_path() + "/chainCode/event/remove"
        event_remove_obj = EventRemove(eventId)
        event_remove_obj.set_config(self.config)
        req_data = self.build_req_data(event_remove_obj.req_body())
        mac = event_remove_obj.sign(req_data)
        req_data["mac"] = mac
        res_data = self.common_request(req_url, req_data)
        assert event_remove_obj.verify(res_data), "verification failure"
        return res_data

