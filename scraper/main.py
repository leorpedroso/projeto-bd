from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
webdriver_service = Service(executable_path="../chromedriver/chromedriver")
driver = webdriver.Chrome(service=webdriver_service)


driver.get("https://leagueoflegends.fandom.com/wiki/List_of_champions")

input()

