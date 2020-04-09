from obtain_order.assistence import generate_order_xlsx, calculate_register_number_now

from common.imitate_login import validate_cookie, obtain_image, obtain_cookie, check_login

from flask import Flask, render_template, request, url_for, redirect, jsonify, make_response, session

import json
from datetime import timedelta
import common
from calculation import *
from school import *
from commute import *

app = Flask(__name__)
app.register_blueprint(calculation)
app.register_blueprint(school)
app.register_blueprint(commute)

app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config['SECRET_KEY'] = "12587asiwbqwp"


@app.before_request
def before_request():
    if request.path == '/login':
        # print("登录login")
        return None
    if request.path.startswith("/static"):
        # print("静态资源不拦截")
        return None
    if not request.cookies.get("jid"):
        return redirect('/login')

    # 恢复session
    if request.cookies.get("jid"):
        common.download.COOKIES['JSESSIONID'] = request.cookies.get("jid")
    print("有session")
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 将验证码内容融合，正确的get_cookies,
    if request.method == 'POST':
        code = request.form.get('validateCode')
        # print("后台收到的验证码：{}".format(code))
        # print("发送验证码的", COOKIES)
        if validate_cookie(code):
            # success
            temp = render_template('index.html')
            res = make_response(temp)
            res.set_cookie('jid', common.download.COOKIES["JSESSIONID"], max_age=600)
            return res
        else:
            # fail
            return redirect(url_for('login'))
    else:
        obtain_cookie()
        obtain_image()
        return render_template('login.html')


@app.route('/schoolBus')
def school_bus():
    return render_template("school_bus.html")


@app.route('/commuteBus')
def commute_bus():
    return render_template("commute_bus.html")


@app.route('/update_info', methods=['GET', 'POST'])
def update_info():
    if request.method == 'GET':
        return render_template("update_info.html")
    else:
        return "ok"


@app.route('/logout', methods=['GET'])
def logout():
    temp = render_template("login.html")
    res = make_response(temp)
    res.delete_cookie('jid')
    return res


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

    # TODO 执行导出excel订单文件, 退单文件
    calculate_register_number_now(passager_type)
    generate_order_xlsx(passager_type, start_date, end_date)

    # count_each_schedule_number("各站点购票情况", ["站点", "人数", "名单"])
    response = make_response(jsonify({'code': 200, 'message': ''}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    # 保证了跨域不出错

    return response


@app.route('/statistics', methods=['GET'])
def statistics():
    return render_template("export_page.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
