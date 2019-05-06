from urllib.parse import quote


# 拼接起始url
def start_url_function():
    # 定义起始url列表
    start_urls = []

    # 根据分类和关键字拼接url

    # 分类    期刊   学位   会议
    classifys = ['QK', 'XW', 'HY']
    # 关键字    法律  政治
    keyworks = ['法律', '政治']

    #         科技报告   专利    法规
    p_n_cs = ['NSTR', 'patent', 'Claw']

    # 拼接首页url
    for page in range(1, 2):
        # 遍历分类
        for classify in classifys:
            # 遍历关键字
            for keywork in keyworks:
                url = 'http://s.wanfangdata.com.cn/Paper.aspx?q={}+DBID%3AWF_{}&f=top&p={}'.format(quote(keywork),
                                                                                                   classify, str(page))
                # 添加进url列表
                start_urls.append(url)

    # 拼接首页url
    for page in range(1, 2):
        # 遍历科技报告   法规    专利
        for p_n_c in p_n_cs:
            # 遍历关键字
            for keywork in keyworks:
                url = 'http://s.wanfangdata.com.cn/{}.aspx?q={}&f=top&p={}'.format(p_n_c, quote(keywork), str(page))

                # 遍历关键字
                start_urls.append(url)

    return start_urls


if __name__ == '__main__':
    start_url_function()
