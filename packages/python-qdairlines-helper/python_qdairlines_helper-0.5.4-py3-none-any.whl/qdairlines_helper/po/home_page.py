# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     home_page.py
# Description:  首页页面对象
# Author:       ASUS
# CreateDate:   2026/01/04
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from typing import Optional
from playwright.async_api import Page
from playwright_helper.libs.base_po import BasePo
import qdairlines_helper.config.url_const as url_const


class HomePage(BasePo):
    url: str = url_const.home_url
    __page: Page

    def __init__(self, page: Page, url: Optional[str] = None) -> None:
        super().__init__(page, url or url_const.home_url)
        self.__page = page
