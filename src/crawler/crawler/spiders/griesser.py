import colorama
import scrapy


class GriesserSpider(scrapy.Spider):
    name = 'griesser'
    allowed_domains = ['griesser.ch']

    def __init__(self, *args, **kwargs):
        super(GriesserSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://griesser.ch/"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        product_section = response.css("div#lstProdukteBigmenu")
        product_columns = product_section.css("ul")
        for column in product_columns:
            product_category = column.css("li a::text").get()
            product_category_values = column.css("li a span::text").getall()
            # self.products.append({product_category: product_category_values})
            self.products += product_category_values
            self.logger.info(f"{product_category} --> {product_category_values}")

        self.logger.info(f"Product: {self.products}")
