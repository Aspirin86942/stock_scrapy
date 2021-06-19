import stock_scrapy
import trading_date
import pandas as pd
from sqlalchemy import create_engine
import time
from time import strftime
import pymysql


def check_date(connect, cursor, date):
    sql = "select count(re_date) from stock_info where re_date='{0}';".format(date)
    cursor.execute(sql)
    while True:
        res = cursor.fetchone()
        if res is None:
            # 表示已经取完结果集
            break
        if res[0] == 0:
            return True
        else:
            return False
    db_close(connect=connect, cursor=cursor)


def check_sheet(connect, cursor, sheet_name):
    sql = "select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA='stock' and TABLE_NAME='{0}' ;"\
        .format(sheet_name)
    cursor.execute(sql)
    while True:
        res = cursor.fetchone()
        if res is None:
            # 表示已经取完结果集
            break
        # print(res)
        if res is None:
            return False
        else:
            return True


def db_update(date):
    conn = db_connect()
    cur = db_cursor(connect=conn)
    if check_sheet(connect=conn, cursor=cur, sheet_name="stock_info"):
        if check_date(connect=conn, cursor=cur, date=date):
            df = stock_scrapy.input_dataframe(df=stock_scrapy.stock_collection())
            # print(df)
            data_send(df, connect=conn, cursor=cur)
        else:
            print("今日数据已经更新完毕，不再重复更新")
    else:
        df = stock_scrapy.input_dataframe(df=stock_scrapy.stock_collection())
        data_send(df, connect=conn, cursor=cur)
        db_close(connect=conn, cursor=cur)


def data_send(df, connect, cursor):
    if check_sheet(connect=connect, cursor=cursor, sheet_name="stock_info"):
        # MySQL的用户：root, 密码:123456, 端口：3306, 数据库：stock
        engine = create_engine('mysql+pymysql://root:123456@localhost:3306/stock')
        # 将DataFrame储存为MySQL中的数据表
        df.to_sql('stock_info', engine, if_exists="append", index=False)
        print('数据更新完毕')
    else:
        engine = create_engine('mysql+pymysql://root:123456@localhost:3306/stock')
        # 将DataFrame储存为MySQL中的数据表
        df.to_sql('stock_info', engine, index=False)
        print('数据初次更新完毕')


def db_connect():
    connect = pymysql.connect(  # 连接数据库服务器
        user="root",
        password="123456",
        host="localhost",
        port=3306,
        db="stock"
    )
    return connect


def db_cursor(connect):
    cursor = connect.cursor()  # 创建操作游标
    return cursor


def db_close(connect, cursor):
    cursor.close()
    connect.close()


if __name__ == "__main__":
    # date = strftime(r"%Y-%m-%d", time.localtime(time.time()))
    date = trading_date.get_date()
    db_update(date=date)
    # conn = db_connect()
    # cur = db_cursor(conn)
    # check_date(cursor=cur,date="2021-05-25")
    # check_sheet(connect=conn, cursor=cur, sheet_name="stock_code")
