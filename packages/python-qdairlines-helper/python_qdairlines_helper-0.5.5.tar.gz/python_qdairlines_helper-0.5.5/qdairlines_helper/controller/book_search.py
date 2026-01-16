# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     book_search.py
# Description:  航班搜索控制器
# Author:       ASUS
# CreateDate:   2026/01/04
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import asyncio
from time import time
from logging import Logger
from typing import Dict, Any, List
from playwright.async_api import Page, Locator
import qdairlines_helper.config.url_const as url_const
from qdairlines_helper.po.book_search_page import BookSearchPage
from qdairlines_helper.utils.po_utils import get_ip_access_blocked_msg
from flight_helper.models.dto.booking import OneWayBookingDTO, BookingInputDTO
from flight_helper.utils.exception_utils import NotEnoughTicketsError, ExcessiveProfitdError, ExcessiveLossesError, \
    IPBlockError


async def open_book_search_page(
        *, page: Page, logger: Logger, protocol: str, domain: str, timeout: float = 60.0
) -> BookSearchPage:
    url_prefix = f"{protocol}://{domain}"
    book_search_url = url_prefix + url_const.book_search_url
    await page.goto(book_search_url)

    book_search_po = BookSearchPage(page=page, url=book_search_url)
    await book_search_po.url_wait_for(url=book_search_url, timeout=timeout)
    logger.info(f"即将进入青岛航空官网航班预订查询页面，页面URL<{book_search_url}>")
    ip_access_blocked_msg = await get_ip_access_blocked_msg(page=page, timeout=3)
    if ip_access_blocked_msg:
        raise IPBlockError(ip_access_blocked_msg)
    return book_search_po


async def _book_search_dialog_handle(*, logger: Logger, page: BookSearchPage, timeout: float = 20.0) -> None:
    end_time = time() + timeout
    while time() < end_time:
        try:
            continue_book_btn = await page.get_reminder_dialog_continue_book_btn(timeout=1)
            await continue_book_btn.click(button="left")
            logger.info("航班预订查询页面，出现温馨提醒弹框，【继续购票】按钮点击完成")
            return
        except (Exception,):
            pass
        await asyncio.sleep(0.1)  # 快速轮询


async def book_search(
        *, book_search_page: BookSearchPage, logger: Logger, passengers: int, book_input_dto: BookingInputDTO,
        one_way_booking_dto: OneWayBookingDTO, timeout: float = 60.0
) -> None:
    # 1.搜索栏输入起飞城市
    depart_city_input = await book_search_page.get_depart_city_input(timeout=timeout)
    # await depart_city_input.fill(value=one_way_booking_dto.dep_code)
    await book_search_page.simulation_input_element(
        locator=depart_city_input, text=one_way_booking_dto.dep_code, delay=200
    )
    await asyncio.sleep(delay=1)
    # await depart_city_input.press("Enter")
    depart_city_result = await book_search_page.get_depart_city_search_result(
        depart_city=one_way_booking_dto.dep_city, timeout=timeout
    )
    await depart_city_result.click(button="left")
    logger.info(
        f"航班预订查询页面，搜索栏-起飞城市<{one_way_booking_dto.dep_city} {one_way_booking_dto.dep_code}>输入完成")

    # 2.搜索栏输入抵达城市
    arrive_city_input = await book_search_page.get_arrive_city_input(timeout=timeout)
    # await arrive_city_input.fill(value=one_way_booking_dto.arr_code)
    await book_search_page.simulation_input_element(
        locator=arrive_city_input, text=one_way_booking_dto.arr_code, delay=200
    )
    await asyncio.sleep(delay=1)
    # await arrive_city_input.press("Enter")
    arrive_city_result = await book_search_page.get_arrive_city_search_result(
        arrive_city=one_way_booking_dto.arr_city, timeout=timeout
    )
    await arrive_city_result.click(button="left")
    logger.info(
        f"航班预订查询页面，搜索栏-抵达城市<{one_way_booking_dto.arr_city} {one_way_booking_dto.arr_code}>输入完成")

    # 3.搜索栏输入起飞时间
    depart_date_input = await book_search_page.get_depart_date_input(timeout=timeout)
    await depart_date_input.fill(value=one_way_booking_dto.dep_date)
    await asyncio.sleep(delay=1)
    await depart_date_input.press("Enter")
    logger.info(f"航班预订查询页面，搜索栏-起飞日期<{one_way_booking_dto.dep_date}>输入完成")

    # 4.点击【查询机票】按钮
    flight_query_btn = await book_search_page.get_flight_query_btn(timeout=timeout)
    await flight_query_btn.click(button="left")
    logger.info(f"航班预订查询页面，【查询机票】按钮点击完成")

    # 5.点击查询后，再次处理是否有弹框，并航班基本信息plane locator
    await _book_search_dialog_handle(logger=logger, page=book_search_page, timeout=timeout)

    # 6.获取航班基本信息plane locator
    flight_info_plane: Locator = await book_search_page.get_flight_info_plane(
        flight_no=one_way_booking_dto.flight_no, timeout=timeout
    )

    # 8. 获取产品类型
    flight_product_nav: Locator = await book_search_page.get_flight_product_nav(
        locator=flight_info_plane, product_type=book_input_dto.product_type, timeout=timeout
    )
    await flight_product_nav.click(button="left")
    logger.info(f"航班预订查询页面，产品类型【{book_input_dto.product_type}】选择完成")

    # 9. 点击获取更多产品和价格的按钮
    more_product_btn = await book_search_page.get_more_product_btn(locator=flight_info_plane, timeout=timeout)
    await more_product_btn.click(button="left")
    logger.info(f"航班预订查询页面，航班<{one_way_booking_dto.flight_no}>产品列表，【更多舱位及价格】按钮点击完成")

    # 9. 获取所有的产品
    products: List[Dict[str, Any]] = await book_search_page.get_flight_products(
        locator=flight_info_plane, flight_no=one_way_booking_dto.flight_no, logger=logger
    )
    # 取出需要预订的舱位产品
    products = [x for x in products if x.get("cabin") == one_way_booking_dto.cabin and not x.get("ticket_info")]
    # 根据价格升序排序（默认）
    products = sorted(products, key=lambda x: x["amounts"]["amount"])
    # 9.1 判断是否存在该舱位
    if len(products) == 0:
        raise RuntimeError(
            f"航班预订查询页面，没有搜索到航班<{one_way_booking_dto.flight_no}>的{one_way_booking_dto.cabin}舱数据")
    cabin_product = products[0]
    # 9.2 判断余座
    seats_status = cabin_product.get("seats_status")
    logger.info(
        f"航班预订查询页面，航班<{one_way_booking_dto.flight_no}>舱位<{one_way_booking_dto.cabin}>的座位情况：{seats_status}")
    if seats_status < passengers:
        raise NotEnoughTicketsError(
            flight_no=one_way_booking_dto.flight_no, seats_status=seats_status, passengers=passengers
        )
    # 9.3. 判断货币符号，是否为 ¥(人民币结算)
    # 目前都为国内航班，暂不考虑货币种类

    # 9.4 判断销售价格是否满足预订需要
    amounts: Dict[str, Any] = cabin_product.get("amounts")
    amount: float = amounts.get("amount")
    if amount > one_way_booking_dto.standard_price + book_input_dto.standard_increase_threshold:
        raise ExcessiveLossesError(
            flight_no=one_way_booking_dto.flight_no, query_price=amount, order_price=one_way_booking_dto.standard_price,
            increase_threshold=book_input_dto.standard_increase_threshold, asset="票面价"
        )
    if amount < one_way_booking_dto.standard_price - book_input_dto.standard_reduction_threshold:
        raise ExcessiveProfitdError(
            flight_no=one_way_booking_dto.flight_no, query_price=amount, order_price=one_way_booking_dto.standard_price,
            reduction_threshold=book_input_dto.standard_reduction_threshold, asset="票面价"
        )
    if book_input_dto.sale_increase_threshold > 0:
        if amount > one_way_booking_dto.sale_price + book_input_dto.sale_increase_threshold:
            raise ExcessiveLossesError(
                flight_no=one_way_booking_dto.flight_no, query_price=amount, order_price=one_way_booking_dto.sale_price,
                increase_threshold=book_input_dto.sale_increase_threshold, asset="销售价"
            )
    if book_input_dto.sale_increase_threshold > 0:
        if amount < one_way_booking_dto.sale_price - book_input_dto.sale_reduction_threshold:
            raise ExcessiveProfitdError(
                flight_no=one_way_booking_dto.flight_no, query_price=amount,
                order_price=one_way_booking_dto.sale_price,
                reduction_threshold=book_input_dto.sale_reduction_threshold, asset="销售价"
            )

    # 10. 点击【购票】按钮
    booking_btn: Locator = cabin_product.get("booking_btn")
    await booking_btn.click(button="left")
    logger.info(f"航班预订查询页面，【购票】按钮点击完成")
