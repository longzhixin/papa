import time
import requests
import random
from lxml import etree
from lxml.html import clean
# encoding: utf-8

import sys

headers = [{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}]

def main():
    fileContent = '生成时间: ' + time.asctime()
    for page in range(1, 3):
        fileContent += '>>>page= '+ str(page)+ '<<<>>>>生成时间: '+time.asctime()+"<<<<<<<<我是分隔符"
        fileContent += tradedgtle(str(page))
    with open("tradedgtle.html", 'w', encoding='utf-8') as f:
        f.write(fileContent)

def tradedgtle(page):
    global headers
    result = ''
    divide = '\n' + '--' * 30 + '\n' + '--' * 30 + '\n'
    result += divide + '\t' * 4 + '开始抓取' + '：' + divide
    url = 'http://trade.dgtle.com/dgtle_module.php?mod=trade&ac=index&typeid=&PName=&searchsort=0&page='+page
    html = requests.get(url, headers=random.choice(headers)).content
    #清理掉可恶的css
    cleaner = clean.Cleaner(style=True, scripts=True, page_structure=False, safe_attrs_only=False)
    html = cleaner.clean_html(html)
    tree = etree.HTML(html.decode('utf-8'))

    products = tree.xpath("//*[@id='wp']/div[3]/div[position()>5 and position()<36]")

    for product in products:
        tradetitle = product.xpath("div[2]/p[1]/@title")
        tradeuser = product.xpath("div[2]/p[2]/text()")
        tradeprice = product.xpath("p[1]/text()")[0]
        tradeurl = product.xpath("div[1]/a/@href")
        tradedata = product.xpath("p[2]/span[1]/text()")[0]
        tradeurl = 'http://trade.dgtle.com/'+ tradeurl[0]


        result += tradedata+'\t'+ tradetitle[0]+ '\t'+tradeuser[0]+'\t'+tradeprice[1:]+'\t'+ tradeurl +divide

    return result

if __name__ == "__main__":
    main()


