import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, PrivateFormat
from cryptography.x509 import load_pem_x509_certificate, NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
# Import hfc crypto utilities (used for ECDSA_R1 signature)
# Note: hfc is still used for Ecies crypto functions, but Fabric protobuf is no longer loaded
from hfc.util.crypto.crypto import Ecies, ecies, CURVE_P_256_Size, SHA2
from bsn_sdk_py.until.bsn_logger import log_debug, log_info
import OpenSSL

class BsnCrypto():
    """
    :description  : bsn basic signature Class
    """
    def __init__(self, private_key_path, public_key_path):
        self.private_key_data = self._load_private_key_data(private_key_path)
        self.public_key_data = self._load_public_key_data(public_key_path)

    def _load_private_key_data(self, private_key_path):
        """
        Load private key data
        Must be implemented by subclasses
        :param private_key_path: path to private key file
        :return: private key object
        """
        raise NotImplementedError("Subclasses must implement _load_private_key_data()")

    def _load_public_key_data(self, public_key_path):
        """
        Load public key data
        Must be implemented by subclasses
        :param public_key_path: path to public key certificate file
        :return: public key object
        """
        raise NotImplementedError("Subclasses must implement _load_public_key_data()")

    def sign(self, message):
        """
        Sign message
        Must be implemented by subclasses
        :param message: message to sign
        :return: signature
        """
        raise NotImplementedError("Subclasses must implement sign()")

    def verify(self, message, signature):
        """
        Verify signature
        Must be implemented by subclasses
        :param message: original message
        :param signature: signature to verify
        :return: True if valid, False otherwise
        """
        raise NotImplementedError("Subclasses must implement verify()")


class ECDSA_R1(BsnCrypto):
    """
    :description  : ECDSA signature Class (secp256r1)
    """
    
    
    def __init__(self, private_key_path, public_key_path):
        super().__init__(private_key_path, public_key_path)

    def _load_private_key_data(self, user_private_cert_path):
        with open(user_private_cert_path, "rb") as fp:
            user_private_key = fp.read()
        skey = load_pem_private_key(user_private_key,
                                    password=None,
                                    backend=default_backend())
        return skey

    def _load_public_key_data(self, app_public_cert_path):
        with open(app_public_cert_path, "rb") as fp:
            public_key_data = fp.read()
        # Load the X509 cert public key cert
        # cert = load_pem_x509_certificate(public_key_data, default_backend())
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, public_key_data)
        # print("public key cert:", cert)

        # take contents of public key
        public_key = cert.get_pubkey().to_cryptography_key()
        # print("content of public key public_key:", public_key)
        return public_key

    def sign(self, message):
        log_info("ECDSA sign")
        # load private key
        # Sign using the function in the official library
        signature = Ecies(CURVE_P_256_Size,
                          SHA2).sign(private_key=self.private_key_data,
                                     message=message.encode('utf-8'))
        # print("signature:", signature)
        # return signarure value in base64 format
        return base64.b64encode(signature)

    def verify(self, message, signature):
        log_info("ECDSA verify signature")
        print(message)
        # read the signed data
        mac = signature
        # verify the signature
        verify_results = Ecies().verify(public_key=self.public_key_data,
                                        message=message.encode('utf-8'),
                                        signature=base64.b64decode(mac))
        # print("verify_results:", verify_results)

        # return value T or F
        return verify_results


# Backward compatibility: ECDSA alias for ECDSA_R1
ECDSA = ECDSA_R1


class ECDSA_K1(BsnCrypto):
    """
    :description  : ECDSA signature Class (secp256k1)
    """
    
    def __init__(self, private_key_path, public_key_path):
        super().__init__(private_key_path, public_key_path)

    def _load_private_key_data(self, user_private_cert_path):
        """
        Load private key for secp256k1
        :param user_private_cert_path: path to private key file
        :return: private key object
        """
        with open(user_private_cert_path, "rb") as fp:
            user_private_key = fp.read()
        skey = load_pem_private_key(user_private_key,
                                    password=None,
                                    backend=default_backend())
        
        # Verify that the key is using secp256k1 curve
        if isinstance(skey, ec.EllipticCurvePrivateKey):
            curve = skey.curve
            if not isinstance(curve, ec.SECP256K1):
                raise ValueError(
                    f"Private key must use secp256k1 curve, but got {curve.name if hasattr(curve, 'name') else type(curve).__name__}"
                )
        
        return skey

    def _load_public_key_data(self, app_public_cert_path):
        """
        Load public key for secp256k1
        :param app_public_cert_path: path to public key certificate file
        :return: public key object
        """
        with open(app_public_cert_path, "rb") as fp:
            public_key_data = fp.read()
        # Load the X509 cert public key cert
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, public_key_data)
        
        # take contents of public key
        public_key = cert.get_pubkey().to_cryptography_key()
        
        # Verify that the key is using secp256k1 curve
        if isinstance(public_key, ec.EllipticCurvePublicKey):
            curve = public_key.curve
            if not isinstance(curve, ec.SECP256K1):
                raise ValueError(
                    f"Public key must use secp256k1 curve, but got {curve.name if hasattr(curve, 'name') else type(curve).__name__}"
                )
        
        return public_key

    def sign(self, message):
        """
        Sign message using ECDSA secp256k1
        :param message: message to sign (string)
        :return: base64 encoded signature
        """
        log_info("ECDSA secp256k1 sign")
        
        # Get the private key
        private_key = self.private_key_data
        
        # Ensure it's an EC private key with secp256k1 curve
        if not isinstance(private_key, ec.EllipticCurvePrivateKey):
            raise ValueError("Private key must be an EC private key")
        
        # Verify curve is secp256k1
        if not isinstance(private_key.curve, ec.SECP256K1):
            raise ValueError(
                f"Private key must use secp256k1 curve, but got {private_key.curve.name if hasattr(private_key.curve, 'name') else type(private_key.curve).__name__}"
            )
        
        # Sign the message using ECDSA with SHA256 hash
        # The cryptography library will automatically use the key's curve (secp256k1)
        signature = private_key.sign(
            message.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        
        # Encode signature as base64
        return base64.b64encode(signature)

    def verify(self, message, signature):
        """
        Verify signature using ECDSA secp256k1
        :param message: original message (string)
        :param signature: base64 encoded signature
        :return: True if signature is valid, False otherwise
        """
        log_info("ECDSA secp256k1 verify signature")
        
        # Get the public key
        public_key = self.public_key_data
        
        # Ensure it's an EC public key with secp256k1 curve
        if not isinstance(public_key, ec.EllipticCurvePublicKey):
            raise ValueError("Public key must be an EC public key")
        
        # Verify curve is secp256k1
        if not isinstance(public_key.curve, ec.SECP256K1):
            raise ValueError(
                f"Public key must use secp256k1 curve, but got {public_key.curve.name if hasattr(public_key.curve, 'name') else type(public_key.curve).__name__}"
            )
        
        try:
            # Decode the signature from base64
            signature_bytes = base64.b64decode(signature)
            
            # Verify the signature using ECDSA with SHA256 hash
            # The cryptography library will automatically use the key's curve (secp256k1)
            public_key.verify(
                signature_bytes,
                message.encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception as e:
            log_info(f"Signature verification failed: {str(e)}")
            return False


class SM2(BsnCrypto):
    """
    :description  : sm signature Class
    """
    
    
    def __init__(self, private_key_path, public_key_path):
        super().__init__(private_key_path, public_key_path)

    def _load_private_key_data(self, user_private_cert_path):
        pass

    def _load_public_key_data(self, app_public_cert_path):
        pass

    def sign(self, message):
        log_info("SM2 sign")
        return message

    def verify(self, message, signature):
        log_info("SM2 verify the signature")
        return True



if __name__ == '__main__':
    s = SM2()