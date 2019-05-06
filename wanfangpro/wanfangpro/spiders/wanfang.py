# -*- coding: utf-8 -*-
import scrapy
from lxml.html import etree
from wanfangpro.start_urls import start_url_function
from urllib.parse import quote


class WanfangSpider(scrapy.Spider):
    name = 'wanfang'
    allowed_domains = ['wanfangdata.com.cn']
    start_urls = start_url_function()

    def parse(self, response):
        print(response.url)

        # 获取列表页的源码
        res = response.body.decode()
        xpath_html = etree.HTML(res)

        # 匹配总页数
        page = xpath_html.xpath("//p[@class='pager']/span[1]/text()")[0]
        page = page.split('/')

        # 关键字    法律  政治
        keyworks = ['法律', '政治']
        # 期刊
        if 'QK' in response.url:
            for i in range(int(page[0]), 2):  # int(page[1]) + 1
                for keywork in keyworks:
                    urls = 'http://s.wanfangdata.com.cn/Paper.aspx?q={}%20DBID%3AWF_QK&f=top&p={}'.format(
                        quote(keywork), i)
                    yield scrapy.Request(url=urls, callback=self.old_list_url)
        # 学位
        elif 'XW' == response.url:
            for i in range(int(page[0]), 2):
                for keywork in keyworks:
                    urls = 'http://s.wanfangdata.com.cn/Paper.aspx?q={}%20DBID%3AWF_XW&f=top&p={}'.format(
                        quote(keywork), i)
                    yield scrapy.Request(url=urls, callback=self.old_list_url)
        # 会议
        elif 'HY' == response.url:
            for i in range(int(page[0]), 2):
                for keywork in keyworks:
                    urls = 'http://s.wanfangdata.com.cn/Paper.aspx?q={}%20DBID%3AWF_HY&f=top&p={}'.format(
                        quote(keywork), i)
                    yield scrapy.Request(url=urls, callback=self.old_list_url)
        # 科技报告
        elif 'NSTR' in response.url:
            for i in range(int(page[0]), 2):
                for keywork in keyworks:
                    urls = 'http://s.wanfangdata.com.cn/NSTR.aspx?q={}&f=top&p={}'.format(quote(keywork), i)
                    yield scrapy.Request(urls, callback=self.old_list_url)
        # 专利
        elif 'patent' in response.url:
            for i in range(int(page[0]), 2):
                for keywork in keyworks:
                    urls = 'http://s.wanfangdata.com.cn/patent.aspx?q={}&f=top&p={}'.format(quote(keywork), i)
                    yield scrapy.Request(urls, callback=self.old_list_url)
        # 法规
        elif 'Claw' in response.url:
            for i in range(int(page[0]), 2):
                for keywork in keyworks:
                    urls = 'http://s.wanfangdata.com.cn/Claw.aspx?q={}&f=top&p={}'.format(quote(keywork), i)
                    yield scrapy.Request(urls, callback=self.old_list_url)

    # 通过旧版列表页url切割出文章详情id号   然后拼接进新版列表页url发起请求
    def old_list_url(self, response):
        res = response.body.decode()
        xpath_html = etree.HTML(res)
        # 旧版详情链接
        old_detail_link = xpath_html.xpath('//div[@class="record-title"]/a[@class="title"]/@href')
        # 遍历旧版详情链接    取详情id号
        for detail_link in old_detail_link:
            # 转换为字符串
            detail_links = str(detail_link)
            # 倒数第二位开始往后切割   然后取列表最后一位
            detail_link = detail_links.split('/')[-2:][1]
            # 判断如果取到空串   就取列表第一位
            if detail_link == '':
                detail_link = detail_links.split('/')[-2:][0]
            # # 遍历  去除空串
            # for i in detail_link:
            #     if i == "":
            #         detail_link.remove(i)
            # # 取倒数第一位的值 得到详情id号
            # detail_link = detail_link[-1:]
            # print(detail_link)
            # 期刊
            if 'QK' in response.url:
                # 拼接新版详情url
                new_detail_url = 'http://wanfangdata.com.cn/details/detail.do?_type=perio&id=' + detail_link
                yield scrapy.Request(url=new_detail_url, callback=self.qk_detail)
                # print(new_detail_url)
            # 学位
            elif 'XW' == response.url:
                new_detail_url = 'http://wanfangdata.com.cn/details/detail.do?_type=degree&id=' + detail_link
                yield scrapy.Request(url=new_detail_url, callback=self.xw_detail)
                # print(new_detail_url)
            # 会议
            elif 'HY' == response.url:
                new_detail_url = 'http://wanfangdata.com.cn/details/detail.do?_type=conference&id=' + detail_link
                yield scrapy.Request(url=new_detail_url, callback=self.hy_detail)
                # print(new_detail_url)
            # 科技报告
            elif 'NSTR' in response.url:
                new_detail_url = 'http://wanfangdata.com.cn/details/detail.do?_type=tech&id=' + detail_link
                yield scrapy.Request(url=new_detail_url, callback=self.kjbg_detail)
                # print(new_detail_url)
            # 专利
            elif 'patent' in response.url:
                new_detail_url = 'http://wanfangdata.com.cn/details/detail.do?_type=patent&id=' + detail_link
                yield scrapy.Request(url=new_detail_url, callback=self.zl_detail)
                # print(new_detail_url)
            # 法规
            elif 'Claw' in response.url:
                new_detail_url = 'http://wanfangdata.com.cn/details/detail.do?_type=legislations&id=' + detail_link
                yield scrapy.Request(url=new_detail_url, callback=self.fg_detail)
                # print(new_detail_url)

    # 获取政治  法律  文章的详情内容
    # 期刊详情函数
    def qk_detail(self, response):
        # 中文标题
        chinese_title = response.xpath('//*[@id="div_a"]/div/div[2]/div[1]/div[1]/text()').extract_first()
        # 英文标题
        english_title = response.xpath('//div[@class="English"]/text()').extract_first()
        # 摘要
        abstract = response.xpath('//div[@class="abstract"]/textarea/text()').extract_first()

        if response.xpath('//ul/li[2]/div[1]/text()').extract_first() == '关键词：':
            # 关键字
            chinese_antistop = response.xpath('//ul/li[2]/div[2]/a/text()').extract()
            # print(chinese_antistop)

        lis = response.xpath('//ul[@class="info"]//li')
        for li in lis:
            # print(li.xpath('./div[@class="info_left"]/text()').extract_first(''))
            if li.xpath('./div[@class="info_left"]/text()').extract_first() == 'doi：':
                # doi
                doi = li.xpath('./div[@class="info_right author"]/a/text()').extract_first()
                # print(doi)
            elif li.xpath('./div[@class="info_left"]/text()').extract_first() == '作者：':
                # 作者中文名
                author_chinese_name = li.xpath('./div[2]/a/text()').extract()
                # print(author_chinese_name)
            elif li.xpath('./div[@class="info_left"]/text()').extract_first() == 'Author：':
                # 作者英文名
                author_english_name = li.xpath('./div[2]/a/text()').extract()
                # print(author_english_name)
            elif li.xpath('./div[@class="info_left"]/text()').extract_first() == '作者单位：':
                # 作者单位
                author_unit = li.xpath('./div[2]/a/text()').extract()
                # print(author_unit)
            elif li.xpath('./div[@class="info_left"]/text()').extract_first() == '刊名：':
                # 刊名
                journal_name = li.xpath('./div[2]/a/text()').extract()
                # print(journal_name)
            elif li.xpath('./div[@class="info_left"]/text()').extract_first() == 'Journal：':
                # Journal
                Journal = li.xpath('./div[2]/a/text()').extract()
                # print(Journal)
            elif li.xpath('./div[@class="info_left"]/text()').extract_first() == '年，卷(期)：':
                # 作者单位
                year_expect = li.xpath('./div[2]/a/text()').extract()
                # print(year_expect)
            elif li.xpath('./div[@class="info_left"]/text()').extract_first() == '所属期刊栏目：':
                # 所属期刊栏目
                periodical_column = li.xpath('./div[2]/a/text()').extract()
                # print(periodical_column)
            elif li.xpath('./div[@class="info_left"]/text()').extract_first() == '分类号：':
                # 分类号
                class_number = li.xpath('./div[2]/text()').extract_first()
                # print(class_number)
            elif li.xpath('./div[@class="info_left"]/text()').extract_first() == '基金项目：':
                # 基金项目
                fund_project = li.xpath('./div[2]/a/text()').extract()
                # print(fund_project)
            # elif li.xpath('./div[@class="info_left"]/text()').extract_first() == '在线出版日期：':
            #     # 在线出版日期
            #     publication_date = li.xpath('./div[2]/a/text()').extract()
            #     print(publication_date)
            # elif li.xpath('./div[@class="info_left"]/text()').extract_first() == '页数：':
            #     # 页数
            #     number_of_pages = li.xpath('./div[2]/a/text()').extract()
            #     print(number_of_pages)
            # elif li.xpath('./div[@class="info_left"]/text()').extract_first() == '页码：':
            #     # 页码
            #     pagination = li.xpath('./div[2]/a/text()').extract()
            #     print(pagination)

        # # 所属期刊栏目
        # periodical_column = response.xpath(
        #     '//ul[@class="info"]/li[9]/div[@class="info_right author"]/a/text()').extract_first()
        # # 分类号
        # class_number = response.xpath(
        #     '///ul[@class="info"]/li[10]/div[@class="info_right author"]/text()').extract_first()
        # # 基金项目
        # fund_project = response.xpath(
        #     '//ul[@class="info"]/li[11]/div[@class="info_right author"]/a/text()').extract_first()
        # # 在线出版日期
        # publication_date = response.xpath(
        #     '//ul[@class="info"]/li[12]/div[@class="info_right author"]/text()').extract_first()
        # # 页数
        # number_of_pages = response.xpath(
        #     '//ul[@class="info"]/li[13]/div[@class="info_right author"]/text()').extract_first()
        # # 页码
        # pagination = response.xpath('//ul[@class="info"]/li[14]/div[@class="info_right author"]/text()').extract_first()

        # print(
        #     chinese_title,
        #     english_title,
        #     abstract,
        #     doi,
        #     chinese_antistop,
        #     author_chinese_name,
        #     author_unit,
        #     journal_name,
        #     Journal,
        #     year_expect,
        #     periodical_column,
        #     number_of_pages,
        #     pagination

        # print(chinese_antistop)
        # print(author_chinese_name)
        """
        ,
            '中文关键词' + ':' + chinese_antistop,
            '作者中文名' + ':' + author_chinese_name,
            '作者英文名' + ':' + author_english_name,
            '作者单位' + ':' + author_unit,
            '刊名' + ':' + journal_name,
            'Journal' + ':' + Journal,
            '年，卷(期)' + ':' + year_expect,
            '所属期刊栏目' + ':' + periodical_column,
            '分类号' + ':' + class_number,
            '基金项目' + ':' + fund_project,
            '在线出版日期' + ':' + publication_date,
            '页数' + ':' + number_of_pages,
            '页码' + ':' + pagination
        """

    # 学位
    def xw_detail(self, response):
        pass

    # 会议
    def hy_detail(self, response):
        pass

    # 科技报告
    def kjbg_detail(self, response):
        pass

    # 专利
    def zl_detail(self, response):
        pass

    # 法规
    def fg_detail(self, response):
        pass
