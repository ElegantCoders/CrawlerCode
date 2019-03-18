# -*- coding: utf-8 -*-
import scrapy
from caipiao.items import CaipiaoItem as a

class ShuangseqiuSpider(scrapy.Spider):
    name = 'shuangseqiu'
    allowed_domains = ['500.com']
    start_urls = ['http://kaijiang.500.com/ssq.shtml']
    def parse(self, response):
        # print(response.status)
        if response.status == 200:
            try:
                lianjie = response.xpath('//span[@class="iSelectBox"]/div/a/@href').extract()
                for i in lianjie:
                    yield scrapy.Request(i,callback=self.meiye)

            except:
                return '没有获取到数据'
    def meiye(self,response):
        # print(response.status)
        item = a()

        item['qishu'] = response.xpath('//td[@class="td_title01"]/span/a/font/strong/text()').extract()[0]

        item['open_data'] = response.xpath('//td[@class="td_title01"]/span[2]/text()').extract()[0]

        item['nub'] = response.xpath('//div[@class="ball_box01"]/ul/li/text()').extract()
        # print(item['qishu'])
        # print(item['open_data'])
        # print(item['nub'])
        yield item



        # # 双色球期数
        # CaipiaoItem['qishu']  = response.xpath('//td[@class="td_title01"]/span/a/font/strong/text()').extract()
        #
        # # 开奖日期
        # CaipiaoItem['open_data'] = response.xpath('//td[@class="td_title01"]/span[2]/text()').extract()
        #
        # # 双色球号码
        # CaipiaoItem['nub'] = response.xpath('//div[@class="ball_box01"]/ul/li/text()').extract()


        # yield CaipiaoItem