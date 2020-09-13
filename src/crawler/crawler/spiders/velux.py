import colorama
import scrapy


class VeluxSpider(scrapy.Spider):
    name = 'velux'
    allowed_domains = ['velux.com']

    def __init__(self, *args, **kwargs):
        super(VeluxSpider, self).__init__(*args, **kwargs)
        self.start_url = "https://www.velux.com/what-we-sell/product-overview"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        # Get all the section with style "padding-top:0em;"
        product_section = response.css('section[style="padding-top:0em;"]')
        self.products += product_section.css("div.container_12.clearfix  h3::text").getall()
        self.logger.info(f"Products: {self.products}")


