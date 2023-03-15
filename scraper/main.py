from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import attributes as Att
import lore_attributes as Lore


def get_urls():
    urls = []

    for row in rows:
        url = row.find_element(By.XPATH, ".//a").get_attribute('href')
        print(url)
        urls.append(url)

    return urls

def get_champ_name_from_url():
    # https://leagueoflegends.fandom.com/wiki/CHAMP_NAME/LoL
    url = driver.current_url
    str1, str2 = '/wiki/', '/LoL'
    lo, hi = url.find(str1), url.find(str2)

    name = url[lo+len(str1) : hi]
    return name

def go_to_champ_page(url):
    # click champ name
    driver.get(url)

    champ_name = get_champ_name_from_url()

    # wait load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, f'Health_{champ_name}')))

    return champ_name

def get_by_id(champ_name, dict):
    for name, id in Att.search_by_id.items():
        try:
            value = driver.find_element(By.ID, f'{id}_{champ_name}')
            dict[name] = value.text
        except NoSuchElementException:
            dict[name] = None

    return dict

def get_champ_attributes(champ_name):
    atts = {}
    atts = get_by_id(champ_name, atts)
    # atts = get_by_text()
    # atts = ...
    print(atts)

def search_champ(url):
    # navigate directly to champ page
    champ_name = go_to_champ_page(url)
    get_champ_attributes(champ_name)


def search_champs(urls):
    for url in urls:
        search_champ(url)
        


DRIVER_PATH = '/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument("--disable-cookies")

# Go to landing page
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
driver.get('https://leagueoflegends.fandom.com/wiki/List_of_champions')

# Locate the table element
table = driver.find_element(By.CLASS_NAME, "article-table")

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//tbody//tr")))

# Find length of table (number of champs)
rows = table.find_elements(By.XPATH, ".//tbody//tr")

urls = get_urls()

search_champs(urls)

# Close the driver
driver.quit()