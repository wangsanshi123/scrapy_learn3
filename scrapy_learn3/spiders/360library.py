# -*- coding: utf-8 -*-


import json
import sys

import scrapy
from scrapy import Selector

from scrapy_learn3.items import Article
from scrapy_learn3.utils import emailUtil


class ZhihuSpider(scrapy.Spider):
    name = "360library"

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')

    def start_requests(self):
        url = "https://m.baidu.com/mip?ext=%7B%22lid%22%3A%2213822225533373016556%22%2C%22url%22%3A%22%2F%2Fmipcache.bdstatic.com%2Fc%2Fwww.360doc.cn%2Fmip%2F301900478.html%22%7D&title=360doc%E4%B8%AA%E4%BA%BA%E5%9B%BE%E4%B9%A6%E9%A6%86"
        yield scrapy.Request(url=url)

    def parse(self, response):
        print (response)

        pass

    def close(self, reason):  # 爬取结束的时候发送邮件

        with open("exceptions.txt", 'r') as f:
            message = f.read().decode('utf-8')
            emailUtil.sendMsg_QQ(info=(u'具体信息：' + message))
        pass
