import time
import requests
import random
from lxml import etree
from lxml.html import clean
# encoding: utf-8

headers = [{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}]


def main():
    """
    程序入口
    :return: 将爬到的数据以utf-8格式写入到tradedgtle.html，总共爬取1-3页
    """
    file_content = '生成时间: ' + time.asctime()
    for page in range(1, 3):
        file_content += '>>>page= ' + str(page) + '<<<>>>>生成时间: ' + time.asctime() + "<<<<<<<<我是分隔符"
        file_content += tradedgtle(str(page))
    with open("tradedgtle.html", 'w', encoding='utf-8') as f:
        f.write(file_content)


def tradedgtle(page):
    """
    :param page: 要爬取的页码
    :return: 返回result， 包含一个商品的item，price，date，author等
    """
    global headers
    result = ''
    divide = '\n' + '--' * 30 + '\n' + '--' * 30 + '\n'
    result += divide + '\t' * 4 + '开始抓取' + '：' + divide
    url = 'http://trade.dgtle.com/dgtle_module.php?mod=trade&ac=index&typeid=&PName=&searchsort=0&page='+page
    html = requests.get(url, headers=random.choice(headers)).content

    # 清理掉可恶的css
    cleaner = clean.Cleaner(style=True, scripts=True, page_structure=False, safe_attrs_only=False)
    html = cleaner.clean_html(html)
    # html convert to etree格式
    tree = etree.HTML(html.decode('utf-8'))

    # 使用xpath method 查找页面中30个商品
    products = tree.xpath("//*[@id='wp']/div[3]/div[position()>5 and position()<36]")

    # products is list， 遍历list， 对于每一个prodcut就是一个element. 每一个element块抽取数据
    for product in products:

        trade_title = product.xpath("div[2]/p[1]/@title")
        trade_user = product.xpath("div[2]/p[2]/text()")
        trade_price = product.xpath("p[1]/text()")[0]
        trade_url = product.xpath("div[1]/a/@href")
        trade_data = product.xpath("p[2]/span[1]/text()")[0]
        trade_url = 'http://trade.dgtle.com/'+ trade_url[0]
        result += trade_data+'\t' + trade_title[0] + '\t' + trade_user[0] + '\t' + trade_price[1:]+'\t' + trade_url + divide
    return result

if __name__ == "__main__":
    main()


