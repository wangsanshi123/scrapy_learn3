# -*- coding: utf-8 -*-
import scrapy


class BitecoinSpider(scrapy.Spider):
    name = "bitecoin"
    allowed_domains = ["btc123.com"]

    def start_requests(self):
        # symbol = 'btcchinabtccny'
        symbol = 'huobibtccny'
        timeframe = '1day'
        size = 10
        # https: // www.btc123.com / market / kline?symbol = '+symbol+' & type = '+timeframe+' & size = '+(includeLastBar ? size : size+1)))
        # url = "https://www.btc123.com/api/getTicker?symbol={}&type={}".format(symbol, timeframe)
        url = "https://www.btc123.com/market/kline?symbol={}&type={}&size={}".format(symbol, timeframe,size)
        yield scrapy.Request(url=url)

    def parse(self, response):
        print response.text

        pass
