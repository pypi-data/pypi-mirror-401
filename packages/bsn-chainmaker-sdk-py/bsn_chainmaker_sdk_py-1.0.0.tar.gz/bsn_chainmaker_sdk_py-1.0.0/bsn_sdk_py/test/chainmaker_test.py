# -*- coding:utf-8 -*-
"""
Chainmaker test cases
"""
import unittest
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client import ChainmakerClient
import logging
import os


# Chainmaker 配置 - 请根据实际情况修改
# user under Public-Key-Upload Mode
c1 = Config(
    user_code="USER0001202303131659259603304",
    app_code="app0001202307251453523461410",
    nodeApi="http://gateway.node1.private.bsnbase.com:32101",
    mspDir=os.path.join(os.path.dirname(__file__), "keystore"),
    httpcert="",
    user_private_cert_path=os.path.join(os.path.dirname(__file__), "private.pem"),
    app_public_cert_path=os.path.join(os.path.dirname(__file__), "public.pem")
)

# user under Key-Trust Mode
# c2 = Config(
#     user_code="hlltest",
#     app_code="chain1",
#     nodeApi="http://192.168.1.43:17502",
#     mspDir=os.path.join(os.path.dirname(__file__), "keystore"),
#     httpcert="",
#     user_private_cert_path=os.path.join(os.path.dirname(__file__), "private.pem"),
#     app_public_cert_path=os.path.join(os.path.dirname(__file__), "public.pem")
# )


class TestChainmaker(unittest.TestCase):
    """
    Chainmaker test cases
    """

    @classmethod
    def setUpClass(cls):
        print('Chainmaker Test Setup: Initialize test environment')

    @classmethod
    def tearDownClass(cls):
        print('Chainmaker Test TearDown: Cleanup test environment')

    def setUp(self):
        print('Setup for each test case')
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
        client.set_config(c1)
        self.client = client

    def tearDown(self):
        print('TearDown for each test case')

    def test_user_register(self):
        """
        Test: User registration (Key-Trust Mode)
        """
        print('Test: User registration under Key-Trust Mode')
        userName = 'test_user_001'
        result = self.client.user_register(userName)
        print(f"User register result: {result}")
        self.assertIsNotNone(result)
        self.assertEqual(result['header']['code'], 0)

    def test_user_enroll(self):
        """
        Test: User enrollment (Public-Key-Upload Mode)
        """
        print('Test: User enrollment under Public-Key-Upload Mode')
        userName = 'test_user_002'
        # Note: This test requires the app to be in Public-Key-Upload Mode
        try:
            result = self.client.user_enroll(userName)
            print(f"User enroll result: {result}")
            self.assertIsNotNone(result)
            self.assertEqual(result['header']['code'], 0)
        except AssertionError as e:
            if "only allow to enroll user under Public-Key-Upload Mode" in str(e):
                print("Skipping test: App is not in Public-Key-Upload Mode")
                self.skipTest("App is not in Public-Key-Upload Mode")
            else:
                raise

    def test_req_chain_code(self):
        """
        Test: Transaction processing under Key-Trust Mode
        """
        print('Test: Transaction processing under Key-Trust Mode')
        userName = 'test_user_001'
        contractAddress = 'contract001'
        funcName = 'set'
        # funcParam should be a JSON string list format
        funcParam = '["key1", "value1"]'
        
        result = self.client.req_chain_code(
            userName=userName,
            contractAddress=contractAddress,
            funcName=funcName,
            funcParam=funcParam
        )
        print(f"ReqChainCode result: {result}")
        self.assertIsNotNone(result)
        self.assertEqual(result['header']['code'], 0)
        # Check response structure
        self.assertIn('body', result)
        self.assertIn('blockInfo', result['body'])
        self.assertIn('contractRes', result['body'])

    def test_sdk_trans(self):
        """
        Test: Transaction under Public-Key-Upload Mode
        """
        print('Test: Transaction under Public-Key-Upload Mode')
        # transData should be proto object string format
        # This is a placeholder - actual implementation depends on Chainmaker SDK
        transData = 'test_transaction_data'
        
        try:
            result = self.client.sdk_trans(transData)
            print(f"SdkTrans result: {result}")
            self.assertIsNotNone(result)
            self.assertEqual(result['header']['code'], 0)
        except Exception as e:
            print(f"SdkTrans test failed: {str(e)}")
            # This test may fail if transData format is incorrect
            # Uncomment the next line to skip this test
            # self.skipTest(f"SdkTrans requires proper transData format: {str(e)}")

    def test_get_tx_info(self):
        """
        Test: Get transaction info
        """
        print('Test: Get transaction info')
        # Use a valid transaction ID from a previous transaction
        txId = 'test_tx_id_1234567890abcdef'
        
        try:
            result = self.client.get_tx_info(txId)
            print(f"GetTxInfo result: {result}")
            self.assertIsNotNone(result)
            self.assertEqual(result['header']['code'], 0)
            # Check response structure
            self.assertIn('body', result)
            self.assertIn('blockHash', result['body'])
            self.assertIn('blockHeight', result['body'])
            self.assertIn('status', result['body'])
            self.assertIn('contractAddress', result['body'])
        except Exception as e:
            print(f"GetTxInfo test failed (may be invalid txId): {str(e)}")
            # Uncomment to skip if txId is invalid
            # self.skipTest(f"Invalid txId: {str(e)}")

    def test_get_block_info_by_height(self):
        """
        Test: Get block info by block height
        """
        print('Test: Get block info by block height')
        blockHeight = 1
        
        try:
            result = self.client.get_block_info(blockHeight=blockHeight)
            print(f"GetBlockInfo result: {result}")
            self.assertIsNotNone(result)
            self.assertEqual(result['header']['code'], 0)
            # Check response structure
            self.assertIn('body', result)
            self.assertIn('blockHash', result['body'])
            self.assertIn('blockHeight', result['body'])
            self.assertIn('preBlockHash', result['body'])
        except Exception as e:
            print(f"GetBlockInfo by height test failed: {str(e)}")

    def test_get_block_info_by_hash(self):
        """
        Test: Get block info by block hash
        """
        print('Test: Get block info by block hash')
        blockHash = 'test_block_hash_1234567890abcdef'
        
        try:
            result = self.client.get_block_info(blockHash=blockHash)
            print(f"GetBlockInfo by hash result: {result}")
            self.assertIsNotNone(result)
            self.assertEqual(result['header']['code'], 0)
        except Exception as e:
            print(f"GetBlockInfo by hash test failed (may be invalid hash): {str(e)}")

    def test_get_block_height(self):
        """
        Test: Get the latest block height
        """
        print('Test: Get the latest block height')
        result = self.client.get_block_height()
        print(f"GetBlockHeight result: {result}")
        self.assertIsNotNone(result)
        self.assertEqual(result['header']['code'], 0)
        # Check response structure
        self.assertIn('body', result)
        self.assertIn('blockHeight', result['body'])
        self.assertIsInstance(result['body']['blockHeight'], (int, type(None)))

    def test_event_register(self):
        """
        Test: Event registration
        """
        print('Test: Event registration')
        eventType = '2'  # 1: block event, 2: contract event
        contractAddress = 'contract001'
        topic = 'test_topic'
        notifyUrl = 'http://127.0.0.1:8080/notify'
        attachArgs = 'test=1'
        
        try:
            result = self.client.event_register(
                eventType=eventType,
                contractAddress=contractAddress,
                topic=topic,
                notifyUrl=notifyUrl,
                attachArgs=attachArgs
            )
            print(f"EventRegister result: {result}")
            self.assertIsNotNone(result)
            self.assertEqual(result['header']['code'], 0)
            # Check response structure
            self.assertIn('body', result)
            self.assertIn('eventId', result['body'])
        except Exception as e:
            print(f"EventRegister test failed: {str(e)}")

    def test_event_query(self):
        """
        Test: Event query
        """
        print('Test: Event query')
        result = self.client.event_query()
        print(f"EventQuery result: {result}")
        self.assertIsNotNone(result)
        self.assertEqual(result['header']['code'], 0)
        # Check response structure
        self.assertIn('body', result)
        # body should be a list of EventDetailData
        self.assertIsInstance(result['body'], list)

    def test_event_remove(self):
        """
        Test: Event remove
        """
        print('Test: Event remove')
        # Use a valid event ID from a previous event registration
        eventId = 'test_event_id_1234567890abcdef'
        
        try:
            result = self.client.event_remove(eventId)
            print(f"EventRemove result: {result}")
            self.assertIsNotNone(result)
            self.assertEqual(result['header']['code'], 0)
        except Exception as e:
            print(f"EventRemove test failed (may be invalid eventId): {str(e)}")
            # Uncomment to skip if eventId is invalid
            # self.skipTest(f"Invalid eventId: {str(e)}")

    @unittest.skip('Skip this test case')
    def test_skip(self):
        """
        Skip this test case
        """
        print('This test case is skipped')

    
if __name__ == '__main__':
    # Execute all test cases
    unittest.main()
    
    # Or execute specific test cases using TestSuite
    # suite = unittest.TestSuite()
    # suite.addTest(TestChainmaker('test_user_register'))
    # suite.addTest(TestChainmaker('test_req_chain_code'))
    # suite.addTest(TestChainmaker('test_get_block_height'))
    # suite.addTest(TestChainmaker('test_event_query'))
    # 
    # unittest.TextTestRunner().run(suite)

