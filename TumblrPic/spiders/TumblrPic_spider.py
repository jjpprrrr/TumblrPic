# -*- coding: utf-8 -*-
# Copyright 2016 jjpprrrr

import sys
reload(sys)
import os
import string
import re

from os.path import expanduser

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from TumblrPic.items import TumblrpicItem

class TumblrPicSpider(CrawlSpider):
    # gather inputs of user IDs
    start_page = raw_input("user ids seperated with comma: ")
    ids = [x.strip() for x in start_page.split(',')]

    # create a directory ~/Pictures/TumblrPic
    home = expanduser("~")
    data_path = os.path.join(home, 'Pictures')
    data_path = os.path.join(data_path, 'TumblrPic')
    try:
        os.mkdir(data_path)
    except:
        pass

    # now create subdictories for user IDs
    for userid in ids:
        try:
            os.mkdir(os.path.join(data_path, userid))
        except:
            pass

    name = 'TumblrPic'
    allowed_domains = ['tumblr.com']
    start_urls = []
    for userid in ids:
        start_urls.append('http://' + userid + '.tumblr.com/archive')


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

            if imgUrl[:12] == 'http://media':
                item['imageUrl'] = 'https://vt.tumblr.com/tumblr' + re.search(r"_([^_]+)_", imgUrl).group(0)[:-1] + '.mp4'
            else:
                item['imageUrl'] = imgUrl

            item['postDate'] = post_date
            item['userID'] = re.search('http://[_a-zA-Z0-9-]+.',response.url).group(0).split('//')[-1][:-1]

            yield item
