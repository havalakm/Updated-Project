"""
File:           sathualab_crawler.py
Author:         Havala
Created on:     13/09/20, 1:37 PM

References:
    https://stackoverflow.com/questions/46871133/get-all-spiders-class-name-in-scrapy/46871206
    https://stackoverflow.com/questions/15564844/locally-run-all-of-the-spiders-in-scrapy
"""
import os
import hashlib

import colorama
from scrapy import spiderloader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class SathualabCrawler:
    """ Wrapper class to run scrapy crawler """
    def __init__(self):
        settings_file_path = "src.crawler.crawler.settings"
        os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings_file_path)
        settings = get_project_settings()
        self.process = CrawlerProcess(settings=settings)
        spider_loader = spiderloader.SpiderLoader.from_settings(settings)
        self.spiders = spider_loader.list()
        self.spiders_products = {}
        self.spiders_products_hash = {}

    def crawl(self):
        """ Crawl the website to extract the data """
        for spider in self.spiders:
            self.spiders_products[spider] = []
            self.process.crawl(spider, products=self.spiders_products[spider])

        self.process.start()

        for spider in self.spiders:
            print(f"\n{colorama.Fore.GREEN}Products from {colorama.Fore.MAGENTA}{spider}"
                  f"{colorama.Fore.GREEN} spider: {self.spiders_products[spider]}")
            hash_string = "".join(self.spiders_products[spider]).encode("utf-8")
            self.spiders_products_hash[spider] = hashlib.sha256(hash_string).hexdigest()


if __name__ == "__main__":
    crawler = SathualabCrawler()
    crawler.crawl()
