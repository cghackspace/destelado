# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings

from scrapy import log

from urlparse import urljoin
from fetcher.items import *

import tempfile
import os
import re

import urlparse


class FaultsSpider(BaseSpider):
    name = "faults"
    allowed_domains = ['excelencias.org.br']
    start_urls = ['http://www.excelencias.org.br/@busca.php?nome=%20Nome%20(ou%20parte)']
    base_url = 'http://www.excelencias.org.br'

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        for div in hxs.select('//div[@id="contem_boxes"]'):
            titulo = div.select('.//div[@id="contem_titulo"]/text()').extract()[0]

            if titulo != u'Câmara dos Deputados/BR':
                continue
            else:
                reg = re.compile('<a class="listapar" href="(?P<url>.*?)">(?P<name>[\w\s]*[\w]+)\s*\(<b>[\w\s]+</b>\)\s-\s(?P<party>.*?)\/(?P<state>.*?)</a><br>', flags=re.U)
                for r in reg.finditer(div.extract()):
                    dep = DeputyItem()
                    dep.update(r.groupdict())
                    if dep['state'] in settings['STATE_TO_FILTER']:
                        id = urlparse.parse_qs(urlparse.urlparse(dep['url']).query).get('id', [0])[0]
                        if not id:
                            continue
                        request = Request(urljoin(self.base_url, '@presencas.php?id=%s' % id), callback=self.parse_deputy_assiduity)
                        request.meta['dep'] = dep
                        yield request
                 
    def parse_deputy_assiduity(self, response):
        hxs = HtmlXPathSelector(response)
        dep = response.meta['dep']

        reg = re.compile('<tr>\s*<td>(?P<date>.*?)\s*<td>[\d]+\s*<td>(?P<present>.*?)\s*<td>(?P<misses>.*?)\s*<td>')
        for r in reg.finditer(response.body):
            fault = FaultItem()
            fault['deputy'] = dep['name']
            fault.update(r.groupdict())
            yield fault
