# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import re
from scrapy import Request

from scrapy.pipelines.images import ImagesPipeline


class NanrentuPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self,item,info):
        print("-----------------")
        print(item['img_url'])

        yield Request(item['img_url'],meta={'item':item['folder_path'],
                                            'guid':item['img_url']})

    def file_path(self,request,response=None,info=None):
        name = request.meta['item']
        guid=request.meta['guid'].split('/')[-1]

        filename ='full/{0}/{1}/{2}'.format(name[0],name[1],guid)

        return filename