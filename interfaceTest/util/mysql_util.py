# coding=utf-8
import json
from datetime import datetime

import configparser
import pymysql
from decimal import Decimal

config = configparser.ConfigParser()
config.read('../conf/config.ini')

mysql_host = config['DEFAULT']['MYSQL_HOST']
mysql_port = config['DEFAULT']['MYSQL_PORT']
mysql_db = config['DEFAULT']['MYSQL_DB']
mysql_user = config['DEFAULT']['MYSQL_USER']
mysql_password = config['DEFAULT']['MYSQL_PASSWORD']


def __get_connection():
    connection = pymysql.connect(host=mysql_host,
                                 user=mysql_user,
                                 password=mysql_password,
                                 db=mysql_db,
                                 port=int(mysql_port),
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def insert(table, **kwargs):
    """
    插入数据
    :param table: 表名
    :param kwargs: 字段参数
    :return:
    """
    connection = __get_connection()

    if len(kwargs.items()) > 0:
        col_str = "("
        value_str = "("
        for key, value in kwargs.items():
            col_str = col_str + "`{0}`,".format(key)
            if isinstance(value, basestring):
                value_str = value_str + "\"{0}\",".format(value)
            else:
                value_str = value_str + "{0},".format(value)
        col_str = col_str[:-1] + ")"
        value_str = value_str[:-1] + ")"
    else:
        col_str = "()"
        value_str = "()"

    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `{0}` {1} VALUES {2}".format(table, col_str, value_str)
        print "===>mysql: ", sql
        cursor.execute(sql)
    connection.commit()


def update(table, where_string, **columns):
    if not where_string:
        raise Exception, u"where语句不能为空"
    if len(columns.items()) <= 0:
        raise Exception, u"必须指定更新字段"
    sql = "update {0} set  ".format(table)

    for key, value in columns.items():
        if isinstance(value, basestring):
            sql += u" {0}='{1}',".format(key, value)
        else:
            sql += u" {0}={1},".format(key, value)

    sql = sql[:-1]
    sql += " where {0} ".format(where_string)

    connection = __get_connection()
    with connection.cursor() as cursor:
        print "===>mysql: ", sql
        cursor.execute(sql)
    connection.commit()

def query(table, **wheres):
    result = []
    where_str = ""
    index = 0
    for key, value in wheres.items():
        index += 1
        if isinstance(value, basestring):
            where_str += u" {0}='{1}'".format(key, value)
        else:
            where_str += u" {0}={1}".format(key, value)
        if index < len(wheres):
            where_str += " and"

    sql = "SELECT * FROM %s " % table
    if where_str:
        sql += " where %s " % where_str
    try:

        connection = __get_connection()
        with connection.cursor() as cursor:
            print "===>mysql: ", sql
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        connection.close()

    for item in result:
        for key, value in item.items():
            if isinstance(value, datetime):
                item[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(value, Decimal):
                item[key] = str(value)
    return result

def clear(*tables):
    """
    清除表所有数据
    :param tables: 表名，可以多个
    :return:
    """
    if len(tables) > 0:
        for table in tables:
            connection = __get_connection()
            with connection.cursor() as cursor:
                sql = "delete from {0}".format(table)
                cursor.execute(sql)
            connection.commit()


if __name__ == '__main__':
    # insert("users", email="hhh@hhh.com", password="asdfasd")
    # clear("users")
    # update settle_payment_bill set state=0 where id=8844
    # update("settle_payment_bill", "id=8844", state=0)
    ret = query(table="settle_payment_bill_biz",state=0,ret_code=2005)
    print json.dumps(ret, indent=4, sort_keys=True)