# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-qdairlines-helper
# FileName:     url_const.py
# Description:  url配置模块
# Author:       ASUS
# CreateDate:   2026/01/04
# Copyright ©2011-2026. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
# https://www.qdairlines.com/api/auth/auth/form?username=xxx&password=xxx&NECaptchaValidate=CN31_xxx 登录表单
auth_form_api_url: str = "/api/auth/auth/form"
# https://www.qdairlines.com/api/auth/user/loginAfter 登录成功后状态
login_after_api_url: str = "/api/auth/user/loginAfter"
# https://www.qdairlines.com/api/ewp/order/v1/orderInfo
order_info_api_url: str = "/api/ewp/order/v1/orderInfo"

# https://www.qdairlines.com/user/airorder，没有登录，是打不开这个页面
air_order_url: str = "/user/airorder"
login_url: str = "/login"
home_url: str = "/index"
book_search_url: str = "/book/flightSearch"
add_passenger_url: str = "/book/verifySecure"
order_verify_url: str = "/book/orderVerify"
cash_pax_info_url: str = "/book/cashPaxInfoInput"
# https://nhlms.cloudpnr.com/nobel/WebEntry.do  汇付天下收银台
nhlms_cashdesk_url: str = "/nobel/WebEntry.do"
# https://nhlms.cloudpnr.com/nobel/n1026/error?RegionId=P
nhlms_error_url: str = "/nobel/n1026/error"


# https://excashier.alipay.com/standard/auth.htm?payOrderId=4e3606b1c842414c88f631c35952a88e.85  支付宝收银台
alipay_url: str = "/standard/auth.htm"
# https://www.qdairlines.com/book/payPreCash?orderNo=OW20260105B1154687  微信支付收银台
wechat_pay_url: str = "/book/payPreCash"
# https://cashdesk.yeepay.com/bc-cashier/bcnewpc/request/10034054916/POWJP260105003882378  易宝支付收银台
yeepay_cashdesk_url: str = "/bc-cashier/bcnewpc/request/{}/{}"
# https://www.qdairlines.com/user/airorder/orderdetail?orderNo=OW20260105B1154687&orderType=2
order_detail_url: str = "/user/airorder/orderdetail"
# https://www.qdairlines.com/pay/success
pay_success_url: str = "/pay/success"
