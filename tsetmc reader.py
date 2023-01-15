#!/usr/bin/env python
# coding: utf-8

# ## Imports

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import datetime;


# ## Constants

MAIN_URL = "http://main.tsetmc.com/MsgTop"
ROW_CLASS = "ag-row"
CELL_CLASS = "ag-cell"
CONTAINER_CLASS = "ag-center-cols-clipper"
CHROME_DRIVER = 'D:\ChromeDriver\chromedriver.exe'
CSV_PATH = 'D:/tsetmc.csv'


# ## Functions

def create_browser(webdriver_path):
    #create a selenium object that mimics the browser
    browser_options = Options()
    #headless tag created an invisible browser
    browser_options.add_argument("--headless")
    browser_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(webdriver_path, options=browser_options)
    print("Done Creating Browser")
    return browser

def scrollDown(driver):
    for i in range(2):
            driver.execute_script("window.scrollBy(0,500)")
            time.sleep(2)

def get_url(url):
    browser = create_browser(CHROME_DRIVER) #DON'T FORGET TO CHANGE THIS AS YOUR DIRECTORY
    browser.get(url)
    scrollDown(browser)
    page_html = browser.page_source
    return page_html

def get_cells(text):
    result = []
    
    soup = BeautifulSoup(text,features="html.parser")
    container = soup.find('div', class_ = CONTAINER_CLASS)
    rows = container.find_all('div', class_ = ROW_CLASS)
    for row in rows:
        cells = row.find_all('div', class_ = CELL_CLASS)
        result.append(list(cells)[2].text)
    return result

def create_csv(cells, path):
    f = open(path, "w", encoding='utf-8-sig')
    for cell in cells:
        prant = ' '
        if (cell.find('(') >= 0) :
            prant = cell[cell.find("(")+1:cell.find(")")]
        rest = cell.replace(prant, '').replace('-','').replace(',','').replace('\n','').replace('  ', ' ').replace('\t', '').replace('()','-')
        f.write(prant + ',' + rest + '\n')
    f.close()
    

# ## Main

while True :
    ct = datetime.datetime.now().strftime("%d%m%y-%H%M%S")
    print ('starting at: ', ct)
    
    url_html = get_url(MAIN_URL)
    cells = get_cells(url_html)
    path = CSV_PATH.replace('.csv','') + ' - ' + ct + '.csv'
    create_csv(cells, path)
    print ('completed waiting 30 sec')
    time.sleep(30)
    

