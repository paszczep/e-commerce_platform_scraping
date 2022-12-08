from selenium import webdriver
# import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utility import unique_list, write_to_csv_file
# from time import sleep


def try_except(func, *args):
    try:
        val = func(*args)
        return val
    except NoSuchElementException:
        return None


def get_product_group(group_driver):
    product_selector = ".meqh_en.m6ax_n4.msa3_z4"
    product_group = group_driver.find_elements(By.CSS_SELECTOR, product_selector)
    product_group = [el.text for el in product_group]
    return product_group


def get_shop_url(shop_driver):
    soup = BeautifulSoup(shop_driver.page_source, 'html.parser')
    all_links = soup.find_all('a', href=True)
    shop_links = [link['href'] for link in all_links if '/sklep' in link['href']]
    try:
        shop_link = unique_list(shop_links)[0]
    except IndexError:
        return None
    return shop_link


def get_reviews(reviews_driver):
    reviews_element_xpath = "//a[@href='#productReviews']"
    reviews_element = reviews_driver.find_element(By.XPATH, reviews_element_xpath).text
    return reviews_element


def get_price(price_driver):
    price_xpath = "//meta[@itemprop='price']"
    price_value = price_driver.find_element(By.XPATH, price_xpath).get_attribute('content')
    return price_value


def get_bought(bought_driver):
    bought_selector = ".mp0t_0a.mqu1_21.mli8_k4.mgn2_13.mgmw_ag.mp4t_8"
    bought_element = bought_driver.find_element(By.CSS_SELECTOR, bought_selector).text
    if 'hit' in bought_element:
        bought_element = bought_element[3:]
    return bought_element


def get_title(title_driver):
    title_classes = ".mp4t_0.mryx_0.mj7a_4._77895_1qhyc.mp0t_ji.m9qz_yo.munh_0.m3h2_0.mqu1_1j.mgmw_wo.mgn2_21.mgn2_25_s"
    title_element = title_driver.find_element(By.CSS_SELECTOR, title_classes)
    return title_element.text


def get_offer_info(offer_driver: webdriver, offer_url: str):
    offer_driver.get(offer_url)
    offer_driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.ENTER)
    offer_title = get_title(offer_driver)
    buys_number = try_except(get_bought, offer_driver)
    product_price = try_except(get_price, offer_driver)
    reviews = try_except(get_reviews, offer_driver)
    seller_url = try_except(get_shop_url, offer_driver)
    product_group = get_product_group(offer_driver)
    info_list = [offer_url, offer_title, buys_number, product_price, reviews, seller_url, product_group]
    return info_list


def try_captcha_except(func, *args):
    try:
        value = func(*args)
        return value
    except NoSuchElementException:
        what_next = input("'Enter' to continue, input to skip ")
        if not bool(what_next):
            value = try_captcha_except(func, *args)
            return value


def write_data_from_listing_page(page_driver: webdriver):
    listing_source = page_driver.page_source
    soup = BeautifulSoup(listing_source, 'html.parser')
    all_hrefs = soup.find_all('a', href=True)
    all_links = [link['href'] for link in all_hrefs if '/oferta/' in link['href']][:3]
    all_links = unique_list(all_links)
    body = page_driver.find_element(By.CSS_SELECTOR, 'body')
    body.send_keys(Keys.ENTER)
    data_rows = []
    for link in all_links:
        data_row = try_captcha_except(get_offer_info, page_driver, link)
        data_rows.append(data_row)
    write_to_csv_file(data_rows)

