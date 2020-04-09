# coding:utf-8

import requests
import time

"""
用于下载模块
"""

POST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
}

GET_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
}

COOKIES = {
    "JSESSIONID": None
}


# def get_cookies():
#     """识别验证码得到cookie"""
#     # global COOKIES
#     # with open("cookie.txt") as f:
#     #     COOKIES = f.read()
#     # print(COOKIES)


def is_login():
    pass


def send_get(url):
    """
    :param url: 要请求的URL
    :return:    返回unicode结果
    """
    try:
        response = requests.get(url=url, headers=GET_HEADERS, cookies=COOKIES)
        if response.status_code == 200:
            return response.text
        else:
            raise response.status_code
    except Exception as e:
        print("download error {}".format(e))


def send_post(url, data):
    """

    :param url:     要请求的url
    :param data:    要传输的数据
    :return:        返回unicode结果
    """
    try:
        response = requests.post(url=url, headers=POST_HEADERS, cookies=COOKIES, data=data)
        if response.status_code == 200:
            # print(response.text)
            time.sleep(0.5)
            return response.text
        else:
            raise response.status_code
    except Exception as e:
        print("download error {}".format(e))


if __name__ == '__main__':
    pass
    #   print(send_get("http://www.jkxabus.com/mgt/login"))
    #   get_cookies()

