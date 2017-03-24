#coding  utf-8
#v2ex_login.py
# by ouyang , learned from fuck_login

"""
Required
---requests
--- lxml
"""

import requests
from io import StringIO
from lxml import etree


class V2exLogin(object):
    """

    """

    def __init__(self):
        # 用户名
        self.user_name = 'xxxppp'
        # 密码
        self.user_password = 'long15254815094'
        self.login_url = 'https://www.v2ex.com/signin'

        # 用来保持与服务器通讯时候的相关参数
        session = requests.session()

        session.headers ={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

        self.session = session


    def get_login_parameters(self):
        """
        :return: the login parameters, {user_name_key, user_password_key, once}
        """
        # get the raw html
        response = self.session.get(self.login_url)
        parser = etree.HTMLParser()

        # 将我们html 转化成etree
        tree = etree.parse(StringIO(response.text), parser)

        ##other method acquire the xpath
        #elements = tree.xpath('//form[@method="post" and @action="/signin"]/table[@cellpadding="5" and @cellspacing="0" and @border="0" and @width="100%"]//tr[position()<last()]/td[2]/input')

        # xpath 寻找我们需要的元素
        elements = tree.xpath('//*[@id="Main"]/div[2]/div[2]/form//tr[position()<last()]/td[2]/input')

        # 获取表单：user_name_key user_password_key, once = value
        user_name_key = elements[0].xpath('@name')[0]
        user_password_key = elements[1].xpath('@name')[0]
        user_once = elements[2].xpath('@value')


        return user_name_key, user_password_key, user_once

    def login(self, user_name_key, user_password_key, user_once):
        """
        :param user_name_key:
        :param user_password_key:
        :param user_once:
        :return:
        this is used to 模拟登陆
        """

        # TODO I don't know how this works
        self.session.headers.update({'referer':self.login_url})

        # 用来提交的表单数据
        form_data = {user_name_key : self.user_name,
                     user_password_key: self.user_password,
                     'once': user_once ,
                      'next': '/'
                     }
        # 提交数据后，接收服务器返回的网页
        response = self.session.post(self.login_url, form_data)

        flag = False
        if '条未读提醒' in  response.text:
            flag = True
        print(flag)

    def test_login(self):
        """
        :return: if login suceessed ，it will print true, then we use session() to acquire
        what we want;
        """
        user_name_key, user_password_key, user_once = self.get_login_parameters()
        self.login(user_name_key, user_password_key, user_once)

# instance for tests
# if __name__ == '__main__':
#      v2ex = V2exLogin()
#      v2ex.papa_buy('https://www.v2ex.com/go/all4all?p=1')