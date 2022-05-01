from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from .constants import *
import math
import re

class Olx(webdriver.Chrome):
    def __init__(self, silent_client=False):
        self.items_dict_list = []
        if silent_client != False:
            op = webdriver.ChromeOptions()
            op.add_argument('headless')
            super().__init__(ChromeDriverManager().install(), options=op)
        else:
            super().__init__(ChromeDriverManager().install())

    def open_homepage(self):
        self.get(BASE_URL)

    def search_query(self,query):
        self.implicitly_wait(5)
        search_bar = self.find_element(by=By.CSS_SELECTOR, value=SEARCH_BAR_SELECTOR)
        search_bar.send_keys(query)
        search_button = self.find_element(by=By.CSS_SELECTOR, value=SEARCH_BUTTON_SELECTOR)
        search_button.click()
    
    def get_sellers(self, links):
        items_seller = []
        new_driver = Olx(silent_client=True)
        for link in links:
            new_driver.get(link)
            new_driver.implicitly_wait(5)
            item_seller = new_driver.find_element(by=By.CSS_SELECTOR,value=ITEMS_SELLER_SELECTOR).text
            items_seller.append(item_seller)
        return items_seller

    def get_page_items_data(self, results_count=RESULTS_PER_PAGE):
        items_title = [element.text for element in self.find_elements(by=By.CSS_SELECTOR, value=ITEMS_TITLE_SELECTOR)]
        items_price = [element.text for element in self.find_elements(by=By.CSS_SELECTOR, value=ITEMS_PRICE_SELECTOR)]
        items_link = [element.get_attribute('href') for element in self.find_elements(by=By.CSS_SELECTOR, value=ITEMS_LINK_SELECTOR)]
        items_location = [element.text.replace("•","") for element in self.find_elements(by=By.CSS_SELECTOR, value = ITEMS_LOCATION_SELECTOR)]
        items_creation_date = [element.text for element in self.find_elements(by=By.CSS_SELECTOR, value=ITEMS_CREATION_DATE_SELECTOR)]
        items_seller = self.get_sellers(items_link)
        for i in range(results_count):
            temp_dict = {
                "title": items_title[i],
                "price": int(re.sub('\D','',items_price[i])),
                "link": items_link[i],
                "location": items_location[i],
                "creation_date": items_creation_date[i],
                "seller": items_seller[i]
            }
            self.items_dict_list.append(temp_dict)

    def next_page(self):
        next_page_btn = self.find_element(by=By.CSS_SELECTOR,value=NEXT_PAGE_BUTTON)
        next_page_btn.click()

    @staticmethod
    def scrap_items(query,results_count):
        with Olx(silent_client=True) as olx:
            olx.open_homepage()
            olx.search_query(query)
            needed_pages = math.ceil(results_count / RESULTS_PER_PAGE)
            items_in_last_page = results_count % RESULTS_PER_PAGE
            for i in range(needed_pages):
                if needed_pages - i == 1 and items_in_last_page != 0:
                    olx.get_page_items_data(results_count=items_in_last_page)
                else:
                    olx.get_page_items_data()
                    olx.next_page()
            return olx.items_dict_list


