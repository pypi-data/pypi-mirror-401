import os
import base64
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, PrivateFormat, PublicFormat
from cryptography.x509 import load_pem_x509_certificate, NameOID
# introduce signature class Ecies in the official package, default instantiation(CURVE_P_256_Size, SHA2)，CURVE_P_256_Size elliptic curvature and sha256 algorithm
from hfc.util.crypto.crypto import Ecies, ecies, CURVE_P_256_Size, SHA2
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes


# ecdsa256 signature
def ecdsa_sign(message, key_data):
    """
	:param message: character string to sign
	:param pri_key_file_name: user private key path
	:return: return signature value in base64 format
	"""
    # Read the pri_key_file
    # path = os.path.abspath('.')
    # file = os.path.join(path, pri_key_file_name)
    # print('private key storage path: ', file)
    # pri_key_file = open(file, "rb")
    # key_data = pri_key_file.read()
    # pri_key_file.close()

    # load private key
    skey = load_pem_private_key(key_data, password=None, backend=default_backend())

    # sign using the function in the official library 
    signature = Ecies(CURVE_P_256_Size, SHA2).sign(private_key=skey, message=message)

    # print("signature:", signature)
    # return signature value in base64 format base64.b64encode(signature)
    return signature


# ecdsa256 verification function
def ecdsa_verify(message, signature, key_data):
    """
	:param message: character string to sign 
	:param signature: mac value in the return message 
	:param pub_key_file: gateway public key path
	:return: return True or False
	"""
    # read the content of public key 
    # path = os.path.abspath('.')
    # file = os.path.join(path, pub_key_file)
    # print('gateway public key directory path: ', file)
    # pub_key_file = open(file, "rb")
    # key_data = pub_key_file.read()
    # pub_key_file.close()

    # load X509 cert public key
    cert = load_pem_x509_certificate(key_data, default_backend())
    # print("public key cert:", cert)

    # read the content of public key
    public_key = cert.public_key()
    # print("the content of public key public_key:", public_key)

    # read the signed data 
    mac = signature

    # verify the signature
    verify_results = Ecies().verify(public_key=public_key, message=message.encode('utf-8'),
                                    signature=base64.b64decode(mac))
    # print("verify_results:", verify_results)

    # return value T or F
    return verify_results


def certificate_request(name, save_path):
    ecies256 = ecies()
    private_key = ecies256.generate_private_key()
    csr = ecies256.generate_csr(private_key, x509.Name(
        [x509.NameAttribute(NameOID.COMMON_NAME, name)]))  # test02@app0001202004161020152918451
    csr_pem = csr.public_bytes(Encoding.PEM)
    sk_pem = private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, serialization.NoEncryption())
    with open(save_path, mode='wb') as f:
        f.write(sk_pem)

    # with open('pub.csr', mode='wb') as f:
    #     f.write(csr_pem)
    return csr_pem, save_path


def generate_secp256r1_keypair_for_chainmaker(private_key_path=None, public_key_path=None):
    """
    生成针对 Chainmaker 框架认证方式为 PermissionedWithKey 时的 secp256r1 密钥对
    私钥格式为 SEC1 格式（-----BEGIN EC PRIVATE KEY-----）
    
    :param private_key_path: 私钥保存路径，如果为 None 则不保存文件
    :param public_key_path: 公钥保存路径，如果为 None 则不保存文件
    :return: tuple (private_key_pem_bytes, public_key_pem_bytes, private_key_path)
    """
    # 生成 secp256r1 曲线上的私钥
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    
    # 生成对应的公钥
    public_key = private_key.public_key()
    
    # 将私钥序列化为 SEC1 格式（TraditionalOpenSSL 格式）
    # 这会生成 -----BEGIN EC PRIVATE KEY----- 格式
    private_key_pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # 将公钥序列化为 PEM 格式
    public_key_pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo
    )
    
    # 保存私钥文件
    if private_key_path:
        # 确保目录存在
        os.makedirs(os.path.dirname(private_key_path) if os.path.dirname(private_key_path) else '.', exist_ok=True)
        with open(private_key_path, mode='wb') as f:
            f.write(private_key_pem)
    
    # 保存公钥文件
    if public_key_path:
        # 确保目录存在
        os.makedirs(os.path.dirname(public_key_path) if os.path.dirname(public_key_path) else '.', exist_ok=True)
        with open(public_key_path, mode='wb') as f:
            f.write(public_key_pem)
    
    return private_key_pem, public_key_pem, private_key_path


def hash256_sign(o_str):
    sha256 = hashlib.sha256()
    sha256.update(o_str.encode('utf-8'))
    return sha256.hexdigest()  # .upper()

# ecdsa256 signature
def ecdsaR1_sign(message, key_data:ec.EllipticCurvePrivateKey):
    """
	:param message: character string to sign
	:param pri_key_file_name: user private key path
	:return: return signature value in base64 format
	"""


    # load private key
    # skey = load_pem_private_key(key_data, password=None, backend=default_backend())

    # sign using the function in the official library 
    # signature = Ecies(CURVE_P_256_Size, SHA2).sign(private_key=skey, message=message)
    signature = key_data.sign(message.encode('utf-8'), ec.ECDSA(hashes.SHA256()))
    # print("signature:", signature)
    # return signature value in base64 format base64.b64encode(signature)
    return signature

if __name__ == '__main__':
    o_str = 'USER0001202004151958010871292app00012020041610201529184510364a7ce7c1f7c3fb7afb3ea2b9c678ed3dfd5e7c61ae72c4541822646fd24a19'
    print((hash256_sign(o_str)))
    pri_pem, pub_pem, private_path = generate_secp256r1_keypair_for_chainmaker()
    print("pri_pem:", pri_pem)
    print("pub_pem:", pub_pem)
    print("private_path:", private_path)
