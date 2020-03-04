from flask import Flask, render_template, request, url_for, redirect

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


if __name__ == '__main__':
    app.run()
