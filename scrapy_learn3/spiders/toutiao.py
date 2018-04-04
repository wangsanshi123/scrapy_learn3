# -*- coding: utf-8 -*-
import json

import scrapy

from scrapy_learn3.items import Article
from scrapy_learn3.utils import emailUtil
from scrapy_learn3.utils.timeUtil import formatTime, formatTimestamp


class ToutiaoSpider(scrapy.Spider):
    "直接通过web端爬取文章信息（ToutiaoSpider是通过手机端爬取，手机端只能保存一段时间，能爬到的文章数有限）"
    name = "toutiao"
    allowed_domains = ["toutiao.com"]
    keywords = ['vivo+x20', 'vivox20']
    # start_urls = ['http://www.toutiao.com/search/?keyword={}'.format(keyword)]
    url = "http://www.toutiao.com/search_content/?offset=0&format=json&keyword=vivo+x20&autoload=true&count=20&cur_tab=1"

    def start_requests(self):
        for keyword in self.keywords:
            offset = 0
            time = 0
            while True:
                if time > 12:  # 头条上大概只能搜索到近期的10页内容
                    break
                url = "http://www.toutiao.com/search_content/?offset={}&format=json&keyword={}&autoload=true&count=20&cur_tab=1".format(
                    offset, keyword)
                yield scrapy.Request(url=url)
                time += 1
                offset += 20

    def parse(self, response):

        data = json.loads(response.text)['data']
        # if not data:
        #     self.runFlag = False
        #     print u'爬取结束'
        # print len(data)

        for item in data:
            try:
                group_id = item['group_id']
                comment_count = item['comment_count']
                title = item['title']
                article_url = item['article_url']
                media_name = item['media_name']
                datetime = formatTime(item['datetime'])
                abstract = item['abstract']

                publish_time = formatTimestamp(item['publish_time'])
                behot_time = formatTimestamp(item['behot_time'])
                yield Article(group_id=group_id, comment_count=comment_count, title=title, article_url=article_url,
                              offset=0, media_name=media_name, datetime=datetime, abstract=abstract,
                              publish_time=publish_time, behot_time=behot_time)
            except Exception, e:
                continue
                pass

        pass

    def close(self, reason):  # 爬取结束的时候发送邮件

        with open("exceptions.txt", 'r') as f:
            message = f.read().decode('utf-8')
            emailUtil.sendMsg_QQ(info=(u'具体信息：' + message))
