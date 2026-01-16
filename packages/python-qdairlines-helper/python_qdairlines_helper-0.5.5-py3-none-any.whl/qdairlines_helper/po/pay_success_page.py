# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     pay_success_page.py
# Description:  支付成功页面对象
# Author:       ASUS
# CreateDate:   2026/01/09
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from typing import Optional
from playwright.async_api import Page, Locator
from playwright_helper.libs.base_po import BasePo
import qdairlines_helper.config.url_const as url_const


class PaySuccessPage(BasePo):
    url: str = url_const.pay_success_url
    __page: Page

    def __init__(self, page: Page, url: Optional[str] = None) -> None:
        super().__init__(page, url or url_const.pay_success_url)
        self.__page = page

    async def get_pay_success_image(self, timeout: float = 5.0) -> Locator:
        """
        获取支付成功image图标
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = '//img[@alt="支付成功"]'
        return await self.get_locator(selector=selector, timeout=timeout)
