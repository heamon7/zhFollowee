# -*- coding: utf-8 -*-
import scrapy

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request,FormRequest
from scrapy.conf import settings
from scrapy.selector import Selector
from scrapy import log
from scrapy.shell import inspect_response


import leancloud

from leancloud import Object
from leancloud import LeanCloudError
from leancloud import Query

from datetime import datetime
from zhFollowee import settings

from zhFollowee.items import ZhfolloweeItem
import re

import json
import redis

class FolloweerSpider(scrapy.Spider):
    name = "followeer"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/',
    )
    followeeCountList =[967]
    handle_httpstatus_list = [401,429,500]
    reqLimit =20

    def __init__(self):
        pass

    def start_requests(self):
        #print "start_requests ing ......"
        return [Request("http://www.zhihu.com",callback = self.post_login)]

    def post_login(self,response):
       # print "post_login ing ......"
        xsrfvalue = response.xpath('/html/body/input[@name= "_xsrf"]/@value').extract()[0]
        return [FormRequest.from_response(response,
                                          #headers = self.headers,
                                          formdata={
                                              '_xsrf':xsrfvalue,
                                              'email':'heamon8@163.com',
                                              'password':'heamon8@()',
                                              'rememberme': 'y'
                                          },
                                          dont_filter = True,
                                          callback = self.after_login
                                        #  dont_filter = True
                                          )]

    def after_login(self,response):
        #print "after_login ing ....."
        self.urls = ['http://www.zhihu.com/node/ProfileFolloweesListV2']


        print "after_login ing ....."
        #inspect_response(response,self)
        #inspect_response(response,self)
        #self.urls = ['http://www.zhihu.com/question/28626263','http://www.zhihu.com/question/22921426','http://www.zhihu.com/question/20123112']
        for index0 ,followeeCount in enumerate(self.followeeCountList):
            if followeeCount:
                # inspect_response(response,self)
                xsrfValue = response.xpath('/html/body/input[@name= "_xsrf"]/@value').extract()[0]

                reqUrl = self.urls[0]

                reqTimes = (int(followeeCount)+self.reqLimit-1)/self.reqLimit
                print "reqTimes %s" %str(reqTimes)
                for index in reversed(range(reqTimes)):
                    print "request index: %s"  %str(index)
                    yield FormRequest(url =reqUrl,
                                              #headers = self.headers,
                                              meta={'offset':index*self.reqLimit,'xsrfValue':xsrfValue},
                                              formdata={
                                                  'method':'next',
                                                  'params':'{"offset":'+ str(index*self.reqLimit)+',"order_by":"created","hash_id":"7e6bee8b4c8c826d76230cd6c139fa27"}',
                                                  '_xsrf':xsrfValue,

                                              },
                                              dont_filter = True,
                                              callback = self.parsePage
                                              )

    def parsePage(self,response):

        if response.status != 200:
            print "ParsePage HTTPStatusCode: %s Retrying !" %str(response.status)
            yield FormRequest(url =response.request.url,
                                              #headers = self.headers,
                                              meta={'offset':response.meta['offset'],'xsrfValue':response.meta['xsrfValue']},
                                              formdata={
                                                  'method':'next',
                                                  'params':'{"offset":'+ str(response.meta['offset'])+',"order_by":"created","hash_id":"7e6bee8b4c8c826d76230cd6c139fa27"}',
                                                  '_xsrf':response.meta['xsrfValue'],

                                              },
                                              dont_filter = True,
                                              callback = self.parsePage
                                              )
        else:
            item =  ZhfolloweeItem()

        #         if response.status != 200:
        # #            print "ParsePage HTTPStatusCode: %s Retrying !" %str(response.status)
        #             yield  self.make_requests_from_url(response.url)
        #
        #         else:

               # inspect_response(response,self)
            data = json.loads(response.body)
            userCountRet = len(data['msg'])
            print "userCountRet: %s" %userCountRet
            selData =''
            if userCountRet:
                for element in data['msg']:
                    selData= selData + element

                sel = Selector(text = selData)

                #item['offset'] = response.meta['offset']
                item['followerLinkId'] = 'sublate'
                item['followerDataId'] = "7e6bee8b4c8c826d76230cd6c139fa27"
                item['followeeDataIdList'] = sel.xpath('//button/@data-id').extract()
                item['followeeLinkList'] = sel.xpath('//a[@class="zm-item-link-avatar"]/@href').extract()
                item['followeeImgUrlList'] = sel.xpath('//a[@class="zm-item-link-avatar"]/img/@src').extract()
                item['followeeNameList'] = sel.xpath('//h2/a/text()').extract()
                item['followeeFollowersList'] = sel.xpath('//div[@class="details zg-gray"]/a[1]//text()').extract()
                item['followeeAskList'] = sel.xpath('//div[@class="details zg-gray"]/a[2]//text()').extract()
                item['followeeAnswerList'] = sel.xpath('//div[@class="details zg-gray"]/a[3]//text()').extract()
                item['followeeUpList'] = sel.xpath('//div[@class="details zg-gray"]/a[4]//text()').extract()

            yield item