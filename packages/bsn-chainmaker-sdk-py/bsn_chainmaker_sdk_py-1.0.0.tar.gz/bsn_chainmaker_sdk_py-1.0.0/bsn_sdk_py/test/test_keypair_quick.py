# -*- coding:utf-8 -*-
"""
快速测试 secp256r1 密钥对生成函数
独立版本，不依赖 hfc 模块
"""
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat


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


def test_generate_secp256r1_keypair_for_chainmaker():
    """测试生成 secp256r1 密钥对"""
    print("=" * 60)
    print("测试生成 secp256r1 密钥对（Chainmaker）")
    print("=" * 60)
    
    # 生成密钥对（不保存文件）
    pri_pem, pub_pem, private_path = generate_secp256r1_keypair_for_chainmaker()
    
    print("\n【私钥 PEM】")
    print(pri_pem.decode('utf-8'))
    
    print("\n【公钥 PEM】")
    print(pub_pem.decode('utf-8'))
    
    print(f"\n【私钥路径】: {private_path}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_generate_secp256r1_keypair_for_chainmaker()
