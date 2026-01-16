# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     pay_success.py
# Description:  支付成功控制器
# Author:       ASUS
# CreateDate:   2026/01/09
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from logging import Logger
from aiohttp import CookieJar
from playwright.async_api import Page
from typing import Dict, Any, Optional, Callable
import qdairlines_helper.config.url_const as url_const
from qdairlines_helper.po.pay_success_page import PaySuccessPage
from qdairlines_helper.po.nhlms_cash_desk_page import NhlmsCashDeskPage
from qdairlines_helper.utils.po_utils import get_ip_access_blocked_msg
from qdairlines_helper.controller.order_detail import get_order_detail
from flight_helper.models.dto.itinerary import QueryItineraryRequestDTO
from flight_helper.utils.exception_utils import IPBlockError, PaymentFailedError


async def load_pay_success_page(
        *, page: Page, logger: Logger, protocol: str, domain: str, timeout: float = 60.0
) -> PaySuccessPage:
    url_prefix = f"{protocol}://{domain}"
    pay_success_url = url_prefix + url_const.pay_success_url
    pay_success_po = PaySuccessPage(page=page, url=pay_success_url)
    await pay_success_po.url_wait_for(url=pay_success_url, timeout=timeout)
    logger.info(f"即将进入青岛航空官网支付成功页面，页面URL<{pay_success_url}>")
    ip_access_blocked_msg = await get_ip_access_blocked_msg(page=page, timeout=3)
    if ip_access_blocked_msg:
        raise IPBlockError(ip_access_blocked_msg)
    return pay_success_po


async def two_check_pay_success(
        *, page: NhlmsCashDeskPage, logger: Logger, query_dto: QueryItineraryRequestDTO, callback_get_proxy: Callable,
        cookie_jar: Optional[CookieJar] = None, timeout: float = 60.0, retry: int = 0, enable_log: bool = True
) -> None:
    try:
        # 1. 看支付成功页面是否加载完成
        await page.check_is_pay_success(logger=logger)
        return
    except Exception as e:
        logger.error(e)

    # 2. 尝试取查询票号，看订单状态，是 BOOKED，还是 TICKETED
    order_detail: Dict[str, Any] = await get_order_detail(
        query_dto=query_dto, timeout=int(timeout), retry=retry, enable_log=enable_log, cookie_jar=cookie_jar,
        callback_get_proxy=callback_get_proxy, logger=logger
    )
    order_status = (order_detail.get("orderStatus", "")).upper()
    if order_status not in ("TICKED", "PAYED"):
        raise PaymentFailedError(pre_order_no=query_dto.pre_order_no, order_status=order_status)
