# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     po_utils.py
# Description:  页面工具模块
# Author:       ASUS
# CreateDate:   2026/01/05
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from typing import Optional, List, Dict, Any
import qdairlines_helper.config.url_const as url_const
from playwright.async_api import Page, Locator, Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError


async def get_ip_access_blocked_msg(page: Page, timeout: float = 60.0) -> Optional[str]:
    selector: str = '//h3[contains(text(), "您的IP")]'
    locator: Locator = page.locator(selector=selector)
    try:
        await locator.first.wait_for(state='visible', timeout=timeout * 1000)
        return (await locator.inner_text()).strip()
    except (PlaywrightTimeoutError, PlaywrightError, Exception):
        return


def parse_user_info_from_page_response(network_logs: List[Dict[str, Any]]) -> dict:
    user_info = dict()
    for network_log in network_logs:
        try:
            if network_log.get('type') == 'response':
                if url_const.auth_form_api_url in (network_log.get("url") or ""):
                    body = network_log.get("body")
                    result = body.get('result')
                    user_info["access_token"] = result.get('access_token')
                    user_info["expires"] = result.get('expires_in')
                elif url_const.login_after_api_url in (network_log.get("url") or ""):
                    body = network_log.get("body")
                    result = body.get('result')
                    user_info["user_id"] = result.get('userId')
                    user_info["id"] = result.get('id')
            elif network_log.get('type') == 'request':
                if url_const.login_after_api_url in (network_log.get("url") or ""):
                    headers = network_log.get('headers')
                    headers.pop("referer", None)
                    headers.pop("timestamp", None)
                    user_info["headers"] = headers
        except (Exception,):
            pass
    return user_info
