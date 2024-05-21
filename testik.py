#Парсинг бампера для ссылок по маркам, моделям и годам, ничего лишнего

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
import ftplib


HOST = '171.25.166.53'
PORT = 3121
USER = 'Reppart'
PASSWORD = 'Nikitos21@Artem'


headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}








first_page = "https://bamper.by/zchbu/zapchast_kapot/marka_bmw/model_5f10f11gtf07/"



print(first_page)
req = requests.get(url=first_page, headers=headers)
src = req.text
soup_1 = BeautifulSoup(src, 'html.parser')
href_part = soup_1.find_all("div", class_="add-image")

#print(href_part)
for item in href_part:
    item = str(item) #replace("\n","").replace("\r",""))
    stroka_novya = item
    #print(item)
    #print(item)
    foto = " "
    version = "    "
    item = item[item.find("href")+7: item.find("target=") -2]
    #print(foto)
    href_to_zapchast = "https://bamper.by/" + item
    print(href_to_zapchast)
    number_href_reverse = item[::-1]
    number_href_reverse_second = number_href_reverse[1:]
    number_href_reverse = number_href_reverse_second[: number_href_reverse_second.find("/")]
    name_href = number_href_reverse[::-1]
    name_href = name_href.replace("*","_").replace('%','_')
    #print(name_href)
    num_provider = name_href[: name_href.find("-")]
    #print(num_provider)
    
    try:
        req = requests.get(url=href_to_zapchast, headers=headers)
        src = req.text

        soup = BeautifulSoup(src, 'html.parser')  
                        
        status = "б/у"
        order = "     "    
        info = "     "
        info_obj = soup.find_all("span", class_="media-heading cut-h-375")
        for item_info in info_obj:
            info = str(item_info.text.replace("  ","").replace("\n",""))
            info = info.replace(","," ").replace('"',' ')
            info = info.replace("\r","").replace(';',"*#")
            info_lower = info.lower()
            if "под заказ" in info_lower:
                order = "ПОД ЗАКАЗ"
        preorder = soup.find_all("div", class_="preorder ")
        #print(preorder)
        for item_preorder in preorder:
            if "под заказ" in item_preorder:
                order = "ПОД ЗАКАЗ"
        if "под заказ" in str(href_part):
            order = "ПОД ЗАКАЗ"   
        #print(order, "ОРДЕР ЗДЕСЬ")
        #print(info)
        #item = "новая з/ч"
        if "новая з/ч" in stroka_novya:
            status = "новая"   
        print(status, "СТАТУС")
        print()
        print()
        print()
                
                
                
    except Exception:
        print("какая-то хуйня с карточкой запчастей")

        


