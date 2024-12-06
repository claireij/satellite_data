from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "Users/claire/downloads/selenium"}

options.add_experimental_option("prefs",prefs)

service = Service(executable_path = "./chromedriver", chrome_options=options)

driver = webdriver.Chrome(service =service)

driver.get("http://localhost:3000/")

download_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
download_button.click()

time.sleep(20)

driver.quit()