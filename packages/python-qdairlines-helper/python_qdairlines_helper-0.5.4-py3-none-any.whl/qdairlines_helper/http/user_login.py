# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     user_login.py
# Description:  用户登录模块
# Author:       ASUS
# CreateDate:   2026/01/13
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from aiohttp import CookieJar
from typing import Optional, Dict, Any
from qdairlines_helper.http.http_base import HttpBase
import qdairlines_helper.config.url_const as url_const
from flight_helper.models.dto.http_schema import HTTPRequestDTO


class UserLogin(HttpBase):
    def __init__(self, *, http_request_dto: HTTPRequestDTO, cookie_jar: Optional[CookieJar] = None):
        super().__init__(http_request_dto=http_request_dto, cookie_jar=cookie_jar)

    async def get_user_info(
            self, *, proxy: Optional[Dict[str, Any]] = None, headers: Dict[str, str] = None,
            is_end: Optional[bool] = None
    ) -> Dict[str, Any]:
        _headers = self._get_headers()
        if headers is not None:
            _headers.update(headers)
        _headers["referer"] = f"{self._origin}{url_const.login_url}"
        if is_end is None:
            is_end = True
        if proxy:
            self._proxy = proxy
        exception_keywords = [r'<h3[^>]*class="font-bold"[^>]*>([^<]+)</h3>']
        return await self._get_http_client().request(
            method="GET",
            url=url_const.login_after_api_url,
            headers=_headers,
            is_end=is_end,
            proxy_config=self._proxy or None,
            exception_keywords=exception_keywords
        )
