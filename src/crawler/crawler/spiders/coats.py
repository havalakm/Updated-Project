import colorama
import scrapy


class CoatsSpider(scrapy.Spider):
    name = 'coats'
    allowed_domains = ['coats.com']

    def __init__(self, *args, **kwargs):
        super(CoatsSpider, self).__init__(*args, **kwargs)
        self.start_url = "http://www.coats.com/it/Products"
        self.start_parse = self.parse_products
        self.products = kwargs["products"] if "products" in kwargs else []

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.start_parse)

    def parse_products(self, response):
        """ Parse products """
        print(f"\t{colorama.Fore.CYAN}Crawling: {response.url}")
        self.products += [
            x.strip()
            for x in response.css(
                "div.related-card.related-card--product.js-equalise h3.related-card__title ::text"
            ).getall()
        ]
        self.logger.info(f"Products: {self.products}")

        # Extract next link
        next_link = response.css(
            "button.pagination__button-next:not([disabled])::attr(formaction)"
        ).get()
        if next_link is not None:
            next_link = next_link.replace(" ", "%20")
            self.logger.info(f"Next link: {next_link}")
            yield response.follow(url=next_link, callback=self.parse_products)
