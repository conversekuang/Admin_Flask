# coding:utf-8

"""
Author      : converse
filename    : imitate_login.py
created Date: 2019/10/30 16:22
software    : PyCharm
version     : 3.7.2
"""

import requests
import json
from common.download import POST_HEADERS, GET_HEADERS
import common.download
import os
import time


def obtain_cookie():
    response = requests.get("http://www.jkxabus.com/mgt/login", headers=GET_HEADERS)
    cookie = response.headers['Set-Cookie'].split(";")[0].split("=")[1]
    common.download.COOKIES["JSESSIONID"] = cookie
    # print("第一次获取的", cookie)


def obtain_image():
    img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'validateCode.jpeg')
    url = "http://www.jkxabus.com/mgt/captcha/captchaImage?type=math"
    response = requests.get(url, cookies=common.download.COOKIES)
    if response.status_code == 200:
        with open(img_path, 'wb') as f:
            f.write(response.content)
    time.sleep(0.3)
    # print("获取图片的", COOKIES)


def validate_cookie(code):
    data = {"username": "admin001",
            "password": "123456",
            "validateCode": str(code),
            "rememberMe": "false"
            }
    # print("验证码", COOKIES)
    response = requests.post("http://www.jkxabus.com/mgt/login", data=data, headers=POST_HEADERS,
                             cookies=common.download.COOKIES)
    res_dict = json.loads(response.text)
    if res_dict['code'] == 0:
        print(res_dict['msg'])
        return True
    else:
        print(res_dict['msg'])
        return False


def check_login():
    url = "http://www.jkxabus.com/mgt/index"
    response = requests.get(url, cookies=common.download.COOKIES)
    # 请求的url 和 返回的url并不符合，因为location：跳转了
    print(url)
    print(response.request.url)
    print("check_login", common.download.COOKIES)
    if response.request.url == url:
        return True
    else:
        return False


if __name__ == '__main__':
    # obtain_cookie()
    obtain_image()
