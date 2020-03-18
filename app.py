from flask import Flask, render_template, request, url_for, redirect, jsonify, make_response
import json

app = Flask(__name__)


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


@app.route('/date_check', methods=['POST'])
def date_check():
    """
    bootstrap的时间选择器
    https://www.bootcss.com/p/bootstrap-datetimepicker/
    :return:
    """
    data = json.loads(request.get_data())
    print(data)

    # TODO 提取数据出来
    passager_type = data['passager_type']

    # 传入乘客类型 string 类型
    passager_type = "{} {}".format(passager_type.upper(), passager_type.lower())
    print(passager_type)  # 大小写均可

    # 传入日期 int 类型
    start_date = int(data['start'].replace("-", ""))
    end_date = int(data['end'].replace('-', ""))
    print(start_date, end_date)

    # TODO 返回导出文件
    response = make_response(jsonify({'code': 200, 'message': ''}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    # 保证了跨域不出错

    return response


@app.route('/calendar', methods=['GET'])
def calendar():
    return render_template("calendar.html")

    # return data['test']
    # password = request.args['password']
    # print(username, password)
    # return 201
    # return render_template("index.html")


if __name__ == '__main__':
    app.run()
