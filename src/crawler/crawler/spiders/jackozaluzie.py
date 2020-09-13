import colorama
import scrapy


class JackozaluzieSpider(scrapy.Spider):
    name = 'jackozaluzie'
    allowed_domains = ['jackozaluzie.sk']

    def __init__(self, *args, **kwargs):
        super(JackozaluzieSpider, self).__init__(*args, **kwargs)
        self.start_url = "https://www.jackozaluzie.sk/de/isso-retiazka--jackodesign.c1.html"
        self.start_parse = self.parse_product_links
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_product_links(self, response):
        """ Parse product links """
        product_links = response.css(
            "ul#mainmenu > li:nth-child(3) li > a::attr(href)"
        ).getall()
        self.logger.info(f"Product links: {product_links}")
        for link in product_links:
            yield response.follow(url=link, callback=self.parse_products)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        current_page_products = response.css(
            "ul.sidemenu-nav > li a ::text"
        ).getall()
        self.products += [x.strip() for x in current_page_products if x.strip()]
        self.logger.info(f"Products: {self.products}")
