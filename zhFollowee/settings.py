# -*- coding: utf-8 -*-

# Scrapy settings for zhFollowee project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'zhFollowee'

SPIDER_MODULES = ['zhFollowee.spiders']
NEWSPIDER_MODULE = 'zhFollowee.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhFollowee (+http://www.yourdomain.com)'
LOG_LEVEL = 'ERROR'
ITEM_PIPELINES = {
    'zhFollowee.pipelines.ZhfolloweePipeline': 300,
   # 'zhihut.pipelines.SecondPipline': 800,
}


DEFAULT_REQUEST_HEADERS = {
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2',
           'Connection': 'keep-alive',
           'Host': 'www.zhihu.com',
           'Referer': 'http://www.zhihu.com/',

}
#
# DEFAULT_REQUEST_HEADERS = {
#            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#            'Accept-Encoding': 'gzip, deflate, sdch',
#            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2',
#            'Connection': 'keep-alive',
#            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#            'Host': 'www.zhihu.com',
#            'Referer': 'http://www.zhihu.com/',
#            'X-Requested-With': 'XMLHttpRequest',
#
# }

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'


APP_ID = '5uvre75z5nydbfsf87mbezlvc3i9103iluvwnepcva59fc22'
MASTER_KEY = 'mq1xdyg72xjet9kln9zzbtorbgf52mc2mxls244cpbd6ujny'

SPIDER_MIDDDLEWARES = {
    'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware':300,
}

DUPEFILTER_CLASS = 'zhFollowee.custom_filters.SeenURLFilter'