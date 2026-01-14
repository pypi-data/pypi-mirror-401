# -*- coding:utf-8 -*-
"""
BSN SDK Python Package
Supports Chainmaker blockchain framework.

使用示例:
    from bsn_sdk_py.client import ChainmakerClient, Config
    
    client = ChainmakerClient()
    client.set_config(config)
"""
__auther__ = 'hll'
__version__ = '1.0.7'

# 导出通用配置类和 ChainMaker 客户端
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.chainmaker import ChainmakerClient

__all__ = [
    'Config',
    'ChainmakerClient',
]
