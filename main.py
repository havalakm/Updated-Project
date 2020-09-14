"""
File:           main.py
Author:         Havala
Created on:     13/09/20, 4:25 PM
"""
import os
import json
import smtplib
from email.message import EmailMessage
from collections import defaultdict

import colorama

from src import SathualabCrawler
import socket

socket.getaddrinfo('localhost', 25)


def send_mail(to_addr, websites):
    """ Sending mail for mismatch is product hash """
    message = EmailMessage()
    message.set_content(f"Products in the following websites are changed: {', '.join(websites)}")
    message["Subject"] = "Product change notification"
    message["From"] = "juliuskoch12@gmail.com"
    message["To"] = to_addr

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("juliuskoch12@gmail.com", "veget@ble")
        server.send_message(message)


def main():
    """ Main function """
    crawler = SathualabCrawler()
    crawler.crawl()
    spider_product_hashes = crawler.spiders_products_hash.copy()
    current_dir = os.path.dirname(os.path.abspath("__file__"))
    data_dir = os.path.join(current_dir, "data")
    config_dir = os.path.join(current_dir, "config")
    current_hash_file = os.path.join(data_dir, "current_hash.json")
    reference_hash_file = os.path.join(data_dir, "reference_hash.json")
    config_file = os.path.join(config_dir, "config.json")

    print(f"{colorama.Fore.BLUE}Saving product hash to JSON file: {current_hash_file}")
    with open(current_hash_file, mode="w") as outfile:
        json.dump(spider_product_hashes, outfile)

    if not os.path.isfile(reference_hash_file):
        print(f"{colorama.Fore.RED}No reference hash file to compare. Exiting...")
        return None

    print(f"{colorama.Fore.BLUE}Comparing current hash with reference hash")
    # Read reference hash file if exists for comparison
    with open(reference_hash_file, mode="r") as infile:
        reference_hashes = json.load(infile)

    mismatch_spider = []
    for spider, hash in spider_product_hashes.items():
        if spider in reference_hashes:
            if hash != reference_hashes[spider]:
                print(f"{colorama.Fore.LIGHTMAGENTA_EX}Hash mismatch for {spider}")
                mismatch_spider.append(spider)
        else:
            print(f"{colorama.Fore.CYAN}{spider} hash doesn't found in reference hashes")

    if mismatch_spider:
        with open(config_file, mode="r") as infile:
            config_data = json.load(infile)

        spider_website_mapping = {}
        spider_mail_mapping = {}
        for mailing_addr, spiders in config_data.items():
            spider_website_mapping.update(spiders)
            spider_mail_mapping.update({key: mailing_addr for key in spiders.keys()})

        recipient = defaultdict(list)
        for spider in mismatch_spider:
            if spider in spider_mail_mapping:
                recipient[spider_mail_mapping[spider]].append(spider_website_mapping[spider])

        for key, value in recipient.items():
            send_mail(key, value)

    else:
        print(f"{colorama.Fore.GREEN}No differences found")


if __name__ == "__main__":
    main()
