# Scrapy settings for transparency project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'fetcher'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['fetcher.spiders']
NEWSPIDER_MODULE = 'fetcher.spiders'
DEFAULT_ITEM_CLASS = 'fetcher.items.TransparencyItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = ['fetcher.pipelines.JsonWriterPipeline']

STATE_TO_FILTER = ['PB']
