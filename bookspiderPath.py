import time
import requests
import random
from lxml import etree
# encoding: utf-8
import sys

headers = [{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}]


def main():
    tags = ['哲学', '计算机', '心理学', '生活', '数学']
    fileContent = ''  # 最终要写到文件里的内容
    fileContent = '生成时间: ' + time.asctime()

    for tag in tags:
        fileContent += bookSpider(tag)
        print("%s down!" % tag)

    with open('book_list.txt', 'w') as f:
        f.write(fileContent)


def bookSpider(booktag):
    result = ''
    divide = '\n' + '--' * 30 + '\n' + '--' * 30 + '\n'
    result += divide + '\t' * 4 + booktag + '：' + divide

    url = "https://www.douban.com/tag/%s/book" % booktag
    global headers
    html = requests.get(url, headers=random.choice(headers)).content

    with open('book.html', 'w') as f:
        f.write(str(html))
    print (html)
    tree = etree.HTML(html.decode('utf-8'))
    print (tree)
    books = tree.xpath("//dl/dd")
    print (type(books))
    print (type(books[0].xpath("a/text()")))
    # print (tree.tag)

        # title = book.xpath("a/text()")[0].strip()
        # # 得到出版信息
        # desc = book.xpath("div[@class='desc']/text()")[0].strip()
        # descL = desc.split('/')
        # authorInfo = '作者/译者： ' + '/'.join(descL[:-3])
        # pubInfo = '出版信息： ' + '/'.join(descL[-3:])
        # # 得到评分
        # rating = book.xpath("div/span[@class='rating_nums']/text()")[0].strip()
        # # 加入结果字符串
        # result += "*%d\t《%s》\t评分：%s\n\t%s\n\t%s\n\n" \
        #           % (count, title, rating, authorInfo, pubInfo)
        #
        # count += 1

    return result


bookSpider('哲学')

# if __name__ == "__main__":
#     main()
#     #  bookSpider('哲学')
