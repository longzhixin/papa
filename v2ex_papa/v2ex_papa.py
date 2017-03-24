import time
import requests
import random
from lxml import etree
from v2ex_login import v2ex_login

from io import StringIO

class V2ex(v2ex_login):
    def __init__(self):
        v2ex_login.__init__(self)

    def spider_buy_main(self):

        self.content = "生成时间: "+ ' '+ time.asctime()+'\t'
        for page in range(1, 20):
            self.content += '   page= ' +str(page)+ '      生成时间: '+time.asctime()+"-----------我是分隔符"
            page_url = "https://www.v2ex.com/go/all4all?p=" + str(page)
            self.content += self.spider(page_url)
        with open('v2ex_buy.txt', 'w', encoding='utf-8') as f:
            f.write(self.content)

    def spider(self, page_url):
        """
        :param page_url:
        :return:
        """
        result = ''
        divide = '\n' + '--' * 30 + '\n' + '--' * 30 + '\n'
        result += divide + '\t' * 4 + '开始抓取www.v2ex.com' + '：' + divide
        response = self.session.get(page_url)
        parser = etree.HTMLParser(encoding='utf-8')
        buy_tree = etree.parse(StringIO(response.text), parser=parser)

        # parser = etree.HTMLParser(encoding='utf-8')
        # buy_tree = etree.parse('juat.html', parser=parser)

        elements  = buy_tree.xpath("//*[@id='TopicsNode']/div[position()<21]/table/tr/td[3]")

        for element in elements:
            thing = element.xpath("span[1]/a")[0]
            thing_title = thing.text
            thing_link = 'https://www.v2ex.com'+ thing.xpath('@href')[0]
            thing_date = element.xpath("span[2]/strong[1]/a")[0]
            last_response = element.xpath("span[2]/strong[1]")[0].tail
            author = element.xpath("span[2]/strong[2]/a")
            if len(author):
                last_author = author[0].text
            else:
                last_author = 'NO ONE'
            result += thing_title + '\t\t'+ thing_date.text +'\t'+ last_response+ '\t'+last_author+'\t'+thing_link+ divide
        return   (result)

v2ex = V2ex()
# 登陆
v2ex.test_login()
# 爬取
#v2ex.spider('https://www.v2ex.com/go/all4all')
# 处理
v2ex.spider_buy_main()
