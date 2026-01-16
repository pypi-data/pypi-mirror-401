# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     user_login.py
# Description:  用户登录控制器
# Author:       ASUS
# CreateDate:   2026/01/04
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import inspect
from logging import Logger
from aiohttp import CookieJar
from typing import Dict, Any, Optional, Callable
from playwright.async_api import Page, BrowserContext
from qdairlines_helper.po.login_page import LoginPage
import qdairlines_helper.config.url_const as url_const
from qdairlines_helper.http.user_login import UserLogin
from qdairlines_helper.controller.home import load_home_po
from flight_helper.utils.exception_utils import IPBlockError
from flight_helper.models.dto.http_schema import HTTPRequestDTO
from playwright.async_api import Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError
from qdairlines_helper.utils.po_utils import get_ip_access_blocked_msg, parse_user_info_from_page_response


async def open_login_page(
        *, page: Page, logger: Logger, protocol: str, domain: str, timeout: float = 60.0
) -> LoginPage:
    url_prefix = f"{protocol}://{domain}"
    login_url = url_prefix + url_const.login_url
    await page.goto(login_url)

    login_po = LoginPage(page=page, url=login_url)
    await login_po.url_wait_for(url=login_url, timeout=timeout)
    logger.info(f"即将进入青岛航空官网登录页面，页面URL<{login_url}>")
    ip_access_blocked_msg = await get_ip_access_blocked_msg(page=page, timeout=3)
    if ip_access_blocked_msg:
        raise IPBlockError(ip_access_blocked_msg)
    return login_po


async def _user_login(
        *, page: LoginPage, logger: Logger, protocol: str, domain: str, username: str, password: str,
        timeout: float = 60.0
) -> None:
    # 1. 输入用户名
    username_input = await page.get_login_username_input(timeout=timeout)
    await username_input.fill(value=username.strip())
    logger.info(f"青岛航空官网登录页面，用户名<{username}>输入完成")

    # 2. 输入密码
    password_input = await page.get_login_password_input(timeout=timeout)
    await password_input.fill(value=password.strip())
    logger.info(f"青岛航空官网登录页面，密码<{password}>输入完成")

    # 3. 点击易盾验证logo
    check_logo_icon = await page.get_check_logo_icon(timeout=timeout)
    await check_logo_icon.click(button="left")
    logger.info("青岛航空官网登录页面，【易盾验证logo】点击完成")

    # 4. 获取校验成功的结果
    check_pass_text = await page.get_check_pass_text(timeout=timeout)
    logger.info(f"青岛航空官网登录页面，易盾验证logo点击后，校验结果【{check_pass_text}】获取完成")

    # 4. 点击登录
    login_btn = await page.get_login_btn(timeout=timeout)
    await login_btn.click(button="left")
    logger.info("青岛航空官网登录页面，【登录】按钮点击完成")

    # 5. 加载首页页面对象，加载成功说明进入了首页，登录成功
    try:
        await load_home_po(page=page.get_page(), logger=logger, protocol=protocol, domain=domain, timeout=timeout)
        logger.info(f"青岛航空官网登录页面，用户：{username}, 密码：{password}登录成功")
    except (PlaywrightError, PlaywrightTimeoutError, EnvironmentError, RuntimeError, Exception) as e:
        raise RuntimeError(f"青岛航空官网登录页面，用户：{username}, 密码：{password}登录失败，原因：{e}")


async def user_login_callback(
        *, page: Page, context: BrowserContext, logger: Logger, protocol: str, domain: str, username: str,
        password: str, timeout: float = 60.0, **kwargs: Any
) -> Dict[str, Any]:
    # 1. 打开登录页面
    login_po = await open_login_page(page=page, logger=logger, protocol=protocol, domain=domain, timeout=timeout)

    # 2. 开启网络监听
    keywords = [url_const.auth_form_api_url, url_const.login_after_api_url]
    network_logs = await login_po.capture_network(
        keywords=keywords, include_post_data=True, include_response_body=True, parse_form_data=True
    )
    # network_logs1 = await login_po.capture_network_by_route(keywords=keywords, parse_form_data=True)

    # 2. 执行登录操作
    await _user_login(
        page=login_po, protocol=protocol, logger=logger, domain=domain, username=username, password=password,
        timeout=timeout
    )
    user_info = parse_user_info_from_page_response(network_logs=network_logs)
    user_info.update(dict(storage_state=await context.storage_state()))
    return user_info


async def get_user_info(
        *, logger: Logger, http_request_dto: HTTPRequestDTO, callback_get_proxy: Callable,
        cookie_jar: Optional[CookieJar] = None
) -> Dict[str, Any]:
    user_login = UserLogin(http_request_dto=http_request_dto, cookie_jar=cookie_jar)
    last_user_info: Dict[str, Any] = dict()
    count = 2
    for index in range(count):
        proxy = None
        is_end: bool = True if index + 1 == count else False
        if index != 0:
            if inspect.iscoroutinefunction(callback_get_proxy):
                proxy = await callback_get_proxy(logger=logger)
            else:
                proxy = callback_get_proxy(logger=logger)
        try:
            last_user_info = await user_login.get_user_info(
                is_end=is_end, proxy=proxy, headers=http_request_dto.headers
            )
            await user_login.http_client.close()
            logger.info("获取青岛航空官网的用户详情数据成功")
            break
        except (Exception,) as e:
            logger.error(e)
            pass
    if isinstance(last_user_info, dict) and last_user_info.get("result") and last_user_info.get("code") == 1:
        return last_user_info.get("result")
    else:
        raise RuntimeError(f"获取用户详情数据异常，返回值：{last_user_info}")
