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
import sys
import time
import requests
from bs4 import BeautifulSoup
import os
import shutil
import csv
from PIL import Image, UnidentifiedImageError
import time
import ftplib
from telegram import Bot
from openpyxl import load_workbook


headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


first_page = "https://bamper.by/zapchast_pompa/77449-134065521_3/"
req = requests.get(url=first_page, headers=headers)
src = req.text
soup = BeautifulSoup(src, 'html.parser')
#print(soup)


info = "     "
info_obj = soup.find_all("span", class_="media-heading cut-h-375")
#print(info_obj)
for item_info in info_obj:
    info = str(item_info.text.replace("  ","").replace("\n",""))
    info = info.replace(","," ").replace('"',' ')
    info = info.replace("\r","").replace(';',"*#")
    info_lower = info.lower()
print(info_lower)