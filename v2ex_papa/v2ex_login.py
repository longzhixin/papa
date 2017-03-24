#coding  utf-8
#v2ex_login.py
# by ouyang , learned from fuck_login

"""
Requred
---requests
---lxml
"""

import requests
from io import StringIO
from lxml import etree

class v2ex_login(object):

    def __init__(self):
        self.user_name = 'xxxppp'
        self.user_password = 'long15254815094'
        self.login_url = 'https://www.v2ex.com/signin'
        session = requests.session()

        session.headers ={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

        self.session = session
    def get_login_parameters(self):
        self.response = self.session.get(self.login_url)

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(self.response.text), parser)

        ##other method acquire the xpath
        #elements = tree.xpath('//form[@method="post" and @action="/signin"]/table[@cellpadding="5" and @cellspacing="0" and @border="0" and @width="100%"]//tr[position()<last()]/td[2]/input')

        elements = tree.xpath('//*[@id="Main"]/div[2]/div[2]/form//tr[position()<last()]/td[2]/input')
        user_name_key = elements[0].xpath('@name')[0]
        user_password_key = elements[1].xpath('@name')[0]
        user_once = elements[2].xpath('@value')
        # print (user_once)
        # print (len(elements))
        return user_name_key, user_password_key, user_once

    def login(self, user_name_key, user_password_key, user_once):
        ## update session;
        self.session.headers.update({'referer':self.login_url})
        form_data = {user_name_key : self.user_name,
                     user_password_key: self.user_password,
                     'once': user_once ,
                      'next': '/'
                     }
        response = self.session.post(self.login_url, form_data)
        flag = False
        if '条未读提醒' in  response.text:
            flag = True
        print (flag)
    def test_login(self):
        user_name_key, user_password_key, user_once = self.get_login_parameters()
        self.login(user_name_key, user_password_key, user_once)
    # def papa_buy(self,page_url):
    #     self.test_login()
    #     buy = self.session.get(page_url)
    #     p
    #     parser = etree.HTMLParser()
    #     buy_tree = etree.parse(StringIO(buy.text), parser)
    #    # print (buy_tree.text)
# if __name__ == '__main__':
#      v2ex = v2ex_login()
#      v2ex.papa_buy('https://www.v2ex.com/go/all4all?p=1')