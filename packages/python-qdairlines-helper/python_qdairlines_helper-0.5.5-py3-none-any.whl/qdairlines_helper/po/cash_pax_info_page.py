# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     cash_pax_info_page.py
# Description:  支付类型页面对象
# Author:       ASUS
# CreateDate:   2026/01/05
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from typing import Optional
from urllib.parse import urlparse, parse_qs
from playwright.async_api import Page, Locator
from playwright_helper.libs.base_po import BasePo
import qdairlines_helper.config.url_const as url_const
from flight_helper.utils.exception_utils import PaymentChannelError


class CashPaxInfoPage(BasePo):
    url: str = url_const.cash_pax_info_url
    __page: Page

    def __init__(self, page: Page, url: Optional[str] = None) -> None:
        super().__init__(page, url or url_const.cash_pax_info_url)
        self.__page = page

    async def get_payment_channel_checkbox(self, channel_name: str, timeout: float = 5.0) -> Locator:
        """
        获取支付方式页面中的支付渠道【支付宝|微信|汇付天下|易宝支付】单选框
        :param channel_name: 支付渠道，支付宝|微信|汇付天下|易宝支付
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        if channel_name == '支付宝':
            for_class = 0
        elif channel_name == "微信":
            for_class = 1
        elif channel_name == "汇付天下":
            for_class = 2
        elif channel_name == "易宝支付":
            for_class = 3
        else:
            raise PaymentChannelError(channel_name=channel_name)
        selector: str = f'xpath=//label[@for="passengerAdult{for_class}"]//span[@class="checkbox"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_confirm_payment_btn(self, timeout: float = 5.0) -> Locator:
        """
        获取支付方式页面中的【确认支付】按钮
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = '//button[@class="search_btn" and contains(text(), "确认支付")]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_pre_order_no(self, timeout: float = 5.0) -> str:
        """
        获取青岛航空官网订单号
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        try:
            query = urlparse(self.__page.url).query
            params = parse_qs(query)
            # 取第一个值（即使有多个 orderNo）
            pre_order_no = params.get('orderNo', [""])[0]
            if pre_order_no and len(pre_order_no) == 18 and pre_order_no.startswith("OW") is True:
                return pre_order_no
        except (Exception,):
            pass
        selector: str = '//div[@class="order-form"]//span[contains(text(), "订单编号")]/../span[@class="font_red"]'
        locator = await self.get_locator(selector=selector, timeout=timeout)
        return (await locator.inner_text()).strip()
