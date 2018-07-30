# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NanrentuItem(scrapy.Item):
    # define the fields for your item here like:
    # #明星姓名
    # name = scrapy.Field()
    # #明星所属区域
    # area = scrapy.Field()
    # #明星小类别
    # category =scrapy.Field()
    #明星详情
    folder_path = scrapy.Field()    #列表,[港台帅哥,吴尊]
    #图片下载地址
    img_url = scrapy.Field()    #完整url, http://www.nanrentu.cc/uploads/allimg/170121/7-1F121151600.jpg



