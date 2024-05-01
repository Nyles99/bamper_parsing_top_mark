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


item_href_page = "https://bamper.by/zapchast_shleyf-rulya/9676-108946063/"


req = requests.get(url=item_href_page, headers=headers)
print(req)
src = req.text
soup = BeautifulSoup(src, 'html.parser')
num_obj = soup.find_all("span", class_="media-heading cut-h-65")
print(num_obj)
for item_num in num_obj:
    num_zap = str(item_num.text).replace("  ","").replace('"',"")
    num_zap = num_zap.replace(",","").replace("\n","")
    num_zap = num_zap.replace("далее","").replace(';',"*#")
"""print(num_zap, "Номер запчасти")
all_num_zap = num_zap    
list_num_zap = num_zap.split()
print(list_num_zap, "Список номеров")"""
#print(num_zap, "Номер запчасти")
one_num_zap = num_zap[ : num_zap.find(' ')]
num_zap = num_zap.rstrip().replace(" ","; ")
print(len(num_zap))
print(len(one_num_zap))
if (int(len(num_zap)) - int(len(one_num_zap))) == 1:
    one_num_zap = num_zap
print(num_zap)
print(one_num_zap)

a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие - ")
