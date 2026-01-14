# -*- coding:utf-8 -*-
"""
Base client class for all blockchain framework clients
"""
# Delay Config import to avoid protobuf conflicts with chainmaker
# Config will be imported when needed
# from bsn_sdk_py.client.config import Config
from bsn_sdk_py.common.api_requestor import APIRequestor
from bsn_sdk_py.until.bsn_logger import log_info


class BaseClient(object):
    """
    Base client class for unified blockchain app requests
    All framework-specific clients should inherit from this class
    """

    def __init__(self):
        self.config = None
        self.framework_type = None

    def set_config(self, config):  # type: (object) -> None
        """
        Set configuration for the client
        :param config: Config object
        """
        self.config = config

    def build_req_data(self, req_body):
        """
        Uniformly create the request message
        :param req_body: request body
        :return: build result
        """
        data = {
            "header": {
                "userCode": self.config.user_code,
                "appCode": self.config.app_code,
            },
            "body": req_body,
            "mac": "",
        }
        return data

    def common_request(self, req_url, req_data):
        """
        Send HTTP POST request
        :param req_url: request url
        :param req_data: request data
        :return: response result
        """
        res = APIRequestor().request_post(req_url, req_data)
        return res

    def get_api_base_path(self):
        """
        Get API base path for the framework
        Should be overridden by subclasses
        :return: API base path (e.g., "/api/chainmaker/v1")
        """
        raise NotImplementedError("Subclasses must implement get_api_base_path()")



