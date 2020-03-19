# coding:utf-8
import time
from common.database import DB
"""
用于将站点name与站点code之间的转换
"""

db = DB("stations")
stations_cache = {}  # 利用cache减少检索数据库相同数据的次数{"PXX":(PXX,yy), "yy":(PXX,yy)}为保证双向
"""
['嘉兴一中实验学校', '泾水公寓西区', '中山西路秀园路(民泰银行)']
耗时0.0018355000000000177
['嘉兴一中实验学校', '泾水公寓西区', '中山西路秀园路(民泰银行)']
耗时6.8000000000012495e-06    
['P94', 'P85', 'P26']
耗时5.699999999997374e-06
['P94', 'P85', 'P26']
耗时4.599999999993498e-06
"""


def print_time(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        print("耗时{}".format(end - start))
    return inner


def convert_name_to_code(stop_name):
    """
    单个站点转换
    :param stop_name: str类型的站点名称
    :return:    返回代码
    """
    sql = "SELECT station_id FROM station_table WHERE station_name ='{}'".format(stop_name)
    db.execute_sql(sql)
    # print(db.get_one())
    stop_id = db.get_one()
    stations_cache[stop_name] = (stop_id, stop_name)
    stations_cache[stop_id] = (stop_id, stop_name)
    return stop_id


# @print_time
def convert_name_to_code_arr(stop_name_arr):
    arr = []
    for stop_name in stop_name_arr:
        if stop_name in stations_cache:
            stop_id = stations_cache[stop_name][0]
        else:
            stop_id = convert_name_to_code(stop_name)
        arr.append(stop_id)
    # print(arr)
    return arr


def convert_code_to_name(stop_id):
    """
    单个站点转换
    :param stop_id: str类型的站点名称
    :return:    返回名称
    """
    sql = "SELECT station_name FROM station_table WHERE station_id ='{}'".format(stop_id)
    db.execute_sql(sql)
    # print(db.get_one())
    stop_name = db.get_one()
    stations_cache[stop_name] = (stop_id, stop_name)
    stations_cache[stop_id] = (stop_id, stop_name)
    return stop_name


# @print_time
def convert_code_to_name_arr(stop_id_arr):
    arr = []
    for stop_id in stop_id_arr:
        if stop_id in stations_cache:
            stop_name = stations_cache[stop_id][1]
        else:
            stop_name = convert_code_to_name(stop_id)
        arr.append(stop_name)
    # print(arr)
    return arr


if __name__ == "__main__":
    # convert_name_to_code("真合路城南路")
    # convert_code_to_name("P111")
    convert_code_to_name_arr(["P94", "P85", "P26"])
    convert_code_to_name_arr(["P94", "P85", "P26"])
    convert_name_to_code_arr(['嘉兴一中实验学校', '泾水公寓西区', '中山西路秀园路(民泰银行)'])
    convert_name_to_code_arr(['嘉兴一中实验学校', '泾水公寓西区', '中山西路秀园路(民泰银行)'])
    print(stations_cache)
