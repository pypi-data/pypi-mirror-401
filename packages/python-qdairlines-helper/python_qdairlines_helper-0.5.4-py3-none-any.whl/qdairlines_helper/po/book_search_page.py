# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     book_search_page.py
# Description:  预订查询页面对象
# Author:       ASUS
# CreateDate:   2026/01/04
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import re
from logging import Logger
from playwright.async_api import Page, Locator
from playwright_helper.libs.base_po import BasePo
from typing import Optional, Dict, Any, List, Literal
import qdairlines_helper.config.url_const as url_const
from flight_helper.utils.exception_utils import ProductTypeError
from playwright_helper.utils.type_utils import convert_order_amount_text, safe_convert_advanced
from playwright.async_api import Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError


class BookSearchPage(BasePo):
    url: str = url_const.book_search_url
    __page: Page

    def __init__(self, page: Page, url: Optional[str] = None) -> None:
        super().__init__(page, url or url_const.book_search_url)
        self.__page = page

    async def get_empyt_data_page(self, timeout: float = 5.0) -> Locator:
        """
        打开搜索页后，看看当前默认状态是不是空数据页，非空数据页，会有弹框
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息 | 元素对象)
        """
        selector: str = '//strong[contains(text(), "没有在飞航班")]'
        return await self.get_locator(selector=selector, timeout=timeout)

    @staticmethod
    def _get_reminder_dialog_selector() -> str:
        return '//div[@class="el-dialog__body"]//button[contains(@class, "search_btn")]'

    async def is_exist_reminder_dialog(self) -> bool:
        # 使用 count() 快速判断是否存在（不会因找不到而抛异常）
        return await self.__page.locator(selector=self._get_reminder_dialog_selector()).count() > 0

    async def get_reminder_dialog_continue_book_btn(self, timeout: float = 5.0) -> Locator:
        """
        获取预订搜索页的温馨提醒弹框中的【继续购票】按钮
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        return await self.get_locator(selector=self._get_reminder_dialog_selector(), timeout=timeout)

    async def get_depart_city_input(self, timeout: float = 5.0) -> Locator:
        """
        获取预订搜索页搜索栏的起飞城市输入框
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = '//div[contains(@class, "flight_search_form")]//input[@id="orig"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    @staticmethod
    def _get_city_search_result_selector(city_name: str, endpoint: Literal["orig", "dest"]) -> str:
        return f'xpath=//div[@name="{endpoint}" and @class="vcp-select"]//span[contains(text(), "{city_name}")]/..'

    async def get_depart_city_search_result(self, depart_city: str, timeout: float = 5.0) -> Locator:
        """
        获取预订搜索页搜索栏的起飞城市搜索结果
        :param depart_city: 起飞城市
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector = self._get_city_search_result_selector(city_name=depart_city, endpoint="orig")
        return await self.get_locator(selector=selector, timeout=timeout, strict=False)

    async def get_arrive_city_input(self, timeout: float = 5.0) -> Locator:
        """
        获取预订搜索页搜索栏的抵达城市输入框
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = '//div[contains(@class, "flight_search_form")]//input[@id="dest"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_arrive_city_search_result(self, arrive_city: str, timeout: float = 5.0) -> Locator:
        """
        获取预订搜索页搜索栏的抵达城市搜索结果
        :param arrive_city: 抵达城市
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector = self._get_city_search_result_selector(city_name=arrive_city, endpoint="dest")
        return await self.get_locator(selector=selector, timeout=timeout, strict=False)

    async def get_depart_date_input(self, timeout: float = 5.0) -> Locator:
        """
        获取预订搜索页搜索栏的起飞日期输入框
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = '//div[contains(@class, "flight_search_form")]//input[contains(@placeholder, "去程日期")]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_flight_query_btn(self, timeout: float = 5.0) -> Locator:
        """
        获取预订搜索页搜索栏的【查询机票】按钮
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = '//div[contains(@class, "flight_search_form")]//button[@class="search_btn"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_flight_info_plane(self, flight_no: str, timeout: float = 5.0) -> Locator:
        """
        获取预订搜索页航班内容栏航班基本信息
        :param flight_no: 航班编号
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        try:
            selector: str = f'//div[contains(@class, "flight_qda")]/span[contains(text(), "{flight_no}")]/../../../..'
            return await self.get_locator(selector=selector, timeout=timeout)
        except (Exception,):
            raise RuntimeError(f"航班预订查询页面，没有搜索到航班<{flight_no}>数据")

    async def get_flight_product_nav(self, locator: Locator, product_type: str, timeout: float = 5.0) -> Locator:
        """
        获取预订搜索页航班产品类型nav
        :param timeout: 超时时间（秒）
        :param product_type: 产品类型
        :param locator: flight_info_plane Locator 对象
        :return: (是否存在, 错误信息|元素对象)
        """
        if product_type == "经济舱":
            index = 1
        elif product_type == "超级经济舱":
            index = 2
        elif product_type == "公务舱":
            index = 3
        else:
            raise ProductTypeError(product_type=product_type)
        selector: str = f'xpath=(.//div[contains(@class, "nav_item el-col el-col-24")])[{index}]'
        return await self.get_sub_locator(locator=locator, selector=selector, timeout=timeout)

    async def get_more_product_btn(self, locator: Locator, timeout: float = 5.0) -> Locator:
        """
        获取预订搜索页航班列表更多产品
        :param timeout: 超时时间（秒）
        :param locator: flight_info_plane Locator 对象
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = f'xpath=.//span[@class="fa el-icon-caret-bottom"]'
        return await self.get_sub_locator(locator=locator, selector=selector, timeout=timeout)

    async def get_flight_products(self, locator: Locator, logger: Logger, flight_no: str) -> List[Dict[str, Any]]:
        """
        获取预订搜索页航班内容栏所有航班产品
        :param locator: flight_info_plane Locator 对象
        :param logger: Logger 对象，日志记录
        :param flight_no: 航班编号
        :return: (是否存在, 错误信息|元素对象)
        """
        timeout: float = 1.0
        selector: str = 'xpath=.//div[@class="text-center cabinClasses_info el-row" and not(@style="display: none;")]//table/tbody/tr[not(@class)]/td[@class]/..'
        products_locator: Locator = await self.get_sub_locator(locator=locator, selector=selector, timeout=timeout)
        locators: List[Locator] = await products_locator.all()
        flight_products = list()
        logger.info(f"当前找到了关于航班<{flight_no}>的<{len(locators)}>条产品数据")
        for locator in locators:
            try:
                booking_btn: Locator = await self._get_flight_product_booking_btn(locator=locator, timeout=timeout)
                amounts: Dict[str, Any] = await self._get_flight_product_price(locator=locator, timeout=timeout)
                seats_status: int = await self._get_flight_product_seats_status(locator=locator, timeout=timeout)
                cabin = await self._get_flight_product_cabin(locator=locator, timeout=timeout)
                ticket_info: str = await self._get_flight_product_ticket_info(locator=locator, timeout=timeout)
                flight_products.append(dict(
                    amounts=amounts, cabin=cabin, seats_status=seats_status, booking_btn=booking_btn,
                    ticket_info=ticket_info
                ))
            except (PlaywrightError, PlaywrightTimeoutError, EnvironmentError, RuntimeError, Exception) as e:
                logger.error(e)
                continue
        return flight_products

    async def _get_flight_product_cabin(self, locator: Locator, timeout: float = 5.0) -> str:
        """
        获取预订搜索页航班内容栏航班产品下的舱位
        :param timeout: 超时时间（秒）
        :param locator: flight_product Locator 对象
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=.//div[@class="ticket_clazz"]/div/span'
        locator: Locator = await self.get_sub_locator(locator=locator, selector=selector, timeout=timeout)
        text: str = (await locator.inner_text(timeout=timeout * 1000)).strip()
        match = re.search(r'\((.*?)舱\)', text)
        if match:
            return match.group(1).strip()
        raise RuntimeError(f"获取到的航班舱位信息：{text}，提取异常")

    async def _get_flight_product_price(self, locator: Locator, timeout: float = 5.0) -> Dict[str, Any]:
        """
        获取预订搜索页航班内容栏航班产品下的销售价格
        :param timeout: 超时时间（秒）
        :param locator: flight_product Locator 对象
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=.//div[@class="price_flex_top"]'
        locator: Locator = await self.get_sub_locator(locator=locator, selector=selector, timeout=timeout)
        amount_text: str = (await locator.inner_text(timeout=timeout * 1000)).strip()
        return convert_order_amount_text(amount_text=amount_text)

    async def _get_flight_product_booking_btn(self, locator: Locator, timeout: float = 5.0) -> Locator:
        """
        获取预订搜索页航班内容栏航班产品下的【购票】按钮
        :param timeout: 超时时间（秒）
        :param locator: flight_product Locator 对象
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=(.//td[@class="ticket_num"]/div/span)[1]'
        return await self.get_sub_locator(locator=locator, selector=selector, timeout=timeout)

    async def _get_flight_product_ticket_info(self, locator: Locator, timeout: float = 5.0) -> Optional[str]:
        """
        获取预订搜索页航班内容栏航班产品下的单据信息
        :param timeout: 超时时间（秒）
        :param locator: flight_product Locator 对象
        :return: (是否存在, 错误信息|元素对象)
        """
        try:
            selector: str = 'xpath=.//td[@class="ticket_info"]//span[contains(@class, "text-left")]'
            locator = await self.get_sub_locator(locator=locator, selector=selector, timeout=timeout)
            return (await locator.inner_text()).strip()
        except (Exception,):
            return

    async def _get_flight_product_seats_status(self, locator: Locator, timeout: float = 5.0) -> int:
        """
        获取预订搜索页航班内容栏航班产品下的余票信息
        :param timeout: 超时时间（秒）
        :param locator: flight_product Locator 对象
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=(.//td[@class="ticket_num"]/div/span)[2]'
        locator: Locator = await self.get_sub_locator(locator=locator, selector=selector, timeout=timeout)
        more_seats_text: str = (await locator.inner_text(timeout=timeout * 1000)).strip()
        match = re.search(r'\d+', more_seats_text)
        if match:
            # ⚠️ 正则 \d+ 没有捕获组，只能用 group(0) 或 group()
            return safe_convert_advanced(value=match.group().strip())
        else:
            return 999999
