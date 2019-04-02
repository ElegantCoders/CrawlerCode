import re
import json
import requests
import pymysql, threading
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import HTTPError, Timeout, RequestException, ProxyError, ConnectTimeout


class JDPro(object):
    def __init__(self, goodsID):
        self.goodsID = goodsID
        self.url = 'https://sclub.jd.com/comment/productPageComments.action?callback=&productId={}&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
        }
        # 链接数据库
        self.db = pymysql.Connect(
            host='127.0.0.1', user='root', password="jia21990",
            database='jdpro', port=3306, charset='utf8'
        )
        # 创建游标
        self.cursor = self.db.cursor()
        # 实例化一个lock（互斥锁）
        self.myLock = threading.Lock()

    # 获取总页数
    def request_page(self):
        # 拼接url
        url = self.url.format(self.goodsID, 0)
        # 调用发起请求函数 把return结果赋值
        html_text = self.request(url)
        if html_text:
            dict_text = json.loads(html_text)
            # 获取总页数
            maxPage = dict_text['maxPage']
            self.request_pool(maxPage)

    # 添加进线程池
    def request_pool(self, maxPage):
        # 将任务添加线程池中
        pool = ThreadPoolExecutor(10)
        # 遍历出请求的次数  拼接urls
        for count in range(0, maxPage):
            # 拼接url
            urls = self.url.format(self.goodsID, count)

            result = pool.submit(self.request, urls)
            result.add_done_callback(self.parse_comments)

        pool.shutdown()

    # 获取评论详情数据
    def parse_comments(self, future):
        response_text = future.result()
        if response_text:
            dict_text = json.loads(response_text)
            # 通过键取值   取评论
            comments = dict_text['comments'][0]
            # 用户头像
            userImage = comments['userImage']
            # 用户昵称
            nickname = comments['nickname']
            # 评论内容
            content = comments['content']
            # 颜色
            productColor = comments['productColor']
            # 版式
            productSize = comments['productSize']
            # 内存
            saleValue = comments['productSales'][0]['saleValue']
            # 评论时间
            creationTime = comments['creationTime']
            self.save_db(userImage, nickname, content, productColor, productSize, saleValue, creationTime)

    def request(self, url):
        try:
            # 发起请求
            response = requests.get(url, headers=self.headers, timeout=10)
            # 判断响应状态码
            if response.status_code == 200:
                # 获取源码
                html_text = response.text
                return html_text
        except (HTTPError, Timeout, RequestException, ProxyError, ConnectTimeout) as err:
            print(err)
            return None

    # 保存到数据库
    def save_db(self, *args):
        sql = '''insert into jingdong values (0,%s,%s,%s,%s,%s,%s,%s)'''
        # 加锁
        self.myLock.acquire()
        try:
            # 每次运行sql之前，ping一次，如果连接断开就重连
            self.db.ping(reconnect=True)
            self.cursor.execute(sql, (args[0], args[1], args[2], args[3], args[4], args[5], args[6]))
            self.db.commit()
            print('插入数据成功')
        except Exception as err:
            self.db.rollback()
            print(err)
        # 解锁
        self.myLock.release()

    def close(self):
        self.db.close()
        self.cursor.close()


def main():
    url = 'https://item.jd.com/5089253.html'
    goodsid = re.compile('\d+', re.S)
    goodsID = re.findall(goodsid, url)[0]
    jd = JDPro(goodsID)
    jd.request_page()
    jd.close()


if __name__ == '__main__':
    main()
