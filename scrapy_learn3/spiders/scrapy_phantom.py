# -*- coding: utf-8 -*-
import scrapy


class ScrapyPhantomSpider(scrapy.Spider):
    name = "scrapy_phantom"
    allowed_domains = ["cnblogs.com/qiyeboy"]
    start_urls = ['http://cnblogs.com/qiyeboy/']

    def parse(self, response):
        for i in range(10):
            url = response.xpath(
                ".//*[@id='homepage1_HomePageDays_DaysList_ctl0{}_DayList_TitleUrl_0']/@href".format(i)).extract_first()
            # print url
            yield scrapy.Request(url=url, callback=self.parseDetail)
        pass

    def parseDetail(self, response):
        print "=======parseDetail======="
        # print response.xpath(".//*[@id='cb_post_title_url']/text()").extract_first()
        pass
