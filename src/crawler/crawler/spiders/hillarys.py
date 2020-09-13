import colorama
import scrapy


class HillarysSpider(scrapy.Spider):
    name = 'hillarys'
    allowed_domains = ['hillarys.co.uk']
    start_urls = ['']

    def __init__(self, *args, **kwargs):
        super(HillarysSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://hillarys.co.uk/"
        self.start_parse = self.parse_products
        # List of dict where each dict has key as product category and value as list of products
        self.products = kwargs["products"] if "products" in kwargs else []
        self.products_to_extract = {
            "blinds": ["view - our blinds range", "view - room"],
            "curtains": ["view - room", "view - curtain types"],
            "shutters": ["view - our shutters range", "view - room"],
            "awnings": ["view - our awnings range"],
            "conservatory blinds": ["view - type"]
        }

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        all_product_menu = response.css(
            "li.site-navigation__item.site-navigation__item--first-level"
        )

        for menu in all_product_menu:
            data_ga_action_value = menu.css("a::attr(data-ga-action)").get()
            if data_ga_action_value in self.products_to_extract:
                sub_categories = menu.css(
                    "li.site-navigation__item.site-navigation__item--haschild"
                )
                sub_products = []
                for cat in sub_categories:
                    data_ga_label_value = cat.css("button::attr(data-ga-label)").get()
                    if data_ga_label_value in self.products_to_extract[data_ga_action_value]:
                        level2_products = cat.css(
                            'li.site-navigation__item a span[itemprop="name"]::text'
                        ).getall()
                        sub_products += level2_products

                        self.logger.info(f"{data_ga_action_value} | {data_ga_label_value}: "
                                         f"{level2_products}")

                # self.products.append({data_ga_action_value: sub_products})
                self.products += sub_products

        self.logger.info(f"Products: {self.products}")
