# -*- coding: utf-8 -*-
# @Author: dell
# @Date:   2019-05-28 11:07:41
# @Last Modified by:   converse
# @Last Modified time: 2019-08-10 22:29:47

import pandas as pd
from common.database import DB
import os
import json
from obtain_order.assistence import writefile, convert_csv_xls

"""
本文件依赖于
1. mysql数据库中的线路数据，所以要保证最新
2. 依赖总的order.xlsx文件
"""


def count_buyer_in_grade():
    print("统计各年级买票数量")
    df = pd.read_excel("账单的-order.xlsx")
    dic = {}
    total = 0

    for index, item in df.iterrows():
        if item['Account'][2:4] in dic.keys():
            dic[item['Account'][2:4]] += 1
        else:
            dic[item['Account'][2:4]] = 1

    for values in dic.values():
        total += values
    print(total)
    print("7年级 %d 买票人数" % dic['18'])
    print("8年级 %d 买票人数" % dic['17'])

    print("高一年级 %d 买票人数" % dic['21'])
    print("高二级 %d 买票人数" % dic['20'])


def count_buyer_in_type():
    print("统计购买乘车类型")
    df = pd.read_excel("账单的-order.xlsx")
    dic = {}
    total = 0

    for index, item in df.iterrows():
        if item['Account'] in dic.keys():
            dic[item['Account']].append(item['lineName'])
        else:
            dic[item['Account']] = [item['lineName']]

    both = 0
    friday = 0
    weekday = 0
    for key, value in dic.items():
        if len(value) == 2:
            both += 1
        elif len(value) == 1 and int(value[0][3:]) < 11:
            friday += 1
        elif len(value) == 1 and int(value[0][3:]) > 10:
            weekday += 1
        else:
            print(key, value)
    print("周日到周四", weekday)
    print("周五", friday)
    print("两种都买", both)


def count_each_route_number():
    """

    :return:
    """
    print("统计线路人数")
    df = pd.read_excel(r"F:\Python_project\IDE\Institude\download\order.xlsx")
    dic = {}
    total = 0
    for index, item in df.iterrows():
        if item['lineName'] in dic.keys():
            dic[item['lineName']] += 1
        else:
            dic[item['lineName']] = 1

    for key, val in sorted(dic.items(), key=lambda d: d[1], reverse=True):
        print(key, val)
    print(sum(dic.values()))


def count_each_schedule_number1():
    """
    统计班次总人数
    :return:
    """
    print("统计班次总人数")
    df = pd.read_excel("账单的-order.xlsx")
    dic = {}
    total = 0
    for index, item in df.iterrows():
        if item['scheduledName'] in dic.keys():
            dic[item['scheduledName']] += 1
        else:
            dic[item['scheduledName']] = 1
    count = 0
    for key, val in dic.items():
        if val > 0:
            print(key, '\t', val)
        count += 1
    print(count)


def count_each_schedule_number(filename, fieldnames):
    """
    打印线路以及站点的人数信息
    :return:
    """
    db = DB("busline")

    # TimeTable = {
    #     "JN1": "21:00:00",
    #     "JN2": "21:30:00",
    #     "JF1": "15:25:00",
    #     "JF2": "16:15:00",
    #     "JF3": "17:05:00",
    #     "JS1": "10:20:00",
    #     "JS2": "15:25:00",
    #     "SN2": "21:30:00",
    #     "SS1": "10:20:00"
    #
    # }

    print("统计班次总人数")
    line_number_dict = {}
    df = pd.read_excel(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "账单的-order.xlsx"))
    dic = {}
    names_dic = {}
    total = 0
    for index, item in df.iterrows():
        if item['lineName'] in dic.keys():
            if 'go' in item['lineName']:
                # boardingCode
                if item['boardingCode'] in dic[item['lineName']].keys():
                    dic[item['lineName']][item['boardingCode']] += 1
                    names_dic[item['lineName']][item['boardingCode']].append(item['memberName'])
                else:
                    dic[item['lineName']][item['boardingCode']] = 1
                    names_dic[item['lineName']][item['boardingCode']] = [item['memberName']]
            else:
                # dropOffCode

                if item['dropOffCode'] in dic[item['lineName']].keys():
                    dic[item['lineName']][item['dropOffCode']] += 1
                    names_dic[item['lineName']][item['dropOffCode']].append(item['memberName'])
                else:
                    dic[item['lineName']][item['dropOffCode']] = 1
                    names_dic[item['lineName']][item['dropOffCode']] = [item['memberName']]
        else:
            dic[item['lineName']] = {}
            names_dic[item['lineName']] = {}

            if 'go' in item['lineName']:
                dic[item['lineName']][item['boardingCode']] = 1
                names_dic[item['lineName']][item['boardingCode']] = [item['memberName']]
            else:
                dic[item['lineName']][item['dropOffCode']] = 1
                names_dic[item['lineName']][item['dropOffCode']] = [item['memberName']]

    total = 0
    print(dic)
    print(names_dic)
    json.dump(dic, open("人数.json", 'w'))
    json.dump(names_dic, open("人名称.json", 'w'))

    # for busno in range(51, 80):  # 修改辅号码
    #     db.execute_sql("SELECT lineName FROM ins36_busline WHERE busNumber ='{}'".format("辅" + str(busno)))
    #     lineName = db.get_one()

    db.execute_sql("SELECT lineName FROM ins36_busline")
    for lineNames in db.cursor.fetchall():
        lineName = lineNames[0]

        for key, val in dic.items():
            if lineName == key:
                sum_ = 0
                #  FINISHED    线路按站点顺序依次打印出各站点人数
                db.execute_sql(
                    "SELECT stopsNames, grade, endStopName, lineType, busNumber,startStopName FROM ins36_busline WHERE lineName ='{}'".format(
                        key))
                line_info = db.get_all()
                # print("lineinfo---------", line_info)
                if line_info:
                    stops_arr = line_info[0][0].split(",")
                    # grade = line_info[0][1]
                    endstop = line_info[0][2]
                    if int(line_info[0][3]) == 1:
                        lineType = "上班"
                        startTime = "07:20:00"
                    else:
                        lineType = "下班"
                        startTime = "17:05:00"

                    if line_info[0][4] is None:
                        busNumber = ""
                    else:
                        busNumber = line_info[0][4]

                    # busNumber = line_info[0][4]
                    startstop = line_info[0][5]

                    # startTime = ""   TimeTable[key[3:6]]
                    print("{}  {}{}".format(busNumber, lineType, startTime))
                    writefile(filename, fieldnames,
                              {fieldnames[0]: "{} {} {} {}->{}".format(busNumber, lineType, startTime, startstop,
                                                                       endstop), fieldnames[1]: "", fieldnames[2]: ""})
                    for stop in stops_arr:
                        if stop in val.keys():
                            if stop not in ("中电科技三十六所", "36所智慧园"):
                                print("{}\t{}".format(stop, val[stop]))
                                writefile(filename, fieldnames,
                                          {fieldnames[0]: stop, fieldnames[1]: "{}".format(val[stop]),
                                           fieldnames[2]: ",".join(names_dic[lineName][stop])})
                                sum_ += val[stop]
                        else:
                            if stop not in ("中电科技三十六所", "36所智慧园"):
                                print("{}\t{}".format(stop, 0))
                                writefile(filename, fieldnames,
                                          {fieldnames[0]: stop, fieldnames[1]: "{}".format(0), fieldnames[2]: ""})
                    print('线路总人数是\t%d\n' % sum_)
                    writefile(filename, fieldnames,
                              {fieldnames[0]: "线路总人数是", fieldnames[1]: sum_})
                    writefile(filename, fieldnames,
                              {fieldnames[0]: "", fieldnames[1]: "", fieldnames[2]: ""})
                    line_number_dict[busNumber] = sum_
                    total += sum_
                    break
    print(total)
    writefile(filename, fieldnames,
              {fieldnames[0]: "总人数", fieldnames[1]: total})
    json.dump(line_number_dict,
              open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "people_number.json"), "w"))
    convert_csv_xls(filename)


def count_type_in_grade():
    """
    每个年级购买的情况
    :return:
    """
    """
    orderNo
    orderId
    orderTime
    lineId
    lineName
    scheduledId
    scheduledName
    startTime
    startStopName
    endStopName
    boardingCode
    dropOffCode
    userId
    memberId
    memberName
    teleNum
    Account
    payAmount
    payType
    """
    result_dict = {
        "night": {"one": [], "two": [], "three": [], "seven": [], "eight": [], "nine": []},
        "day": {"one": [], "two": [], "three": [], "seven": [], "eight": [], "nine": []}
    }

    name_dict = {}

    df = pd.read_excel("账单的-order.xlsx")
    for index, row in df.iterrows():
        # 九年级
        if row["Account"][2:4] == '17':
            if row['lineName'][4:5] == 'N':
                result_dict['night']['nine'].append(row['memberId'])
            if row['lineName'][4:5] == 'F':
                result_dict['day']['nine'].append(row['memberId'])

        # 八年级
        elif row["Account"][2:4] == '18':
            if row['lineName'][4:5] == 'N':
                result_dict['night']['eight'].append(row['memberId'])
            if row['lineName'][4:5] == 'F':
                result_dict['day']['eight'].append(row['memberId'])

        # 七年级
        elif row["Account"][2:4] == '19':
            if row['lineName'][4:5] == 'N':
                result_dict['night']['seven'].append(row['memberId'])
            if row['lineName'][4:5] == 'F':
                result_dict['day']['seven'].append(row['memberId'])

        # 高三
        elif row["Account"][2:4] == '20':
            if row['lineName'][4:5] == 'N':
                result_dict['night']['three'].append(row['memberId'])
            if row['lineName'][4:5] == 'S':
                result_dict['day']['three'].append(row['memberId'])

        # 高二
        elif row["Account"][2:4] == '21':
            if row['lineName'][4:5] == 'N':
                result_dict['night']['two'].append(row['memberId'])
            if row['lineName'][4:5] == 'S':
                result_dict['day']['two'].append(row['memberId'])

        # 高一
        elif row["Account"][2:4] == '22':
            if row['lineName'][4:5] == 'N':
                result_dict['night']['one'].append(row['memberId'])
            if row['lineName'][4:5] == 'S':
                result_dict['day']['one'].append(row['memberId'])
        else:
            pass

        if row['memberName'] in name_dict.keys():
            name_dict[row['memberName']] += 1
        else:
            name_dict[row['memberName']] = 1

    two = 0
    one = 0
    err = 0
    for val in name_dict.values():
        if val == 2:
            two += 1
        elif val == 1:
            one += 1
        else:
            err += 1

    print("1次:{}，2次:{}，其他:{}".format(one, two, err))

    for key, val in result_dict.items():
        for k, v in val.items():
            if v:
                set_ = set(v)
                print(len(set_), len(v))
                # assert len(set_) == len(v), "有人买重复线路"
            # print v
    buy_both_seven = len(set(result_dict['day']['seven']).intersection(set(result_dict['night']['seven'])))
    buy_both_eight = len(set(result_dict['day']['eight']).intersection(set(result_dict['night']['eight'])))
    buy_both_nine = len(set(result_dict['day']['nine']).intersection(set(result_dict['night']['nine'])))

    buy_both_one = len(set(result_dict['day']['one']).intersection(set(result_dict['night']['one'])))
    buy_both_two = len(set(result_dict['day']['two']).intersection(set(result_dict['night']['two'])))
    buy_both_three = len(set(result_dict['day']['three']).intersection(set(result_dict['night']['three'])))

    print("七年级：晚自习{}, 周末{}, 两者均购买的有{}".format(len(result_dict['night']['seven']), len(result_dict['day']['seven']),
                                              buy_both_seven))
    print("八年级：晚自习{}, 周末{}, 两者均购买的有{}".format(len(result_dict['night']['eight']), len(result_dict['day']['eight']),
                                              buy_both_eight))
    print("九年级：晚自习{}, 周末{}, 两者均购买的有{}".format(len(result_dict['night']['nine']), len(result_dict['day']['nine']),
                                              buy_both_nine))
    print("高一：晚自习{}, 周末{},两者均购买的有{}".format(len(result_dict['night']['one']), len(result_dict['day']['one']),
                                            buy_both_one))
    print("高二：晚自习{}, 周末{},两者均购买的有{}".format(len(result_dict['night']['two']), len(result_dict['day']['two']),
                                            buy_both_two))
    print("高三：晚自习{}, 周末{},两者均购买的有{}".format(len(result_dict['night']['three']), len(result_dict['day']['three']),
                                            buy_both_three))
    sum = 0
    for key, val in result_dict.items():
        for k, v in val.items():
            sum += len(v)
    print("一共{}人".format(sum))


def generate_files_for_school():
    """
    根据数据库和order.xlsx文件。   为学校生成文件。各年级班级乘坐情况统计表
    :return:
    """
    db = DB("busline")
    db.execute_sql("SELECT lineName,busNumber, lineTypeDesc FROM yzbusline")
    bus_info = dict()
    for each in db.get_all():
        # print(each[0], each[1], each[2])
        if each[0] not in bus_info.keys():
            bus_info[each[0]] = []
            bus_info[each[0]].append(each[1])
            bus_info[each[0]].append(each[2])

    # 统一放在download文件夹
    basedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download')
    # 目标文件夹
    target_dir = os.path.join(basedir, '各年级乘车情况')

    df = pd.read_excel(os.path.join(basedir, "账单的-order.xlsx"))

    grade_classes_dict = {"17": {}, "18": {}, "19": {}, "20": {}, "21": {}, "22": {}}
    for index, row in df.iterrows():
        # print(index)
        if row['Account'] == "0A171202":
            row['Account'] = "0A181202"
        new_row = pd.DataFrame({"学号": row['Account'],
                                "姓名": row['memberName'],
                                "车号": bus_info[row['lineName']][0],
                                "时间段": bus_info[row['lineName']][1],
                                "发车时间": row['startTime'],
                                "下车点": row['dropOffCode']
                                }, columns=["学号", "姓名", "时间段", "车号", "发车时间", "下车点"], index=[index])

        grade = row['Account'][2:4]
        if grade in ("17", "18", "19"):
            class_name = row['Account'][4:6]
            class_id = row['Account'][6:]
            if class_name in grade_classes_dict[grade].keys():
                if class_id in grade_classes_dict[grade][class_name].keys():
                    grade_classes_dict[grade][class_name][class_id].append(new_row)
                else:
                    grade_classes_dict[grade][class_name][class_id] = []
                    grade_classes_dict[grade][class_name][class_id].append(new_row)
            else:
                grade_classes_dict[grade][class_name] = {}
                grade_classes_dict[grade][class_name][class_id] = []
                grade_classes_dict[grade][class_name][class_id].append(new_row)

        else:
            class_name = row['Account'][4:5]
            class_id = row['Account'][5:]
            if class_name in grade_classes_dict[grade].keys():
                if class_id in grade_classes_dict[grade][class_name].keys():
                    grade_classes_dict[grade][class_name][class_id].append(new_row)
                else:
                    grade_classes_dict[grade][class_name][class_id] = []
                    grade_classes_dict[grade][class_name][class_id].append(new_row)
            else:
                grade_classes_dict[grade][class_name] = {}
                grade_classes_dict[grade][class_name][class_id] = []
                grade_classes_dict[grade][class_name][class_id].append(new_row)

    for grade, classes in sorted(grade_classes_dict.items(), key=lambda x: x[0]):  # 年级
        # 年级判断
        if grade == "19":
            dirname = "初一"
        elif grade == "18":
            dirname = "初二"
        elif grade == "17":
            dirname = "初三"
        elif grade == "22":
            dirname = "高一"
        elif grade == "21":
            dirname = "高二"
        else:
            dirname = "高三"
        # 若不存在年级文件夹则新建
        # if not os.path.exists(os.path.join(target_dir, dirname)):
        #     os.mkdir(os.path.join(target_dir, dirname))
        # base_dir = os.path.join(target_dir, dirname)
        for class_name, class_accounts in sorted(classes.items(), key=lambda x: x[0]):  # 班级
            class_arr = []
            for account, orders in sorted(class_accounts.items(), key=lambda x: x[0]):  # 学号
                for order in orders:  # 一个学号可能下多个单
                    class_arr.append(order)
            # print(class_arr)
            dfs = pd.concat(class_arr, ignore_index=True, axis=0)
            dfs.index = range(1, len(dfs) + 1)
            pd.DataFrame(dfs).to_excel(os.path.join(target_dir, dirname + class_name + "班.xlsx"))


def generate_files_for_bus_company():
    db = DB("busline")
    db.execute_sql("SELECT lineName, busNumber,lineTypeDesc, stopsNames FROM ins36_busline WHERE busNumber is not null")
    bus_info = dict()

    for each in db.get_all():
        if each[0] not in bus_info.keys():
            bus_info[each[0]] = {}
            bus_info[each[0]]["num"] = each[1]
            bus_info[each[0]]["period"] = each[2]
            bus_info[each[0]]["stops"] = [i for i in each[3].split(',') if i != "嘉兴一中实验学校"]
    dirname = "各辆车乘坐明细"
    if not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), dirname)):
        os.mkdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), dirname))
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'download', dirname)
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    df = pd.read_excel(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "账单的-order.xlsx"))

    for lineName in bus_info.keys():
        passagers_arr = []
        for index, row in df.iterrows():
            if lineName == row['lineName']:

                if 'go' in lineName:
                    order_station_ = row['boardingCode']
                else:
                    order_station_ = row['dropOffCode']

                new_row = pd.DataFrame({"学号": row['Account'],
                                        "姓名": row['memberName'],
                                        "车号": bus_info[row['lineName']]["num"],
                                        "时间段": bus_info[row['lineName']]["period"],
                                        "发车时间": row['startTime'],
                                        "下车点": order_station_,
                                        "电话": row['teleNum'],
                                        "备注": ""
                                        }, columns=["学号", "姓名", "时间段", "车号", "发车时间", "下车点", "电话", "备注"],
                                       index=[index])
                passagers_arr.append(new_row)

        sorted_passagers_arr = []
        # for passager in passagers_arr:
        #     for index, row in passager.iterrows():
        #         print(row["下车点"])
        for stop in bus_info[lineName]["stops"]:
            for passager in passagers_arr:
                for index, row in passager.iterrows():
                    if stop == row["下车点"]:
                        sorted_passagers_arr.append(passager)

        print(sorted_passagers_arr)
        dfs = pd.concat(sorted_passagers_arr, ignore_index=True, axis=0)
        # print(dfs)
        dfs.index = range(1, len(dfs) + 1)
        if bus_info[lineName]["num"] is not None:
            pd.DataFrame(dfs).to_excel(os.path.join(base_dir, bus_info[lineName]["num"] + lineName + ".xlsx"))


if __name__ == '__main__':
    # count_type_in_grade()
    # generate_files_for_school()
    generate_files_for_bus_company()

    # count_buyer_in_grade()
    # count_buyer_in_type()
    # count_each_route_number()

    # count_each_schedule_number("各站点购票情况", ["站点", "人数", "名单"])

    # count_each_schedule_number1()
