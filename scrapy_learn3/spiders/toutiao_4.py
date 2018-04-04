# -*- coding: utf-8 -*-
import json

import scrapy

from scrapy_learn3.items import Article, Comment
from scrapy_learn3.utils import emailUtil
from scrapy_learn3.utils.timeUtil import formatTimestamp


class Toutiao4Spider(scrapy.Spider):
    '用于缺失评论数据的重爬'
    name = "toutiao_4"
    urls = []

    def start_requests(self):
        with open('missing.json', 'r+') as f:
            data = json.load(f)
            for item in data:
                article_url = item['article_url']
                title = item['title']
                url = item['url']

                yield scrapy.Request(url=url, meta={'url': url, 'article_url': article_url, 'title': title})

                pass

    def parse(self, response):
        "从搜索结果中直接解析出相关文章的评论"
        data = json.loads(response.text)['data']
        article_url = response.meta['article_url']
        title = response.meta['title']

        if len(data) < 20:
            url = response.meta['url']
            dict = {}
            dict['len'] = len(data)
            dict['article_url'] = article_url
            dict['title'] = title
            dict['url'] = url
            self.urls.append(dict)

        for item in data:
            data = item['comment']

            id = data['id']
            reply_count = data['reply_count']
            digg_count = data['digg_count']
            create_time = formatTimestamp(data['create_time'])
            score = data['score']
            user_id = data['user_id']

            user_name = data['user_name']
            text = data['text']
            yield Comment(user_name=user_name, text=text, article_url=article_url, title=title, id=id,
                          reply_count=reply_count, digg_count=digg_count, create_time=create_time, score=score,
                          user_id=user_id)
        pass

        pass

    def close(self, reason):  # 爬取结束的时候发送邮件
        with open('missing.json', 'w') as f:
            f.write(json.dumps(self.urls))

        print "===close==="

        with open("exceptions.txt", 'r') as f:
            message = f.read().decode('utf-8')
            emailUtil.sendMsg_QQ(info=(u'具体信息：' + message))
