# -*- coding: utf-8 -*-
import os

from scrapy.dupefilter import RFPDupeFilter
from scrapy.utils.request import request_fingerprint

class SeenURLFilter(RFPDupeFilter):
    def __getid(self,url):
        return url

    def request_seen(self,request):
        fp = self.__getid(request.url)

        if fp in self.fingerprints:
            return False    # Never do dupefilter
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
