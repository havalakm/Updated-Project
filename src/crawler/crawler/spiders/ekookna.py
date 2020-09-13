import colorama
import scrapy


class EkooknaSpider(scrapy.Spider):
    name = 'ekookna'
    allowed_domains = ['ekookna.de']

    def __init__(self, *args, **kwargs):
        super(EkooknaSpider, self).__init__(*args, **kwargs)
        self.start_url = "https://ekookna.de/fensterhersteller-fenster-t%C3%BCren-tore-rolll%C3%A4den-eko-okna-s-a-/unsere-produkte"
        self.start_parse = self.parse_product_links
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_product_links(self, response):
        """ Parse product links """
        product_links = response.css(
            "div.menu-product div.item div.show ul li a::attr(href)"
        ).getall()
        self.logger.info(f"Product links: {product_links}")
        for link in product_links:
            yield response.follow(url=link, callback=self.parse_products)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        current_page_products = response.css(
            "div.item.new-item div.content div.title ::text"
        ).getall()
        self.products += [x.strip() for x in current_page_products if x.strip()]
        self.logger.info(f"Products: {self.products}")
