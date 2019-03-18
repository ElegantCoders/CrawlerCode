import requests
from lxml.html import etree
import pymysql
import datetime,time


class ZhongLiang():
    def __init__(self):
        self.req_url = 'http://www.womai.com/index-31000-0.htm'
        self.req_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        self.db = pymysql.connect(host='127.0.0.1', db='leshop', user='root', charset='utf8',
                                  password='jia21990')
        self.cursor = self.db.cursor()

    def fenlei(self):
        req = requests.get(
            self.req_url,
            headers=self.req_header
        )
        if req.status_code == 200:
            req.encoding = 'GBK'
            html = req.text
            # print(html)
            htmls = etree.HTML(html)
            # 一级类别
            self.fenlei_one = htmls.xpath('//li[@class="kinds"]/h3/a/text()')
            print(self.fenlei_one)
            # 二级类别
            self.fenlei_two = [x.strip() for x in htmls.xpath('//h4[@class="sub_head"]/a/text()')]
            print(self.fenlei_two)
            # 三级类别
            self.fenlei_three = [x.strip() for x in htmls.xpath('//li[@class="sub_kind"]/a/text()')]
            print(self.fenlei_three)
            for i in self.fenlei_three:
                sql = '''insert into goods_goodscategory values(null ,%s," "," ",3,0 ,%s,null )'''
                times = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                self.cursor.execute(sql, (i, times))
                self.db.commit()
            print('成功')
            self.cursor.close()
            self.db.close()




if __name__ == '__main__':
    a = ZhongLiang()
    a.fenlei()
