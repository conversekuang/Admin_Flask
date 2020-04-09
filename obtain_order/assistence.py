# -*- coding: utf-8 -*-
# @Author: dell
# @Date:   2019-05-27 13:04:26
# @Last Modified by:   dell
# @Last Modified time: 2019-08-30 18:19:10

import pandas as pd
import time
import requests
import json
import os
import csv
import common.download


def calculate_register_number(passager_type, filename="download_user_excel.xlsx"):
    df = pd.read_excel(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', filename), headers=True)
    total_user = 0
    register_count = 0

    for index, row in df.iterrows():
        row.fillna(0, inplace=True)
        if row[u'手机号'] != 0 and row[u'登录名'] != 0 and (
                passager_type.lower() in row[u'登录名'] or passager_type.upper() in row[u'登录名']):
            register_count += 1

        if row[u'登录名'] != 0 and (
                passager_type.lower() in row[u'登录名'] or passager_type.upper() in row[u'登录名']):
            total_user += 1

    print("总内置账号数量为:%d" % total_user)
    print("截止至", time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))
    print("现在内置账号绑定手机用户数量, %d" % register_count)

    # print("7年级人数:%d" % seven)
    # print("8年级人数:%d" % eight)
    # print("9年级人数:%d" % nine)
    # print("高一年级人数:%d" % one)
    # print("高二级人数:%d" % two)
    # print("高三级人数:%d" % three)


headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01'
}


def download_user_xlsx():
    data = {'type': 0, "userName": ""}
    fileName = ""
    url = "http://www.jkxabus.com/mgt/system/sysuser/export"
    response = requests.post(url, data=data, headers=headers, cookies=common.download.COOKIES)

    if response.status_code == 200:
        dic = json.loads(response.text)
        fileName = dic['msg']  # 返回filename

    downloadurl = "http://www.jkxabus.com/mgt/common/download?fileName=" + fileName + "&delete=true"
    headers['Content-Type'] = None
    response = requests.get(downloadurl, headers=headers, cookies=common.download.COOKIES, stream=True)

    if response.status_code == 200:
        filename = "download_user_excel.xlsx"
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
    time.sleep(0.1)


def calculate_register_number_now(passager_type):
    """
    计算当前绑定手机的用户数量
    """
    download_user_xlsx()
    calculate_register_number(passager_type)


def get_register_result_dict(passager_type):
    """
    注册信息的的字典集合
    """
    dic = {}
    filename = "download_user_excel.xlsx"
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', filename)

    while True:
        if os.path.exists(filepath):
            print("已生成用户信息表")
            break
        else:
            time.sleep(0.3)

    df = pd.read_excel(filepath)
    # print df

    for index, row in df.iterrows():
        row.fillna(0, inplace=True)
        if row[u'手机号'] != 0 and row[u'登录名'] != 0 and (
                passager_type.lower() in row[u'登录名'] or passager_type.upper() in row[u'登录名']):
            userid = int(row[u'用户ID'])
            dic[userid] = [str(row[u'手机号']), str(row[u'登录名'])]

    # TODO 如果需要添加测试账号人员在此处添加userid，telenumber，account
    # dic[1325] = ["13586451921", "00002"]
    # dic[1324] = ["13967384976", "00001"]
    # dic[1334] = ["18357352770", "00011"]

    return dic


def get_stations_result_dict():
    dic = {}
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', 'upload.xlsx')
    df = pd.read_excel(filepath, header=None)
    # print df
    for index, row in df.iterrows():
        code = row[0]
        if '\ufeff' in code:
            code = code.replace("\ufeff", '').strip()
        dic[code] = row[1]
    return dic


def writefile(filename, fieldnames, row):
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', filename + '.csv')
    if not os.path.exists(filepath):
        with open(filepath, "w+", encoding='utf_8_sig', newline="") as f:
            # 文件头以列表的形式传入函数，列表的每个元素表示每一列的标识
            # f.write(codecs.BOM_UTF8)
            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerow(row)
    else:
        with open(filepath, "a+", encoding='utf_8_sig', newline="") as f:
            # 文件头以列表的形式传入函数，列表的每个元素表示每一列的标识
            # f.write(codecs.BOM_UTF8)
            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
            # dict_writer.writeheader()
            dict_writer.writerow(row)


def convert_csv_xls(filename):
    df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', filename + '.csv'),
                     encoding="utf_8_sig")
    df.to_excel(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', filename + ".xlsx"), index=False)
    os.remove(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', filename + '.csv'))


def download_order(pagesize, pagenum):
    url = "http://www.jkxabus.com/mgt/order/orderMaster/list"
    dic = {"pageSize": pagesize, "pageNum": pagenum, "isAsc": "asc", "orderByColumn": ""}
    response = requests.post(url, headers=headers, cookies=common.download.COOKIES, data=dic)
    if response.status_code == 200:
        dic = json.loads(response.text)
        print("第 %d 页, 每页 %d 单" % (pagenum, pagesize))
        return dic
    else:
        print("download_error")
        exit()


totoal_already_paid_num = 0


def generate_order_xlsx(passager_type, minDate, maxDate):
    """
    通过请求后台数据，生成xlsx文件，主要是对订单信息进行整理。
    """
    global totoal_already_paid_num

    # 如果有存在的文件，直接删除之前的。
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "order.csv")):
        os.remove(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "order.csv"))
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "refund_order.csv")):
        os.remove(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "refund_order.csv"))
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "order.xlsx")):
        os.remove(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "order.xlsx"))
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "refund_order.xlsx")):
        os.remove(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "refund_order.xlsx"))

    pagesize = 200
    pagenum = 1
    result_dic = download_order(pagesize, pagenum)

    total_order = result_dic['total']
    print("订单总人数: %d" % (int(result_dic['total'])))  # 内测订单

    clean_order_data(result_dic, passager_type, minDate, maxDate)

    while True:
        if total_order - pagesize * pagenum > 0:
            pagenum += 1
            result_dic = download_order(pagesize, pagenum)
            clean_order_data(result_dic, passager_type, minDate, maxDate)
        else:
            break
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "order.csv")):
        convert_csv_xls("order")
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', "refund_order.csv")):
        convert_csv_xls("refund_order")

    print("已付款%d人" % (totoal_already_paid_num))


def clean_order_data(result_dic, passager_type, minDate, maxDate):
    # exclude_orderNo = ['20200220000027', '20200220000042', '20200221000063', '20200220000011', '20200222000008']
    global totoal_already_paid_num
    refund_number = 0

    all_stations_dic = get_stations_result_dict()  # 得到所有站点的集合
    all_register_dic = get_register_result_dict(passager_type)
    # 原信息
    # fieldnames = ['orderId', 'orderTime', 'lineName', 'startStopName', 'userId', 'boardingCode','endStopName', 'scheduledId', 'orderNo', 'memberName', 'dropOffCode', 'payAmount', 'takeBusDates', 'searchValue', 'scheduledName', 'payType', 'startTime', 'lineId', 'createTime', 'remark', 'memberId']
    # 不带用户信息
    # fieldnames = ['orderNo','orderId', 'orderTime', 'lineId','lineName','startStopName','endStopName','boardingCode','dropOffCode', 'userId', 'memberId', 'memberName' ,'payAmount', 'scheduledId','scheduledName','startTime', 'payType' ]
    # 带用户信息
    fieldnames = ['orderNo', 'orderId', 'orderTime', 'lineId', 'lineName', 'scheduledId', 'scheduledName', 'startTime',
                  'startStopName', 'endStopName', 'boardingCode', 'dropOffCode', 'userId', 'memberId', 'memberName',
                  'teleNum', 'Account', 'payAmount', 'payType']

    fieldnames_refund = ['orderNo', 'orderId', 'orderTime', 'lineId', 'lineName', 'scheduledId', 'scheduledName',
                         'startTime', 'startStopName', 'endStopName', 'boardingCode', 'dropOffCode', 'userId',
                         'memberId', 'memberName', 'teleNum', 'Account', 'payAmount', 'payType', 'refundAmount',
                         'remark']

    own_dic = {}

    for item in result_dic['rows']:
        if item['userId'] in all_register_dic.keys():
            own_dic['orderNo'] = item['orderNo']
            own_dic['orderId'] = item['orderId']
            own_dic['orderTime'] = item['orderTime']

            own_dic['lineId'] = item['lineId']
            own_dic['lineName'] = item['lineName']
            if (item['startStopName'] != None):
                own_dic['startStopName'] = item['startStopName']
            if (item['endStopName'] != None):
                own_dic['endStopName'] = item['endStopName']

            # own_dic['boardingCode'] = all_stations_dic[item['boardingCode']].encode('utf-8')  # 转换上车点

            if '\ufeff' in item['boardingCode']:
                code = item['boardingCode'].replace("\ufeff", '').strip()
                own_dic['boardingCode'] = all_stations_dic[code]  # 转换上车点
            else:
                own_dic['boardingCode'] = all_stations_dic[str(item['boardingCode'])]  # 转换上车点

            if '\ufeff' in item['dropOffCode']:
                code = item['dropOffCode'].replace("\ufeff", '').strip()
                own_dic['dropOffCode'] = all_stations_dic[code]  # 转换上车点
            else:
                own_dic['dropOffCode'] = all_stations_dic[str(item['dropOffCode'])]  # 转换下车点

            own_dic['userId'] = item['userId']
            own_dic['memberId'] = item['memberId']
            own_dic['memberName'] = item['memberName']

            own_dic['teleNum'] = all_register_dic[item['userId']][0]
            own_dic['Account'] = all_register_dic[item['userId']][1]

            own_dic['payAmount'] = item['payAmount'] / 100

            own_dic['scheduledId'] = item['scheduledId']
            own_dic['scheduledName'] = item['scheduledName']
            own_dic['startTime'] = item['startTime']
            if item['payType'] == 1:
                own_dic['payType'] = "微信"
            elif item['payType'] == 2:
                own_dic['payType'] = "支付宝"
            else:
                own_dic['payType'] = "测试"
            # if item['orderStatus'] == 1 and (item['orderNo'][4:6] in ('07') or (
            #         item['orderNo'][4:6] in ('08') and int(
            #     item['orderNo'][6:8]) <= 26)):
            #     totoal_already_paid_num += 1
            #     writefile("first_order", fieldnames, own_dic)
            #     writefile("order", fieldnames, own_dic)

            if item['orderStatus'] == 1 and (len(item['refundList']) == 0) and int(
                    item['orderNo'][:8]) >= minDate and int(item['orderNo'][:8]) <= maxDate:
                totoal_already_paid_num += 1
                # writefile("second_order", fieldnames, own_dic)
                own_dic['refundAmount'] = 0
                own_dic['remark'] = ""
                writefile("order", fieldnames_refund, own_dic)

            # TODO 退款的人
            if item['orderStatus'] == 1 and (len(item['refundList']) != 0) and int(
                    item['orderNo'][:8]) >= minDate and int(item['orderNo'][:8]) <= maxDate:
                refund_number += 1
                own_dic['refundAmount'] = int(item['refundList'][0]['refundAmount']) / 100
                own_dic['remark'] = item['refundList'][0]['remark']
                try:
                    writefile("refund_order", fieldnames_refund, own_dic)
                except Exception as e:
                    print(item)


if __name__ == '__main__':
    passager_type = "0D"
    minDate = 20200228
    maxDate = 20200310
    calculate_register_number_now(passager_type)
    generate_order_xlsx(passager_type, minDate, maxDate)
    # convert_csv_xls("order")
    # convert_csv_xls("refund_order")
    # all_register_dic = get_register_result_dict()
    # for key in all_register_dic.keys():
    # 	print key, type(key)
    # 	print all_register_dic[key][0], type(all_register_dic[key][0])
    # 	print all_register_dic[key][1], type(all_register_dic[key][1])
