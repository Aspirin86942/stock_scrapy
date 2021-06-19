import requests
import re
import json
import pandas
import time
from time import strftime


def stock_scrapy(page: int):
    """
    :param page: int 向服务器请求的当前页数
    :return: response.text 返回页面请求后服务器发回的字符串
    """

    """
    1. 目标页面：http://quote.eastmoney.com/center/gridlist.html#hs_a_board
    2. 根据网页源代码发现后台请求地址：http://71.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240708890588897763_1621786127
    509&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,
    m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,
    f136,f115,f152&_=1621786127510
    3. 网页请求方式：get  
    """

    url = "http://71.push2.eastmoney.com/api/qt/clist/get?"

    # 封装headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "90.0.4430.212 Safari/537.36"
    }

    # 封装params
    params = {
        "cb": "jQuery11240708890588897763_1621786127509",
        "pn": page,
        "pz": "20",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,"
                  "f22,f11,f62,f128,f136,f115,f152",
        "_": "1621786127510"
    }

    resp = requests.get(url=url, headers=headers, params=params)
    resp.close()
    time.sleep(1)
    return resp.text
    # print(resp.url)
    # print(resp.text)


def convert_json(resp_string: str):
    """
    :param resp_string:
    :return: json_content 返回可以识别的json格式
    """

    """
      对于服务器返回内容进行一定的处理，使用正则去除前面部分数字，返回标准的json格式
    """
    reg_content = str()
    obj = re.compile(r"jQuery[0-9]+_[0-9]+[(](?P<content>.*?)[)]", re.S)
    result = obj.finditer(resp_string)
    for it in result:
        reg_content = it.group("content")
    json_content = json.loads(reg_content)
    # print(json_content)
    return json_content


def content_parser(json_content):
    """

    :param json_content:
    :return:
    """

    """
    1.取得的字段：
    json格式第一层级取数key值为data，第二层级key值为diff，对应的value值为list，循环取字段去除list中的字典的key值，
    形成pandas可以读取的格式
    2.参数
    参数 f1 null
    参数 f2 最新价 recent_quotation
    参数 f3 涨跌幅（百分之）change_percent
    参数 f4 涨跌额 change_price
    参数 f5 成交量（手） turnover
    参数 f6 成交额  business_volume
    参数 f7 振幅（百分之） amplitude_percent
    参数 f8 换手率（百分之） turnover_rate_percent
    参数 f9 市盈率（动态） pe_ratio_dynamic
    参数 f10 量比 volumes_ratio
    参数 f11 5分钟涨跌 change_5m
    参数 f12 代码 stock_code
    参数 f13 null
    参数 f14 名称 stock_name
    参数 f15 最高 highest
    参数 f16 最低 lowest
    参数 f17 今开 open
    参数 f18 昨收 close
    参数 f20 总市值 market_value
    参数 f21 流动市值 fluid_value
    参数 f22 涨速（百分之）rising_speed_percent
    参数 f23 市净率 pb_ratio
    参数 f24 60日涨跌幅（百分之） change_60d_percent
    参数 f25 年初至今日涨跌幅（百分之） change_BY_percent
    参数 f62 今日主力净流入 m_inflow
    补充一个参数 日期
    """
    containers = list()
    re_date = strftime(r"%Y-%m-%d", time.localtime(time.time()))
    for stock_info in json_content["data"]["diff"]:
        # print(stock_info)
        container = [
            stock_info["f2"], stock_info["f3"], stock_info["f4"], stock_info["f5"], stock_info["f6"],
            stock_info["f7"], stock_info["f8"], stock_info["f9"], stock_info["f10"], stock_info["f11"],
            "{0}".format(stock_info["f12"]), stock_info["f14"], stock_info["f15"], stock_info["f16"], stock_info["f17"],
            stock_info["f18"], stock_info["f20"], stock_info["f21"], stock_info["f22"], stock_info["f23"],
            stock_info["f24"], stock_info["f25"], stock_info["f62"], re_date
        ]
        # print(container)
        # print(stock_info["f12"])
        containers.append(container)
    return containers


def input_dataframe(df):
    """
    对相关数据进行排序和重命名
    并且添加一列日期
    并且对于空值"-"替换为0
    """
    rename_dict = {
        0: "recent_quotation",
        1: "change_percent",
        2: "change_price",
        3: "turnover",
        4: "business_volume",
        5: "amplitude_percent",
        6: "turnover_rate_percent",
        7: "pe_ratio_dynamic",
        8: "volumes_ratio",
        9: "change_5m",
        10: "stock_code",
        11: "stock_name",
        12: "highest",
        13: "lowest",
        14: "open",
        15: "close",
        16: "market_value",
        17: "fluid_value",
        18: "rising_speed_percent",
        19: "pb_ratio",
        20: "change_60d_percent",
        21: "change_BY_percent",
        22: "m_inflow",
        23: "re_date"
    }

    df.rename(columns=rename_dict, inplace=True)
    # print(df)
    df.replace("^-$", 0, regex=True, inplace=True)
    # print(df)
    return df


def store_dataframe(df):
    filename = strftime(r"%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    df.to_csv(path_or_buf="{0}.csv".format(filename), header=True, index=True, index_label="index",
              encoding='utf_8_sig')
    print("{0}.csv已生成".format(filename))


def stock_collection():
    """
    对于网页的页数对应生成循环查询，归集到容器stock_list中，统一进入pandas
    """
    loop_page = 1
    stock_list = list()
    while True:
        stock_json = convert_json(resp_string=stock_scrapy(page=loop_page))
        if stock_json["data"] is None:
            print("读取到尽头")
            break
        else:
            print("正在读取第{0}页".format(loop_page))
            stock_list += content_parser(stock_json)
            loop_page += 1
            # if loop_page == 142:
            #     break
    df_stock = pandas.DataFrame(stock_list)
    # print(df_stock)
    return df_stock


if __name__ == "__main__":
    df = stock_collection()
    df = input_dataframe(df=df)
    store_dataframe(df=df)
