import selenium
from selenium import webdriver
import os

def main(): 
	
	driver_path = os.getcwd() + "/chromedriver"
	driver = webdriver.Chrome(executable_path=driver_path)
	driver.get('https://www.grailed.com/')

main()