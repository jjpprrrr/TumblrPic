# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import os

class TumblrpicPipeline(object):
    def process_item(self, item, spider):
        urls = item['imageUrl']
        post_date = item['postDate']
        fileName = urls.split('/')[-1]
        filePath = item['userID']

        picture = urllib2.urlopen(urls)

        f = open(os.path.join(filePath, post_date + '_' + fileName), 'wb')
        f.write(picture.read())
        f.close()


        return item
