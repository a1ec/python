# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DA(scrapy.Item):
# Application No:	CDC-12/2015
# Description:	Proposed internal fit out and additional use of grocery shop to include a butcher
# Type:	Complying Development (Council)
# Date Lodged:	06/07/2015
# Date Determined:	25/08/2015
# Responsible Officer:	Nazim Bhuiyan
# Estimated Cost:	$15,000
# Status:	Approved
# Decision:	Approved
    da_no = scrapy.Field()
    lga = scrapy.Field()
    url = scrapy.Field()
    date_lodged = scrapy.Field()

    house_no = scrapy.Field()
    street = scrapy.Field()
    town = scrapy.Field()
    
    desc_full = scrapy.Field()
    est_cost = scrapy.Field()
    status = scrapy.Field()
    
    date_determined = scrapy.Field()
    decision = scrapy.Field()
    date_scr_created = scrapy.Field()
    date_scr_modified = scrapy.Field()
    
    def address():
        pass # return full string of address, like "17 Troy Street, CAMPSIE"
    # TODO people list: name_no and roles
    # TODO properties list: property_no
    
class Person(scrapy.Item):
    name_no = scrapy.Field()
    full_name = scrapy.Field()
    
class Property(scrapy.Item):
    property_no = scrapy.Field()
    full_address = scrapy.Field()
