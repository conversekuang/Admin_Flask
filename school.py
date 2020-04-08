# coding:utf-8

"""
Author      : converse
filename    : school.py
created Date: 2020/4/8 16:26
software    : PyCharm
version     : 3.7.2
"""
from flask import Blueprint
from flask import render_template
from obtain_order.order_analyze import count_each_schedule_number


school = Blueprint("school", __name__)


@school.route('/station_calculation_for_school')
def station_calculation():
    count_each_schedule_number("各站点购票情况", ["站点", "人数", "名单"])
    return "station_calculation_for_school"
    # TODO 站点人数计算
