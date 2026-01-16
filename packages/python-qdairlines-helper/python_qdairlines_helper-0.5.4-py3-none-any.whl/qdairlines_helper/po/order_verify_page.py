# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     order_verify_page.py
# Description:  订单校验页面对象
# Author:       ASUS
# CreateDate:   2026/01/04
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from logging import Logger
from typing import Optional
from playwright.async_api import Page, Locator
from playwright_helper.libs.base_po import BasePo
import qdairlines_helper.config.url_const as url_const
from playwright.async_api import Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError


class OrderVerifyPage(BasePo):
    url: str = url_const.order_verify_url
    __page: Page

    def __init__(self, page: Page, url: Optional[str] = None) -> None:
        super().__init__(page, url or url_const.order_verify_url)
        self.__page = page

    async def handle_yidun_icon(self, logger: Logger, timeout: float = 20.0) -> None:
        """
        获取订单校验页中的易盾校验弹框
        :param logger: 日志对象
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=//div[@class="yidun_intelli-tips"]//div[@class="yidun_intelli-icon"]'
        try:
            locator: Locator = await self.get_locator(selector=selector, timeout=timeout, strict=False)
            await locator.click(button="left")
            logger.info(f"订单校验页面，易盾校验框【易盾icon】点击完成")
        except (Exception,):
            pass

    async def get_order_info_plane(self, timeout: float = 5.0, refresh_attempt: int = 3) -> Locator:
        """
        获取订单校验页中的订单信息版面，注意这里有个小坑，经常出现已经进入了该页面，但是订单信息没有加载出来，需要不断尝试刷新页面
        :param timeout: 超时时间（秒）
        :param refresh_attempt: 尝试刷新次数
        :return: (是否存在, 错误信息|元素对象)
        """
        attempt = 0
        selector: str = 'xpath=//div[@class="order_info"]'
        while attempt <= refresh_attempt:
            try:
                await self.__page.reload(timeout=timeout * 1000)
                return await self.get_locator(selector=selector, timeout=timeout)
            except (PlaywrightError, PlaywrightTimeoutError, EnvironmentError, RuntimeError, Exception) as e:
                attempt += 1
        raise RuntimeError("订单校验页面中的订单信息加载出现异常，可能是网络拥塞或者用户被风控")

    async def get_agree_checkbox(self, timeout: float = 5.0) -> Locator:
        """
        获取订单校验页中的【同意条款】单选框
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=//span[@class="el-checkbox__inner"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_next_btn(self, timeout: float = 5.0) -> Locator:
        """
        获取添加乘客页中的【下一步】按钮
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=//span[contains(text(), "立即购票")]'
        return await self.get_locator(selector=selector, timeout=timeout)
