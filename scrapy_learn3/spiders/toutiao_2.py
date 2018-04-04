# -*- coding: utf-8 -*-
import json

import logging

import scrapy

from scrapy_learn3.items import Article
from scrapy_learn3.utils import emailUtil
from scrapy_learn3.utils.timeUtil import formatTime, formatTimestamp

logger = logging.getLogger(__name__)


class Toutiao2Spider(scrapy.Spider):
    name = "toutiao_2"
    runFlag = True
    keyword = 'vivo%20x20'
    count = 10  # 搜索显示条目数

    ticket = '1506320458475'  # 未知标签

    commentUrl = "http://is.snssdk.com/article/v2/tab_comments/?group_id={}&item_id={}&aggr_type=1&count={}&offset={}&tab_index=0&fold=0&iid=15456210477&device_id=39490187575&ac=wifi" \
                 "&channel=baidu&aid=13&app_name=news_article&version_code=636&version_name=6.3.6&device_platform=android&ab_version=173477%2C179885%2C159913%2C177252%2C179332%2C172664%" \
                 "2C172658%2C171194%2C180995%2C180360%2C170354%2C180929%2C178898%2C176177%2C179981%2C171602%2C169430%2C179196%2C178242%2C174396%2C178732%2C180777%2C181197%2C181230%2C180699" \
                 "%2C177166%2C152027%2C176590%2C177009%2C178532%2C180705%2C180718%2C181217%2C170713%2C179372%2C176739%2C156262%2C145585%2C179382%2C174430%2C177257%2C181223%2C176457%2C162572%2C" \
                 "181181%2C176601%2C176609%2C179624%2C169176%2C175631%2C179898%2C176617%2C164943%2C170988%2C180928%2C181000%2C178902%2C176596%2C176653%2C177702%2C176615%2C180150%2C180117&ab_c" \
                 "lient=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_feature=94563%2C102749&abflag=3&ssmix=a&device_type=SM-N900P&device_brand=samsung&language=zh&os_api=19&os_version=4.4.2&uuid=8643940107620" \
                 "47&openudid=4ccc6af075ab2956&manifest_version_code=636&resolution=720*1280&dpi=240&update_version_code=6368&_rticket={}&plugin=2431%20HTTP/1.1"
    list = []
    lastTime = '2017-09-01 00:00:00'

    def __init__(self):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')

    def start_requests(self):
        time = 0
        offset = 0

        while self.runFlag:
            url = 'http://ib.snssdk.com/api/2/wap/search_content/?from=search_tab&keyword={}&plugin_enable=3&followbtn_template=%7B%2522color_style%2522%3A%2522red%2522%7D&iid=15456210477&device_id=39490187575&ac=wifi&channel=baidu&aid=13&app_name=news_article&version_code=636&version_name=6.3.6&device_platform=android&ab_version=173477%252C179885%252C159913%252C177252%252C179332%252C181412%252C172664%252C172658%252C171194%252C180360%252C181466%252C170354%252C180929%252C178898%252C181479%252C179981%252C171602%252C169430%252C179196%252C178242%252C174396%252C178732%252C180777%252C181197%252C181230%252C180699%252C177166%252C152027%252C176590%252C181531%252C177009%252C178532%252C180705%252C180718%252C181217%252C170713%252C179372%252C176739%252C156262%252C145585%252C179382%252C174430%252C181819%252C177257%252C181223%252C176457%252C162572%252C181181%252C176601%252C176609%252C179624%252C169176%252C175631%252C179898%252C176617%252C164943%252C170988%252C180928%252C181000%252C178902%252C176596%252C176653%252C177702%252C176615%252C180150%252C180117&ab_client=a1%252Cc4%252Ce1%252Cf2%252Cg2%252Cf7&ab_feature=94563%252C102749&abflag=3&device_type=SM-N900P&device_brand=samsung&language=zh&os_api=19&os_version=4.4.2&uuid=864394010762047&openudid=4ccc6af075ab2956&manifest_version_code=636&resolution=1280*720&dpi=240&update_version_code=6368&_rticket=1506395883474&plugin=2431&search_sug=1&forum=1&latitude=30.001249999999995&longitude=110.56358166666665&no_outsite_res=0&as=A1E579FCD93C6EC&cp=59C9DC263EFC9E1&count={}&cur_tab=1&format=json&offset={}&search_text={}&keyword_type=&action_type=input_keyword_search&search_id=' \
                .format(self.keyword, self.ticket, self.count, offset, self.keyword)

            yield scrapy.Request(url=url, meta={'url': url})
            time += 1
            offset += self.count
        pass

    pass

    def parse(self, response):
        "从搜索结果中直接解析出相关文章的评论"
        data = json.loads(response.text)['data']
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
                if datetime < self.lastTime:
                    print "datetime:", datetime
                    print "lastTime:", self.lastTime
                    self.runFlag = False

            except Exception, e:
                continue
                pass

            yield Article(group_id=group_id, comment_count=comment_count, title=title, article_url=article_url,
                          offset=0, media_name=media_name, datetime=datetime, abstract=abstract,
                          publish_time=publish_time, behot_time=behot_time)

        pass

    def close(self, reason):  # 爬取结束的时候发送邮件

        with open("exceptions.txt", 'r') as f:
            message = f.read().decode('utf-8')
            emailUtil.sendMsg_QQ(info=(u'具体信息：' + message))
