# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyLearn3Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JubiItem(scrapy.Item):
    date = scrapy.Field()

    token = scrapy.Field()
    open = scrapy.Field()
    max = scrapy.Field()
    close = scrapy.Field()
    min = scrapy.Field()
    amount = scrapy.Field()


class Article(scrapy.Item):
    group_id = scrapy.Field()
    comment_count = scrapy.Field()
    title = scrapy.Field()
    article_url = scrapy.Field()
    offset = scrapy.Field()

    media_name = scrapy.Field()
    datetime = scrapy.Field()
    abstract = scrapy.Field()

    publish_time = scrapy.Field()
    behot_time = scrapy.Field()


class Comment(scrapy.Item):
    user_name = scrapy.Field()
    text = scrapy.Field()
    article_url = scrapy.Field()
    title = scrapy.Field()

    id = scrapy.Field()
    reply_count = scrapy.Field()
    digg_count = scrapy.Field()
    create_time = scrapy.Field()
    score = scrapy.Field()
    user_id = scrapy.Field()


class CommentReply(scrapy.Item):
    comment_id = scrapy.Field()
    text = scrapy.Field()
    digg_count = scrapy.Field()
    content = scrapy.Field()

    create_time = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()



