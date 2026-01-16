# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     home.py
# Description:  主页控制器模块
# Author:       ASUS
# CreateDate:   2026/01/04
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from logging import Logger
from playwright.async_api import Page
from qdairlines_helper.po.home_page import HomePage
import qdairlines_helper.config.url_const as url_const
from flight_helper.utils.exception_utils import IPBlockError
from qdairlines_helper.utils.po_utils import get_ip_access_blocked_msg


async def load_home_po(*, page: Page, logger: Logger, protocol: str, domain: str, timeout: float = 60.0) -> HomePage:
    url_prefix = f"{protocol}://{domain}"
    home_url = url_prefix + url_const.home_url
    home_po = HomePage(page=page, url=home_url)
    await home_po.url_wait_for(url=home_url, timeout=timeout)
    logger.info(f"即将进入青岛航空官网首页，页面URL<{home_url}>")
    ip_access_blocked_msg = await get_ip_access_blocked_msg(page=page, timeout=3)
    if ip_access_blocked_msg:
        raise IPBlockError(ip_access_blocked_msg)
    return home_po
