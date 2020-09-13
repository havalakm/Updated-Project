import colorama
import scrapy


class AluluxSpider(scrapy.Spider):
    name = 'alulux'
    allowed_domains = ['alulux.de']

    def __init__(self, *args, **kwargs):
        super(AluluxSpider, self).__init__(*args, **kwargs)
        self.start_url = ["https://www.alulux.de/rollladen/systeme/",
                          "https://www.alulux.de/raffstore/systeme/",
                          "https://www.alulux.de/garagentor/systeme/"
                          ]
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []
        # self.products = []

    def start_requests(self):
        for url in self.start_url:
            yield scrapy.Request(url=url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        self.products += [
            x.strip()
            for x in response.css("section.productline > h2 ::text").getall()
            if x.strip()
        ]
        self.logger.info(f"Products: {self.products}")
