from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from offer import write_data_from_listing_page
from time import sleep


platform_url = 'https://allegro.pl/'
search_phrase = 'french press'

driver = webdriver.Firefox()

driver.get(platform_url)
driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.ENTER)

searchbar_xpath = "//input[@placeholder='czego szukasz?']"
searchbar = driver.find_element(By.XPATH, searchbar_xpath)
searchbar.send_keys(search_phrase)
searchbar.send_keys(Keys.ENTER)
sleep(3)
body = driver.find_element(By.CSS_SELECTOR, 'body')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
write_data_from_listing_page(driver)
for page_number in range(2, 51):
    url_str = f"{platform_url}/listing?string={search_phrase}&p={str(page_number)}"
    driver.get(url_str)
    if page_number == 1:
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.ENTER)
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    write_data_from_listing_page(driver)
