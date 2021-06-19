class Scrapy (object):
    def __init__(self):
        pass

    def get(self, url: str):
        """
        向服务器url请求一次数据，并接受一次返回值
        :param url: str
        :return:
        """

        pass

    def gets(self):
        """
        生成json_parser实例
        向服务器url请求多次数据，然后使用Parser.str_to_json转换并将返回值合一，形成dataframe可以辨认的格式返回
        最终返回格式为[{key:value},{key:value},...]
        :param
        :return:
        """
        pass


class Parser(object):
    def __init__(self):
        pass

    def str_to_json(self):
        pass

    def json_to_df(self):
        """
        提供rename方法和replace方法
        :return:
        """
        pass


def main():
    """
    生成stock_scrapy实例
    调用stock_scrapy.gets查询数据，返回df形式数据
    调用json_to_df将字符串数据清洗并整理好，返回df数据
    """
    pass
