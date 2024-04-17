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

input_url = input("Введи ссылку c бамперочка без фильтра по годам, без прайса -  ")
input_name = "foto"



folder_name =f"{input_name}_" + time.strftime('%Y-%m-%d')
if os.path.exists(folder_name):
    print("Папка уже есть")
else:
    os.mkdir(folder_name)

watermark = Image.open("moe.png")




req = requests.get(url=input_url, headers=headers)
src = req.text

soup = BeautifulSoup(src, 'html.parser')



foto_href = str(soup.find_all("div", class_="detail-image"))
#print(foto_href, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
foto = "https://bamper.by" + foto_href[foto_href.find('src=') + 5 : foto_href.find('"/>')]
print(foto, "ССЫЛКА НА ФОТОГРАФИИ!!!!!!!!!!!!!!!!")

if "nophoto_car.png" not in foto:
    img = requests.get(url=foto, headers=headers)
    img_option = open(f"{folder_name}/1.png", 'wb')
    img_option.write(img.content)
    img_option.close
    try:
        im = Image.open(f"{folder_name}/1.png")
        pixels = im.load()  # список с пикселями
        x, y = im.size  # ширина (x) и высота (y) изображения
        min_line_white = []
        n=0
        for j in range(y):
            white_pix = 0

            for m in range(x):
                # проверка чисто белых пикселей, для оттенков нужно использовать диапазоны
                if pixels[m, j] == (248,248,248):         # pixels[i, j][q] > 240  # для оттенков
                    white_pix += 1
            if white_pix == x:
                n += 1
            #print(white_pix, x, n)

            #print(white_pix)
            min_line_white.append(white_pix)
        left_border = int(min(min_line_white)/2)
        #print(left_border)
        im.crop(((left_border+15), n/2+20, (x-left_border-20), y-(n/2)-20)).save(f"{folder_name}/1.png", quality=95)




        foto = "http://171.25.166.53/~Reppart/reppart/"+ str(1) + ".png"
        img = Image.open(f"{folder_name}/1.png")
        #print(foto)
        #img = Image.open(f"fotku/{name_href}.png")    
        img.paste(watermark,(-272,-97), watermark)
        img.paste(watermark,(-230,1), watermark)
        img.save(f"{folder_name}/1.png", format="png")
        img_option.close
        #os.remove("img.png")
        #print(f"{name_href} - неверный формат или ерунда")
    except UnidentifiedImageError:
        foto = "Битая фотка"
        print("Битая фотка")
        foto = "http://171.25.166.53/~Reppart/reppart/"+ str(1) + ".png"
        #os.remove(f"{folder_name}/{name_href}.png")
else:
    foto = "Нет фото"
    print ("Нет фото")                   
a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие - ")
