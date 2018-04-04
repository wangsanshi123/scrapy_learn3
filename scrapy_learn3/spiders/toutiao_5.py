# -*- coding: utf-8 -*-
import json

import scrapy

from scrapy_learn3.items import Article, Comment, CommentReply
from scrapy_learn3.utils import emailUtil
from scrapy_learn3.utils.databaseUtil import MysqlUtil
from scrapy_learn3.utils.timeUtil import formatTimestamp


class Toutiao5Spider(scrapy.Spider):
    '用于评论回复的爬取'
    name = "toutiao_5"
    "http://is.snssdk.com/2/comment/v1/reply_list/?id=1579677646145549&count=20&offset=0&iid=15456210477&device_id=39490187575&ac=wifi&channel=baidu&aid=13&app_name=news_article&version_code=636&version_name=6.3.6&device_platform=android&ab_version=173477%2C179885%2C159913%2C177252%2C182659%2C181412%2C172664%2C172658%2C171194%2C181915%2C181466%2C170354%2C180929%2C178898%2C181479%2C179981%2C171602%2C169430%2C179196%2C174396%2C182609%2C182870%2C177166%2C152027%2C176590%2C181531%2C177009%2C182980%2C180705%2C182569%2C180718%2C181217%2C170713%2C179372%2C176739%2C182216%2C156262%2C145585%2C179382%2C174430%2C181819%2C177257%2C182939%2C182847%2C162572%2C181181%2C176601%2C176609%2C179624%2C169176%2C175631%2C179898%2C176617%2C164943%2C170988%2C180928%2C181000%2C176596%2C176653%2C177702%2C176615%2C180150%2C180117&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_feature=94563%2C102749&abflag=3&ssmix=a&device_type=SM-N900P&device_brand=samsung&language=zh&os_api=19&os_version=4.4.2&uuid=864394010762047&openudid=4ccc6af075ab2956&manifest_version_code=636&resolution=1280*720&dpi=240&update_version_code=6368&_rticket=1506512276391&plugin=2431"

    replyUrl = "http://is.snssdk.com/2/comment/v1/reply_list/?id={}&count={}&offset={}&iid=15456210477&device_id=39490187575&ac=wifi&channel=baidu&aid=13&app_name=news_article&version_code=636&version_name=6.3.6&device_platform=android&ab_version=173477%2C179885%2C159913%2C177252%2C182659%2C181412%2C172664%2C172658%2C171194%2C181915%2C181466%2C170354%2C180929%2C178898%2C181479%2C179981%2C171602%2C169430%2C179196%2C174396%2C182609%2C182870%2C177166%2C152027%2C176590%2C181531%2C177009%2C182980%2C180705%2C182569%2C180718%2C181217%2C170713%2C179372%2C176739%2C182216%2C156262%2C145585%2C179382%2C174430%2C181819%2C177257%2C182939%2C182847%2C162572%2C181181%2C176601%2C176609%2C179624%2C169176%2C175631%2C179898%2C176617%2C164943%2C170988%2C180928%2C181000%2C176596%2C176653%2C177702%2C176615%2C180150%2C180117&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_feature=94563%2C102749&abflag=3&ssmix=a&device_type=SM-N900P&device_brand=samsung&language=zh&os_api=19&os_version=4.4.2&uuid=864394010762047&openudid=4ccc6af075ab2956&manifest_version_code=636&resolution=1280*720&dpi=240&update_version_code=6368&_rticket=1506512276391&plugin=2431"
    count = 20

    def __init__(self):
        self.mysqlUtil = MysqlUtil()

    def start_requests(self):
        self.mysqlUtil.cur.execute('select * from toutiao_comment where reply_count >0')
        self.mysqlUtil.conn.commit()
        dataSet = self.mysqlUtil.cur.fetchall()
        for item in dataSet:
            id = item['id']
            title = item['title']
            text = item['text']

            reply_count = int(item['reply_count'])
            offset = 0
            for i in range(reply_count / self.count + 1):
                url = self.replyUrl.format(id, self.count, offset)
                yield scrapy.Request(url=url, meta={'id': id, 'title': title, 'text': text})
                offset += self.count

        pass

    def parse(self, response):
        comment_id = response.meta['id']
        title = response.meta['title']
        text = response.meta['text']

        data = json.loads(response.text)['data']['data']
        # print len(data)
        for item in data:
            digg_count = item['digg_count']
            content = item['content']
            create_time = formatTimestamp(item['create_time'])
            name = item['user']['name']
            id = item['id']
            yield CommentReply(comment_id=comment_id, text=text, digg_count=digg_count, content=content,
                               create_time=create_time, name=name,
                               id=id, title=title)
        pass

    def close(self, reason):  # 爬取结束的时候发送邮件

        print "===close==="

        with open("exceptions.txt", 'r') as f:
            message = f.read().decode('utf-8')
            emailUtil.sendMsg_QQ(info=(u'具体信息：' + message))
