from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


import attributes as Att
import lore_attributes as Lore


def get_urls():
    urls = []

    for row in rows:
        url = row.find_element(By.XPATH, ".//a").get_attribute('href')
        print(url)
        urls.append(url)

    return urls

def normalize_champ_name(name):
    name = name.replace('_', '')
    name = name.replace('.', '')

    name = name.replace("'", ' ')
    name = name.replace('%27', ' ')

    # names with "'" are written with only the first letter as uppercase
    # Ex: Cho'Gath = Chogath
    # Except for K'Sante, as it is written as KSante
    if name.find(' ') != -1:
        names = name.split()
        if len(names[0]) != 1:
            names[1] = names[1].lower()

        name = ''.join(names)

    # for some reason Kled is written as Kled1
    if name == 'Kled':
        name = 'Kled1'

    return name

def get_champ_name_from_url():
    # https://leagueoflegends.fandom.com/wiki/CHAMP_NAME/LoL
    url = driver.current_url
    str1, str2 = '/wiki/', '/LoL'
    lo, hi = url.find(str1), url.find(str2)

    name = url[lo+len(str1) : hi]
    
    return normalize_champ_name(name)

def go_to_champ_page(url):
    trying = 0
    while trying < 5:
        try:
            driver.get(url)
            trying += 1
        except:
            sleep(5)

    champ_name = get_champ_name_from_url()
    print(champ_name)

    # wait load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, f'Health_{champ_name}')))

    return champ_name

def go_to_lore_page(url):
    trying = 0
    while trying < 5:
        try:
            driver.get(url[0:len(url)-4])
            trying = 5
        except:
            sleep(5)
            trying += 1

    # wait load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@role, 'region')]")))


def get_by_id(champ_name, dict):
    for name, id in Att.search_by_id.items():
        try:
            value = driver.find_element(By.ID, f'{id}_{champ_name}')
            dict[name] = value.text
        except NoSuchElementException:
            dict[name] = None

    return dict

def get_by_data_source(dict):
    for name, txt in Att.search_by_data_source.items():
        try:
            row = driver.find_element(By.XPATH, f"//*[contains(@data-source, '{txt}')]")
            div = row.find_element(By.XPATH, ".//div")
            dict[name] = div.text.split()

        except NoSuchElementException as e:
            dict[name] = None
            print(e)

    return dict

def get_crit_damage(dict):
    for name, txt in Att.search_crit_damage.items():
        try:
            row = driver.find_element(By.XPATH, f"//*[contains(@data-source, '{txt}')]")
            dict[name] = row.text.split()[-1]

        except NoSuchElementException as e:
            dict[name] = None
            print(e)

    return dict

def get_store_price(dict):
    try:
        row = driver.find_element(By.XPATH, f"//*[contains(@data-source, 'cost')]")
        div = row.find_element(By.XPATH, ".//div")
        anchors = div.find_elements(By.XPATH, ".//a")
        costs = [anchors[1].text, anchors[3].text]

        for i, key in enumerate(Att.search_store_price):
                dict[key] = costs[i]

    except NoSuchElementException as e:
        for i, key in enumerate(Att.search_store_price):
            dict[key] = None
        
        print(e)

    return dict

def get_champ_attributes(champ_name, atts):
    atts = get_by_id(champ_name, atts)
    atts = get_by_data_source(atts)
    atts = get_crit_damage(atts)
    atts = get_store_price(atts)
    # atts = ...
    
    return atts

def get_lore_by_data_source(dict):
    for name, txt in Lore.search_by_data_source.items():
        try:
            row = driver.find_element(By.XPATH, f"//*[contains(@data-source, '{txt}')]")

            # can either be a list (ul html element) or a single element (div)
            ul = row.find_elements(By.XPATH, ".//ul/li")

            if len(ul) == 0:
                div = row.find_element(By.XPATH, ".//div")
                dict[name] = div.text
                continue

            lis = []
            for li in ul:
                lis.append(li.text)

            dict[name] = lis
            

        except NoSuchElementException as e:
            dict[name] = None
            print(e)

    return dict

def filter_quote(og):
    index = og[1:].find('"')
    return og[1:index+1]

def get_quote(dict):
    for name, txt in Lore.search_by_class.items():
        try:
            table = driver.find_element(By.CLASS_NAME, f"{txt}")
            tds = table.find_elements(By.XPATH, ".//td")
            dict[name] = filter_quote(tds[1].text)

        except NoSuchElementException as e:
            dict[name] = None
            print(e)

    return dict

def get_lore_attributes(atts):
    atts = get_lore_by_data_source(atts)
    atts = get_quote(atts)
    

    return atts

def get_attributes(champ_name, url):
    atts = {}
    atts = get_champ_attributes(champ_name, atts)
    
    try:
        go_to_lore_page(url)
        atts = get_lore_attributes(atts)

    except TimeoutException as e:
        print(e)
        

    print(atts)
    return atts


def search_champ(url):
    # navigate directly to champ page
    try:
        champ_name = go_to_champ_page(url)
        get_attributes(champ_name, url)

    except TimeoutException as e:
        print(e)

def search_champs(urls):
    for url in urls:
        search_champ(url)
        


DRIVER_PATH = '/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument("--disable-cookies")
# options.add_argument('--headless')

# Go to landing page
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
driver.get('https://leagueoflegends.fandom.com/wiki/List_of_champions')

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@data-tracking-opt-in-accept, 'true')]")))

cookie = driver.find_element(By.XPATH, "//*[contains(@data-tracking-opt-in-accept, 'true')]").click()

driver.set_page_load_timeout(20)

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