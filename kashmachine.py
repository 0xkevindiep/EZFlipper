import selenium
from selenium import webdriver
import os
import time

brands = ["supreme"]

# ADJUST MINIMUM PROFIT THRESHOLD
min_profit = 20.00

# ADJUST HOW NEW ITEMS ARE IN HOURS
max_time = 24

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

		

		
		


		


		




main()