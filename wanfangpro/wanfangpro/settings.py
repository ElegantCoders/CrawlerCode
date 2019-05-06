# -*- coding: utf-8 -*-

# Scrapy settings for wanfangpro project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wanfangpro'

SPIDER_MODULES = ['wanfangpro.spiders']
NEWSPIDER_MODULE = 'wanfangpro.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'wanfangpro (+http://www.yourdomain.com)'

# Obey robots.txt rules  (遵守robots . txt规则)
ROBOTSTXT_OBEY = False


# Configure maximum concurrent requests performed by Scrapy (default: 16) (配置由Scrapy执行的最大并发请求)
CONCURRENT_REQUESTS = 16  # 并发请求

# Configure a delay for requests for the same website (default: 0) (为同一网站的请求配置延迟)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2  # 下载延迟
# The download delay setting will honor only one of: (下载延迟设置只适用于以下一种情况:)
# CONCURRENT_REQUESTS_PER_DOMAIN = 16  # 每个域的并发请求
# CONCURRENT_REQUESTS_PER_IP = 16  # 每个IP的并发请求

# Disable cookies (enabled by default)  (禁用cookie(默认启用))
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)  (禁用Telnet控制台(默认启用))
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:  (覆盖默认的请求头:)
DEFAULT_REQUEST_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

# Enable or disable spider middlewares  (启用或禁用爬虫中间件)
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'wanfangpro.middlewares.WanfangproSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares  (启用或禁用下载中间件)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'wanfangpro.middlewares.WanfangproDownloaderMiddleware': 543,
#}

# Enable or disable extensions  (启用或禁用扩展)
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines  (配置item管道)
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'wanfangpro.pipelines.WanfangproPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay  (初始下载延迟)
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies  (最大下载延迟要设置在高延迟的情况下)
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to  (Scrapy应该并行发送的请求的平均数量)
# each remote server  (每个远程服务器)
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:  (启用显示节流统计为每个收到的响应:)
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)  (启用和配置HTTP缓存)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
