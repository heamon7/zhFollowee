# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import leancloud
from leancloud import Object
from leancloud import LeanCloudError
from leancloud import Query
from scrapy import log
from scrapy.exceptions import DropItem
from zhFollowee import settings
import re

import redis

class ZhfolloweePipeline(object):
    dbPrime1 = 97
    dbPrime2 = 997

    def __init__(self):
        leancloud.init(settings.APP_ID, master_key=settings.MASTER_KEY)




#这里简单处理，不考虑关注者的前后顺序，处理为一个集合,每个关注在数据库里存为一条记录，在缓存里存为一个hash表
    def process_item(self, item, spider):
        if item['followeeDataIdList']:

            # item['followerLinkId'] = re.split('http://www.zhihu.com/people/(\w*)/followees',response.url)[1]
            # item['followerDataId'] = "7e6bee8b4c8c826d76230cd6c139fa27"
            # item['followeeDataIdList'] = sel.xpath('//button/@data-id').extract()
            # item['followeeLinkList'] = sel.xpath('//a[@class="zm-item-link-avatar"]/@href').extract()
            # item['followeeImgUrlList'] = sel.xpath('//a[@class="zm-item-link-avatar"]/img/@src').extract()
            # item['followeeNameList'] = sel.xpath('//h2/a/text()').extract()
            # item['followeeFollowersList'] = sel.xpath('//div[@class="details zg-gray"]/a[1]//text()').extract()
            # item['followeeAskList'] = sel.xpath('//div[@class="details zg-gray"]/a[2]//text()').extract()
            # item['followeeAnswerList'] = sel.xpath('//div[@class="details zg-gray"]/a[3]//text()').extract()
            # item['followeeUpList'] = sel.xpath('//div[@class="details zg-gray"]/a[4]//text()').extract()
            #

            QuestionFollowee = Object.extend('Followee'+item['followerDataId'])
            for index ,value in enumerate(item['followeeDataIdList']):

                questionFollowee = QuestionFollowee()
                if questionFollowee.get('followeeDataId',item['followeeDataIdList'][index]):
                    pass
                else:
                    questionFollowee.set('followerDataId',item['followerDataId'])
                    questionFollowee.set('followerLinkId',item['followerLinkId'])
                    questionFollowee.set('followeeDataId',item['followeeDataIdList'][index])
                    questionFollowee.set('followeeLinkList',item['followeeLinkList'][index])
                    # questionFollowee.set('userIndex',str(userIndex))
                    # questionFollowee.set('userDataId',userDataIdStr)
                    # questionFollowee.set('userLinkId',userLinkId)
                    # questionFollowee.set('tableIndexStr',tableIndexStr)
                    # questionFollowee.set('questionId',questionIdStr)
                    # questionFollowee.set('userIndex',str(userIndex))
                    # questionFollowee.set('userDataId',userDataIdStr)
                    # questionFollowee.set('userLinkId',userLinkId)
                    try:
                        questionFollowee.save()
                    except LeanCloudError,e:
                        try:
                            questionFollowee.save()
                        except LeanCloudError,e:
                            print e




        DropItem()

