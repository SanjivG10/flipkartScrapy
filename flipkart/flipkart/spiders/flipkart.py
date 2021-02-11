import scrapy
from scrapy_splash import SplashRequest
from xPaths import NAVBAR_CATEGORIES
from items_scraper import *
from lua import scroll

import subprocess


def copy2clip(txt):
    cmd = 'echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)


class QuotesSpider(scrapy.Spider):
    name = "flipkart"

    def start_requests(self):
        urls = ['https://www.flipkart.com/']

        for url in urls:
            yield SplashRequest(url, self.parse, args={'wait': 1, 'url': url, 'lua_source': scroll, 'scroll_number': 5, 'scroll_wait': 1}, endpoint='execute')

    def parse(self, response):
        navbar_categories = response.xpath(NAVBAR_CATEGORIES).getall()
        top_stories = extract_top_stories_footer_divs(
            response)

        home_page_top_offers = extract_home_page_offers_link(
            response)

        for offer_type, offer_link in home_page_top_offers:
            yield SplashRequest(offer_link, self.parse_category_list, args={'wait': 1, 'url': offer_link, 'lua_source': scroll, 'scroll_number': 1, 'scroll_wait': 0.5}, endpoint='execute', meta={"category": offer_type})
            break

    # after going inside every view all link here!
    def parse_category_list(self, response):
        all_category_list_hrefs = extract_category_list_descriptions(
            response)

        category = response.meta.get("category")

        for each_category_href in all_category_list_hrefs[:1]:
            yield SplashRequest(each_category_href, self.parse_each_category, args={'wait': 2, 'url': each_category_href, 'lua_source': scroll, 'scroll_number': 5, 'scroll_wait': 0.5}, endpoint='execute', meta={"category": category})

    def parse_each_category(self, response):
        item_hrefs = extract_item_list_category(
            response)

        category = response.meta.get("category")

        if not item_hrefs:
            # print("NOTHING HAPPENED => It still has more category on itself! ")
            response.meta["category"] = category
            all_category_list_hrefs = extract_category_list_descriptions(
                response)

            category = response.meta.get("category")
            # now we need to go through each item inside all_items_list_hrefs
            for each_category_href in all_category_list_hrefs[:1]:
                yield SplashRequest(each_category_href, self.parse_each_category, args={'wait': 2, 'url': each_category_href, 'lua_source': scroll, 'scroll_number': 5, 'scroll_wait': 0.5}, endpoint='execute', meta={"category": category})
                break
        else:
            # lets parse every item url now!!
            for index, each_item_href in enumerate(item_hrefs):
                yield SplashRequest(each_item_href, self.parse_each_item, args={'wait': 1, 'url': each_item_href, 'lua_source': scroll, 'scroll_number': 1, 'scroll_wait': 0.5}, endpoint='execute')
                if index >= 10:
                    break

    def parse_each_item(self, response):
        # this is where we yield product attribs!
        yield extract_item_attributes(response)
