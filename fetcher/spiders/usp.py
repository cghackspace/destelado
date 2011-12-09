# -*- coding: utf-8 -*-

from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings

from model.api import DataAPI
from model.entities import *

from urlparse import urljoin
from decimal import Decimal

import datetime
import re
import urlparse


class FaultsSpider(BaseSpider):
    name = "faults"
    allowed_domains = ['excelencias.org.br']
    start_urls = ['http://www.excelencias.org.br/@busca.php?nome=%20Nome%20(ou%20parte)']
    base_url = 'http://www.excelencias.org.br'
    api = DataAPI("mysql://root:010203@localhost:3306/destelado")

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        for div in hxs.select('//div[@id="contem_boxes"]'):
            titulo = div.select('.//div[@id="contem_titulo"]/text()').extract()[0]

            if not titulo.endswith(u'mara dos Deputados/BR'):
                continue
            else:
                reg = re.compile('<a class="listapar" href="(?P<url>.*?)">(?P<name>[\w\s]*[\w]+)\s*\(<b>[\w\s]+</b>\)\s-\s(?P<party>.*?)\/(?P<state>.*?)</a><br>', flags=re.U)
                for r in reg.finditer(div.extract()):
                    dict_deputy = r.groupdict()
                    #if dict_deputy['state'] in settings['STATE_TO_FILTER']:
                    db_deputy = self.api.get_deputado_por_nome(dict_deputy['name'])
                    if not db_deputy:
                        dep = Deputado(dict_deputy['name'], dict_deputy['state'], dict_deputy['party'])
                        self.api.inserir_deputado(dep)
                    else:
                        dep = db_deputy[0]

                    id = urlparse.parse_qs(urlparse.urlparse(dict_deputy['url']).query).get('id', [0])[0]
                    if not id:
                        continue
                    request = Request(urljoin(self.base_url, '@presencas.php?id=%s' % id), callback=self.parse_deputy_assiduity)
                    request.meta['dep'] = dep
                    yield request
                    
                    request = Request(urljoin(self.base_url, '@uso_verbas_als.php?uf=16&id=%s' % id), callback=self.parse_deputy_costs)
                    request.meta['dep'] = dep
                    yield request
                 
    def parse_deputy_assiduity(self, response):
        hxs = HtmlXPathSelector(response)
        dep = response.meta['dep']

        reg = re.compile('<tr>\s*<td>(?P<date>.*?)\s*<td>[\d]+\s*<td>(?P<present>.*?)\s*<td>(?P<misses>.*?)\s*<td>')
        for r in reg.finditer(response.body):
            dict_assiduidade = r.groupdict()
            mes, ano = dict_assiduidade['date'].split('/')
            date = datetime.date(int(ano), int(mes), 1)
            assiduidade = Assiduidade(dep.id, date, dict_assiduidade['present'], dict_assiduidade['misses'])
            self.api.inserir_assiduidade(assiduidade)

    def parse_deputy_costs(self, response):
        pass
        hxs = HtmlXPathSelector(response)
        dep = response.meta['dep']
        reg = re.compile('<tr>\s*<td[\s\w=]*>(?P<description>.*?)\s*<td nowrap><p class=dir>R\$\s(?P<gasto2011>.*?)\s*<td', flags=re.U)
        for r in reg.finditer(response.body):
            dict_gasto = r.groupdict()
            gasto = Gasto(dep.id, 2011, dict_gasto['description'].decode('iso-8859-1'), '', Decimal(dict_gasto['gasto2011'].replace('.','').replace(',','.')))
            if gasto.valor:
                self.api.inserir_gasto(gasto)
