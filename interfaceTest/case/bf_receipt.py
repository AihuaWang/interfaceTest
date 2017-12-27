#!/bin/env python
# -*- coding: utf-8 -*-
from lib import req_model
from util import assert_util
from util import http_util
from util.case_util import TestCase
from util import mysql_util
import time
import json


"""
1、代收状态验证：交易失败、交易成功、交易处理中（订单已接收、渠道已受理）
"""


@TestCase
def test_receipt():
    # 单笔代扣接口等待收款
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263410"))
    assert_util.verify(result, state="0", resultCode="2001", resultMsg=u'等待收款', receiveTime=req_model.current_time,
                       bizId="s0012017111422263410", successAmount=0, systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiidcardptfail():
    # 单笔代收交易失败：id_card校验失败
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263411"))
    assert_util.verify(result, state="-1", resultCode="3000", resultMsg=u'交易失败：报文交易要素格式错误密文域中参数id_card校验失败', receiveTime=req_model.current_time,bizId="s0012017111422263411", successAmount=0, systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptaccountNamefail():
    # 单笔代收交易失败：持卡人姓名校验失败
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263421"))
    assert_util.verify(result, state="-1", resultCode="3000", resultMsg=u'交易失败：报文交易要素格式错误密文域中参数id_holder格式校验失败', receiveTime=req_model.current_time,bizId="s0012017111422263421", successAmount=0, systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptaccountNofail():
    # 单笔代收交易失败：卡号校验失败
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263431"))
    assert_util.verify(result, state="-1", resultCode="3000", resultMsg=u'交易失败：卡号校验失败', receiveTime=req_model.current_time,bizId="s0012017111422263431", successAmount=0, systemSourceId="s001", chnId="ch001")

def test_receiptsuccess():
    # 单笔代收交易成功
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263412"))
    assert_util.verify(result, state="1", resultCode="0000", resultMsg=u'处理成功', receiveTime=req_model.current_time,bizId="s0012017111422263412", successAmount=10, systemSourceId="s001", chnId="ch001")


"""
2、代收路由校验
"""

@TestCase
def test_receipt_chnstate():
    # 渠道不可用的
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=19", chn_status=0)
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263410"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：订单[s0012017111422263410]-渠道未配置或不可用',
                       receiveTime=req_model.current_time, bizId="s0012017111422263410", systemSourceId="s001",
                       chnId="ch001")
    sql = mysql_util.update("settle_channel_route", "id=19", chn_status=1)

@TestCase
def test_receipt_isable_time():
    # 系统不可用时间范围
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=19", disable_time_interval_start=req_model.start_date,disable_time_interval_end=req_model.end_date)
    result = http_util.post("/route/receipt/single",body=req_model.addreceiptstate("s0012017111422263410"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263410]-渠道在不可用时间范围内',receiveTime=req_model.current_time,bizId="s0012017111422263410",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=19", disable_time_interval_start="" ,disable_time_interval_end ="")

@TestCase
def test_receipt_transamountlowerlimit():
    # 单笔代收交易金额下限不能低于15元
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=19", trans_amount_lower_limit=15)
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263410"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263410]-单笔交易额受限',receiveTime=req_model.current_time,bizId="s0012017111422263410",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=19", trans_amount_lower_limit=0)

@TestCase
def test_receipt_transamountupperlimit():
    # 单笔代收交易金额上限不能超过20元
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=19", trans_amount_upper_limit=9)
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263410"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263410]-单笔交易额受限',receiveTime=req_model.current_time,bizId="s0012017111422263410",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=19", trans_amount_upper_limit=0)

@TestCase
def test_receipt_dayamountlimit():
    # 单笔代收单日交易额受限
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=19", day_amount_limit=15)
    test_receiptsuccess()
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263410"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263410]-单日交易额受限',receiveTime=req_model.current_time,bizId="s0012017111422263410",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=19", day_amount_limit=0)

@TestCase
def test_receipt_daytimeslimit():
    # 单笔代收单日交易次数受限
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=19", day_times_limit=1)
    test_receiptsuccess()
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263410"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263410]-单日交易次数受限',receiveTime=req_model.current_time,bizId="s0012017111422263410",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=19", day_times_limit=0)

@TestCase
def test_receipt_monthamountlimit():
    # 单笔代收单月交易额受限
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    sql = mysql_util.update("settle_channel_route", "id=19", month_amount_limit=15)
    test_receiptsuccess()
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263410"))
    assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263410]-单月交易额受限',receiveTime=req_model.current_time,bizId="s0012017111422263410",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.update("settle_channel_route", "id=19", day_amount_limit=0)

@TestCase
def test_receipt_amount600():
    # 单笔代收单月交易次数受限
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptroute("600"))
    #assert_util.verify(result,state="-2",resultCode="1000",resultMsg=u'订单接收失败：订单[s0012017111422263410]-单月交易额受限',receiveTime=req_model.current_time,bizId="s0012017111422263410",systemSourceId="s001",chnId="ch001")


"""
3、代收状态验证：入参校验
"""

@TestCase
def test_receiptinvalid():
    # 单笔代扣接口：无效的订单号
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("1000001"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：订单号长度无效,请不要低于15个字符或高于30个字符：1000001；订单号格式无效，请按开头四位为系统来源【s001】生成订单号：1000001；', receiveTime=req_model.current_time,bizId="1000001",  systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptnull():
    # 单笔代扣接口：订单号为空
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame(""))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：订单号(bizId)是必填项；', receiveTime=req_model.current_time, bizId="",systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptrepeat():
    # 单笔代扣接口：重复的订单号
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    test_receipt()
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s0012017111422263410"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：订单[s0012017111422263410]正在处理或已处理完成', receiveTime=req_model.current_time, bizId="s0012017111422263410",systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptwrong():
    # 单笔代扣接口：订单号非s001开头
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s00002201711142226333313"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：订单号格式无效，请按开头四位为系统来源【s001】生成订单号：s00002201711142226333313；订单号格式无效，请按中间八位【02201711】为日期生成订单号：s00002201711142226333313；订单号格式无效，中间八位日期【02201711】不在有效区间内：s00002201711142226333313；', receiveTime=req_model.current_time, bizId="s00002201711142226333313",systemSourceId="s001", chnId="ch001")

def test_receiptsystemSourceIdinvalid():
    # 单笔代扣接口：无效的系统来源
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226422"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：未授权的系统来源ID：s0000001；订单号格式无效，请按开头四位为系统来源【s0000001】生成订单号：s001201711142226422；', receiveTime=req_model.current_time,bizId="s001201711142226422",  systemSourceId="s0000001", chnId="ch001")

@TestCase
def test_receiptsystemSourceIdnull():
    # 单笔代扣接口：系统来源为空
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226421"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：系统来源ID(systemSourceId)是必填项；', receiveTime=req_model.current_time, bizId="s001201711142226421",systemSourceId="", chnId="ch001")

@TestCase
def test_receiptamountnull():
    # 单笔代扣接口：金额为空
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226423"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：金额(amount)是必填项；', receiveTime=req_model.current_time, bizId="s001201711142226423",systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptamount():
    # 单笔代扣接口：金额为空
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226424"))
    assert_util.verify(result, state="0", resultCode="2001", resultMsg=u'等待收款', receiveTime=req_model.current_time, bizId="s001201711142226424",systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptaaccountNamenull():
    # 单笔代扣接口：持卡人姓名为空
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226425"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：付款方账户名称(accountName)是必填项；', receiveTime=req_model.current_time, bizId="s001201711142226425",systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptbankIdnull():
    # 单笔代扣接口：银行卡代码为空
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226426"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：付款方银行代码(bankId)是必填项；', receiveTime=req_model.current_time, bizId="s001201711142226426",systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptbankIdnot():
    # 单笔代扣接口：银行卡代码与银行不一致
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226427"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：订单[s001201711142226427]-渠道未配置或不可用', receiveTime=req_model.current_time, bizId="s001201711142226427",systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptaccountNonull():
    # 单笔代扣接口：银行卡号为空
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226428"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：付款方银行账号(accountNo)是必填项；', receiveTime=req_model.current_time, bizId="s001201711142226428",systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptidCardnull():
    # 单笔代扣接口：身份证号id为空
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226430"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：身份证号(idCard)是必填项；', receiveTime=req_model.current_time, bizId="s001201711142226430",systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptchnIdinvalid():
    # 单笔代扣接口：渠道来源为无效
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226434"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：渠道不存在：ch000001；', receiveTime=req_model.current_time, bizId="s001201711142226434",systemSourceId="s001", chnId="ch000001")

@TestCase
def test_receiptmobilenull():
    # 单笔代扣接口：手机号为空
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226435"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：银行卡绑定手机号(mobile)是必填项；', receiveTime=req_model.current_time, bizId="s001201711142226435",systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptmobileinvalid():
    # 单笔代扣接口：手机号非1开头
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226436"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：手机号无效：31513134715；', receiveTime=req_model.current_time, bizId="s001201711142226436",systemSourceId="s001", chnId="ch001")

@TestCase
def test_receiptmobilewrong():
    # 单笔代扣接口：手机号不是11位
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptparame("s001201711142226437"))
    assert_util.verify(result, state="-2", resultCode="1000", resultMsg=u'订单接收失败：手机号无效：159015375；', receiveTime=req_model.current_time, bizId="s001201711142226437",systemSourceId="s001", chnId="ch001")

"""
4、代扣单笔轮训

"""

@TestCase
def test_receiptrotationSuccess():
    # 单笔代扣轮训成功接口
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263410"))
    assert_util.verify(result, state="0", resultCode="2001", resultMsg=u'等待收款', receiveTime=req_model.current_time,bizId="s0012017111422263410", systemSourceId="s001", chnId="ch001")
    sql = mysql_util.update("settle_receipt_bill_biz", "account_no=6214830101923232", biz_id="s0012017111422263412")
    sql = mysql_util.update("settle_receipt_bill", "account_no=6214830101923232", biz_id="s0012017111422263412")
    time.sleep(6)
    sql = mysql_util.query(table="settle_receipt_bill_biz",state=1,ret_code=0000,biz_id="s0012017111422263412",ret_info=u"处理成功")
    print json.dumps(sql, indent=4, sort_keys=True)
    assert_util.verify(sql[0], state="1", ret_code="0000", ret_info=u'处理成功', receive_time=req_model.current_time,biz_id="s0012017111422263412")

@TestCase
def test_receiptrotationfail():
    # 单笔代扣轮训处理中接口
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/single", body=req_model.addreceiptstate("s0012017111422263410"))
    assert_util.verify(result, state="0", resultCode="2001", resultMsg=u'等待收款', receiveTime=req_model.current_time,bizId="s0012017111422263410", systemSourceId="s001", chnId="ch001")
    time.sleep(6)
    sql = mysql_util.query(table="settle_receipt_bill_biz",state=0,ret_code=2001,biz_id="s0012017111422263410")
    print json.dumps(sql, indent=4, sort_keys=True)
    assert_util.verify(sql[0], state="0", ret_code="2001", receive_time=req_model.current_time,biz_id="s0012017111422263410",success_amount="0.00")




#####################################################################################单笔代扣查询#########################################################################################
@TestCase
def test_receiptqueryreSuccess():
    # 单笔代扣查询：交易成功的单笔代付查询
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    test_receiptsuccess()
    result = http_util.post("/route/payment/singleQuery", body={"bizId":"s0012017111422263312","systemSourceId":"s001"})
    assert_util.verify(result, state="1", resultCode="0000", resultMsg=u'处理成功',bizId="s0012017111422263312", systemSourceId="s001")

@TestCase
def test_receiptqueryreFail():
    # 单笔代扣查询：交易失败的单笔代付查询
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    test_receiptaccountNamefail()
    result = http_util.post("/route/receipt/singleQuery", body={"bizId":"s0012017111422263421","systemSourceId":"s001"})
    assert_util.verify(result, state="-1", resultCode="3000", resultMsg=u'交易失败：报文交易要素格式错误密文域中参数id_holder格式校验失败', bizId="s0012017111422263421", systemSourceId="s001")

@TestCase
def test_receiptqueryreProcess():
    # 单笔代扣查询：交易处理中
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    test_receipt()
    result = http_util.post("/route/receipt/singleQuery", body={"bizId":"s0012017111422263410","systemSourceId":"s001"})
    assert_util.verify(result, state="0", resultCode="2001", resultMsg=u'等待收款', bizId="s0012017111422263410", systemSourceId="s001")

@TestCase
def test_receiptqueryrenotbizId():
    # 单笔代扣查询：单笔交易为空订单号为空
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/singleQuery", body={"bizId":"","systemSourceId":"s001"})
    assert_util.verify(result, resultCode="2800", resultMsg=u'单笔收款结果查询出错：订单号(bizId)是必填项；')

@TestCase
def test_receiptqueryrenullbizId():
    # 单笔代扣查询:订单号不存在
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/singleQuery", body={"bizId":"s00120171130p03003648","systemSourceId":"s001"})
    assert_util.verify(result, state="0",resultCode="2009", resultMsg=u'业务订单不存在',bizId="s00120171130p03003648", systemSourceId="s001")

@TestCase
def test_receiptqueryresynullstemSourceId():
    # 单笔代扣查询：查询系统来源为空
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/singleQuery", body={"bizId":"s00120171130p03003648","systemSourceId":""})
    assert_util.verify(result, resultCode="2800", resultMsg=u'单笔收款结果查询出错：系统来源ID(systemSourceId)是必填项；')

#####################################################################################批量扣款#########################################################################################
@TestCase
def test_receiptbatchsuccess():
    # 批量扣款：验证请求成功
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/batch", body=req_model.addreceiptparame("s001201711142226438"))
    assert_util.verify(result, resultCode="0000", resultMsg=u"处理成功", reqSn="s0012017092200000917",systemSourceId="s001", chnId="ch001")
    assert_util.verify(result["receipRestList"][0],state="0",resultCode="2001",resultMsg=u"等待收款",bizId="s0012017111422263413",systemSourceId="s001",chnId="ch001")
    assert_util.verify(result["receipRestList"][1],state="0",resultCode="2001",resultMsg=u"等待收款",bizId="s001201709290021338",systemSourceId="s001",chnId="ch001")
    sql= mysql_util.query("settle_receipt_bill_biz",req_sn='s0012017092200000917')
    print json.dumps(sql, indent=4, sort_keys=True)
    assert_util.verify(sql[0],ret_code=2001,state="0",biz_id='s0012017111422263413',req_sn='s0012017092200000917')
    assert_util.verify(sql[1],ret_code=2001,state="0",biz_id='s001201709290021338',req_sn='s0012017092200000917')

@TestCase
def test_receiptPartfail():
    # 批量扣款：部分请求成功
    mysql_util.clear("settle_receipt_bill","settle_receipt_bill_biz")
    result = http_util.post("/route/receipt/batch", body=req_model.addreceiptparame("s0012017111422263421"))
    assert_util.verify(result, resultCode="4000", resultMsg=u"部分成功", reqSn="s0012017092200000918",systemSourceId="s001", chnId="ch001")
    assert_util.verify(result["receipRestList"][0], state="-2", resultCode="1000", resultMsg=u"订单接收失败：手机号无效：189；",bizId="s0012017111422263421", systemSourceId="s001", chnId="ch001")
    assert_util.verify(result["receipRestList"][1], state="0", resultCode="2001", resultMsg=u"等待收款", bizId="s0012017111422263431", systemSourceId="s001", chnId="ch001")
    sql = mysql_util.query("settle_receipt_bill_biz", req_sn='s0012017092200000918')
    print json.dumps(sql, indent=4, sort_keys=True)
    assert_util.verify(sql[1], ret_code="2001", state="0", biz_id='s0012017111422263431', req_sn='s0012017092200000918')


if __name__ == '__main__':
    test_receiptPartfail()