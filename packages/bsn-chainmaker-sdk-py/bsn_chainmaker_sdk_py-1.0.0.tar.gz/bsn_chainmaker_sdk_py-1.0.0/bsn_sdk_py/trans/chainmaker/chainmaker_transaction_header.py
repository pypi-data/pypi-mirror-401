# -*- coding:utf-8 -*-
"""
Chainmaker transaction header utilities
用于构建 chainmaker 框架的交易对象
"""
import base64
import hashlib
import time
import json
from bsn_sdk_py.until.tools import nonce_str
from bsn_sdk_py.until.bsn_logger import log_debug, log_info
from bsn_sdk_py.common.myecdsa256 import ecdsaR1_sign
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
# from bsn_sdk_py.trans.chainmaker.protos.accesscontrol import member_pb2
# from bsn_sdk_py.trans.chainmaker.protos.common.request_pb2 import Payload, TxRequest,EndorsementEntry


def hash256_sign(o_str):
    """
    计算 SHA256 哈希值
    :param o_str: 输入字符串
    :return: 十六进制哈希值
    """
    sha256 = hashlib.sha256()
    sha256.update(o_str)
    return sha256.hexdigest()


def get_chainmaker_trans_data(chain_id, contract_name, method, parameters, 
                               cert_pub_path, userName=None, tx_id=None, 
                               expiration_time=None):
    """
    构建 chainmaker 交易数据
    
    注意：此函数返回的是交易数据的字符串表示，需要符合 chainmaker Transaction protobuf 的 CompactTextString 格式。
    由于项目中没有 chainmaker 的 protobuf Python 文件，当前实现使用 JSON 格式作为基础格式。
    如果后续有 chainmaker 的 protobuf 定义文件，应该使用 protobuf 对象来构建和序列化。
    
    :param chain_id: 链ID
    :param contract_name: 合约名称（合约地址）
    :param method: 合约方法名
    :param parameters: 合约参数列表，格式为 [{"key": "key1", "value": "value1"}, ...]
                       或者简单的字符串列表，会在调用方转换为 KeyValuePair 格式
    :param cert_pub_path: 用户证书公钥路径
    :param userName: 用户名（可选）
    :param tx_id: 交易ID（可选，如果不提供则自动生成）
    :param expiration_time: 过期时间（可选，毫秒级时间戳）
    :return: 构建好的交易数据（字符串格式，应该是 protobuf CompactTextString 格式）
    """
    # 读取证书
    with open(cert_pub_path, "rb") as fp:
        cert_data = fp.read()
    
    # 生成交易ID（如果没有提供）
    if not tx_id:
        nonce = nonce_str()
        sign_str = bytes(nonce, 'utf-8') + cert_data
        tx_id = hash256_sign(sign_str)
    
    # 获取当前时间戳（毫秒）
    timestamp = int(time.time() * 1000)
    
    # 设置过期时间（默认30分钟后过期）
    if expiration_time is None:
        expiration_time = timestamp + 30 * 60 * 1000  # 30分钟
    elif expiration_time < 1000000000000:  # 如果小于这个值，说明是秒级时间戳
        expiration_time = expiration_time * 1000
    
    # 构建 Payload
    # 根据 chainmaker Transaction protobuf 结构
    # Payload 包含：chain_id, tx_type, tx_id, timestamp, expiration_time, contract_name, method, parameters, sequence, limit
    payload = {
        "chain_id": chain_id,
        "tx_type": 2,  # INVOKE_CONTRACT = 2 (根据 chainmaker 定义)
        "tx_id": tx_id,
        "timestamp": timestamp,
        "expiration_time": expiration_time,
        "contract_name": contract_name,
        "method": method,
        "parameters": parameters or [],
        "sequence": 0,
    }
    
    # 构建 Transaction 对象
    # 根据 chainmaker 的 Transaction protobuf 结构：
    # Transaction 包含：payload, sender (EndorsementEntry), signature
    # 注意：这里使用简化的结构，实际应该根据 chainmaker protobuf 定义构建
    transaction = {
        "payload": payload,
        "sender": {
            "signer": {
                "org_id": "",  # 组织ID，可以从配置中获取
                "member_info": base64.b64encode(cert_data).decode('utf-8'),  # 证书信息
            }
        },
        "signature": "",  # 签名会在后续步骤中添加
    }
    
    # 将 Transaction 转换为字符串格式
    # 注意：根据 proto 文件说明，transData 应该是 "proto对象string格式化，proto.CompactTextString(m) string串"
    # CompactTextString 是 protobuf 的紧凑文本格式（类似 JSON 但更紧凑）
    # 由于没有 chainmaker 的 protobuf Python 文件，这里使用紧凑的 JSON 格式
    # TODO: 如果后续有 chainmaker 的 protobuf 定义文件，应该使用如下方式：
    #   from chainmaker_pb2 import Transaction
    #   tx = Transaction()
    #   # ... 填充字段 ...
    #   trans_data_str = str(tx)
    trans_data_str = json.dumps(transaction, separators=(',', ':'))
    
    log_debug(f"Chainmaker transaction data: {trans_data_str}")
    
    return trans_data_str


def create_chainmaker_signed_transaction(transaction_str, signature):
    """
    创建已签名的 chainmaker 交易
    
    :param transaction_str: 交易数据字符串
    :param signature: 签名数据（base64编码）
    :return: 包含签名的完整交易数据（base64编码）
    """
    try:
        transaction = json.loads(transaction_str)
        transaction["signature"] = signature
        
        # 重新序列化
        signed_transaction_str = json.dumps(transaction, separators=(',', ':'))
        
        # 返回 base64 编码的交易数据
        return base64.b64encode(signed_transaction_str.encode('utf-8')).decode('utf-8')
    except Exception as e:
        log_info(f"Error creating signed transaction: {str(e)}")
        raise



if __name__ == '__main__':
    # 测试代码
    chain_id = 'chain1'
    contract_name = 'contract001'
    method = 'set'
    parameters = [
        {"key": "key1", "value": "value1"},
        {"key": "key2", "value": "value2"}
    ]
    cert_pub_path = r'E:\test\cert.pem'
    
    trans_data = get_chainmaker_trans_data(
        chain_id=chain_id,
        contract_name=contract_name,
        method=method,
        parameters=parameters,
        cert_pub_path=cert_pub_path
    )
    print(trans_data)
