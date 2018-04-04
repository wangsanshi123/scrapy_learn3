# -*- coding: utf-8 -*-
# @Time : 2017/1/1 17:51
# @Author : woodenrobot
from scrapy import cmdline

# name = 'toutiao_2'
# name = 'toutiao_3'
# name = 'toutiao'
name = 'amazon'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
