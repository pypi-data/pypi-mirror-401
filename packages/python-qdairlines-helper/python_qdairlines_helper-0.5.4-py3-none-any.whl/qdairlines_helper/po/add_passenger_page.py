# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     add_passenger_page.py
# Description:  添加乘客页面对象
# Author:       ASUS
# CreateDate:   2026/01/04
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from typing import Optional
from playwright.async_api import Page, Locator
from playwright_helper.libs.base_po import BasePo
import qdairlines_helper.config.url_const as url_const
from flight_helper.utils.exception_utils import PassengerTypeError


class AddPassengerPage(BasePo):
    url: str = url_const.add_passenger_url
    __page: Page

    def __init__(self, page: Page, url: Optional[str] = None) -> None:
        super().__init__(page, url or url_const.add_passenger_url)
        self.__page = page

    async def get_add_passenger_btn(self, passenger_type: str, timeout: float = 5.0) -> Locator:
        """
        获取添加乘客页中的【添加成人|添加儿童|添加婴儿】按钮
        :param passenger_type: 乘客类型，成人|儿童|婴儿
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        if passenger_type == '成人':
            btn_text = "添加成人"
        elif passenger_type == "儿童":
            btn_text = "添加儿童"
        elif passenger_type == "婴儿":
            btn_text = "添加婴儿"
        else:
            raise PassengerTypeError(passenger_type=passenger_type)
        selector: str = f'//div[@class="el-row"]//button[@class="search_btn" and contains(text(), "{btn_text}")]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_add_passenger_plane(self, timeout: float = 5.0, position_index: int = 0) -> Locator:
        """
        获取添加乘客页中的乘机人信息面板，按索引提取
        :param timeout: 超时时间（秒）
        :param position_index: 元素位置索引，该元素在页面中可能存在多组，默认从第0组开始
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = f'xpath=//label[@for="passengerAdult{position_index}"]/../../../..'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_passenger_type_checkbox(
            self, passenger_type: str, timeout: float = 5.0, position_index: int = 0
    ) -> Locator:
        """
        获取添加乘客页中的旅客类型【成人|儿童|婴儿】单选框
        :param passenger_type: 乘客类型，成人|儿童|婴儿
        :param timeout: 超时时间（秒）
        :param position_index: 元素位置索引，该元素在页面中可能存在多组，默认从第0组开始
        :return: (是否存在, 错误信息|元素对象)
        """
        if passenger_type == '成人':
            passenger_class = f"passengerAdult{position_index}"
        elif passenger_type == "儿童":
            passenger_class = f"passengerChild{position_index}"
        elif passenger_type == "婴儿":
            passenger_class = f"passengerBaby{position_index}"
        else:
            raise PassengerTypeError(passenger_type=passenger_type)
        selector: str = f'//label[@for="{passenger_class}"]/span[@class="checkbox"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_passenger_username_input(self, locator: Locator, timeout: float = 5.0) -> Locator:
        """
        获取添加乘客页中的乘客姓名输入框
        :param locator: 乘机人信息面板  passenger_plane的Locator对象
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=.//input[contains(@placeholder, "乘机人姓名")]'
        return await self.get_sub_locator(locator=locator, selector=selector, timeout=timeout)

    async def get_gender_checkbox(self, locator: Locator, gender: str, timeout: float = 5.0) -> Locator:
        """
        获取添加乘客页中的乘客性别【男|女】单选框
        :param locator: 乘机人信息面板  passenger_plane的Locator对象
        :param gender: 性别
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        if gender in ['male', '男', '男士', '男生']:
            index = 0
        else:
            index = -1
        selector: str = f'xpath=.//label[@tabindex="{index}"]//span[@class="el-radio__inner"]'
        return await self.get_sub_locator(locator=locator, selector=selector, timeout=timeout)

    async def get_id_type_dropdown(self, locator: Locator, timeout: float = 5.0) -> Locator:
        """
        获取添加乘客页中的证件号码类型下拉菜单按钮
        :param locator: 乘机人信息面板  passenger_plane的Locator对象
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = f'xpath=.//input[contains(@placeholder, "请选择")]'
        return await self.get_sub_locator(locator=locator, selector=selector, timeout=timeout)

    async def get_id_type_dropdown_selection(self, id_type: str = "身份证", timeout: float = 5.0) -> Locator:
        """
        获取添加乘客页中的证件号码类型下拉菜单按钮
        :param id_type: 乘机人的证件类型
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = f'xpath=//div[@x-placement="bottom-start"]//ul[@class="el-scrollbar__view el-select-dropdown__list"]//span[contains(text(), "{id_type}")]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_id_no_input(self, locator: Locator, timeout: float = 5.0) -> Locator:
        """
        获取添加乘客页中的乘客证件号码输入框
        :param locator: 乘机人信息面板  passenger_plane的Locator对象
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=.//input[contains(@placeholder, "请输入证件号")]'
        return await self.get_sub_locator(locator=locator, selector=selector, timeout=timeout)

    async def get_service_mobile_input(self, timeout: float = 5.0) -> Locator:
        """
        获取添加乘客页中的联系人手机号码输入框
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=//input[contains(@placeholder, "请输入联系人手机号码")]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_agree_checkbox(self, timeout: float = 5.0) -> Locator:
        """
        获取添加乘客页中的【已阅读并同意】单选框
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = f'xpath=//label[contains(text(), "已阅读并同意")]/../label/span'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_next_btn(self, timeout: float = 5.0) -> Locator:
        """
        获取添加乘客页中的【下一步】按钮
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=//div[@class="el-row"]//button[contains(text(), "下一步")]'
        return await self.get_locator(selector=selector, timeout=timeout)
