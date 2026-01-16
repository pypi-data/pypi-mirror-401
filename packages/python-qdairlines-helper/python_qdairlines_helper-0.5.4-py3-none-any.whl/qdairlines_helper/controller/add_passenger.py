# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     add_passenger.py
# Description:  添加乘客控制器
# Author:       ASUS
# CreateDate:   2026/01/04
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from typing import List
from logging import Logger
from playwright.async_api import Page
import qdairlines_helper.config.url_const as url_const
from flight_helper.models.dto.passenger import PassengerDTO
from flight_helper.utils.exception_utils import IPBlockError
from flight_helper.models.dto.booking import BookingInputDTO
from qdairlines_helper.po.add_passenger_page import AddPassengerPage
from qdairlines_helper.utils.po_utils import get_ip_access_blocked_msg


async def load_add_passenger_po(
        *, page: Page, logger: Logger, protocol: str, domain: str, timeout: float = 60.0
) -> AddPassengerPage:
    url_prefix = f"{protocol}://{domain}"
    add_passenger_url = url_prefix + url_const.add_passenger_url
    add_passenger_po = AddPassengerPage(page=page, url=add_passenger_url)
    await add_passenger_po.url_wait_for(url=add_passenger_url, timeout=timeout)
    logger.info(f"即将进入青岛航空官网添加乘客页面，页面URL<{add_passenger_url}>")
    ip_access_blocked_msg = await get_ip_access_blocked_msg(page=page, timeout=3)
    if ip_access_blocked_msg:
        raise IPBlockError(ip_access_blocked_msg)
    return add_passenger_po


async def add_passenger(
        *, page: AddPassengerPage, logger: Logger, passengers_dto: List[PassengerDTO], book_input_dto: BookingInputDTO,
        timeout: float = 60.0
) -> None:
    # 遍历方式添加乘客
    for index, passenger_dto in enumerate(passengers_dto):
        if index != 0:
            # 1. 点击【添加成人|添加儿童|添加婴儿】按钮
            add_adult_btn = await page.get_add_passenger_btn(
                passenger_type=passenger_dto.passenger_type, timeout=timeout
            )
            await add_adult_btn.click(button="left")
            logger.info(f"添加乘客页面，【添加{passenger_dto.passenger_type}】按钮点击完成")
        # 2. 获取 乘机人信息plane
        passenger_info_plane = await page.get_add_passenger_plane(timeout=timeout, position_index=index)
        logger.info(f"添加乘客页面，第<{index + 1}>乘机人信息---plane获取完成")

        # 3. 选择旅客类型
        adult_checkbox = await page.get_passenger_type_checkbox(
            passenger_type=passenger_dto.passenger_type, timeout=timeout, position_index=index
        )
        await adult_checkbox.click(button="left")
        logger.info(f"添加乘客页面，第<{index + 1}>乘机人信息---旅客类型【{passenger_dto.passenger_type}】单选框点击完成")

        # 4. 输入姓名
        username_input = await page.get_passenger_username_input(locator=passenger_info_plane, timeout=timeout)
        await username_input.fill(value=passenger_dto.passenger_name)
        logger.info(f"添加乘客页面，第<{index + 1}>乘机人信息---姓名<{passenger_dto.passenger_name}>输入完成")

        # 5. 选择性别
        gender_checkbox = await page.get_gender_checkbox(
            locator=passenger_info_plane, gender=passenger_dto.gender, timeout=timeout
        )
        await gender_checkbox.click(button="left")
        logger.info(f"添加乘客页面，第<{index + 1}>乘机人信息---性别【{passenger_dto.gender}】单选框点击完成")

        # 6. 选择证件类型 TODO 暂时只支持身份证类型，待后续完善
        if passenger_dto.id_type != "身份证":
            raise EnvironmentError(f"乘客证件类型<{passenger_dto.id_type}>暂不支持")

        # 7. 输入证件号码
        id_no_input = await page.get_id_no_input(locator=passenger_info_plane, timeout=timeout)
        await id_no_input.fill(value=passenger_dto.id_number)
        logger.info(f"添加乘客页面，第<{index + 1}>乘机人信息---证件号码<{passenger_dto.id_number}>输入完成")

    # 8. 输入联系人电话
    service_mobile_input = await page.get_service_mobile_input(timeout=timeout)
    await service_mobile_input.fill(value=book_input_dto.specialist_mobile)
    logger.info(f"添加乘客页面，联系人信息---手机号码<{book_input_dto.specialist_mobile}>输入完成")

    # 9. 勾选同意单选框
    agree_checkbox = await page.get_agree_checkbox(timeout=timeout)
    await agree_checkbox.click(button="left")
    logger.info(f"添加乘客页面，购票须知---【已阅读并同意】单选框点击完成")

    # 10. 点击【下一步】
    next_btn = await page.get_next_btn(timeout=timeout)
    await next_btn.click(button="left")
    logger.info(f"添加乘客页面，【下一步】按钮点击完成，<{len(passengers_dto)}>名乘客信息添加成功")
