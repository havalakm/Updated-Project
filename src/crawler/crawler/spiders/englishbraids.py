import scrapy


class EnglishbraidsSpider(scrapy.Spider):
    name = 'englishbraids'
    allowed_domains = ['englishbraids.com']
    start_urls = ['http://englishbraids.com/']

    def parse(self, response):
        pass
