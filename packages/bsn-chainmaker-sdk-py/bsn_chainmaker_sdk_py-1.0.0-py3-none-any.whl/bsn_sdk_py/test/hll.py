import os
from chainmaker.utils.evm_utils import calc_evm_contract_name, calc_evm_method_params
from chainmaker.protos.common.request_pb2 import TxRequest
import base64

def crypto_config_path1(config_dir):
    """crypto-config配置路径"""
    return os.path.join(config_dir, 'keystore')

def config_dir1():
    """返回配置目录路径 tests/config"""
    TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
    return TESTS_DIR

def create_chain_client_with_args1():
    from chainmaker.chain_client import ChainClient
    from chainmaker.node import Node
    from chainmaker.keys import AuthType,HashType
    from chainmaker.user import User
    from chainmaker.utils import file_utils

    crypto_config_path = crypto_config_path1(config_dir1())
    user = User('org1',
                sign_key_bytes=file_utils.read_file_bytes(
                    f'{crypto_config_path}\\test_user_001@chain1_private.pem'),
                auth_type=AuthType.PermissionedWithKey,
                hash_type=HashType.SHA256
                )

    node = Node(
        node_addr='node1.org1.grpc.chainmakersharedchain.sbpsuite-np.hksarg:32001',
        conn_cnt=1,
        enable_tls=False,
        trust_cas=[
            
        ],
        tls_host_name='node1.org1.grpc.chainmakersharedchain.sbpsuite-np.hksarg'
    )

    cc = ChainClient(chain_id='chain1', user=user, nodes=[node])
    print("===============>", cc.get_chainmaker_server_version())
    return cc


def create_counter_evm(cc, testdata_dir):
    origin_contract_name = "balance001" #str(uuid.uuid4()).replace('-', '')
    contract_name = calc_evm_contract_name(origin_contract_name)
    byte_code_path = os.path.join(testdata_dir, 'byte_codes', 'ledger_balance.bin')
    payload = cc.create_contract_create_payload(contract_name, '1.0', byte_code_path, 'EVM', None)
    print(payload)
    res = cc.send_manage_request(payload)
    message = res.contract_result.message
    if 'contract exist' in message:
        print(f'合约{origin_contract_name}已安装')
    else:
        assert res.code == 0, res.contract_result.message
        print(f'合约{origin_contract_name}安装成功')
    return contract_name

def invoke_contract_evm(cc):
    # 调用EVM合约
    contract_name = 'balance001'
    method = 'updateBalance'
    params = [{"uint256": "10000"}, {"address": "0xa166c92f4c8118905ad984919dc683a7bdb295c1"}]
    contract_name = calc_evm_contract_name(contract_name)
    method, params = calc_evm_method_params(method, params)

    res = cc.invoke_contract(contract_name, method, params, with_sync_result=True)
    assert res.code == 0, res.contract_result.message
    print("调用EVM合约===>", res)

def query_contract_evm(cc):
    # 调用EVM合约
    contract_name = 'balance001'
    method = 'balances'
    params = [{"address": "0xa166c92f4c8118905ad984919dc683a7bdb295c1"}]

    contract_name = calc_evm_contract_name(contract_name)
    method, params = calc_evm_method_params(method, params)
    print(method, params)
    res = cc.query_contract(contract_name, method, params)
    print("查询EVM合约===>", res)

def send(txs):
    tx_request = TxRequest()
    tx_request.ParseFromString(txs)
    res = cc.send_tx_request(tx_request, with_sync_result=True)
    print(res, type(res))

if __name__ == '__main__':
    cc = create_chain_client_with_args1()
    create_counter_evm(cc, config_dir1())
    invoke_contract_evm(cc)

    query_contract_evm(cc)

    # txB = 'CpgCCgZjaGFpbjEaQDM2NDVlZDFiMDg1NjQ2MzU5MGI4MGM2N2U3NjE1ZTMwYjMxNTNhZWM0ZDI5NGNjMjg2YzdmMTgyNGE1YWQxMGEgrteXywYyKDUzMmMyMzhjZWM3MDcxY2U4NjU1YWJhMDdlNTBmOWZiMTZmNzJjYTE6CDJlMmFkMDAxQpEBCgRkYXRhEogBMmUyYWQwMDEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAyNzEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwYTE2NmM5MmY0YzgxMTg5MDVhZDk4NDkxOWRjNjgzYTdiZGIyOTVjMRKKAgq9AQoEb3JnMRACGrIBLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUZrd0V3WUhLb1pJemowQ0FRWUlLb1pJemowREFRY0RRZ0FFVnUzMlF5K0tUZk1MRkplYmJralhjRFhTdU11VgpGYU1iRFVXZTg3c1l2MjBMeUhteU9oNVd0NGF0VTJtNzI3RTU4cUoxTzV1WVRyRThzeXg0dGxmeVNnPT0KLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tChJIMEYCIQCmp/y6FP8QBzqDixXTEb3xWW+8YmgpkFTRAxEI8yMcywIhANhpD9C7qnE4qPE5K+XAUBBi8ID6sferoBnhlADIBGn4'
    #
    # tx_bytes  = base64.b64decode(txB)
    # send(tx_bytes)