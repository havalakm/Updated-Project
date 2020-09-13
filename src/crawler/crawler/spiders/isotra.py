import colorama
import scrapy


class IsotraSpider(scrapy.Spider):
    name = 'isotra'
    allowed_domains = ['isotra.eu']

    def __init__(self, *args, **kwargs):
        super(IsotraSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://isotra.eu/"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        main_navigation = response.css("ul#list-menu-header")
        product_menu = main_navigation.css("li:nth-child(2) div.submenu")
        product_categories = product_menu.css("li a")
        for category in product_categories:
            link = category.attrib["href"]
            name = category.css("*::text").get()
            yield response.follow(
                url=link,
                callback=self.parse_product_category,
                cb_kwargs={"category": name}
            )

    def parse_product_category(self, response, category):
        """ Parse products from each category """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        gallery = response.css("div.white-top ul.list-basic-gallery")
        category_products = gallery.css("li small ::text").getall()
        # self.products.append({category: category_products})
        self.products += category_products
        self.logger.info(f"Products: {self.products}")
