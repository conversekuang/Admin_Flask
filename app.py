from obtain_order.assistence import generate_order_xlsx, calculate_register_number_now
from obtain_order.order_analyze import count_each_schedule_number

from flask import Flask, render_template, request, url_for, redirect, jsonify, make_response

import json
from datetime import timedelta

from calculation import *

app = Flask(__name__)
app.register_blueprint(calculation)

app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        # return redirect(url_for("hello_world")) 跳转

        username = request.form['username']
        password = request.form['password']
        # TODO 验证账户、密码 逻辑
        return username + "," + password
        # return render_template("index.html")


@app.route('/schoolBus')
def school_bus():
    return render_template("school_bus.html")


@app.route('/commuteBus')
def commute_bus():
    return render_template("commute_bus.html")


@app.route('/update_info', methods=['GET'])
def update_info():
    return render_template("update_info.html")


@app.route('/logout', methods=['GET'])
def logout():
    return render_template("school_bus.html")


@app.route('/calendar', methods=['GET'])
def calendar():
    """
    bootstrap的时间选择器
    https://www.bootcss.com/p/bootstrap-datetimepicker/
    :return:
    """
    return render_template("calendar.html")


@app.route('/obtain_order', methods=['POST'])
def obtain_order():
    data = json.loads(request.get_data())
    print(data)

    # 提取数据类型
    passager_type = data['passager_type']
    # 传入日期 int 类型
    start_date = int(data['start'].replace("-", ""))
    end_date = int(data['end'].replace('-', ""))

    # TODO 执行导出excel订单文件
    calculate_register_number_now(passager_type)
    generate_order_xlsx(passager_type, start_date, end_date)

    count_each_schedule_number("各站点购票情况", ["站点", "人数", "名单"])
    response = make_response(jsonify({'code': 200, 'message': ''}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    # 保证了跨域不出错

    return response


@app.route('/statistics', methods=['GET'])
def station_number_calculation():
    return render_template("export_page.html")


if __name__ == '__main__':
    app.run(debug=True)
