# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

from scrapy_learn3.items import JubiItem, Article, Comment, CommentReply

logger = logging.getLogger(__name__)


class MySQLStorePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        self.i = 0

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        if isinstance(item, JubiItem):
            d = self.dbpool.runInteraction(self._process_jubi, item, spider)
        elif isinstance(item, Article):
            d = self.dbpool.runInteraction(self._process_article, item, spider)
        elif isinstance(item, Comment):
            d = self.dbpool.runInteraction(self._process_comment, item, spider)
        elif isinstance(item, CommentReply):
            d = self.dbpool.runInteraction(self._process_commentReply, item, spider)


        else:
            d = self.dbpool.runInteraction(self._process_nothing, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    # 将每行更新或写入数据库中
    def _process_jubi(self, conn, item, spider):
        try:
            conn.execute("insert into jubi VALUES (%s,%s,%s,%s,%s,%s,%s)",
                         (item['date'], item['token'], item['open'],
                          item['max'], item['close'], item['min'], item['amount']))
        except Exception, e:
            logger.error(e)
            pass

        pass

    def _process_article(self, conn, item, spider):
        conn.execute("select * from toutiao_article where group_id=%s", (item['group_id'],))
        ret = conn.fetchone()

        try:
            if ret:
                conn.execute("update toutiao_article set comment_count=%s where group_id=%s",
                             (item['comment_count'], item['group_id']))

            else:
                conn.execute("insert into toutiao_article VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                             (item['group_id'], item['comment_count'], item['title'], item['article_url'],
                              item['offset'], item['media_name'], item['datetime'], item['abstract'],
                              item['publish_time'], item['behot_time']))
        except Exception, e:
            logger.error(e)
            pass

        pass

    def _process_comment(self, conn, item, spider):
        try:
            conn.execute("insert into toutiao_comment VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                         (item['user_name'], item['text'], item['article_url'], item['title'], item['id'],
                          item['reply_count'], item['digg_count'], item['create_time'], item['score'], item['user_id']))
        except Exception, e:
            logger.error(e)
            pass

        pass



    def _process_nothing(self, conn, item, spider):
        # do nothing

        pass
        # 异常处理

    def _handle_error(self, failure, item, spider):
        logging.log.err(failure)
