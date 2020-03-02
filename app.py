from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():
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


@app.route('/logout', methods=['GET'])
def logout():
    pass


if __name__ == '__main__':
    app.run()
