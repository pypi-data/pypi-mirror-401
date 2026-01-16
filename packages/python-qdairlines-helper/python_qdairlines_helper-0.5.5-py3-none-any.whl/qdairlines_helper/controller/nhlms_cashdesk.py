# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     nhlms_cashdesk.py
# Description:  汇付天下收银台控制器
# Author:       ASUS
# CreateDate:   2026/01/05
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import inspect
from logging import Logger
from typing import Callable
from playwright.async_api import BrowserContext
import qdairlines_helper.config.url_const as url_const
from flight_helper.utils.exception_utils import DuplicatePaymentError
from qdairlines_helper.po.nhlms_cash_desk_page import NhlmsCashDeskPage
from playwright_helper.utils.browser_utils import switch_for_table_window
from flight_helper.models.dto.payment import HFPaidAccountPaymentInputDTO, PaymentResultDTO


async def load_nhlms_cash_desk_po(
        *, context: BrowserContext, logger: Logger, domain: str, protocol: str, timeout: float = 60.0
) -> NhlmsCashDeskPage:
    url_prefix = f"{protocol}://{domain}"
    nhlms_cashdesk_url = url_prefix + url_const.nhlms_cashdesk_url

    current_page = await switch_for_table_window(
        browser=context, url_keyword=url_const.nhlms_cashdesk_url, wait_time=int(timeout)
    )

    nhlms_cashdesk_po = NhlmsCashDeskPage(page=current_page, url=nhlms_cashdesk_url)
    await nhlms_cashdesk_po.url_wait_for(url=nhlms_cashdesk_url, timeout=timeout)
    logger.info(f"即将进入汇付天下收银台页面，页面URL<{nhlms_cashdesk_url}>")
    return nhlms_cashdesk_po


async def hf_paid_account_payment(
        *, page: NhlmsCashDeskPage, logger: Logger, order_no: int, is_pay_completed_callback: Callable,
        hf_paid_account_payment_dto: HFPaidAccountPaymentInputDTO, timeout: float = 60.0
) -> PaymentResultDTO:
    # 1. 获取收银台支付流水
    pay_transaction = await page.get_order_transaction(timeout=timeout)
    logger.info(f"汇付天下收银台页面，支付流水<{pay_transaction}>获取完成")

    # 2. 获取订单支付金额
    actual_payment_amount = await page.get_order_amount(timeout=timeout)
    logger.info(f"汇付天下收银台页面，支付金额<{actual_payment_amount}>获取完成")

    # 3. 获取付款方式tab
    payment_type_tab = await page.get_payment_type_tab(
        payment_type=hf_paid_account_payment_dto.payment_type, timeout=timeout
    )
    await payment_type_tab.click(button="left")
    logger.info(f"汇付天下收银台页面，【{hf_paid_account_payment_dto.payment_type}】Tab点击完成")

    # 4. 输入操作员号
    username_input = await page.get_username_input(timeout=timeout)
    await username_input.fill(value=hf_paid_account_payment_dto.account)
    logger.info(f"汇付天下收银台页面，操作员号<{hf_paid_account_payment_dto.account}>输入完成")

    # 5. 输入交易密码
    password_input = await page.get_password_input(timeout=timeout)
    await password_input.fill(value=hf_paid_account_payment_dto.password)
    logger.info(f"汇付天下收银台页面，交易密码<{hf_paid_account_payment_dto.password}>输入完成")

    # 6. 校验订单是否已经被支付
    if inspect.iscoroutinefunction(is_pay_completed_callback):
        is_pay: bool = await is_pay_completed_callback(order_id=order_no)
    else:
        is_pay: bool = is_pay_completed_callback(order_id=order_no)
    if is_pay is True:
        raise DuplicatePaymentError(order_no=order_no)

    # 6. 点击【确认支付】
    confirm_payment_btn = await page.get_confirm_payment_btn(timeout=timeout)
    await confirm_payment_btn.click(button="left")
    logger.info("汇付天下收银台页面，【确认支付】按钮点击完成")
    return PaymentResultDTO(
        channel_name=hf_paid_account_payment_dto.channel_name,
        payment_type=hf_paid_account_payment_dto.payment_type,
        account=hf_paid_account_payment_dto.account,
        password=hf_paid_account_payment_dto.password,
        order_no=order_no,
        pay_amount=actual_payment_amount,
        pay_transaction=pay_transaction
    )
