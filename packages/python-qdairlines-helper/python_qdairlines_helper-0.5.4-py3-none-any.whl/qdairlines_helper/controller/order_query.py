# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     order_query.py
# Description:  订单查询控制器
# Author:       ASUS
# CreateDate:   2026/01/04
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from typing import Any
from logging import Logger
from playwright.async_api import Page
import qdairlines_helper.config.url_const as url_const
from qdairlines_helper.po.air_order_page import AirOrderPage
from flight_helper.utils.exception_utils import IPBlockError
from qdairlines_helper.utils.po_utils import get_ip_access_blocked_msg


async def open_air_order_page(
        *, page: Page, logger: Logger, protocol: str, domain: str, timeout: float = 60.0
) -> AirOrderPage:
    url_prefix = f"{protocol}://{domain}"
    air_order_url = url_prefix + url_const.air_order_url
    await page.goto(air_order_url)

    air_order_po = AirOrderPage(page=page, url=air_order_url)
    await air_order_po.url_wait_for(url=air_order_url, timeout=timeout)
    logger.info(f"即将进入青岛航空官网航班查询页面，页面URL<{air_order_url}>")
    ip_access_blocked_msg = await get_ip_access_blocked_msg(page=page, timeout=3)
    if ip_access_blocked_msg:
        raise IPBlockError(ip_access_blocked_msg)
    return air_order_po


async def is_open_air_order_page_callback(
        *, page: Page, protocol: str, logger: Logger, domain: str, timeout: float = 60.0, **kwargs: Any
) -> bool:
    try:
        await open_air_order_page(page=page, logger=logger, protocol=protocol, domain=domain, timeout=timeout)
        return True
    except (Exception,):
        return False
