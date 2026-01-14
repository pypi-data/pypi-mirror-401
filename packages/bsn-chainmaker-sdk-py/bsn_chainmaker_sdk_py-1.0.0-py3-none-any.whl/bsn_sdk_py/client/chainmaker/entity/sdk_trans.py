# -*- coding:utf-8 -*-
"""
Chainmaker SDK transaction entity (Public-Key-Upload Mode)
"""
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.chainmaker.entity.bsn_base import BsnBase
from bsn_sdk_py.until.tools import obj_sort
from bsn_sdk_py.trans.chainmaker.chainmaker_not_trust_trans_request import ChainmakerNotTrustTransRequest
from bsn_sdk_py.until.bsn_logger import log_debug, log_info


class SdkTrans(BsnBase):
    """
    SDK transaction for Chainmaker (Public-Key-Upload Mode)
    """
    def __init__(self,
                 contractAddress: str,
                 funcName: str,
                 funcParam: list = None,
                 userName: str = None,
                 isQuery: bool=False):
        """
        :param contractAddress: contract address (合约地址)
        :param funcName: function name (合约方法名)
        :param funcParam: function parameters (合约参数列表)
        :param userName: user name (用户名，公钥上传模式下需要)
        """
        super().__init__()
        self.contractAddress = contractAddress
        self.funcName = funcName
        self.funcParam = funcParam or []
        self.name = userName
        self.isQuery =isQuery

    def req_body(self):
        """
        Build request body
        :return: request body dict
        """
        transRequest = ChainmakerNotTrustTransRequest(
            contractName=self.contractAddress,
            method=self.funcName,
            userName=self.name,
            parameters=self.funcParam
        )
        transRequest.set_config(self.config)
        transRequest_data = transRequest.chainmaker_trans_data(self.isQuery)
        log_info(f"Chainmaker signed transaction: {transRequest_data}")
        req_body = {
            "transData": transRequest_data,
        }
        return req_body

    def sign(self, body):
        """
        Sign the request
        :param body: request body
        :return: signature (mac)
        """
        sign_str = self.config.user_code + self.config.app_code + body['body']["transData"]
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



