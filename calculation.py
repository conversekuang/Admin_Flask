# coding:utf-8

"""
Author      : converse
filename    : calculation.py
created Date: 2020/3/19 15:08
software    : PyCharm
version     : 3.7.2
"""
from flask import Blueprint
from flask import render_template

calculation = Blueprint("calculation", __name__)


@calculation.route('/paid_order')
def paid_order():
    return "paid_order"
    # TODO 导出已付款订单


@calculation.route('/refund_order')
def refund_order():
    return "refund_order"
    # TODO 导出退款订单


@calculation.route('/station_calculation')
def station_calculation():
    return "station_calculation"
    # TODO 站点人数计算

