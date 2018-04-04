# -*- coding: utf-8 -*-
import logging
from time import localtime, strftime

import scrapy
from scrapy.utils.response import get_base_url

from scrapy_learn3.items import JubiItem
from scrapy_learn3.utils import emailUtil

logger = logging.getLogger(__name__)


class JubiSpider(scrapy.Spider):
    name = "jubi"

    start_urls = ['http://www.jubi.com']

    def __init__(self):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def parse(self, response):
        lis = response.xpath(".//*[@id='price_today_ul']/li")

        for li in lis:
            token = li.xpath(".//b/text()").extract_first()
            name = li.xpath(".//p/text()").extract_first()
            url = get_base_url(response) + li.xpath(".//a/@href").extract_first()
            yield scrapy.Request(url=url, meta={"token": token, "name": name}, callback=self.parseCoin)

        pass

    def parseCoin(self, response):
        'https://k.bimao.com/marketCenter/market/v0/kline?symbol=jubi_ltc_cny&type=86400'
        token = response.meta['token']
        name = response.meta['name']
        url = "https://k.bimao.com/marketCenter/market/v0/kline?symbol=jubi_{}_cny&type=86400".format(token.lower())
        print url
        yield scrapy.Request(url=url, callback=self.parseDetail, meta={"name": name, "token": token})
        pass

    def parseDetail(self, response):
        name = response.meta["name"]
        token = response.meta["token"]
        result = response.text
        result = result.split("],")
        for item in result:
            item = item.strip("[]]").split(",")
            date = item[0]
            time_local = localtime(float(date))
            date = strftime("%Y-%m-%d %H:%M:%S", time_local)
            # print date, item[1], "    ", item[2], "    ", item[3], "    ", item[4], "    ", item[5], "\n "

            yield JubiItem(date=date, token=token, open=item[1], max=item[2], min=item[3],
                           close=item[4],
                           amount=item[5])
        pass

    def close(self, reason):  # 爬取结束的时候发送邮件
        logger.info(u"======爬取结束=======")
        with open("exceptions.txt", 'r') as f:
            message = f.read()
            emailUtil.sendMsg_QQ(info=(u"任务结束：" + message))
