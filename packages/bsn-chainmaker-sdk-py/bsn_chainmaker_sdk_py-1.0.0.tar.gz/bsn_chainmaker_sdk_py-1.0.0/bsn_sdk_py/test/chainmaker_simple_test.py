# -*- coding:utf-8 -*-
"""
Chainmaker simple test - Quick test script
"""
import os
import sys

# 将项目根目录添加到 Python 路径，以便能够导入 bsn_sdk_py 模块
# 获取当前文件的目录（bsn_sdk_py/test/）
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录（向上两级：test -> bsn_sdk_py -> 根目录）
project_root = os.path.dirname(os.path.dirname(current_dir))
# 将项目根目录添加到 sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 导入 ChainMaker 客户端和配置
from bsn_sdk_py.client.chainmaker import ChainmakerClient
from bsn_sdk_py.client.config import Config
import logging

# 配置日志
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), 'chainmaker_test.log'),
    filemode='w',
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%Y-%m-%d %H:%M:%S]"
)

# # Chainmaker 配置 - 请根据实际情况修改
config = Config(
    user_code="hlltest-chainmaker",
    app_code="chain1",
    nodeApi="node1.org1.grpc.chainmakersharedchain.sbpsuite-np.hksarg:32001",
    mspDir=os.path.join(os.path.dirname(__file__)), #,"keystore"
    httpcert="",
    user_private_cert_path=os.path.join(os.path.dirname(__file__), "private.pem"),
    app_public_cert_path=os.path.join(os.path.dirname(__file__), "public.pem"),
    org_id='org1',
)

# # 创建客户端
FORMAT = "%(asctime)s %(thread)d %(message)s"
log_file = os.path.join(os.path.dirname(__file__), 'chainmaker_test.log')
logging.basicConfig(
    filename=log_file,
    filemode='w',
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%Y-%m-%d %H:%M:%S]"
)
# Create Chainmaker client
client = ChainmakerClient()
client.set_config(config)

# 测试用例 - 根据需要取消注释

# 1. 用户注册（密钥托管模式）
# result = client.user_register('test_user_001')
# print("User register result:", result)

# 2. 用户注册（公钥上传模式）
def test_user_enroll():
    result = client.user_enroll('test_user_001')
    print("User enroll result:", result)

# 3. 密钥托管模式交易
# result = client.req_chain_code(
#     userName='test_user_001',
#     contractAddress='contract001',
#     funcName='set',
#     funcParam='["key1", "value1"]'
# )
# print("ReqChainCode result:", result)

# 4. 公钥上传模式交易
# result = client.sdk_trans(transData='test_transaction_data')
# print("SdkTrans result:", result)

# 5. 查询交易信息
# result = client.get_tx_info(txId='your_tx_id_here')
# print("GetTxInfo result:", result)

# 6. 获取区块信息（通过块高）
# result = client.get_block_info(blockHeight=1)
# print("GetBlockInfo by height result:", result)

# 7. 获取区块信息（通过块哈希）
# result = client.get_block_info(blockHash='your_block_hash_here')
# print("GetBlockInfo by hash result:", result)

# 8. 获取最新块高
# result = client.get_block_height()
# print("GetBlockHeight result:", result)
# print(f"Latest block height: {result['body']['blockHeight']}")

# 9. 事件注册
# result = client.event_register(
#     eventType='2',  # 1: 出块事件, 2: 合约事件
#     contractAddress='contract001',
#     topic='test_topic',
#     notifyUrl='http://127.0.0.1:8080/notify',
#     attachArgs='test=1'
# )
# print("EventRegister result:", result)

# 10. 事件查询
# result = client.event_query()
# print("EventQuery result:", result)
# print(f"Total events: {len(result['body'])}")

# 11. 事件移除
# result = client.event_remove(eventId='your_event_id_here')
# print("EventRemove result:", result)

print("Chainmaker test script loaded. Uncomment test cases to run.")

from bsn_sdk_py.common import myecdsa256

def test_generate_secp256r1_keypair_for_chainmaker():
    pri_pem, pub_pem, private_path = myecdsa256.generate_secp256r1_keypair_for_chainmaker()
    print("pri_pem:", pri_pem)
    print("pub_pem:", pub_pem)
    print("private_path:", private_path)

def test_chainmaker_simple_test():

    result = client.sdk_trans(
        contractAddress='balance001',
        funcName='updateBalance',
        funcParam=[{"uint256": "10000"},{"address": "0xa166c92f4c8118905ad984919dc683a7bdb295c1"}],
        isQuery=False,
    )
    print("SdkTrans result:", result)
if __name__ == "__main__":
    # test_generate_secp256r1_keypair_for_chainmaker()
    #test_user_enroll()
    test_chainmaker_simple_test()