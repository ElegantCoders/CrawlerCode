from bs4 import BeautifulSoup
from lxml.html import etree
from queue import Queue
import requests
import re




class kaishi():
    def __init__(self):
        self.req_url = 'http://www.zjol.com.cn/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
        }

    def index(self):
        response = requests.get(
            self.req_url,
            headers=self.headers
        )
        if response.status_code == 200:
            html = response.content.decode()
            htmls = etree.HTML(html)
            # 匹配分类   如 浙江  时政   辟谣....    链接
            fenlei_link = htmls.xpath('//div[@class="siteNav cf"]/ul/li/a/@href')
            print(fenlei_link)


if __name__ == '__main__':
    a = kaishi()
    a.index()
