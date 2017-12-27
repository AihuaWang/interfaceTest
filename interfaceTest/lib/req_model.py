# coding=utf-8
import datetime
import time
from util import mysql_util


#获取当前时间
current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#获取昨天的当前时间
start_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
#获取有天的当前时间
end_date =  (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
#获取当天日期
tody=time.strftime('%Y-%m-%d',time.localtime(time.time()))


def addpaymentstate(bankId):
    #构造代付入参
    #接收失败返回-2 bankId：s0012017111422263310
    if bankId=="s0012017111422263310":
        return {"accountName":"刘小燕","accountNo":"64128301019232332","amount":"10","bankId":"308","bizId":"s0012017111422263310","cardKind":"01","chnId":"ch001","openBankName":"商银行","systemSourceId":"s001","receiveTime":current_time}
    # 交易失败的返回状态为-1 bankId：s0012017111422263311
    elif bankId=="s0012017111422263311":
        return {"accountName":"刘小燕","accountNo":"64128301019232332","amount":"10","bankId":"308","bizId":"s0012017111422263311","cardKind":"01","chnId":"ch001","openBankName":"招商银行","systemSourceId":"s001","receiveTime":current_time}
    # 交易成功返回状态为1 bankId：s0012017111422263312
    elif bankId=="s0012017111422263312":
        return {"accountName":"刘小燕","accountNo":"64128301019232332","amount":"10","bankId":"308","bizId":"s0012017111422263312","cardKind":"01","chnId":"ch001","openBankName":"招商银行","systemSourceId":"s001","receiveTime":current_time}
    # 交易处理中（订单已接收，等待交易）返回状态为0 bankId：s0012017111422263313
    elif bankId=="s0012017111422263313":
        return {"accountName":"刘小燕","accountNo":"64128301019232332","amount":"10","bankId":"308","bizId":"s0012017111422263313","cardKind":"01","chnId":"ch001","openBankName":"招商银行","systemSourceId":"s001","receiveTime":current_time}
    # 交易处理中（渠道已受理）返回状态为3 bankId：s0012017111422263315
    elif bankId=="s0012017111422263315":
        return {"accountName":"刘小燕","accountNo":"64128301019232332","amount":"10","bankId":"308","bizId":"s0012017111422263315","cardKind":"01","chnId":"ch001","openBankName":"招商银行","systemSourceId":"s001","receiveTime":current_time}

def addpaymentparame(bizId=None):
    #入参校验：订单号bizId校验
    #有效的入参数校验
    if bizId==("s0012017111422263320"):
        return {"bizId":"s0012017111422263320", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    #入参为无效的订单id，bizId=1000001
    elif bizId == ("1000001"):
        return {"bizId":"1000001", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    #入参为空的订单ID bizId=null
    elif bizId == (""):
        return {"bizId":"", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    #入参为重复的订单ID，bizId=s0012017111422263312
    elif bizId == ("s0012017111422263320"):
        return {"bizId":"s0012017111422263320", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    # 入参的订单ID为s00002开头（s000022017111422263312）
    elif bizId == ("s000022017111422263312"):
        return {"bizId":"s000022017111422263312", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    #入参校验：系统来源systemSourceId
    #入参校验系统来源systemSourceId为空
    elif bizId ==("s0012017111422263351"):
        return {"bizId":"s0012017111422263351", "systemSourceId":"", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    # 入参校验系统来源systemSourceId不存在的
    elif bizId == ("s0012017111422263352"):
        return {"bizId":"s0012017111422263352", "systemSourceId":"s0000001", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    #入参校验：amount
    # 入参校验付款金额:amount为空
    elif bizId == ("s0012017111422263353"):
        return {"bizId":"s0012017111422263353", "systemSourceId":"s001", "amount":"", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    # 入参校验付款金额:amount保留两位小数
    elif bizId == ("s0012017111422263354"):
        return {"bizId":"s0012017111422263354", "systemSourceId":"s001", "amount":10.12, "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    #入参校验：accountName
    # 入参校验银行卡姓名:accountName为空
    elif bizId == ("s0012017111422263355"):
        return {"bizId":"s0012017111422263355", "systemSourceId":"s001", "amount":"10", "accountName":"", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    #入参校验：bankId
    #入参校验银行卡代码:bankId为空
    elif bizId == ("s0012017111422263356"):
        return {"bizId":"s0012017111422263356", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    # 入参校验银行卡代码与银行卡不一致
    elif bizId == ("s0012017111422263357"):
        return {"bizId":"s0012017111422263357", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"3009", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    #入参校验：accountNo
    #入参校验银行卡号:accountNo为空
    elif bizId == ("s0012017111422263358"):
        return {"bizId":"s0012017111422263358", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    #开户行名称：openBankName
    #入参校验开户行名称为空
    elif bizId==("s0012017111422263359"):
        return {"bizId":"s0012017111422263359", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    #入参校验开户行名称与卡号不一致
    elif bizId==("s0012017111422263360"):
        return {"bizId":"s0012017111422263360", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}
    #订单时间：receiveTime
    #入参校验订单时间为空
    elif bizId==("s0012017111422263361"):
        return {"bizId":"s0012017111422263361", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":"", "cardKind":"01", "chnId":"ch001"}
    #渠道来源：chnId
    #入参校验渠道来源为空
    elif bizId==("s0012017111422263362"):
        return {"bizId":"s0012017111422263362", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":""}
    #入参数渠道来源为不存在
    elif bizId==("s0012017111422263363"):
        return {"bizId":"s0012017111422263363", "systemSourceId":"s001", "amount":"10", "accountName":"刘小燕", "bankId":"308", "accountNo":"64128301019232332", "openBankName":"招商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch00001"}

def addpaymentroute(bizId):
    #路由规则校验
    if bizId == ("s0012017111422263390"):
        return {"bizId":"s0012017111422263390", "systemSourceId":"s001", "amount":"200000", "accountName":"刘小燕", "bankId":"102", "accountNo":"6212260200135100697", "openBankName":"工商银行", "receiveTime":current_time, "cardKind":"01", "chnId":"ch001"}



def addreceiptstate(bankId):
    #构造代扣入参
    #接收失败返回-2 bankId：s0012017111422263410
    if bankId=="s0012017111422263410":
        return {"accountName":"刘小燕","accountNo":"6214830101923232","amount":"10","bankId":"308","bizId":"s0012017111422263410","cardKind":"01","chnId":"ch001","idCard":"130728198907127027","mobile":"15901537568", "systemSourceId":"s001","receiveTime":current_time}
    # 交易失败的返回状态为-1 bankId：s0012017111422263411
    elif bankId=="s0012017111422263411":
        return {"accountName":"刘小燕","accountNo":"6295830167899098","amount":"10","bankId":"308","bizId":"s0012017111422263411","cardKind":"01","chnId":"ch001","idCard":"130728198907","mobile":"15901537568", "systemSourceId":"s001","receiveTime":current_time}
    # 交易失败的返回状态为-1 accountName：s0012017111422263421
    elif bankId == "s0012017111422263421":
        return {"accountName": "刘", "accountNo": "6295830167899098", "amount": "10", "bankId": "308","bizId": "s0012017111422263421", "cardKind": "01", "chnId": "ch001", "idCard": "130728198907127027","mobile": "15901537568", "systemSourceId": "s001", "receiveTime": current_time}
    # 交易失败的返回状态为-1 accountNo：s0012017111422263431
    elif bankId == "s0012017111422263431":
        return {"accountName": "刘小燕", "accountNo": "6295830167899098", "amount": "10", "bankId": "308","bizId": "s0012017111422263431", "cardKind": "01", "chnId": "ch001", "idCard": "130728198907127027","mobile": "15901537568", "systemSourceId": "s001", "receiveTime": current_time}
    # 交易成功返回状态为1 bankId：s0012017111422263412
    elif bankId=="s0012017111422263412":
        return {"accountName":"刘小燕","accountNo":"6214830101923232","amount":"10","bankId":"308","bizId":"s0012017111422263412","cardKind":"01","chnId":"ch001","idCard":"130728198907127027","mobile":"15901537568", "systemSourceId":"s001","receiveTime":current_time}
    # 交易处理中（订单已接收，等待交易）返回状态为0返回状态为0 bankId：s0012017111422263413
    elif bankId=="s0012017111422263413":
        return {"accountName":"刘小燕","accountNo":"6295830167899098","amount":"10","bankId":"308","bizId":bankId,"cardKind":"01","chnId":"ch001","idCard":"140421989787876","mobile":"15901537568", "systemSourceId":"s001","receiveTime":current_time}
    # 交易处理中处理中（渠道已受理）返回状态为3 bankId：s0012017111422263415
    elif bankId=="s0012017111422263415":
        return {"accountName":"刘小燕","accountNo":"6295830167899098","amount":"10","bankId":"308","bizId":bankId,"cardKind":"01","chnId":"ch001","idCard":"140421989787876","mobile":"15901537568", "systemSourceId":"s001","receiveTime":current_time}

def addreceiptparame(bizId):
    #入参校验：订单号bizId校验
    #有效的入参数校验
    if bizId==("s001201711142226420"):
        return{"bizId": "s001201711142226420", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    #入参为无效的订单id，bizId=1000001
    elif bizId == ("1000001"):
        return{"bizId": "1000001", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    #入参为空的订单ID bizId=null
    elif bizId == (""):
        return{"bizId": "", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    #入参为重复的订单ID，bizId=s0012017111422263410
    elif bizId == ("s0012017111422263410"):
        return{"bizId": "s0012017111422263410", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    # 入参的订单ID为s00002开头（s00002201711142226333313）
    elif bizId == ("s00002201711142226333313"):
        return{"bizId": "s00002201711142226333313", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    #入参校验：系统来源systemSourceId
    #入参校验系统来源systemSourceId为空
    elif bizId ==("s001201711142226421"):
        return{"bizId": "s001201711142226421", "systemSourceId": "", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    # 入参校验系统来源systemSourceId不存在的
    elif bizId == ("s001201711142226422"):
        return{"bizId": "s001201711142226422", "systemSourceId": "s0000001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    #入参校验：amount
    # 入参校验付款金额:amount为空
    elif bizId == ("s001201711142226423"):
        return{"bizId": "s001201711142226423", "systemSourceId": "s001", "amount": "", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    # 入参校验付款金额:amount保留两位小数
    elif bizId == ("s001201711142226424"):
        return{"bizId": "s001201711142226424", "systemSourceId": "s001", "amount": "10.11", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    #入参校验：accountName
    # 入参校验银行卡姓名:accountName为空
    elif bizId == ("s001201711142226425"):
        return{"bizId": "s001201711142226425", "systemSourceId": "s001", "amount": "10", "accountName": "","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    #入参校验：bankId
    #入参校验银行卡代码:bankId为空
    elif bizId == ("s001201711142226426"):
        return{"bizId": "s001201711142226426", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    # 入参校验银行卡代码与银行卡不一致
    elif bizId == ("s001201711142226427"):
        return{"bizId": "s001201711142226427", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "3009", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    #入参校验：accountNo
    #入参校验银行卡号:accountNo为空
    elif bizId == ("s001201711142226428"):
        return{"bizId": "s001201711142226428", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "", "idCard": "130728198907127027", "mobile":"15901537568"}
    # 入参校验银行卡不足16位
    elif bizId == ("s001201711142226429"):
        return{"bizId": "s001201711142226429", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301", "idCard": "130728198907127027", "mobile":"15901537568"}
    #身份证验证：idCard
    #入参身份证号为空
    elif bizId==("s001201711142226430"):
        return{"bizId": "s001201711142226430", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "", "mobile":"15901537568"}
    #入参校验身份证是无效的
    elif bizId==("s001201711142226431"):
        return{"bizId": "s001201711142226431", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127222", "mobile":"15901537568"}
    #订单时间：receiveTime
    #入参校验订单时间为空
    elif bizId==("s001201711142226432"):
        return{"bizId": "s001201711142226432", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": "", "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    #渠道来源：chnId
    #入参校验渠道来源为空
    elif bizId==("s001201711142226433"):
        return{"bizId": "s001201711142226433", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    #入参数渠道来源为不存在
    elif bizId==("s001201711142226434"):
        return{"bizId": "s001201711142226434", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch000001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"15901537568"}
    #电话号杩校验mobile
    #入参校验电话号码为空
    elif bizId==("s001201711142226435"):
        return{"bizId": "s001201711142226435", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":""}
    #入参校验电话号码非1开头
    elif bizId == ("s001201711142226436"):
        return{"bizId": "s001201711142226436", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"31513134715"}
    #入参校验电话号码不是11位
    elif bizId == ("s001201711142226437"):
        return{"bizId": "s001201711142226437", "systemSourceId": "s001", "amount": "10", "accountName": "刘小燕","bankId": "308", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "64128301019232332", "idCard": "130728198907127027", "mobile":"159015375"}
    #批量请求调用成功的
    elif bizId == ("s001201711142226438"):
        return {"reqSn": "s0012017092200000917", "systemSourceId": "s001", "chnId": "ch001", "receiveTime": current_time,"receiptList": [{"accountName": "刘小燕","accountNo":  "6214830101923232", "amount": "5", "bankId": "308","bizId": "s0012017111422263413", "idCard": "130728198907127027", "mobile": "18910377203"},{"accountName":  "钱宝", "accountNo": "6212260200135100697", "amount": "90", "bankId": "102","bizId": "s001201709290021338", "idCard": "130728198907127027", "mobile": "15901537568"}]}
    #批量请求调用部分成功的
    elif bizId == ("s0012017111422263421"):
        return {"reqSn": "s0012017092200000918", "systemSourceId": "s001", "chnId": "ch001", "receiveTime": current_time,"receiptList": [{"accountName": "刘小燕","accountNo":  "6214830101923232", "amount": "5", "bankId": "308","bizId": "s0012017111422263421", "idCard": "130728198907127027", "mobile": "189"},{"accountName":  "钱宝", "accountNo": "6212260200135100697", "amount": "90", "bankId": "102","bizId": "s0012017111422263431", "idCard": "130728198907127027", "mobile": "15901537568"}]}


def addreceiptroute(amout):
    # 路由规则校验
    if amout == ("600"):
        return {"bizId": "s001201711142226450", "systemSourceId": "s001", "amount": "600", "accountName": "刘小燕","bankId": "102", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "6212260200135100697", "idCard": "130728198907127027", "mobile": "15901537568"}
    elif amout== ("50000"):
        return {"bizId": "s001201711142226450", "systemSourceId": "s001", "amount": "50000", "accountName": "刘小燕","bankId": "102", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "6212260200135100697", "idCard": "130728198907127027", "mobile": "15901537568"}
    elif amout== ("50000"):
        return {"bizId": "s001201711142226450", "systemSourceId": "s001", "amount": "50000", "accountName": "刘小燕","bankId": "102", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "6212260200135100697", "idCard": "130728198907127027", "mobile": "15901537568"}
    elif amout== ("990000"):
        return {"bizId": "s001201711142226450", "systemSourceId": "s001", "amount": "990000", "accountName": "刘小燕","bankId": "102", "receiveTime": current_time, "cardKind": "01", "chnId": "ch001","accountNo": "6212260200135100697", "idCard": "130728198907127027", "mobile": "15901537568"}

def addbacks(bizId):
    # 异步回调
    if bizId == ("s00120171123142223434"):
        mysql_util.insert("settle_payment_bill_biz",id=100,create_time=current_time,modify_time=current_time,status=1,version=1,state=0,chn_id="ch001",ret_code=2005,ret_info="等待付款",account_name='刘小燕',account_no='6214830101923232',amount=11,bank_id=308,biz_id="s00120171123142223434",open_bank_name="招商银行",reserve_time=current_time,system_source_id="s001",trade_time=current_time)
        mysql_util.insert("settle_payment_bill",bill_biz_id=100,create_time=current_time,modify_time=current_time,status=1,version=1,state=2,chn_id="ch001",ret_code=2000,ret_info="渠道已成功接收",account_name='刘小燕',account_no='6214830101923232',amount=11,bank_id=308,biz_id="s00120171123142223434",open_bank_name="招商银行",reserve_time=current_time,system_source_id="s001",trade_time=current_time)
    else:
        mysql_util.insert("settle_receipt_bill_biz",id=200,create_time=current_time,modify_time=current_time,status=1,version=1,state=0,chn_id="ch001",ret_code=2005,ret_info="等待付收款",account_name='刘小燕',account_no='6214830101923232',amount=11,bank_id=308,biz_id="s00120171204r00004866",open_bank_name="招商银行",reserve_time=current_time,system_source_id="s001",trade_time=current_time)
        mysql_util.insert("settle_receipt_bill",id=200,create_time=current_time,modify_time=current_time,status=1,version=1,state=0,chn_id="ch001",ret_code=2005,ret_info="等待收款",account_name='刘小燕',account_no='6214830101923232',amount=11,bank_id=308,biz_id="s00120171204r00004866",open_bank_name="招商银行",reserve_time=current_time,system_source_id="s001",trade_time=current_time)

