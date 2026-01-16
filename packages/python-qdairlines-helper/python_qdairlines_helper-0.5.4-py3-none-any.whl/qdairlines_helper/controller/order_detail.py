# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     order_detail.py
# Description:  订单详情控制器
# Author:       ASUS
# CreateDate:   2026/01/06
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import re
import inspect
from logging import Logger
from aiohttp import CookieJar
from typing import Dict, Any, Optional, List, Callable
from qdairlines_helper.http.flight_order import FlightOrder
from flight_helper.models.dto.http_schema import HTTPRequestDTO
from flight_helper.models.dto.itinerary import QueryItineraryResponseDTO, QueryItineraryRequestDTO


async def get_order_detail(
        *, query_dto: QueryItineraryRequestDTO, logger: Logger, callback_get_proxy: Callable,
        timeout: Optional[int] = None, retry: Optional[int] = None, cookie_jar: Optional[CookieJar] = None,
        enable_log: Optional[bool] = None
) -> Dict[str, Any]:
    http_request_dto = HTTPRequestDTO(
        http_domain=query_dto.payment_domain, http_protocol=query_dto.payment_protocol,
        storage_state=query_dto.storage_state, timeout=timeout, retry=retry, enable_log=enable_log,
        token=query_dto.token
    )
    flight_order = FlightOrder(http_request_dto=http_request_dto, cookie_jar=cookie_jar)
    last_order_info: Dict[str, Any] = dict()
    for index in range(5):
        proxy = None
        is_end: bool = True if index + 1 == 5 else False
        if index != 0:
            if inspect.iscoroutinefunction(callback_get_proxy):
                proxy = await callback_get_proxy(logger=logger)
            else:
                proxy = callback_get_proxy(logger=logger)
        try:
            last_order_info = await flight_order.get_order_details(
                pre_order_no=query_dto.pre_order_no, user_id=query_dto.user_id, is_end=is_end, proxy=proxy,
                headers=query_dto.headers,
            )
            await flight_order.http_client.close()
            logger.info("查询青岛航空官网的订单详情数据成功")
            break
        except (Exception,):
            pass
    if isinstance(last_order_info, dict) and last_order_info.get("result") and last_order_info.get("code") == 1:
        return last_order_info.get("result")
    else:
        raise RuntimeError(f"订单<{query_dto.pre_order_no}>，获取详情数据异常，返回值：{last_order_info}")


async def get_order_itinerary(
        *, query_dto: QueryItineraryRequestDTO, logger: Logger, callback_get_proxy: Callable,
        timeout: Optional[int] = None, retry: Optional[int] = None, cookie_jar: Optional[CookieJar] = None,
        enable_log: Optional[bool] = None
) -> Optional[QueryItineraryResponseDTO]:
    _order_info: Dict[str, Any] = dict(pre_order_no=query_dto.pre_order_no)
    result = await get_order_detail(
        query_dto=query_dto, timeout=timeout, retry=retry, cookie_jar=cookie_jar, enable_log=enable_log,
        callback_get_proxy=callback_get_proxy, logger=logger
    )
    _order_info["cash_unit"] = result.get("cashUnit")
    _order_info["order_status"] = result.get("orderStatus")
    _order_info["order_amount"] = result.get("totalPrice")
    passenger_infos: List[Dict[str, Any]] = result.get("passengerInfoVoList")
    order_itineraries = list()
    for passenger_info in passenger_infos:
        id_no = passenger_info.get("idNo")
        order_itinerary = passenger_info.get("tktNo")
        passenger = passenger_info.get("passName")
        if bool(re.fullmatch(r'\d+-\d+', order_itinerary)):
            order_itineraries.append(dict(
                passenger_name=passenger, id_no=id_no, order_itinerary=order_itinerary,
                pre_order_no=query_dto.pre_order_no
            ))
    if order_itineraries:
        _order_info["itinerary_info"] = order_itineraries
        return QueryItineraryResponseDTO(**_order_info)
    else:
        logger.warning(
            f'青岛航空官网订单<{query_dto.pre_order_no}>，当前状态：{result.get("orderStatus")}，没有生成行程单信息')
