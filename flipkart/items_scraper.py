from xPaths import *
import re
from flipkart.items import FlipkartItem


def extract_top_stories_footer_divs(response):
    top_stories_footer_divs = response.xpath(TOP_STORIES_DIVS)
    top_stories = {}
    for div in top_stories_footer_divs:
        main_category = div.css("span._2oyLgr::text").get()
        items_names = div.css(
            "a._3CuAg8::text").getall()
        items_urls = [response.urljoin(url) for url in div.css(
            "a._3CuAg8::attr(href)").getall()]
        actual_categories = list(zip(items_names, items_urls))
        top_stories[main_category] = actual_categories

    return top_stories


def extract_home_page_offers_link(response):
    all_link_containers = response.xpath(
        HOME_PAGE_OFFERS)
    headings = all_link_containers.css("h2._2cAig-::text").getall()
    anchors = all_link_containers.css(
        "div._30kJiF a._2KpZ6l._3dESVI::attr(href)").getall()
    anchors = [response.urljoin(url) for url in anchors]
    home_page_top_offers = list(zip(headings, anchors))
    return home_page_top_offers


def extract_category_list_descriptions(response):

    # this may contain the category lists, or inside it may contain other items!
    all_categories_container_divs = response.xpath(
        EACH_CATEGORY_LIST_HOME_PAGE)
    links = all_categories_container_divs.css("a._6WQwDJ::attr(href)").getall()
    links = [response.urljoin(url) for url in links]
    return links


def extract_item_list_category(response):
    all_items_desc_divs = response.xpath(
        EACH_ITEM_LIST_CATEGORY)
    items_links = list(set([response.urljoin(url) for url in all_items_desc_divs.css(
        "a ::attr(href)").getall()]))
    return items_links


def extract_item_attributes(response):
    item = FlipkartItem()

    image_background_pattern = re.compile(
        r"background-image:url\((.*)\)", re.I)
    images_pattern = [re.search(image_background_pattern, x) for x in response.xpath(
        ITEM_IMAGES).css("::attr(style)").getall()]
    images = [img.group(1) for img in images_pattern]
    name = " ".join([x
                     for x in response.css(ITEM_FEATURE_NAMES).getall()])
    improved_price = response.css(NEW_IMPROVED_ITEM_PRICE).get()
    old_price = "".join(response.css(OLD_ITEM_PRICE).getall())
    discount_rate = " ".join(response.css(
        ITEM_DISCOUNT).getall())
    rating = response.css(ITEM_RATING).get()
    reviews_rating_total = " ".join(
        [x for x in response.css(ITEM_TOTAL_RATING_REVIEWS).getall()])
    item_services = [x for x in response.css(
        ITEM_SERVICES).getall() if not x == "?"]
    item_seller = response.css(ITEM_SELLER_CONTAINER).css(
        "span span::text").get()
    item_seller_rating = response.css(
        ITEM_SELLER_CONTAINER).css("span div._3LWZlK._1D-8OL::text").get()

    item_specifications = response.css(ITEM_SPECIFICATION)
    item_specs = []
    for item_spec_detail in item_specifications:
        detail = {}
        item_spec_label = item_spec_detail.css(
            "td.col.col-3-12 ::text").get()
        item_spec_info = item_spec_detail.css(
            "td.col.col-9-12 ::text").get()
        detail[item_spec_label] = item_spec_info
        item_specs.append(detail)

    item_description = response.css(ITEM_DESCRIPTION)
    item_details = []
    for item_spec_detail in item_description:
        detail = {}
        item_spec_label = item_spec_detail.css(
            "div.col.col-3-12._2H87wv::text").get()
        item_spec_info = item_spec_detail.css(
            "div.col.col-9-12._2vZqPX::text").get()
        detail[item_spec_label] = item_spec_info
        item_details.append(detail)

    reviews = []
    if item_details:
        for review_container in response.css(ITEM_REVIEWS):
            each_review = {}
            rating = review_container.css("._3LWZlK._1BLPMq::text").get()
            main_comment = review_container.css("._6K-7Co::text").get()
            each_review["rating"] = rating
            each_review["comment"] = main_comment
            reviews.append(each_review)
    else:
        for review_container in response.css(ITEM_REVIEWS):
            each_review = {}
            rating = review_container.css("._3LWZlK._1BLPMq::text").get()
            main_comment = review_container.css("p._2-N8zT::text").get()
            other_comment = review_container.css(
                'div.t-ZTKy div::text').get()
            each_review["rating"] = rating
            each_review["comment"] = main_comment
            each_review["more_comment"] = other_comment
            reviews.append(each_review)

    item_category = [x.css("::text").get()
                     for x in response.css(ITEM_CATEGORY)]

    item_category = item_category[1:]

    offers_container = response.css(ITEM_OFFERS)
    offers = []
    for offer_detail in offers_container:
        offer = {}
        offer_name = offer_detail.css("span.u8dYXW::text").get()
        offer_actual = offer_detail.css("span:not(.u8dYXW)::text").get()
        offer[offer_name] = offer_actual
        offers.append(offer)

    seller = {
        "name": item_seller,
        "rating": item_seller_rating
    },

    item.url = response.url
    item.images = images
    item.name = name
    item.improved_price = improved_price
    item.old_price = old_price
    item.discount_rate = discount_rate
    item.rating = rating
    item.reviews_rating_total = reviews_rating_total
    item.services = item_services
    item.seller = seller
    item.details = item_details
    item.specs = item_specs
    item.reviews = reviews
    item.offers = offers
    item.category = item_category
    return item
