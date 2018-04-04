# -*- coding: utf-8 -*-
import json

import scrapy

from scrapy_learn3.items import Article, Comment
from scrapy_learn3.utils import emailUtil
from scrapy_learn3.utils.databaseUtil import MysqlUtil
from scrapy_learn3.utils.timeUtil import formatTimestamp


class Toutiao3Spider(scrapy.Spider):
    "从给出的article信息中爬出具体评论信息"
    name = "toutiao_3"
    urls = []
    commentUrl = "http://is.snssdk.com/article/v2/tab_comments/?group_id={}&item_id={}&aggr_type=1&count={}&offset={}&tab_index=0&fold=0&iid=15456210477&device_id=39490187575&ac=wifi" \
                 "&channel=baidu&aid=13&app_name=news_article&version_code=636&version_name=6.3.6&device_platform=android&ab_version=173477%2C179885%2C159913%2C177252%2C179332%2C172664%" \
                 "2C172658%2C171194%2C180995%2C180360%2C170354%2C180929%2C178898%2C176177%2C179981%2C171602%2C169430%2C179196%2C178242%2C174396%2C178732%2C180777%2C181197%2C181230%2C180699" \
                 "%2C177166%2C152027%2C176590%2C177009%2C178532%2C180705%2C180718%2C181217%2C170713%2C179372%2C176739%2C156262%2C145585%2C179382%2C174430%2C177257%2C181223%2C176457%2C162572%2C" \
                 "181181%2C176601%2C176609%2C179624%2C169176%2C175631%2C179898%2C176617%2C164943%2C170988%2C180928%2C181000%2C178902%2C176596%2C176653%2C177702%2C176615%2C180150%2C180117&ab_c" \
                 "lient=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_feature=94563%2C102749&abflag=3&ssmix=a&device_type=SM-N900P&device_brand=samsung&language=zh&os_api=19&os_version=4.4.2&uuid=8643940107620" \
                 "47&openudid=4ccc6af075ab2956&manifest_version_code=636&resolution=720*1280&dpi=240&update_version_code=6368&_rticket={}&plugin=2431%20HTTP/1.1"
    ticket = '1506320458475'  # 未知标签

    def __init__(self):
        self.mysqlUtil = MysqlUtil()
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def start_requests(self):
        dataSet = self.mysqlUtil.select('toutiao_article')
        count = 20
        for item in dataSet:
            group_id = item['group_id']
            comment_count = item['comment_count']

            title = item['title']
            article_url = item['article_url']
            self.mysqlUtil.cur.execute("update toutiao_article set offset =%s where group_id = %s",
                                       (comment_count, group_id))  # 更新爬取记录：将offset值设为当前文章的评论数，下次更新时就从这个地方爬取
            self.mysqlUtil.conn.commit()

            offset = item['offset'] / 20 * 20  # 在上次的基础上往前挪一个位置
            for i in range((comment_count - offset) / count + 1):
                url = self.commentUrl.format(group_id, group_id, count, offset,
                                             self.ticket)
                yield scrapy.Request(url=url, meta={'url': url, 'article_url': article_url, 'title': title})
                offset += count
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
