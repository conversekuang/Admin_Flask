# coding:utf-8
import pandas as pd
import os

"""
将excel每一行线路信息转换为后台可识别参数信息
"""


class File(object):
    """
    用于excel文件
    """

    def __init__(self, filepath="C:\\Users\\dell\\Desktop", filename="plan.xlsx"):
        """
        初始化
        :param filepath:    文件路径
        :param filename:    文件名称
        """

        self.path = filepath
        self.name = filename
        self.xls_df = self.convert_xls_to_df()

    def convert_xls_to_df(self):
        """
        将xls文件转换成为dataframe
        :return:
        """
        xls_df = pd.read_excel(os.path.join(self.path, self.name))
        return xls_df

    def convert_each_line_RowItem(self):
        """
        将xls每一行转换为dict类型返回
        :return:
        """
        # 将空的进行处理
        for index, row in self.xls_df.iterrows():
            # row中的字段 'date', 'weekday', 'lineNum', 'busNum', 'driver'
            yield RowItem(dict(row))

    def convert_each_line_into_param(self):
        """
        将xls每一行转换为dict类型返回
        :return:
        """
        self.xls_df.stops = self.xls_df.stops.fillna('')
        # 将空的进行处理
        for index, row in self.xls_df.iterrows():
            stops_arr = []
            # row中的字段 'grade', 'type', 'price', 'startTime', 'stops'
            each_dict = dict(row)
            each_dict['type'] = line_type_dict[each_dict['type']]  # 转换线路类型为int表达
            each_dict['startTime'] = each_dict['startTime'].isoformat()  # 转换时间为str表达
            if "," in each_dict['stops']:
                each_dict['stops'] = convert_name_to_code_arr(each_dict['stops'].split(","))
            else:
                each_dict['stops'] = None
            yield each_dict


class RowItem:

    def __init__(self, params):
        self.date = params['date']
        self.weekday = params['weekday']
        self.lineNum = params['lineNum']
        self.busNum = params['busNum']
        self.driver = params['driver']

    def __repr__(self):
        return "<RowItem(" \
               "date={},weekday={},lineNum={}," \
               "busNum={},driver={})>".format(self.date, self.weekday, self.lineNum,
                                              self.busNum, self.driver)


if __name__ == "__main__":
    file = File("C:\\Users\\dell\\Desktop", "plan.xlsx")
    for item in file.convert_each_line_RowItem():
        print(item)
