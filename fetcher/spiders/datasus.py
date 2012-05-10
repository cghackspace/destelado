# -*- coding: utf-8 -*-

from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest
from scrapy.conf import settings

from model.api import DataAPI
from model.entities import *

from urlparse import urljoin
from decimal import Decimal

import datetime
import re
import urlparse


class SUSSpider(BaseSpider):
    name = "datasus"
    allowed_domains = ['http://tabnet.datasus.gov.br/']
    start_urls = ['http://tabnet.datasus.gov.br/cgi/deftohtm.exe?idb2010/a01.def', 'http://tabnet.datasus.gov.br/cgi/tabcgi.exe?idb2010/f01.def']
    base_url = 'http://tabnet.datasus.gov.br/'
    api = DataAPI()
    estados = {}
    anos_populacao = range(1990, 2010)
    anos_consultas = range(1993, 2010)
    faixas_etarias = ["Menor 1 ano","1 a 4 anos","5 a 9 anos","10 a 14 anos","15 a 19 anos","20 a 24 anos","25 a 29 anos","30 a 34 anos","35 a 39 anos","40 a 44 anos","45 a 49 anos","50 a 54 anos","55 a 59 anos","60 a 64 anos","65 a 69 anos","70 a 74 anos","75 a 79 anos","80 anos e mais","Total"]
    arquivos_populacao = ['popa' + str(ano)[2:4] + '.dbf' for ano in anos_populacao]
    arquivos_consultas = ['inda' + str(ano)[2:4] + '.dbf' for ano in anos_consultas]
    formdatas_populacao = [{'Linha':u'Unidade_da_Federação'.encode('ISO-8859-1'),
                           'Coluna':u'Faixa_Etária'.encode('ISO-8859-1'),
                           'Incremento':u'População'.encode('ISO-8859-1'),
                           'Arquivos':arquivo_populacao,
                           u'SUnidade_da_Federação'.encode('ISO-8859-1'):'TODAS_AS_CATEGORIAS__',
                           u'SRegião'.encode('ISO-8859-1'):'TODAS_AS_CATEGORIAS__',
                           u'SRegião_Metropolitana'.encode('ISO-8859-1'):'TODAS_AS_CATEGORIAS__',
                           'SCapital':'TODAS_AS_CATEGORIAS__',
                           'SSexo':'TODAS_AS_CATEGORIAS__',
                           u'SFaixa_Etária'.encode('ISO-8859-1'):'TODAS_AS_CATEGORIAS__',
                           'formato':'prn',
                           'mostre':'Mostra',
                           } for arquivo_populacao in arquivos_populacao]
    formdatas_consultas = [{'Linha':u'Unidade_da_Federação'.encode('ISO-8859-1'),
                            'Coluna':u'--Não-Ativa--'.encode('ISO-8859-1'),
                            'Incremento':u'Número_consultas'.encode('ISO-8859-1'),
                            'Arquivos':arquivo_consulta,
                            u'SUnidade_da_Federação'.encode('ISO-8859-1'):'TODAS_AS_CATEGORIAS__',
                            u'SRegião'.encode('ISO-8859-1'):'TODAS_AS_CATEGORIAS__',
                            u'SRegião_Metropolitana'.encode('ISO-8859-1'):'TODAS_AS_CATEGORIAS__',
                            'SCapital':'TODAS_AS_CATEGORIAS__',
                            'formato':'prn',
                            'mostre':'Mostra',
                            } for arquivo_consulta in arquivos_consultas]

    def start_requests(self):
        requests_populacao = [FormRequest("http://tabnet.datasus.gov.br/cgi/tabcgi.exe?idb2010/a01.def",
                                        formdata=formdata_populacao,
                                        callback=self.parse_populacao
                                        ) for formdata_populacao in self.formdatas_populacao]
        requests_consultas = [FormRequest("http://tabnet.datasus.gov.br/cgi/tabcgi.exe?idb2010/f01.def",
                                        formdata=formdata_consulta,
                                        callback=self.parse_consultas,
                                        ) for formdata_consulta in self.formdatas_consultas]
        for i in range(len(requests_populacao)):
            requests_populacao[i].meta['ano'] = self.anos_populacao[i]
        for i in range(len(requests_consultas)):
            requests_consultas[i].meta['ano'] = self.anos_consultas[i]
        for f in self.formdatas_consultas:
            print ":::", f['Arquivos']
        return requests_populacao + requests_consultas

    def parse_populacao(self, response):
        hxs = HtmlXPathSelector(response)
        pre = hxs.select('//pre')[0]
        for linha in pre.extract().split('\n'):
            linha = linha.replace('"', '')
            if not linha[0].isalpha():
                continue
            dado = linha.split(';')
            if len(dado) < 2:
                continue
            try:
                if not self.estados.has_key(dado[0]):
                    self.estados[dado[0]] = {'populacao': {}, 'consultas': {}}
                    for ano in self.anos_populacao:
                        self.estados[dado[0]]['populacao'][ano] = {}
                for i in range(len(self.faixas_etarias)):
                    self.estados[dado[0]]['populacao'][response.meta['ano']][self.faixas_etarias[i]] = int(dado[i+1])
            except ValueError:
                continue
            except IndexError:
                continue
            
    def parse_consultas(self, response):
        hxs = HtmlXPathSelector(response)
        try:
            pre = hxs.select('//pre')[0]
        except:
            return
        for linha in pre.extract().split('\n'):
            linha = linha.replace('"', '')
            if not linha[0].isalpha():
                continue
            dado = linha.split(';')
            if len(dado) < 2:
                continue
            try:
                if not self.estados.has_key(dado[0]):
                    self.estados[dado[0]] = {'populacao': {}, 'consultas': {}}
                    for ano in self.anos_populacao:
                        self.estados[dado[0]]['populacao'][ano] = {}
                self.estados[dado[0]]['consultas'][response.meta['ano']] = int(dado[1])
            except ValueError:
                continue
            except IndexError:
                continue
        print self.estados

