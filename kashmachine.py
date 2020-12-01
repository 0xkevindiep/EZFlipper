import selenium
from selenium import webdriver
import os

brands = ["supreme"]

def main(): 
	driver_path = os.getcwd() + "/chromedriver"
	driver = webdriver.Chrome(executable_path=driver_path)
	grailed_url = "https://www.grailed.com/designers/"
	for i in range(len(brands)): 
		url = grailed_url + brands[i]
		driver.get(url)
		filters = driver.find_elements_by_class_name('instant-search-collapsible._collapsed')
		condition = filters[2]
		condition.click()
		new_box = driver.find_element_by_name('New/Never Worn')
		new_box.click()
		


main()