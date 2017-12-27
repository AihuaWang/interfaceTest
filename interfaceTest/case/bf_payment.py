#!/bin/env python
# -*- coding: utf-8 -*-
import json
import time
from lib import req_model
from util import assert_util
from util import http_util
from util import mysql_util
from util.case_util import TestCase

"""
1、代付状态验证：交易失败、交易成功、交易处理中（订单已接收、渠道已受理）
"""


@TestCase
def test_payment():
    # 单笔代付接口
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263320"))
    assert_util.verify(result, state="0", resultCode="2005", resultMsg=u'等待付款', receiveTime=req_model.current_time,bizId="s0012017111422263320", systemSourceId="s001", chnId="ch001")
    sql = mysql_util.query(table="settle_payment_bill_biz",state=0,ret_code=2005)
    #print json.dumps(sql, indent=4, sort_keys=True)
    assert_util.verify(sql[0], state="0", ret_code="2005", ret_info=u'等待付款', receive_time=req_model.current_time,biz_id="s0012017111422263320",success_amount="0.00", system_source_id="s001", chn_id="ch001")


@TestCase
def test_paymentfail():
    # 单笔代付交易失败
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentstate("s0012017111422263311"))
    assert_util.verify(result, state="-1", resultCode="3000", resultMsg=u'交易失败：户代付报文格式不正确,收款方银行名称(to_bank_name)填写有误', receiveTime=req_model.current_time,bizId="s0012017111422263311", successAmount=0, systemSourceId="s001", chnId="ch001")

def test_paymentsuccess():
    # 单笔代付交易成功
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentstate("s0012017111422263312"))
    assert_util.verify(result, state="1", resultCode="0000", resultMsg=u'处理成功', receiveTime=req_model.current_time,bizId="s0012017111422263312", successAmount=10, systemSourceId="s001", chnId="ch001")

"""
2、路由层校验：chn_status，trans_amount_lower_limit,trans_amount_upper_limit,day_amount_limit,day_times_limit,month_amount_limit,month_times_limit,disable_time_interval_star,disable_time_interval_end
"""


@TestCase
def test_payment_chnstate():
    # 渠道不可用的
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=79", chn_status=0)
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263320"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：订单[s0012017111422263320]-渠道未配置或不可用',
                       receiveTime=req_model.current_time, bizId="s0012017111422263320", systemSourceId="s001",
                       chnId="ch001")
    sql = mysql_util.update("settle_channel_route", "id=79", chn_status=1)

@TestCase
def test_payment_isable_time():
    # 系统不可用时间范围
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=79", disable_time_interval_start=req_model.start_date,disable_time_interval_end=req_model.end_date)
    result = http_util.post("/route/payment/single",body=req_model.addpaymentparame("s0012017111422263320"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263320]-渠道在不可用时间范围内',receiveTime=req_model.current_time,bizId="s0012017111422263320",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=79", disable_time_interval_start="" ,disable_time_interval_end ="")

@TestCase
def test_payment_transamountlowerlimit():
    # 单笔代付交易金额下限不能低于15元
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=79", trans_amount_lower_limit=15)
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263320"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263320]-单笔交易额受限',receiveTime=req_model.current_time,bizId="s0012017111422263320",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=79", trans_amount_lower_limit=0)

@TestCase
def test_payment_transamountupperlimit():
    # 单笔代付交易金额上限不能超过20元
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=79", trans_amount_upper_limit=9)
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263320"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263320]-单笔交易额受限',receiveTime=req_model.current_time,bizId="s0012017111422263320",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=79", trans_amount_upper_limit=0)

@TestCase
def test_payment_dayamountlimit():
    # 单笔代付单日交易额受限
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=79", day_amount_limit=15)
    test_paymentsuccess()
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263320"))
    #assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263320]-单日交易额受限',receiveTime=req_model.current_time,bizId="s0012017111422263320",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=79", day_amount_limit=0)

@TestCase
def test_payment_daytimeslimit():
    # 单笔代付单日交易额受限
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=79", day_times_limit=1)
    test_paymentsuccess()
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263320"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263320]-单日交易次数受限',receiveTime=req_model.current_time,bizId="s0012017111422263320",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=79", day_times_limit=0)

@TestCase
def test_payment_monthamountlimit():
    # 单笔代付单月交易额受限
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=79", month_amount_limit=15)
    test_paymentsuccess()
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263320"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263320]-单月交易额受限',receiveTime=req_model.current_time,bizId="s0012017111422263320",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=79", day_amount_limit=0)

@TestCase
def test_payment_monthtimeslimit():
    # 单笔代付单日交易额受限
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=79", month_times_limit=1)
    test_paymentsuccess()
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263320"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263320]-单月交易额受限',receiveTime=req_model.current_time,bizId="s0012017111422263320",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=79", month_times_limit=0)


"""
3、代付入参校验：入参字段逐个校验
"""
@TestCase
def test_paymentinvalidbizId():
    # 订单号：验证无效的订单号
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("1000001"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单号长度无效,请不要低于15个字符或高于30个字符：1000001；订单号格式无效，请按开头四位为系统来源【s001】生成订单号：1000001；',receiveTime=req_model.current_time,bizId="1000001",systemSourceId="s001",chnId="ch001")

@TestCase
def test_paymentnullbizId():
    # 订单号：验证订单号为空
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame(""))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单号(bizId)是必填项；',receiveTime=req_model.current_time,systemSourceId="s001",chnId="ch001")

@TestCase
def test_paymentrepeatbizId():
    # 订单号：验证重复的订单号
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    test_payment()
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263320"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263320]正在处理或已处理完成',receiveTime=req_model.current_time,bizId="s0012017111422263320",systemSourceId="s001",chnId="ch001")

@TestCase
def test_payment002bizId():
    # 订单号：验证的订单id以002开头
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s000022017111422263312"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单号格式无效，请按开头四位为系统来源【s001】生成订单号：s000022017111422263312；订单号格式无效，请按中间八位【02201711】为日期生成订单号：s000022017111422263312；订单号格式无效，中间八位日期【02201711】不在有效区间内：s000022017111422263312；',receiveTime=req_model.current_time,bizId="s000022017111422263312",systemSourceId="s001",chnId="ch001")

@TestCase
def test_paymentnullsystemSourceId():
    # 系统来源：验证系统来源为空
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263351"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：系统来源ID(systemSourceId)是必填项；',receiveTime=req_model.current_time,systemSourceId="",bizId="s0012017111422263351",chnId="ch001")

@TestCase
def test_paymentinvalidsystemSourceId():
    # 系统来源：验证系统来源不存在
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263352"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：未授权的系统来源ID：s0000001；订单号格式无效，请按开头四位为系统来源【s0000001】生成订单号：s0012017111422263352；',receiveTime=req_model.current_time,bizId="s0012017111422263352",systemSourceId="s0000001",chnId="ch001")

@TestCase
def test_paymentinvalidbizId():
    # 订单金额：订单金额为空
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263353"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：金额(amount)是必填项；',receiveTime=req_model.current_time,bizId='s0012017111422263353',systemSourceId="s001",chnId="ch001")

@TestCase
def test_payment2mount():
    # 订单金额：订单金额保留两位小数
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263354"))
    assert_util.verify(result, state="0", resultCode="2005", resultMsg=u'等待付款', receiveTime=req_model.current_time,bizId="s0012017111422263354", successAmount=0.00, systemSourceId="s001", chnId="ch001")

@TestCase
def test_paymentnullaccountName():
    # 银行卡姓名：银行卡姓名为空
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263355"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：账户名称(accountName)是必填项；', receiveTime=req_model.current_time,bizId="s0012017111422263355", systemSourceId="s001", chnId="ch001")

@TestCase
def test_paymentnullbankId():
    # 银行卡代码：验证银行卡代码为空
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263356"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：付款方银行代码(bankId)是必填项；', receiveTime=req_model.current_time,bizId="s0012017111422263356", systemSourceId="s001", chnId="ch001")

@TestCase
def test_paymentnotbankId():
    # 银行卡代码：验证银行卡代码与银行卡不一致
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263357"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：订单[s0012017111422263357]-渠道未配置或不可用', receiveTime=req_model.current_time,bizId="s0012017111422263357", systemSourceId="s001", chnId="ch001")

@TestCase
def test_paymentnullaccountNo():
    # 银行卡号：银行卡为空
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263358"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：付款方银行账号(accountNo)是必填项；', receiveTime=req_model.current_time,bizId="s0012017111422263358", systemSourceId="s001", chnId="ch001")

@TestCase
def test_paymentnullopenBankName():
    # 银行开户行：校验开户行为空
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263359"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：开户行名称(openBankName)是必填项；', receiveTime=req_model.current_time,bizId="s0012017111422263359", systemSourceId="s001", chnId="ch001")

@TestCase
def test_paymentnullreceiveTime():
    # 订单请求时间：校验订单请求时间
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263361"))
    assert_util.verify(result, state="0", resultCode="2005", resultMsg=u'等待付款', bizId="s0012017111422263361", systemSourceId="s001", chnId="ch001")

@TestCase
def test_paymentnotchnId():
    # 渠道来源：校验渠道来源不存在
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentparame("s0012017111422263363"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：渠道不存在：ch00001；', receiveTime=req_model.current_time,bizId="s0012017111422263363", systemSourceId="s001")


"""
4、代付单笔轮训

"""


@TestCase
def test_paymentrotationSuccess():
    # 单笔代付轮训成功接口
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentstate("s0012017111422263313"))
    assert_util.verify(result, state="0", resultCode="2005", resultMsg=u'等待付款', receiveTime=req_model.current_time,bizId="s0012017111422263313", systemSourceId="s001", chnId="ch001")
    sql = mysql_util.update("settle_payment_bill_biz", "account_no=64128301019232332", biz_id="s0012017111422263312")
    sql = mysql_util.update("settle_payment_bill", "account_no=64128301019232332", biz_id="s0012017111422263312")
    time.sleep(6)
    sql = mysql_util.query(table="settle_payment_bill_biz",state=1,ret_code=0000,biz_id="s0012017111422263312",ret_info=u"处理成功")
    print json.dumps(sql, indent=4, sort_keys=True)
    assert_util.verify(sql[0], state="1", ret_code="0000", ret_info=u'处理成功', receive_time=req_model.current_time,biz_id="s0012017111422263312",success_amount="10.00")

@TestCase
def test_paymentrotationfail():
    # 单笔代付轮训处理中接口
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/single", body=req_model.addpaymentstate("s0012017111422263313"))
    assert_util.verify(result, state="0", resultCode="2005", resultMsg=u'等待付款', receiveTime=req_model.current_time,bizId="s0012017111422263313", systemSourceId="s001", chnId="ch001")
    time.sleep(6)
    sql = mysql_util.query(table="settle_payment_bill_biz",state=0,ret_code=2005,biz_id="s0012017111422263313")
    print json.dumps(sql, indent=4, sort_keys=True)
    assert_util.verify(sql[0], state="0", ret_code="2005", receive_time=req_model.current_time,biz_id="s0012017111422263313",success_amount="0.00")


"""
5、单笔代付，异步回调
"""

# def test_paymentbacks():
#     # 单笔代付轮轮接口
#     mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
#     req_model.addbacks("s00120171123142223434")
#     result = http_util.postbf("/bf/callback/payment?data_content=77f530811dd320e5a63118d92f44ec2f8a21574c8bf4a9b565ef24558fa0299d75f49bb7eb4e5ffeeae429cdac8a81aeb786447445f1163445a7fdd9ef9b3dbec373c386fa74e79f01aed5b5c3e31c9059ed24fbeb0ce364bef446246542e5bd88ac49c11eff88284bf10bd41736e5f10843954cd922ea11f9f40d965a7fa1103ffcc6a042714bd9227a9c737410d8f1cf08978fe36fa8b008afd801a1725500dc6443a01b37edb72b80aa976032e230f8ee668151ec786c9cafaa0d54d6396ba4d246f8999d3c5effbaa3101c35b50866a1aa605871089aa19c10dd3f658fc1c53829c268d6cde07ebf9fb88612581af54ea9d2bcae321bec9b034869a5e4310bce35eca06ca4ad556ea5fe5ede4134aff9c3ef040e469db7f2e2f269aee9fbc5dcfbf2f01c31b23eba22bba57bccc1091b9f889020cc2a3496b6ec0f04b40199e9b5543dbf84e67d5da22d66620018d98e22a82e0062be4bea3bdba97486f17ee67ab7c02af8f65dcf782eb755b1c2bfda2fa63a8e36ae855864f21a7140884654eaa6238c4fbdb047f1c3b0ed83a7b26793fbd16b967d1444d43d94f53c3bb96ea8938f92803e969a05431f92907db56e53a5dee39b4c39fec63548e4b3e9ddb90a62339c3dc56fcfa6964f13b2416a50ef6169fc87e26ec8fd49c9ded34841970455f95f50fb175e809ddde56bfb0fbb2a02184adbb50c02cc98e86679d496f61ad2b6f590dbc52b95bcfd4b835397d1fdf04e3837344dce0613e877565efd2a07cfaca14f82a892a1fb5feea5ac607488afa6a10922eb51ac03bfc5ea25d752d8c6dc22e8f701704fa0ccf67b3c4b00b633675d8eeec603b9ca0ec736da4da1757fa4930f1fd18e57d2665bb6e811a42ea7422e0bd4f8368a4b11a7e5103a7c01b32c6e2a4cfcbb44a5c6d2f1ebaa59fd2977de623f575d67ab1af8f7eee5c46b3bcf0044028421de3e3b89bc70e43c49ff69d2cde5791f2fff794444bbc13cd06a8e401c7a4234a48539a5fe0b102627238d8cd381a94ee6d2ad4ec598927424da88e2f3115962dec34fd4f3853751a2eec35c658594d21137b07ea4f891ff10523574592929cba84193889406e94eda853afaef186c7980d9ba29e716bbbc75d9a28a3393b563de1bdf971ad25db24f196d8772091ae447df739ef7aa2cd6a6c87f563a110db1cbdd79b9627228ec35bf5b756e8e0c3010f2a73ea7b66f39c50a5900ca964ae658dfb6f624a3487ddaabbea158e3220233191f997176893167acf822c85e29c1626e8685639928b33a6043346a194de4353e371e9a29d7b2b0f16dcf873f72ec453808eee60ddf843227b807f27760f324fffca86795dc5424629ae7dcfcb56f6c0340078f548e36e54057911219271cc7df31b33d24a6ecd59ce15613386c8c94db99726b5eab8283d59ea5e9112204fd8b69c5614d")

    #sql = mysql_util.query(table="settle_payment_bill_biz",state=0,ret_code=2005)
    #print json.dumps(sql, indent=4, sort_keys=True)
    #assert_util.verify(sql[0], state="0", ret_code="2005", ret_info=u'等待付款', receive_time=req_model.current_time,biz_id="s0012017111422263320",success_amount="0.00", system_source_id="s001", chn_id="ch001")


###########################################################################单笔查询case################################################################################################
def test_queryreSuccess():
    # 单笔查询：交易成功的单笔代付查询
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    test_paymentsuccess()
    result = http_util.post("/route/payment/singleQuery", body={"bizId":"s0012017111422263312","systemSourceId":"s001"})
    assert_util.verify(result, state="1", resultCode="0000", resultMsg=u'处理成功', receiveTime=req_model.current_time,bizId="s0012017111422263312", systemSourceId="s001")

def test_queryreFail():
    # 单笔查询：交易失败的单笔代付查询
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    test_paymentfail()
    result = http_util.post("/route/payment/singleQuery", body={"bizId":"s0012017111422263311","systemSourceId":"s001"})
    assert_util.verify(result, state="-1", resultCode="3000", resultMsg=u'交易失败：户代付报文格式不正确,收款方银行名称(to_bank_name)填写有误', receiveTime=req_model.current_time,bizId="s0012017111422263311", systemSourceId="s001")

def test_queryreProcess():
    # 单笔查询：交易处理中
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    test_payment()
    result = http_util.post("/route/payment/singleQuery", body={"bizId":"s0012017111422263320","systemSourceId":"s001"})
    assert_util.verify(result, state="0", resultCode="2005", resultMsg=u'等待付款', receiveTime=req_model.current_time,bizId="s0012017111422263320", systemSourceId="s001")

def test_queryrenotbizId():
    # 单笔查询：单笔交易为空订单号为空
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/singleQuery", body={"bizId":"","systemSourceId":"s001"})
    assert_util.verify(result, resultCode="2800", resultMsg=u'单笔收款结果查询出错：订单号(bizId)是必填项；',systemSourceId="s001")

def test_queryrenullbizId():
    # 单笔查询:订单号不存在
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/singleQuery", body={"bizId":"s00120171130p03003648","systemSourceId":"s001"})
    assert_util.verify(result, state="0",resultCode="2009", resultMsg=u'业务订单不存在',bizId="s00120171130p03003648", systemSourceId="s001")

def test_queryresynullstemSourceId():
    # 单笔查询：查询系统来源为空
    mysql_util.clear("settle_payment_bill","settle_payment_bill_biz")
    result = http_util.post("/route/payment/singleQuery", body={"bizId":"s00120171130p03003648","systemSourceId":""})
    assert_util.verify(result, resultCode="2800", resultMsg=u'单笔收款结果查询出错：系统来源ID(systemSourceId)是必填项；',bizId="s00120171130p03003648")


if __name__ == '__main__':
    test_paymentrotationfail()
    #test_paymentbacks()
    #test_payment_chnstate()
    # statistic_util.TestStatistic.print_result()
    # try:
    #   test_queryreceipt()
    # except Exception as e:
    #      print e
    #     print e.message
