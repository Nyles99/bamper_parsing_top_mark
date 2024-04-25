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


"""headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
proxy = (input("Введи прокси в формате Fyq9HlP0zQLj4o:Nylesszpg@46.8.158.109:54376 - "))
proxies = {
    'http': f'{proxy}',
    'https': f'{proxy}'
}


item_href_page = "https://bamper.by/zchbu/zapchast_bryzgovik/marka_volkswagen/model_amarok/?ACTION=REWRITED3&FORM_DATA=zapchast_bryzgovik%2Fmarka_volkswagen%2Fmodel_amarok&PAGEN_1=1"


req = requests.get(url=item_href_page, headers=headers, proxies=proxies)
src = req.text
soup_1 = BeautifulSoup(src, 'html.parser')
href_part = soup_1.find_all("div", class_="add-image")
print(href_part,"Здесь должна быть ссылка на запчасть!")"""
cculka = []       
file2 = open(f"ot30000.txt", "r")
while True:
    # считываем строку
    line = file2.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    # прерываем цикл, если строка пустая
    if not line:
        break
    # выводим строку
    cculka.append(line)
#print(black_list)
# закрываем файл
file2.close

for url in cculka:
    pricing = int(url[-1: ])
    url = url[ : -1]
    print(pricing, url)
    if pricing == 4:
        sum = pricing + 1
        print(sum)
     
    



    

            
        

a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие - ")
