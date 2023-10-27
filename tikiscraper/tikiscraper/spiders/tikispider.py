from typing import Iterable
import scrapy
import re

from scrapy.http import Request
# from tikiscraper.items import ProductItem
import json
from time import sleep
from urllib.parse import urlencode

import requests 
# API_KEY = 'bb49a7e2-c24b-4049-bf6c-831f9c8f931b'
# def get_proxy_url(url):
#     payload = {'api_key' : API_KEY, 'url' : url}
#     proxy_url = 'https://proxy.scrapeops.io/v1/' + urlencode(payload)
#     return proxy_url

class TikispiderSpider(scrapy.Spider):
    name = "tikispider"
    allowed_domains = ["tiki.vn"]
    start_urls = ["https://api.tiki.vn/raiden/v2/menu-config?platform=desktop"]
    custom_settings = {
        'FEEDS' : {
            'product_tiki.json' : {'format' : 'json', 'overwrite' : True}
        }
    }
    def parse(self, response):
        category_id_list = re.findall('/c(\d+)"', response.text)

        for category_id in category_id_list:
            page = 1
            while page <= 50:
                url_category = f'https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&category={category_id}&page={page}'
                page+=1
                yield response.follow(url=url_category, callback=self.parse_page)

    def parse_page(self, response):
        product_id = re.findall('{"id":(\d+)', response.text)
        for id in product_id:
            url_product = f'https://tiki.vn/api/v2/products/{id}'
            yield response.follow(url=url_product, callback=self.parse_product)            

    def parse_product(self, response):
        if response.status == 200:
            try:
                data_product = json.loads(response.text)
            except json.JSONDecodeError as e:
                with open("crawler.log", mode="a") as log:
                    log.write(f"JSON Decode Error: {e}: {response}\n")
        else:
            with open("crawler.log", mode="a") as log:
                log.write(f'Status Code {response.status}')
            return
        yield data_product


        
