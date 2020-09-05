import colorama
import scrapy


class EnglishbraidsSpider(scrapy.Spider):
    name = "englishbraids"
    allowed_domains = ["englishbraids.com"]
    not_found = "__NOT_FOUND__"

    def __init__(self, *args, **kwargs):
        super(EnglishbraidsSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://englishbraids.com/"
        self.start_parse = self.parse_products
        self.products = []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        product_category_section = response.css(
            "div.navigation-category-list.navigation-category-products"
        )
        product_categories = product_category_section.css(
            "ul.category-list"
        )

        for category in product_categories:
            name = category.css("li.first a::text").get(default=self.not_found).strip()
            products = category.css("li:not([class]) a::text").getall()
            self.logger.info(f"Name: {name}")
            self.logger.info(f"Products: {products}")
            self.products.append(
                {name: products}
            )

