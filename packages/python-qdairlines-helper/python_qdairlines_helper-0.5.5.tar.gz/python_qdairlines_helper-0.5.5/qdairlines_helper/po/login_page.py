# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     login_page.py
# Description:  登录页面对象
# Author:       ASUS
# CreateDate:   2026/01/04
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from typing import Optional
from playwright.async_api import Page, Locator
from playwright_helper.libs.base_po import BasePo
import qdairlines_helper.config.url_const as url_const


class LoginPage(BasePo):
    url: str = url_const.login_url
    __page: Page

    def __init__(self, page: Page, url: Optional[str] = None) -> None:
        super().__init__(page, url or url_const.login_url)
        self.__page = page

    async def get_login_username_input(self, timeout: float = 5.0) -> Locator:
        """
        获取登录页面的会员卡号输入框
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = '//input[@id="username"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_login_password_input(self, timeout: float = 5.0) -> Locator:
        """
        获取登录页面的密码输入框
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = '//input[@id="password"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_check_logo_icon(self, timeout: float = 5.0) -> Locator:
        """
        获取易盾校验logo图标
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = '//div[@class="yidun_intelli-icon"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_check_pass_text(self, timeout: float = 5.0) -> str:
        """
        点击易盾校验logo图标后，获取验证成功的文案
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = '//span[@class="yidun_tips__text yidun-fallback__tip" and contains(text(), "验证成功")]'
        locator = await self.get_locator(selector=selector, timeout=timeout)
        return (await locator.inner_text()).strip()

    async def get_login_btn(self, timeout: float = 5.0) -> Locator:
        """
        获取登录按钮
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = '//button[@class="search_btn"]'
        return await self.get_locator(selector=selector, timeout=timeout)
