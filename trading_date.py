import requests
import time
import re
import json


def kline_scrapy():
    """

    1.目标页面：
    2.根据网页源代码发现后台请求地址：http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112404834518910200123_1622
    003279709&secid=1.000001&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%
    2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&klt=101&fqt=0&beg=19900101&end=20220101&_=1622003279775
    3.网页请求方式：get

    """
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get?"

    # 封装headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "90.0.4430.212 Safari/537.36"
    }

    # 封装params
    params = {
        "cb": "jQuery112404834518910200123_1622003279709",
        "secid": "1.000001",
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
        "klt": "101",
        "fqt": "0",
        "beg": "20210101",
        "end": "20220101",
        "_": "1622003279775"

    }

    resp = requests.get(url=url, headers=headers, params=params)
    # print(resp.url)
    # print(resp.text)
    resp.close()
    time.sleep(1)

    return resp.text


def convert_json(resp_string, reg_content=None):
    obj = re.compile(r"jQuery[0-9]+_[0-9]+[(](?P<content>.*?)[)]", re.S)
    result = obj.finditer(resp_string)
    for it in result:
        reg_content = it.group("content")
    json_content = json.loads(reg_content)
    # print(json_content)
    return json_content


def date_parser(json_content):
    return str(json_content["data"]["klines"][-1]).split(",")[0]


def get_date():
    return date_parser(convert_json(resp_string=kline_scrapy()))


if __name__ == "__main__":
    print(get_date())
