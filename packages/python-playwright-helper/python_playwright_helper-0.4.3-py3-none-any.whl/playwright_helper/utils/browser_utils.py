# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  playwright-helper
# FileName:     browser_utils.py
# Description:  浏览器工具模块
# Author:       ASUS
# CreateDate:   2025/12/18
# Copyright ©2011-2025. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import time
import asyncio
from playwright.async_api import BrowserContext, Page, TimeoutError as PlaywrightTimeoutError


async def switch_for_table_window(browser: BrowserContext, url_keyword: str, wait_time: float = 10.0) -> Page:
    # 最多等待 wait_time 秒
    end_time = time.time() + wait_time
    while time.time() < end_time:
        for page in browser.pages:
            if url_keyword.lower() in page.url.lower():
                await page.bring_to_front()
                return page
        await asyncio.sleep(delay=0.1)
    raise PlaywrightTimeoutError(f"根据关键信息<{url_keyword}>，没有找到浏览器的page对象")
