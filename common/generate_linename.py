# coding:utf-8
from common.database import DB

"""
本模块  线路信息---->线路名称
由于要计算线路序号，因此要根据已有数据。
1. 需要加载数据库中线路名称（加载数据库信息前必须保证后台信息与db中保持一致）
2. 调用generate_line_name()，生成线路名称。
3. 当线路add成功后，才能将新的线路名称更新到列表：调用update_existing_line_names()
"""


# 为避免不必要的非时间组合错误,分开时间表
junior_timetable_dict = {
    "21:00:00": "N1",   # 周日到周四--初1初2
    "21:30:00": "N2",   # 周日到周四--初3
    "15:25:00": "F1",   # 周五--初1
    "16:15:00": "F2",   # 周五--初2
    "17:05:00": "F3"    # 周五--初3
}

senior_timetable_dict = {
    "21:30:00": "N2",   # 周日到周五--高123
    "15:25:00": "S2",   # 周六--高1/2
    "10:20:00": "S1"    # 周六--高3
}

existing_line_names = []


def ini_existing_line_names():
    """
    加载已有线路列表
    :return:
    """
    db = DB("busline")
    sql = "SELECT lineName FROM yzbusline"
    db_result = db.execute_sql(sql)
    if db_result == 0:
        raise Exception("****ERROR: 数据表中无数据****")
    else:
        items = db.get_all()
        existing_line_names.extend([i[0] for i in items])
    # print("数据库中已存在的线路名称: \n{}".format(existing_line_names))


def generate_line_name(grade, start_time):
    """
    根据输入的年级与时间生成线路名称
    :param grade:          年级
    :param start_time:     开车时间
    :return:               返回线路名称
    """
    assert grade in ["初中", "高中"], "**ERROR: excel中年级类型输入错误**"

    school_prefix = "S0A"  # 一中实验
    if grade == "初中":
        grade_type = "J"
        assert start_time in junior_timetable_dict.keys(), "**ERROR: excel中初中发车时间输入错误{}**".format(start_time)
        period = junior_timetable_dict[start_time]
    else:
        grade_type = "S"
        assert start_time in senior_timetable_dict.keys(), "**ERROR: excel中高中发车时间输入错误{}**".format(start_time)
        period = senior_timetable_dict[start_time]

    pattern = school_prefix + grade_type + period
    # print("当前线路类型{}".format(pattern))

    same_line_pattern = [existing_line_name for existing_line_name in existing_line_names
                         if pattern in existing_line_name]
    # 简化写法
    # for existing_line_name in existing_line_names:
    #     if pattern in existing_line_name:
    #         same_line_pattern.append(existing_line_name)
    # print(same_line_pattern)

    # 若还未存在线路编号
    if len(same_line_pattern) == 0:
        line_number = "{:0>2d}".format(1)
    else:
        same_pattern_final_num = sorted(same_line_pattern, reverse=True)[0].split('-')[1]
        line_number = "{:0>2d}".format(int(same_pattern_final_num) + 1)

    line_name = pattern + '-' + line_number
    print("生成新线路名称:{}".format(line_name))
    return line_name


def update_existing_line_names(new_line_name):
    """
    将生成的新线路名加入已有线路名称列表
    :param new_line_name:   新线路名
    :return:
    """
    existing_line_names.append(new_line_name)


if __name__ == "__main__":
    pass

    # 使用方法
    # ini_existing_line_names()
    # insert_list = [("初中", "21:30:00"), ("初中", "21:30:00"),
    #                ("高中", "21:00:00"), ("高中", "21:30:00")
    #                ]
    # for (grade, time) in insert_list:
    #     try:
    #         new_name = generate_line_name(grade, time)
    #     except Exception as e:
    #         print(e)
    #     update_existing_line_names(new_name)

