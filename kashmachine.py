import selenium
from selenium import webdriver
import os
import time

brands = ["supreme"]

# ADJUST MINIMUM PROFIT THRESHOLD
min_profit = 20.00

# ADJUST HOW NEW ITEMS ARE IN HOURS
max_age = 24.00

class GrailedItem: 
	def __init__(self, brand, name, color, size, price): 
		self.brand = brand
		self.name = name
		self.color = color
		self.size = size
		self.price = price

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

def main(): 
	driver_path = os.getcwd() + "/chromedriver"
	grailed_driver = webdriver.Chrome(executable_path=driver_path)
	# stockx_driver = webdriver.Chrome(executable_path=driver_path)
	grailed_url = "https://www.grailed.com/designers/"
	stockx_url = "https://stockx.com/"
	# stockx_driver.get(stockx_url)

	for i in range(len(brands)): 
		grailed_url = grailed_url + brands[i]
		grailed_driver.get(grailed_url)

		# filter items to be brand new
		filters = grailed_driver.find_elements_by_class_name('instant-search-collapsible._collapsed')
		condition = filters[2]
		condition.click()
		new_box = grailed_driver.find_element_by_name('New/Never Worn')
		new_box.click()

		# sort items by new
		sort_select = grailed_driver.find_element_by_class_name('ais-SortBy-select')
		sort_select.click()
		sorts = grailed_driver.find_elements_by_class_name('ais-SortBy-option')
		new_sort = sorts[4]
		new_sort.click()

		# get all items up until max_time
		xpath = "//div[@class=\"feed-item\"]//span[@class=\"date-ago\"]"
		feed_ages = grailed_driver.find_elements_by_xpath(xpath)
		last_age = time_in_hours(feed_ages[-1].text)
		last_height = grailed_driver.execute_script("return document.body.scrollHeight")
		while last_age < max_age: 
			grailed_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(1.5)
			new_height = grailed_driver.execute_script("return document.body.scrollHeight")
			feed_ages = grailed_driver.find_elements_by_xpath(xpath)
			last_age = time_in_hours(feed_ages[-1].text)
			if new_height == last_height or last_age >= max_age: 
				break
			last_height = new_height

		# get the item's brand, name, color, size, and price with shipping
		xpath = "//div[@class=\"feed-item\"]/a[@class=\"listing-item-link\"]"
		stale_links = grailed_driver.find_elements_by_xpath(xpath)
		links = []
		for stale_link in stale_links:
			links.append(stale_link.get_attribute('href'))

		for link in links: 
			grailed_driver.get(link)


		

# converts time into hours
def time_in_hours(age_text):
	index = 0
	c = age_text[index]
	while ord(c) < 49 or ord(c) > 57: 
		index += 1
		c = age_text[index]
	num = float(c)
	index += 2
	# it can either be years, months, days, hours, or minutes
	if age_text[index] == 'y':
		# convert years to hours
		return num * 8760.0
	elif age_text[index] == 'm': 
		if age_text[index + 1] == 'i':
			# convert minutes to hours 
			return num / 60.0
		else: 
			# convert months to hours
			return num * 730.001
	elif age_text[index] == 'd':
		# convert days to hours
		return num * 24.0
	else: 
		# format already in hours
		return num



main()