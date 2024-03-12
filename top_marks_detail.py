import json
from turtle import pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import os
import shutil
import csv
from PIL import Image, UnidentifiedImageError
import time


headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--ignore-certificate-errors')
options.add_argument("start-maximized") # // https://stackoverflow.com/a/26283818/1689770
options.add_argument("enable-automation")#  // https://stackoverflow.com/a/43840128/1689770
#options.add_argument("--headless")#  // only if you are ACTUALLY running headless
options.add_argument("--no-sandbox")# //https://stackoverflow.com/a/50725918/1689770
options.add_argument("--disable-dev-shm-usage")# //https://stackoverflow.com/a/50725918/1689770
options.add_argument("--disable-browser-side-navigation")# //https://stackoverflow.com/a/49123152/1689770
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")# //https://stackoverflow.com/a/43840128/1689770
options.add_argument("--enable-javascript")

#options.add_argument("--proxy-server=31.204.2.182:9142")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol:
    '''
})

summa = 0
black_list = []
black_model = []

file1 = open("black-list.txt", "r")
while True:
    # считываем строку
    line = file1.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    # прерываем цикл, если строка пустая
    if not line:
        break
    # выводим строку
    black_list.append(line)
#print(black_list)
# закрываем файл
file1.close

file1 = open("black-model.txt", "r")
while True:
    # считываем строку
    line = file1.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    # прерываем цикл, если строка пустая
    if not line:
        break
    # выводим строку
    black_model.append(line)
#print(black_list)
# закрываем файл
file1.close

marka_need_list = {}
model_need_list = {}       

marka_vxod = input("Какую марку будем парсить, выбирай из трех audi, bmw, mercedes - ")
num_vxod = input("на какой странице ты остановился, если начало жми 0 - ")
marka_vxod_in = "marka_" + marka_vxod
with open('zapchast_and_href.json', encoding="utf-8") as file:
    catalog = json.load(file)

for item_href_model, name_zap  in catalog.items():
    if marka_vxod_in in item_href_model:
        print(item_href_model)
        print(name_zap)
        marka = marka_vxod
        model = item_href_model[item_href_model.find("model")+6 : -1]
        print( marka,  model)
        i = 1
        item_href_page = item_href_model + "?ACTION=REWRITED3&FORM_DATA=" + item_href_model[item_href_model.find("zchbu")+6 : item_href_model.find("/marka")] + "%2Fmarka_" + item_href_model[item_href_model.find("/marka")+7 : item_href_model.find("/model")] + "%2Fmodel_" + item_href_model[item_href_model.find("/model_")+7 : -1] + "&PAGEN_1=" + str(i)
        print(item_href_page)
        item_href_page = "https://bamper.by/zchbu/zapchast_zashchita-arok-podkrylok/marka_audi/model_a1/?ACTION=REWRITED3&FORM_DATA=zapchast_zashchita-arok-podkrylok%2Fmarka_audi%2Fmodel_a1&PAGEN_1=1"
        req = requests.get(url=item_href_page, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'html.parser')
        href_part = soup.find_all("ul", class_="pagination")        
        #print(href_part)
        if "След." in str(href_part):
            href_part = str(href_part)
            #print(href_part)
            print("переходим на следующую")
            item_href_page = "https://bamper.by" + href_part[href_part.find("href=") + 6 : href_part.find(f">{int(i+1)}</a>") - 1]
            print(item_href_page, "вот это!")
            
        break

a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие - ")