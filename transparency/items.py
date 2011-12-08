# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class TransparencyItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class DeputyItem(Item):
    url = Field()
    state = Field()
    name = Field()
    party = Field()

class FaultItem(Item):
    deputy = Field()
    date = Field()
    misses = Field()
    present = Field()
