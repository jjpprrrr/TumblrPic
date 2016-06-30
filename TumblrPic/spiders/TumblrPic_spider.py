# -*- coding: utf-8 -*-
# Copyright 2016 jjpprrrr

import sys
reload(sys)
import os
import string

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from TumblrPic.items import TumblrpicItem

class TumblrPicSpider(CrawlSpider):
    start_page = raw_input("user id: ")

    try:
        os.mkdir(start_page)
    except Ex:
        pass

    name = 'TumblrPic'
    allowed_domains = ['tumblr.com']
    start_urls = ['http://' + start_page + '.tumblr.com/archive',]

    rules = [
        # next page link to follow
		Rule(LinkExtractor(restrict_xpaths='//a[@id="next_page_link"]')),

        # links to single post
        Rule(LinkExtractor(restrict_xpaths='//a[@class="hover"]'), callback='parse_item')
	]

    def parse_item(self, response):
        post_date = response.xpath('//a[@class="meta-item post-date"]/text()').extract_first()
        for imgUrl in response.xpath('//meta[@property="og:image"]/@content').extract():
            item = TumblrpicItem()
            item['imageUrl'] = imgUrl
            item['postDate'] = post_date
            item['userID'] = TumblrPicSpider.start_page

            yield item
