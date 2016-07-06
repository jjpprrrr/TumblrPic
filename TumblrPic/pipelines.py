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
from scrapy.exceptions import DropItem
from os.path import expanduser

class TumblrpicPipeline(object):
    def __init__(self):
        self.home = expanduser("~")
        self.data_path = os.path.join(self.home, 'Pictures')
        self.data_path = os.path.join(self.data_path, 'TumblrPic')



        self.ids_seen = set()
        try:
            f = open(os.path.join(self.data_path, 'data.dat'), 'r')
            for line in f:
                self.ids_seen.add(line.rstrip('\n'))
        except:
            pass
        else:
            f.close()

    def process_item(self, item, spider):

        urls = item['imageUrl']
        if urls in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            filePath = os.path.join(self.data_path, item['userID'])
            post_date = item['postDate']
            fileName = urls.split('/')[-1]

            picture = urllib2.urlopen(urls)

            f = open(os.path.join(filePath, post_date + '_' + fileName), 'wb')
            f.write(picture.read())
            f.close()
            self.ids_seen.add(urls)
            f = open(os.path.join(self.data_path, 'data.dat'), 'a')
            f.write(urls + '\n')
            f.close()

            return item
