# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     order_verify.py
# Description:  订单校验控制器
# Author:       ASUS
# CreateDate:   2026/01/05
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from logging import Logger
from playwright.async_api import Page
import qdairlines_helper.config.url_const as url_const
from flight_helper.utils.exception_utils import IPBlockError
from qdairlines_helper.po.order_verify_page import OrderVerifyPage
from qdairlines_helper.utils.po_utils import get_ip_access_blocked_msg


async def load_order_verify_po(
        *, page: Page, logger: Logger, protocol: str, domain: str, timeout: float = 60.0
) -> OrderVerifyPage:
    url_prefix = f"{protocol}://{domain}"
    order_verify_url = url_prefix + url_const.order_verify_url
    order_verify_po = OrderVerifyPage(page=page, url=order_verify_url)
    await order_verify_po.url_wait_for(url=order_verify_url, timeout=timeout)
    logger.info(f"即将进入青岛航空官网订单校验页面，页面URL<{order_verify_url}>")
    ip_access_blocked_msg = await get_ip_access_blocked_msg(page=page, timeout=3)
    if ip_access_blocked_msg:
        raise IPBlockError(ip_access_blocked_msg)
    return order_verify_po


async def order_verify(
        *, page: OrderVerifyPage, logger: Logger, refresh_attempt: int = 3, timeout: float = 60.0
) -> None:
    # 1. 先确认订单数据是否加载出来
    await page.get_order_info_plane(timeout=timeout, refresh_attempt=refresh_attempt)

    # 2. 勾选【同意条款】单选框
    agree_checkbox = await page.get_agree_checkbox(timeout=timeout)
    await agree_checkbox.click(button="left")
    logger.info(f"订单校验页面，规定及条款---【我已核对】单选框点击完成")

    # 3. 点击【下一步】
    next_btn = await page.get_next_btn(timeout=timeout)
    await next_btn.click(button="left")
    logger.info("订单校验页面，【下一步】按钮点击完成")

    # 4. 看看是否出现易盾校验码
    await page.handle_yidun_icon(logger=logger, timeout=5)
