from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sqlite3

def brands(driver, letters):
    url = 'https://www.wildberries.ru/brandlist/all'
    driver.get(url)
    time.sleep(5)

    items = driver.find_elements(By.CLASS_NAME, "brands-by-letter__item")
    for item in items:
        letter = item.find_element(By.TAG_NAME, "a").get_attribute('href')
        letters.append(letter)

    letters.pop(0)
    print(letters)

def scroll(driver):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)

        time.sleep(0.5)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.END)

def link_of_brands(driver, links_of_brands, letters):
    for url in letters:
        driver.get(url)
        time.sleep(5)

        scroll(driver)

        items = driver.find_elements(By.CLASS_NAME, "j-brand-catalog-link")
        for item in items:
            link_of_brand = item.find_element(By.TAG_NAME, "a").get_attribute('href')
            links_of_brands.append(link_of_brand)

    print(links_of_brands)

def links_of_product_cards(driver, links_of_brands, links):
    driver.get(links_of_brands)
    time.sleep(3)

    html = driver.find_element(By.TAG_NAME, 'html')
    while True:
        html.send_keys(Keys.END)
        items = driver.find_elements(By.CLASS_NAME, "product-card__wrapper")
        for item in items:
            link = item.find_element(By.CLASS_NAME, "j-card-link").get_attribute('href')
            links.append(link)

        try:
            next_page = driver.find_element(By.CLASS_NAME, "pagination__next")
            next_page.click()
            time.sleep(3)
        except:
            break

def info(driver, x, links):
    for link in links:
        driver.get(link)
        time.sleep(0.5)

        title = driver.find_element(By.XPATH, "//div[@class='product-page__header']//h1").text
        brand = driver.find_element(By.XPATH, "//div[@class='product-page__header']//a").text
        price = driver.find_element(By.CLASS_NAME, "price-block__final-price").text.replace(' ₽', '')
        article = driver.find_element(By.ID, "productNmId").text
        photo = driver.find_element(By.CLASS_NAME, "j-zoom-image").get_attribute('src')
        link = link

        x.append((title, brand, price, article, photo, link))

def save(x):
    conn = sqlite3.connect('DBwildberries.db')
    cursor = conn.cursor()

    cursor.executemany('INSERT INTO wildberries VALUES (?,?,?,?,?,?)', x)
    conn.commit()
    conn.close()

def parser():
    driver = webdriver.Chrome()

    letters = []
    brands(driver, letters)

    links_of_brands = []
    link_of_brands(driver, links_of_brands, letters)

    links = []
    links_of_product_cards(driver, links_of_brands, links)

    x = []
    info(driver, x, links)

    save(x)

    driver.close()

parser()