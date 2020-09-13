import colorama
import scrapy


class AnwisSpider(scrapy.Spider):
    name = 'anwis'
    allowed_domains = ['anwis.pl']

    def __init__(self, *args, **kwargs):
        super(AnwisSpider, self).__init__(*args, **kwargs)
        self.start_url = "https://anwis.pl/"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        self.products += [
            x.strip()
            for x in response.css("div#nav-offer-oslony_montowane > ul > li > a::text").getall()
        ]

        self.products += [
            x.strip()
            for x in response.css(
                "div#nav-offer-oslony_montowane_na_zewnatrz_domu > ul > li > a::text"
            ).getall()
        ]

        self.products += [
            x.strip()
            for x in response.css("div#nav-offer-oslony_lodziowe > ul > li > a::text").getall()
        ]

        self.logger.info(f"Products: {self.products}")
