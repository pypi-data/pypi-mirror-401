# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     nhlms_cash_desk_page.py
# Description:  汇付天下收银台页面对象
# Author:       ASUS
# CreateDate:   2026/01/05
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import asyncio
from logging import Logger
from typing import Optional, Any
from collections import OrderedDict
from datetime import datetime, timedelta
from playwright.async_api import Page, Locator
from playwright_helper.libs.base_po import BasePo
import qdairlines_helper.config.url_const as url_const
from playwright_helper.utils.type_utils import safe_convert_advanced
from flight_helper.utils.exception_utils import HFPaymentTypeError, PaymentFailError
from playwright.async_api import Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError


class NhlmsCashDeskPage(BasePo):
    url: str = url_const.nhlms_cashdesk_url
    __page: Page

    def __init__(self, page: Page, url: Optional[str] = None) -> None:
        super().__init__(page, url or url_const.nhlms_cashdesk_url)
        self.__page = page

    async def get_order_amount(self, timeout: float = 5.0) -> Any:
        """
        获取汇付天下收银台页的支付金额
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=//div[@class="form-text-info recharge"]'
        locator: Locator = await self.get_locator(selector=selector, timeout=timeout)
        return safe_convert_advanced((await locator.inner_text()).strip())

    async def get_order_transaction(self, timeout: float = 5.0) -> str:
        """
        获取汇付天下收银台页的订单流水
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=//div[@class="mer-info"]//span[contains(text(), "订单号")]//span'
        locator: Locator = await self.get_locator(selector=selector, timeout=timeout)
        return (await locator.inner_text()).strip()

    async def get_payment_type_tab(self, payment_type: str = "付款账户支付", timeout: float = 5.0) -> Locator:
        """
        获取汇付天下收银台页的付款方式tab
        :param payment_type: 付款方式，包括：付款账户支付|保理账户支付|个人网银|企业网银|快捷支付
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        if payment_type == '付款账户支付':
            value = "ap"
        elif payment_type == "保理账户支付":
            value = "bl"
        elif payment_type == "个人网银":
            value = "user"
        elif payment_type == "企业网银":
            value = "mer"
        elif payment_type == "快捷支付":
            value = "fp"
        else:
            raise HFPaymentTypeError(payment_type=payment_type)
        selector: str = f'//div[@class="content-bottom network-recharge"]//li[@value="{value}"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_username_input(self, timeout: float = 5.0) -> Locator:
        """
        获取汇付天下收银台页的操作员号输入框
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=//div[@class="content-bottom network-recharge"]//input[@id="userId"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_password_input(self, timeout: float = 5.0) -> Locator:
        """
        获取汇付天下收银台页的密码输入框
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=//div[@class="content-bottom network-recharge"]//input[@id="usrPw"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def get_confirm_payment_btn(self, timeout: float = 5.0) -> Locator:
        """
        获取汇付天下收银台页中的【确认支付】按钮
        :param timeout: 超时时间（秒）
        :return: (是否存在, 错误信息|元素对象)
        """
        selector: str = 'xpath=//div[@class="content-bottom network-recharge"]//button[@id="submitBtn"]'
        return await self.get_locator(selector=selector, timeout=timeout)

    async def check_is_pay_success(self, logger: Logger) -> None:
        """检查支付是否成功"""
        data = OrderedDict([
            ("支付成功", 'xpath=//img[@alt="支付成功"]'),
            (PaymentFailError("账户余额不足"), 'xpath=//span[contains(text(), "账户余额不足")]'),
            (
                PaymentFailError(
                    "尊敬的旅客:您的IP由于频繁访问已受限，客票预定可前往青岛航空微信公众号预定。如您需要办理其他客票业务，请联系官方客服热线：0532-96630。"
                ),
                '//h3[contains(text(), "您的IP")]'
            )
        ])
        timeout = 60
        end_time = datetime.now() + timedelta(seconds=timeout)

        while datetime.now() < end_time:
            for index, (outcome, selector) in enumerate(data.items()):
                try:
                    await self.get_locator(selector=selector, timeout=1)
                    if index == 0:
                        logger.info(f"支付结果检测：{outcome}")
                        return  # 成功
                    else:
                        # 一旦匹配失败，立即抛出！
                        raise outcome
                except (PlaywrightTimeoutError, PlaywrightError, RuntimeError):
                    # 只捕获“未找到元素”的异常，其他异常往上抛
                    continue
                except Exception:
                    # 可选：记录未知异常，但不吞掉
                    raise  # 或 log 后 re-raise

            await asyncio.sleep(0.5)  # 避免 CPU 占用过高
        logger.error(f"支付结果检测：超时，当前页面url: {self.__page.url}")
        raise PlaywrightTimeoutError(f"支付结果检测超时，{timeout}秒内未出现成功或已知失败状态")
