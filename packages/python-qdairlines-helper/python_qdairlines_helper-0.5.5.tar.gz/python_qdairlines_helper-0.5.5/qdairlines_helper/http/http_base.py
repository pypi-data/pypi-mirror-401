# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     http_base.py
# Description:  http基础模块
# Author:       ASUS
# CreateDate:   2026/01/13
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from aiohttp import CookieJar
from typing import Optional, Dict, Any
from flight_helper.models.dto.http_schema import HTTPRequestDTO
from http_helper.client.async_proxy import HttpClientFactory as _HttpClientFactory


class HttpBase(object):

    def __init__(self, *, http_request_dto: HTTPRequestDTO, cookie_jar: Optional[CookieJar] = None):
        self._domain = http_request_dto.http_domain or "127.0.0.1:18070"
        self._protocol = http_request_dto.http_protocol or "http"
        self._timeout = http_request_dto.timeout or 60
        self._retry = http_request_dto.retry or 0
        self._token = http_request_dto.token
        self._origin = f"{self._protocol}://{self._domain}"
        self._enable_log = http_request_dto.enable_log if http_request_dto.enable_log is not None else True
        self._cookie_jar = cookie_jar or CookieJar()
        self._proxy = http_request_dto.proxy
        self._playwright_state: Dict[str, Any] = http_request_dto.storage_state
        self.http_client: Optional[_HttpClientFactory] = None

    def _get_http_client(self) -> _HttpClientFactory:
        """延迟获取 HTTP 客户端"""
        if self.http_client is None:
            self.http_client = _HttpClientFactory(
                protocol=self._protocol,
                domain=self._domain,
                timeout=self._timeout,
                retry=self._retry,
                enable_log=self._enable_log,
                cookie_jar=self._cookie_jar,
                playwright_state=self._playwright_state
            )
        return self.http_client

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "content-type": "application/json;charset=utf-8",
            "origin": self._domain,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "authorization": f"Bearer {self._token}"
        }
        return headers
