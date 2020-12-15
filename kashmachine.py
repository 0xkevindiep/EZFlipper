import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import os
import time

# ADD/REMOVE DESIRED BRANDS
# BRANDS MUST BE ON GRAILED
brands = ["vlone"]

# ADJUST MINIMUM PROFIT THRESHOLD
min_profit = 20.00

# ADJUST MAX AGE OF ITEMS IN DAYS
max_age = 0.50

# ADJUST TO YOUR STOCKX TRANSACTION FEES
transaction_fee = 0.095

# PAYMENT PROCESSING FEE (USUALLY 3%)
processing_fee = 0.03

class GrailedItem: 
	def __init__(self, link, brand, name, color, size, price): 
		self.link = link
		self.brand = brand
		self.name = name
		self.color = color
		self.size = size
		self.price = price
		self.profit = -1

	def get_link(self): 
		return self.link

	def get_brand(self): 
		return self.brand

	def get_name(self): 
		return self.name

	def get_color(self): 
		return self.color

	def get_size(self): 
		return self.size

	def get_price(self): 
		return self.price

	def get_profit(self): 
		return self.profit

	def adjust_profit(self, profit): 
		self.profit = profit
		return self.profit

def main(): 
	driver_path = os.getcwd() + "/chromedriver"
	driver = webdriver.Chrome(executable_path=driver_path)
	grailed_url = "https://www.grailed.com/designers/"
	grailed_items = []
	# Go through list of brands and scrapes the data
	for i in range(len(brands)): 
		grailed_url = grailed_url + brands[i]
		driver.get(grailed_url)

		# filter items to be brand new
		filters = driver.find_elements_by_class_name('instant-search-collapsible._collapsed')
		condition = filters[2]
		condition.click()
		# checks if Grailed is requesting authentication after clicking an element
		authetication_xpath = "//div[@class=\"UsersAuthentication\"]"
		requesting_authentication = check_element_exists_xpath(driver, authetication_xpath)
		if (requesting_authentication): 
			# clicks off the screen and tries to filter the items again
			log_in_button = driver.find_element_by_link_text('Log in')
			ActionChains(driver).move_to_element_with_offset(log_in_button, 500, 0).click().perform()
			condition.click()
		new_box = driver.find_element_by_name('New/Never Worn')
		new_box.click()

		# sort items by new
		sort_select = driver.find_element_by_class_name('ais-SortBy-select')
		sort_select.click()
		sorts = driver.find_elements_by_class_name('ais-SortBy-option')
		new_sort = sorts[4]
		new_sort.click()
		time.sleep(1.5)

		# get all items up until max_age
		xpath = "//div[@class=\"feed-item\"]//span[@class=\"date-ago\"]"
		feed_ages = driver.find_elements_by_xpath(xpath)
		last_age = time_in_days(feed_ages[-1].text)
		last_height = driver.execute_script("return document.body.scrollHeight")
		while last_age < float(max_age): 
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(1.5)
			new_height = driver.execute_script("return document.body.scrollHeight")
			feed_ages = driver.find_elements_by_xpath(xpath)
			last_age = time_in_days(feed_ages[-1].text)
			if new_height == last_height or last_age >= float(max_age): 
				break
			last_height = new_height

		# get the item's brand, name, color, size, and price with shipping
		xpath = "//div[@class=\"feed-item\"]/a[@class=\"listing-item-link\"]"
		stale_links = driver.find_elements_by_xpath(xpath)
		links = []
		for stale_link in stale_links:
			links.append(stale_link.get_attribute('href'))
		for link in links: 
			driver.get(link)
			xpath = "//div[@class=\"-listing-designer-title-size\"]"
			listing_info = driver.find_element_by_xpath(xpath).text.splitlines()
			brand = listing_info[0]
			name = listing_info[1]
			size = parse_size(listing_info[2])
			color = ""
			if "Color" in listing_info[3]: 
				color = listing_info[3].lstrip('Color: ')
				if "Multi" in color: 
					color = ""
			list_price = driver.find_element_by_class_name('-price').text.lstrip('$')
			if ("," in list_price): 
				list_price = list_price.replace(",", "")
			shipping_price = driver.find_element_by_class_name('-shipping-cost').text.lstrip('+$')
			if ("," in shipping_price): 
				shipping_price = shipping_price.replace(",", "")
			price = int(list_price) + int(shipping_price)
			item = GrailedItem(link, brand, name, color, size, price)
			items.append(item)

	# Go on StockX to compare prices and find profitable items
	profitable_items = []
	stockx_url = "https://stockx.com/"
	driver.get(stockx_url)
	search_bar = driver.find_element_by_id('home-search')
	for item in grailed_items: 
		search_bar.send_keys(item.get_name())
		search_bar.send_keys(Keys.ENTER)

		time.sleep(1)
		stockx_results = driver.find_elements_by_class_name("tile.browse-tile.updated")
		# refine the search by adding brand and color
		if len(stockx_results) > 1: 
				brand_and_color = " " + item.get_brand() + " " + item.get_color()
				search_bar = driver.find_element_by_id('site-search')
				search_bar.send_keys(brand_and_color)
				search_bar.send_keys(Keys.ENTER)
				time.sleep(1)
				stockx_results = driver.find_elements_by_class_name('tile.browse-tile.updated')
		
		if len(stockx_results) > 0: 
			# click the most relevent item
			stockx_results[0].click()

			# select the size
			if item.get_size() != "": 
				exists = False
				while not exists: 
					exists = check_element_exists_class_name(driver, "select-control")
				size_button = driver.find_elements_by_class_name("select-control")[1]
				size_button.click()
				exists = False
				while not exists: 
					exists = check_element_exists_class_name(driver, "select-control")
				size_buttons = driver.find_elements_by_class_name("chakra-menu__menuitem")
				index = int(len(size_buttons) / 2)
				searching_size = True
				while searching_size: 
					if item.get_size() in size_buttons[index].text: 
						loading = True
						while loading: 
							try: 
								size_buttons[index].click()
								searching_size = False
								loading = False
							except ElementClickInterceptedException: 
								loading = True
					index += 1
					if index == len(size_buttons): 
						searching_size = False
			last_height = driver.execute_script("return document.body.scrollHeight")

			# scroll down to load average price data
			while True: 
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(1)
				new_height = driver.execute_script("return document.body.scrollHeight")
				if new_height == last_height: 
					break
				last_height = new_height

			# waits for average price data to load
			exists = False
			while not exists: 
				exists = check_element_exists_class_name(driver, "gauge-value")
			avg_price = driver.find_elements_by_class_name('gauge-value')[-1].text.lstrip('$')
			if ("," in avg_price): 
				avg_price = avg_price.replace(",", "")
			# calculates the estimated total profit
			avg_price = int(avg_price)
			selling_price = avg_price - ((avg_price * transaction_fee) + (avg_price * processing_fee))
			buying_price = item.get_price()
			profit = selling_price - buying_price
			item.adjust_profit(profit)
			if (profit > min_profit): 
				profitable_items.append(item)
		search_bar = driver.find_element_by_id('site-search')
		search_bar.clear()

	# sort the profitable items in descending order
	profitable_items.sort(reverse=True, key=sort_by_profit)

	index = 1
	print("PROFITABLE ITEMS\n")
	for item in profitable_items: 
		profit_description = str(index) + ". PROFIT: ~$" + str(item.get_profit())
		item_description = item.get_brand() + " " + item.get_name() + "\n" + item.get_link()
		print(profit_description)
		print(item_description + "\n")
		index += 1

# sorting function
def sort_by_profit(item): 
	return item.get_profit()
	
# checks if the string is a number
def is_number(s): 
	try: 
		float(s)
	except ValueError: 
		return False
	return True

# check if element exists using xpath
def check_element_exists_xpath(driver, xpath): 
	try: 
		driver.find_element_by_xpath(xpath)
	except NoSuchElementException:
		return False
	return True

# check if element exists using class name
def check_element_exists_class_name(driver, class_name): 
	try: 
		driver.find_element_by_class_name(class_name)
	except NoSuchElementException:
		return False
	return True

# converts time into hours
def time_in_days(age_text):
	index = 0
	c = age_text[index]
	while ord(c) < 49 or ord(c) > 57: 
		index += 1
		c = age_text[index]
	num = float(c)
	index += 2
	# it can either be years, months, days, hours, or minutes
	if age_text[index] == 'y':
		# convert years to days
		return num * 365.0
	elif age_text[index] == 'm': 
		if age_text[index + 1] == 'i':
			# convert minutes to days 
			return num / 1440.0
		else: 
			# convert months to days
			return num * 30.0
	elif age_text[index] == 'h':
		# convert hours to days
		return num / 24.0
	else: 
		# format already in days
		return num

def parse_size(size_text): 
	size_text = size_text.lstrip('Size: ')
	if "ONE SIZE" in size_text: 
		return ""
	if "US" in size_text: 
		size_text = size_text.lstrip('US ')
	result = ""
	index = 0
	while index < len(size_text) and size_text[index] != ' ': 
		result += size_text[index]
		index += 1
	return result

main()