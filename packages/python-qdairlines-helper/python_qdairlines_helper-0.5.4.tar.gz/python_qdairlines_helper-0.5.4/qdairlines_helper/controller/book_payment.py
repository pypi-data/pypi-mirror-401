# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     book_payment.py
# Description:  预订支付控制器
# Author:       ASUS
# CreateDate:   2026/01/04
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from logging import Logger
from aiohttp import CookieJar
from playwright.async_api import Page
from typing import Any, List, Callable, Optional, Dict
from flight_helper.models.dto.passenger import PassengerDTO
from flight_helper.models.dto.itinerary import QueryItineraryRequestDTO
from qdairlines_helper.controller.pay_success import two_check_pay_success
from flight_helper.models.dto.booking import BookingInputDTO, OneWayBookingDTO
from qdairlines_helper.controller.book_search import open_book_search_page, book_search
from qdairlines_helper.controller.order_verify import load_order_verify_po, order_verify
from flight_helper.utils.exception_utils import PaymentChannelMissError, PaymentTypeError
from flight_helper.models.dto.payment import HFPaidAccountPaymentInputDTO, PaymentResultDTO
from qdairlines_helper.controller.add_passenger import add_passenger, load_add_passenger_po
from qdairlines_helper.controller.cash_pax_info import load_cash_pax_info_po, select_payment_channel
from qdairlines_helper.controller.nhlms_cashdesk import load_nhlms_cash_desk_po, hf_paid_account_payment


async def book_payment_callback(
        *, page: Page, logger: Logger, is_pay_completed_callback: Callable, book_input_dto: BookingInputDTO,
        one_way_booking_dto: OneWayBookingDTO, passengers_dto: List[PassengerDTO], qdair_cookie: Dict[str, Any],
        callback_get_proxy: Callable, cookie_jar: Optional[CookieJar] = None, timeout: float = 60.0,
        refresh_attempt: int = 3, retry: int = 0, enable_log: bool = True,
        hf_paid_account_payment_dto: Optional[HFPaidAccountPaymentInputDTO] = None, **kwargs: Any
) -> PaymentResultDTO:
    # 1. 打开预订搜索页面
    book_search_page = await open_book_search_page(
        page=page, logger=logger, protocol=book_input_dto.book_protocol, domain=book_input_dto.book_domain,
        timeout=timeout
    )

    # 2. 预订搜索
    await book_search(
        book_search_page=book_search_page, one_way_booking_dto=one_way_booking_dto, book_input_dto=book_input_dto,
        passengers=len(passengers_dto), logger=logger, timeout=timeout
    )
    logger.info(f"订单<{one_way_booking_dto.order_no}>，预订搜索结束")

    # 3. 加载添加乘客页面对象
    add_passenger_po = await load_add_passenger_po(
        page=page, logger=logger, protocol=book_input_dto.book_protocol, domain=book_input_dto.book_domain,
        timeout=timeout
    )

    # 4. 添加乘客
    await add_passenger(
        page=add_passenger_po, logger=logger, passengers_dto=passengers_dto, book_input_dto=book_input_dto,
        timeout=timeout
    )
    logger.info(f"订单<{one_way_booking_dto.order_no}>，添加乘客结束")

    # 5. 加载订单校验页面对象
    order_verify_po = await load_order_verify_po(
        page=page, logger=logger, protocol=book_input_dto.book_protocol, domain=book_input_dto.book_domain,
        timeout=timeout
    )

    # 6. 校验订单
    await order_verify(page=order_verify_po, logger=logger, refresh_attempt=refresh_attempt, timeout=timeout)
    logger.info(f"订单<{one_way_booking_dto.order_no}>，校验订单结束")

    # 7. 加载支付类型页面对象
    cash_pax_info_po = await load_cash_pax_info_po(
        page=page, logger=logger, protocol=book_input_dto.book_protocol, domain=book_input_dto.book_domain,
        timeout=timeout
    )

    if isinstance(hf_paid_account_payment_dto, HFPaidAccountPaymentInputDTO):
        # 8. 选择支付渠道
        pre_order_no: str = await select_payment_channel(
            page=cash_pax_info_po, logger=logger, channel_name=hf_paid_account_payment_dto.channel_name, timeout=timeout
        )
        logger.info(f"订单<{one_way_booking_dto.order_no}>，选择支付方式结束")

        # 9. 根据支付方式，加载不同的收银台页面对象
        nhlms_cash_desk_po = await load_nhlms_cash_desk_po(
            context=kwargs.get("context"), timeout=timeout, logger=logger,
            domain=hf_paid_account_payment_dto.pay_domain, protocol=hf_paid_account_payment_dto.pay_protocol
        )

        if hf_paid_account_payment_dto.payment_type != "付款账户支付":
            raise PaymentTypeError(payment_type=hf_paid_account_payment_dto.payment_type)

        # 10. 汇付天下操作支付
        payment_result_dto = await hf_paid_account_payment(
            page=nhlms_cash_desk_po, logger=logger, order_no=one_way_booking_dto.order_no, timeout=timeout,
            is_pay_completed_callback=is_pay_completed_callback,
            hf_paid_account_payment_dto=hf_paid_account_payment_dto
        )
        logger.info(f"订单<{one_way_booking_dto.order_no}>，汇付天下操作支付结束")
        payment_result_dto.pre_order_no = pre_order_no

        query_dto = QueryItineraryRequestDTO(
            payment_domain=book_input_dto.book_domain, payment_protocol=book_input_dto.book_protocol,
            storage_state=qdair_cookie.get("storage_state"), token=qdair_cookie.get("token"),
            pre_order_no=pre_order_no, user_id=qdair_cookie.get("user_id"), headers=qdair_cookie.get("headers")
        )
        await two_check_pay_success(
            page=nhlms_cash_desk_po, logger=logger, timeout=timeout, query_dto=query_dto, retry=retry,
            enable_log=enable_log, callback_get_proxy=callback_get_proxy, cookie_jar=cookie_jar
        )
        return payment_result_dto
    else:
        raise PaymentChannelMissError()
