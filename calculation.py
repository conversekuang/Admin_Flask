# coding:utf-8

"""
Author      : converse
filename    : calculation.py
created Date: 2020/3/19 15:08
software    : PyCharm
version     : 3.7.2
"""
from flask import Blueprint, make_response, send_from_directory
from flask import render_template
import os

calculation = Blueprint("calculation", __name__)

directory = os.path.dirname(__file__)


@calculation.route('/paid_order')
def paid_order():
    # TODO 导出已付款订单,如果存在返回文件，不存在则提示。
    filename = 'order.xlsx'
    file_path = os.path.join(directory, 'download', filename)
    print(file_path)
    if os.path.exists(file_path):
        response = make_response(send_from_directory(os.path.join(directory, 'download'), filename, as_attachment=True))
        return response
    else:
        return "未生成订单文件"


@calculation.route('/refund_order')
def refund_order():
    # TODO 导出已付款订单,如果存在返回文件，不存在则提示。
    filename = 'refund_order.xlsx'
    file_path = os.path.join(directory, 'download', filename)
    print(file_path)
    if os.path.exists(file_path):
        response = make_response(send_from_directory(os.path.join(directory, 'download'), filename, as_attachment=True))
        return response
    else:
        return "未生成退款文件"
