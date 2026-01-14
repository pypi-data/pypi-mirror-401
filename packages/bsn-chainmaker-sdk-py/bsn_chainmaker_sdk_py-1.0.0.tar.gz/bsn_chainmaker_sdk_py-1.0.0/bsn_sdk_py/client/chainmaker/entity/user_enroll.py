# -*- coding:utf-8 -*-
"""
Chainmaker user enrollment entity (Public-Key-Upload Mode)
"""
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.chainmaker.entity.bsn_base import BsnBase
from bsn_sdk_py.common import myecdsa256


class UserEnroll(BsnBase):
    """
    User enrollment for Chainmaker (Public-Key-Upload Mode)
    """
    def __init__(self, userName):
        """
        :param userName: user name
        """
        self.userName = userName

    def GetPublicKeyPem(self):
        """
        Get public key in PEM format
        :return: public key PEM string
        """
        # For Chainmaker, we need to generate or load the public key
        # This is a placeholder - actual implementation depends on key management
        name = self.GetCertName()
        # Load public key from file or generate it
        # User enrollment for ChainMaker
        public_key_path = self.config.mspDir + r'\keystore\\' + name + '_public.pem'
        private_path = self.config.mspDir + r'\keystore\\' + name + '_private.pem'
        try:
            with open(public_key_path, "rb") as fp:
                pubkey_pem = fp.read()
            return str(pubkey_pem, encoding="utf-8")
        except FileNotFoundError:
            # Generate key pair if not exists
            pri_pem, pub_pem, private_path = myecdsa256.generate_secp256r1_keypair_for_chainmaker(
                private_path,public_key_path)
            # Extract public key from CSR or generate separately
            # This is simplified - actual implementation may vary
            return str(pub_pem, encoding="utf-8")

    def GetCertName(self):
        return self.userName + "@" + self.config.app_code

    def req_body(self):
        """
        Build request body
        :return: request body dict
        """
        pubkey_pem = self.GetPublicKeyPem()
        req_body = {
            "userName": self.userName,
            "pubkeyPem": pubkey_pem,
        }
        return req_body

    def sign(self):
        """
        Sign the request
        :return: signature (mac)
        """
        pubkey_pem = self.GetPublicKeyPem()
        sign_str = self.config.user_code + self.config.app_code + self.userName + pubkey_pem
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



