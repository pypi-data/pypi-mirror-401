# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     cash_pax_info.py
# Description:  支付类型控制器
# Author:       ASUS
# CreateDate:   2026/01/05
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from logging import Logger
from playwright.async_api import Page
import qdairlines_helper.config.url_const as url_const
from flight_helper.utils.exception_utils import IPBlockError
from qdairlines_helper.po.cash_pax_info_page import CashPaxInfoPage
from qdairlines_helper.utils.po_utils import get_ip_access_blocked_msg


async def load_cash_pax_info_po(
        *, page: Page, logger: Logger, protocol: str, domain: str, timeout: float = 60.0
) -> CashPaxInfoPage:
    url_prefix = f"{protocol}://{domain}"
    cash_pax_info_url = url_prefix + url_const.cash_pax_info_url
    cash_pax_info_po = CashPaxInfoPage(page=page, url=cash_pax_info_url)
    await cash_pax_info_po.url_wait_for(url=cash_pax_info_url, timeout=timeout)
    logger.info(f"即将进入青岛航空官网支付方式页面，页面URL<{cash_pax_info_url}>")
    ip_access_blocked_msg = await get_ip_access_blocked_msg(page=page, timeout=3)
    if ip_access_blocked_msg:
        raise IPBlockError(ip_access_blocked_msg)
    return cash_pax_info_po


async def select_payment_channel(
        *, page: CashPaxInfoPage, logger: Logger, channel_name: str = "汇付天下", timeout: float = 60.0
) -> str:
    # 1. 获取青岛航空官网订单号
    pre_order_no = await page.get_pre_order_no(timeout=timeout)
    logger.info(f"选择支付方式页面，青岛航空官网订单号<{pre_order_no}>获取完成")

    # 2. 选择支付渠道【channel_name】
    payment_channel_checkbox = await page.get_payment_channel_checkbox(channel_name=channel_name, timeout=timeout)
    await payment_channel_checkbox.click(button="left")
    logger.info(f"选择支付方式页面，支付渠道【{channel_name}】单选框点击完成")

    # 3. 点击【确认支付】
    confirm_payment_btn = await page.get_confirm_payment_btn(timeout=timeout)
    await confirm_payment_btn.click(button="left")
    logger.info("选择支付方式页面，【确认支付】按钮点击完成")
    return pre_order_no
