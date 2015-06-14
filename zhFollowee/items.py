# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhfolloweeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    followerLinkId = scrapy.Field()
    followerDataId = scrapy.Field()
    followeeDataIdList = scrapy.Field()
    followeeLinkList = scrapy.Field()
    followeeImgUrlList = scrapy.Field()
    followeeNameList = scrapy.Field()
    followeeFollowersList = scrapy.Field()
    followeeAskList = scrapy.Field()
    followeeAnswerList = scrapy.Field()
    followeeUpList = scrapy.Field()

    pass
