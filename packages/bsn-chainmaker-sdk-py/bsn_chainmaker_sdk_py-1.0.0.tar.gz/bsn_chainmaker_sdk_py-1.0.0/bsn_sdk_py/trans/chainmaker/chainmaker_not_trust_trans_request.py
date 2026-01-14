# -*- coding:utf-8 -*-
"""
Chainmaker Not Trust Transaction Request
用于构建 chainmaker 框架的公钥上传模式（Public-Key-Upload Mode）下的交易请求
"""
import base64
import json
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.until.bsn_logger import log_debug, log_info

#from bsn_sdk_py.trans.chainmaker.user import User
from chainmaker.user import User
#from bsn_sdk_py.trans.chainmaker.payload import PayloadBuilder
from chainmaker.payload import PayloadBuilder
#from bsn_sdk_py.trans.chainmaker.protos.common.request_pb2 import Payload, TxRequest
from chainmaker.protos.common.request_pb2 import Payload, TxRequest, EndorsementEntry
from chainmaker.keys import AuthType, HashType
from chainmaker.utils.evm_utils import calc_evm_contract_name, calc_evm_method_params



class ChainmakerNotTrustTransRequest:
    """
    构建 chainmaker 框架公钥上传模式下的交易数据
    """
    def __init__(self,
                 contractName,
                 method,
                 userName,
                 parameters: list = None,
                 tx_id: str = None,
                 expiration_time: int = None):
        """
        :description: 初始化 chainmaker 交易请求
        :param contractName: 合约名称
        :param method: 合约方法名
        :param userName: 用户名
        :param parameters: 合约参数列表，格式为 [{"key": "key1", "value": "value1"}, ...] 
                          或者简单的字符串列表，会自动转换为 KeyValuePair 格式
        :param tx_id: 交易ID（可选，如果不提供则自动生成）
        :param expiration_time: 过期时间（可选，秒级时间戳）
        :return:
        """
        self.name = userName
        self.contractName = contractName
        self.method = method
        self.parameters = parameters or []
        self.tx_id = tx_id
        self.expiration_time = expiration_time

    def set_config(self, config: Config):
        """
        设置配置对象
        :param config: Config 实例
        """
        self.config = config
        self.payload_builder = PayloadBuilder(self.config.app_code)

        self.user = User(
            org_id=self.config.org_id,
            sign_key_bytes=self._get_not_trust_private_key(),
            auth_type=AuthType.PermissionedWithKey,
            hash_type=HashType.SHA256
        )

    def _get_not_trust_private_key(self):
        """
        :description: 获取应用证书私钥
        :param:
        :return: 私钥数据
        """
        name = self.GetCertName()
        not_trust_tran_private_path = self.config.mspDir + r'\keystore\\' + name + '_private.pem'
        #not_trust_tran_private_path = self.config.mspDir + name + '_private.pem'
        log_info(("user private key path", not_trust_tran_private_path))
        with open(not_trust_tran_private_path, "rb") as f:
            key_data = f.read()
        return key_data

    def GetCertName(self):
        """
        :description: 组装应用证书名称
        :return: 证书名称
        """
        return self.name + "@" + self.config.app_code

    def _convert_parameters_to_keyvalue_pairs(self, parameters):
        """
        将参数转换为 KeyValuePair 格式
        chainmaker 的参数格式：
        - 参数应该是一个 KeyValuePair 列表，每个 KeyValuePair 包含 key 和 value
        - 参数顺序必须与合约方法入参顺序一致
        - 如果传入的是简单值列表，会按照索引顺序转换为 KeyValuePair
        
        :param parameters: 参数列表，可以是：
                          - 字符串列表，如 ["arg1", "arg2"]
                          - KeyValuePair 字典列表，如 [{"key": "key1", "value": "value1"}, ...]
                          - 混合格式
        :return: KeyValuePair 格式的参数列表
        """
        if not parameters:
            return []
        
        key_value_pairs = []
        for idx, param in enumerate(parameters):
            if isinstance(param, dict) and "key" in param and "value" in param:
                # 已经是 KeyValuePair 格式
                key_value_pairs.append({
                    "key": param["key"],
                    "value": param["value"]
                })
            else:
                # 转换为 KeyValuePair 格式
                # 注意：chainmaker 的参数 key 通常是按顺序的，如 "arg0", "arg1" 等
                # 或者根据实际合约方法的参数名来设置
                param_value = param
                if isinstance(param, (list, dict)):
                    # 如果是复杂类型，转换为 JSON 字符串
                    param_value = json.dumps(param)
                else:
                    param_value = str(param)
                
                key_value_pairs.append({
                    "key": f"arg{idx}",  # 使用索引作为 key
                    "value": param_value
                })
        
        return key_value_pairs

    def chainmaker_trans_data(self, isQuery: bool=False):
        """
        :description: 组装 chainmaker 交易数据
        :param:
        :return: base64 编码的交易数据字符串
        """
        #name = self.GetCertName()
        #not_trust_tran_public_path = self.config.mspDir + r'\keystore\\' + name + '_cert.pem'
        
        # 获取 chain_id（从 app_info 中获取，如果没有则使用 app_code） self.config.app_info.get("chainId") or
        #chain_id = self.config.app_code
        
        # 转换参数格式
        method, params = calc_evm_method_params(self.method, self.parameters)
        contract_name = calc_evm_contract_name(self.contractName)
        if isQuery:
            payload = self.payload_builder.create_query_payload(
                contract_name=contract_name,
                method=method,
                params=params,
                tx_id=self.tx_id,
            )
        else:
            payload = self.payload_builder.create_invoke_payload(
                contract_name=contract_name,
                method=method,
                params=params,
                tx_id=self.tx_id,
            )
        
        # 序列化交易数据以便签名
        # transaction_bytes = transaction_str.encode('utf-8')
        transaction_str = payload.SerializeToString()

        # 使用私钥签名
        # private_key = self._get_not_trust_private_key()
        # base64_sign = ecdsa_sign(transaction_str, private_key)
        sender = self.user.endorse(transaction_str)
        # 创建已签名的交易
        tx_request = TxRequest(
            payload=payload,
            sender=sender,
        )
        
        log_debug(f"Chainmaker signed transaction: {tx_request}")

        return str(base64.b64encode(tx_request.SerializeToString()),
            'utf-8')
