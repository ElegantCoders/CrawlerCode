# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from caipiao import settings


class CaipiaoPipeline(object):

    def __init__(self):
        # 链接settings设置里边mysql数据库
        self.db = pymysql.Connect(host=settings.MYSQL_HOST, db=settings.MYSQL_DBNAME, user=settings.MYSQL_USER,
                                  password=settings.MYSQL_PASSWD, port=3306, charset="utf8", use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        try:
            sql = """insert into shuangseqiu(id,qishu,open_data,nub) values(0,%s,%s,%s)"""

            a = str(item['nub'])
            # 插入数据

            self.cursor.execute(sql, (item['qishu'], item['open_data'],
                                      a))
            # 提交sql语句
            self.db.commit()

        except Exception as err:
            return err

        return item

    def close_spider(self, spider):
        print('执行完毕')
        self.cursor.close()
        self.db.close()
