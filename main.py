# run_spider.py
import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from pydispatch import dispatcher
from twisted.internet import reactor, defer
import logging
from shein import SheIn
from zappos import Zappos
from amz_scrap import get_amazon_products
import json 

# Ensure the Scrapy project is on the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Run the spider
def search(keyword):
    if reactor.running:
            reactor.stop()

    # Access the crawled data from SheIn
    shein_data = SheIn(keyword).get_product_details()[:5]

    # Access the crawled data from SheIn
    zappos_data = Zappos(keyword).get_product_details()[:5]

    amazon_data = get_amazon_products(keyword)[:5]
    

    for item in shein_data:
        amazon_data.append(item)
        
    for item in zappos_data:
        amazon_data.append(item)

    # sorted_products = sorted(amazon_data, key=lambda x: (x["p_disc_price"] == 0, x["p_disc_price"], x["p_base_price"]))

    return json.dumps(amazon_data)

