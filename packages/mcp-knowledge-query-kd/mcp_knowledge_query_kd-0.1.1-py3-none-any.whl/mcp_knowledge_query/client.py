import json
import requests
import logging
from collections import OrderedDict
from typing import Dict, Any, Optional
from volcengine.auth.SignerV4 import SignerV4
from volcengine.auth.SignParam import SignParam
from volcengine.Credentials import Credentials

class HiAgentAuth:
    """
    HiAgent (Volcengine) 鉴权与请求处理类
    """
    def __init__(self, ak: str, sk: str, region: str = 'cn-north-1', service: str = 'app'):
        self.ak = ak
        self.sk = sk
        self.region = region
        self.service = service

    def make_request(
        self,
        host: str,
        action: str,
        version: str,
        data: Dict[str, Any],
        method: str = 'POST',
        path: str = '/'
    ) -> Optional[Dict[str, Any]]:
        """
        发送带鉴权的请求
        """
        # 1. 初始化签名器
        sign = SignerV4()

        # 2. 构造签名参数 (SignParam)
        param = SignParam()
        param.path = path
        param.method = method
        param.host = host
        # 遵循原有逻辑：签名时不包含 body 内容 (或者说是空字符串)，但在实际请求中发送 JSON body
        param.body = ''

        # 3. 设置 Query Params (Action, Version)
        query = OrderedDict()
        query['Action'] = action
        query['Version'] = version
        param.query = query

        # 4. 设置 Header
        header = OrderedDict()
        header['Host'] = host
        header['Content-Type'] = 'application/json'
        param.header_list = header

        # 5. 生成凭证并签名
        cren = Credentials(self.ak, self.sk, self.service, self.region)
        # 生成带签名的 query string
        result_url_query = sign.sign_url(param, cren)

        # 6. 发送请求
        request_url = f"{host}{path}?{result_url_query}"

        headers = {
            'Content-Type': 'application/json'
        }

        # 获取 logger
        logger = logging.getLogger(__name__)

        try:
            response = requests.request(
                method=method,
                url=request_url,
                headers=headers,
                data=json.dumps(data)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {e}")
            # 如果有响应内容，打印出来以便调试
            if getattr(e, 'response', None):
                 logger.error(f"响应内容: {e.response.text}")
            return None

