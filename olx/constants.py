BASE_URL = "https://www.olx.com"
RESULTS_PER_PAGE = 45
DB_NAME = "OLX_ITEMS"
FIELDS = ["_id","title","price","link","location","creation_date","seller"]
SEARCH_BAR_SELECTOR = 'input[placeholder="ابحث عن السيارات، الهواتف وأكثر..."]'
SEARCH_BUTTON_SELECTOR = "button._0db6bd2f.a3e390b5"
ITEMS_TITLE_SELECTOR = "div.a5112ca8"
ITEMS_PRICE_SELECTOR = "div._52497c97 > span"
ITEMS_LINK_SELECTOR = "div.a52608cc > a"
ITEMS_LOCATION_SELECTOR = 'span[aria-label="Location"]'
ITEMS_CREATION_DATE_SELECTOR = 'span[aria-label="Creation date"]'
ITEMS_SELLER_SELECTOR = 'div._1075545d._6caa7349._42f36e3b.d059c029 > span._261203a9._2e82a662'
NEXT_PAGE_BUTTON = 'div[title="التالي"]'
MESSAGE_BODY = "Hello,\nThis email is sent to you upon your request.\nYou'll find an attached csv file containing the data you are looking for,\nEnjoy!"
EMAIL_SUBJECT = "Scraping Results"
EMAIL_FROM = "scraping.results@gmail.com"
EMAIL_HOST = 'smtp.gmail.com' 
SMTP_PORT = 587