import selenium
from selenium import webdriver
import os

brands = ["supreme"]

def main(): 
	driver_path = os.getcwd() + "/chromedriver"
	grailed_driver = webdriver.Chrome(executable_path=driver_path)
	stockx_driver = webdriver.Chrome(executable_path=driver_path)
	grailed_url = "https://www.grailed.com/designers/"
	stockx_url = "https://stockx.com/"
	stockx_driver.get(stockx_url)

	for i in range(len(brands)): 
		grailed_url = grailed_url + brands[i]
		grailed_driver.get(grailed_url)
		filters = grailed_driver.find_elements_by_class_name('instant-search-collapsible._collapsed')
		condition = filters[2]
		condition.click()
		new_box = grailed_driver.find_element_by_name('New/Never Worn')
		new_box.click()
		



main()