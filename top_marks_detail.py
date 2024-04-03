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

marka_vxod = input("Какую марку будем парсить, выбирай из трех audi, bmw, mercedes или volkswagen - ")
num_vxod = input("на какой странице ты остановился, если начало жми 0 - ")
marka_vxod_in = "marka_" + marka_vxod

folder_name =f"{marka_vxod}_" + time.strftime('%Y-%m-%d')
if os.path.exists(folder_name):
    print("Папка уже есть")
else:
    os.mkdir(folder_name)

watermark = Image.open("moe.png")
if os.path.exists(f"{marka_vxod}_zzap.csv"):
    print("Папка уже есть")
else:
    with open(f"{marka_vxod}_zzap.csv", "w", encoding="utf-8") as file_data:
        writer = csv.writer(file_data)

        writer.writerow(
            (
                "ПРОИЗВОДИТЕЛЬ",
                "НОМЕР ДЕТАЛИ",
                "НАИМЕНОВАНИЕ ДЕТАЛИ",
                "ОПИСАНИЕ ZZAP",
                "ЦЕНА",
                "СОСТОЯНИЕ",
                "СРОК ДОСТАВКИ",
                "ФОТО",
                "ССЫЛКА НА ЗАПЧАСТЬ",
                """
                "ССЫЛКА НА ЗАПЧАСТЬ",
                "ЦЕНА",
                "ВНУТРЕНЯЯ ИНФОРМАЦИЯ",
                "АРТИКУЛ",
                "ЗАПЧАСТЬ",
                "МАРКА",
                "МОДЕЛЬ",
                "ГОД",
                "ОБЪЕМ",
                "ТОПЛИВО",
                "ТИП КУЗОВА",
                "НОМЕР ЗАПЧАСТИ",
                "ОПИСАНИЕ",
                "ПОД ЗАКАЗ",
                "НОВАЯ",
                "ФОТО",
                "СТРАНИЦА окончания","""
            )
        )

if os.path.exists(f"{marka_vxod}_drom.csv"):
    print("Папка уже есть")
else:
    with open(f"{marka_vxod}_drom.csv", "w", encoding="utf-8") as file_data:
        writer = csv.writer(file_data)

        writer.writerow(
            (
                "АРТИКУЛ",
                "НАИМЕНОВАНИЕ ДЕТАЛИ",
                "СОСТОЯНИЕ",
                "МАРКА",
                "МОДЕЛЬ",
                "ВЕРСИЯ",
                "НОМЕР ЗАПЧАСТИ",
                "ОБЪЕМ ДВИГАТЕЛЯ",
                "ГОД",
                "L_R",
                "F_R",
                "U_D",
                "ЦВЕТ",
                "ОПИСАНИЕ DROM",
                "КОЛИЧЕСТВО",
                "ЦЕНА",
                "НАЛИЧИЕ",
                "СРОК ДОСТАВКИ",
                "ФОТО",
                "ССЫЛКА НА ЗАПЧАСТЬ",
                "ВНУТРЕНЯЯ ИНФОРМАЦИЯ",
            )
        )
with open('zapchast_and_href.json', encoding="utf-8") as file:
    catalog = json.load(file)

def osnova(href, n, marka, model, name_zap, number_page):
    item_href_page = href[:-1]  + str(n)
    print(item_href_page)
    
    req = requests.get(url=item_href_page, headers=headers)
    src = req.text
    soup_1 = BeautifulSoup(src, 'html.parser')
    href_part = soup_1.find_all("div", class_="add-image")
    #print(href_part)
    for item in href_part:
        item = str(item)
        foto = " "
        foto = "https://bamper.by" + item[item.find('"tooltip_" src=') + 16 : item.find('title="Нажми,') -2]
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
        print(num_provider)
        if num_provider not in black_list:
            try:
                req = requests.get(url=href_to_zapchast, headers=headers)
                src = req.text

                soup = BeautifulSoup(src, 'html.parser')
                price_obj = soup.find_all("span", itemprop="offers")
                #print (price_obj)
                #if price_obj != []:
                for item_price in price_obj:
                    price = str(item_price)
                    price = price[price.find("~") + 1 : price.find("$")]
                print( price, " Цена в долларах")
                if int(price) >= 5:
                    print("больше 5")
                    marka_obj = soup.find_all("span", itemprop="name")
                    
                    for item_marka in marka_obj:
                        all_title_name = str(item_marka)
                        string = all_title_name[all_title_name.find("<b>") + 1 : ]
                        model_and_year = string[string.find(' к ')+3 :]
                        
                        year = model_and_year[model_and_year.find("г.")-5 : model_and_year.find("г.")].replace(",","").replace('"',"")
                    print(year)
                    if int(year) > 2011:
                        num_zap = " "
                        num_obj = soup.find_all("span", class_="media-heading cut-h-65")
                        #print(num_obj)
                        for item_num in num_obj:
                            num_zap = str(item_num.text).replace("  ","").replace('"',"")
                            num_zap = num_zap.replace(",","").replace("\n","")
                            num_zap = num_zap.replace("далее","").replace(';',"*#")
                        print(num_zap, "Номер запчасти")
                        all_num_zap = num_zap    
                        list_num_zap = num_zap.split()
                        print(list_num_zap, "Список номеров")
                        
                        artical_obj = soup.find_all("span", class_="data-type f13")
                        for item_artical in artical_obj:
                            artical = item_artical.text

                                
                        #print(marka, model, year, price, number_href)

                                    
                        status = "б/у"
                        order = " "    
                        info = " "
                        info_obj = soup.find_all("span", class_="media-heading cut-h-375")
                        for item_info in info_obj:
                            info = str(item_info.text.replace("  ","").replace("\n",""))
                            info = info.replace(","," ").replace('"',' ')
                            info = info.replace("\r","").replace(';',"*#")
                            info_lower = info.lower()
                            if "под заказ" in info_lower:
                                order = "ПОД ЗАКАЗ"
                        preorder = soup.find_all("div", class_="preorder ")
                        print(preorder)
                        for item_preorder in preorder:
                            if "под заказ" in item_preorder:
                                order = "ПОД ЗАКАЗ"
                        if "под заказ" in str(href_part):
                            order = "ПОД ЗАКАЗ"   
                        print(order, "ОРДЕР ЗДЕСЬ")

                        print(info)
                        if "новый" in info_lower:
                            status = "новая"
                        elif "новая" in info_lower:
                            status = "новая"
                        elif "новые" in info_lower:
                            status = "новая"
                        elif "нов." in info_lower:
                            status = "новая"
                        if "новая з/ч" in str(href_part):
                            status = "новая"   
                        print(status, "СТАТУС")

                        if foto != "https://bamper.by/local/templates/bsclassified/images/nophoto_car.png":
                            try:
                                img = requests.get(foto)
                                img_option = open(f"{folder_name}/{name_href}.png", 'wb')
                                img_option.write(img.content)
                                img_option.close
                                try:
                                    im = Image.open(f"{folder_name}/{name_href}.png")
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
                                    im.crop(((left_border+15), n/2+20, (x-left_border-20), y-(n/2)-20)).save(f"{folder_name}/{name_href}.png", quality=95)




                                    foto = "http://194.58.122.233/"+ name_href + ".png"
                                    img = Image.open(f"{folder_name}/{name_href}.png")
                                    #print(foto)
                                    #img = Image.open(f"fotku/{name_href}.png")    
                                    img.paste(watermark,(-272,-97), watermark)
                                    img.paste(watermark,(-230,1), watermark)
                                    img.save(f"{folder_name}/{name_href}.png", format="png")
                                    img_option.close
                                    #os.remove("img.png")
                                    #print(f"{name_href} - неверный формат или ерунда")
                                except UnidentifiedImageError:
                                        foto = "Битая фотка"
                                        print("Битая фотка")
                                        #os.remove(f"{folder_name}/{name_href}.png")
                            except Exception:
                                print("Какая-то хуйня с ссылкой на фотографию")
                                foto = " "
                        else:
                            foto = "Нет фотографии"
                            print(name_href , "без фотки")
                                
                        benzik_obj = soup.find_all("div", style="font-size: 17px;")
                        fuel = " "
                        transmission = " "
                        engine = " "
                        volume = " "
                        car_body = " "
                        # print(benzik_obj)
                        for item_benzik in benzik_obj:
                            benzik = " "
                            benzik = item_benzik.text.replace("  ","").replace("\n","")
                            if "л," in benzik:
                                volume = benzik[benzik.find("л,") - 5 : benzik.find("л,") + 1]
                            if "бензин" in benzik:
                                fuel = "бензин"
                            elif "дизель" in benzik:
                                fuel = "дизель"
                            elif "электро" in benzik:
                                fuel = "электро"
                            elif "гибрид" in benzik:
                                fuel = "гибрид"
                            if "седан" in benzik:
                                car_body = "седан"
                            elif "хетчбек" in benzik:
                                car_body = "хетчбек"
                            elif "внедорожник" in benzik:
                                car_body = "внедорожник"
                            elif "универсал" in benzik:
                                car_body = "универсал"
                            elif "кабриолет" in benzik:
                                car_body = "кабриолет"
                            elif "микроавтобус" in benzik:
                                car_body = "микроавтобус"
                            elif "пикап" in benzik:
                                car_body = "пикап" 
                        #print(volume, fuel, transmission, engine, car_body)
                        #print(benzik)
                        #another_zap = ""
                        count = 0
                        #if list_num_zap != []:
                        for zap in list_num_zap:
                            count +=1
                        print("До сюда дошло!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        
                        if count > 1:
                            
                            for zap in list_num_zap:
                                another_zap = another_zap + " " + zap 
                            for zap in list_num_zap: 
                                file = open(f"{marka}_added_num_zap.csv", "a", encoding="utf-8", newline='')
                                writer = csv.writer(file)

                                writer.writerow(
                                    (
                                        href_to_zapchast,
                                        price,
                                        "0"+"_PB"+num_provider,
                                        artical,
                                        name_zap,
                                        marka,
                                        model,
                                        year,
                                        volume,
                                        fuel,
                                        car_body,
                                        zap,
                                        another_zap,
                                        info,
                                        order,
                                        status,
                                        foto,
                                        number_page                                   
                                    )
                                )
                                file.close()
                        else:
                            another_zap = " "
                            file = open(f"{marka}_added_num_zap.csv", "a", encoding="utf-8", newline='')
                            writer = csv.writer(file)

                            writer.writerow(
                                (
                                    href_to_zapchast,
                                    price,
                                    "0"+"_PB"+num_provider,
                                    artical,
                                    name_zap,
                                    marka,
                                    model,
                                    year,
                                    volume,
                                    fuel,
                                    car_body,
                                    num_zap,
                                    another_zap,
                                    info,
                                    order,
                                    status,
                                    foto,
                                    number_page                                  
                                )
                            )
                            file.close()
                        file = open(f"{marka}.csv", "a", encoding="utf-8", newline='')
                        writer = csv.writer(file)

                        writer.writerow(
                            (
                                href_to_zapchast,
                                price,
                                "0"+"_PB"+num_provider,
                                artical,
                                name_zap,
                                marka,
                                model,
                                year,
                                volume,
                                fuel,
                                car_body,
                                all_num_zap,
                                info,
                                order,
                                status,
                                foto,
                                number_page                                   
                            )
                        )
                        file.close()
                        #os.remove(f"{name_href}.html")
                        with requests.request("POST", href_to_zapchast, headers=headers) as report:
                            print('report: ', report)
                   
                    else:
                        print(" Запчасть очень старая, мы такими не торгуем")
                else: 
                    print("Цена запчасти меньше 5$")
            except Exception:
                print("какая-то хуйня с карточкой запчастей")

        else:
            print(href_to_zapchast + " находится в black-list, уже ")
            with requests.request("POST", href_to_zapchast, headers=headers) as report:
                print('report: ', report)

    href_part_pag = soup_1.find_all("ul", class_="pagination")
    if "След." in str(href_part_pag):
        href_part_pag = str(href_part_pag)
        #print(href_part)
        print("переходим на следующую")
        n += 1
        if n < 61:
            osnova(item_href_page, n, marka, model, name_zap, number_page)

number_page = 0
for item_href_model, name_zap  in catalog.items():
    if marka_vxod_in in item_href_model:
        if int(number_page) >= int(num_vxod):
            number_page += 1
            print(item_href_model)
            print(name_zap)
            marka = marka_vxod
            model = item_href_model[item_href_model.find("model")+6 : -1]
            print( marka,  model)
            
            i = 1
            print()
            #item_href_model = "https://bamper.by/zchbu/zapchast_bryzgovik/marka_audi/model_a1/"
            item_href_model = item_href_model + "?ACTION=REWRITED3&FORM_DATA=" + item_href_model[item_href_model.find("zchbu")+6 : item_href_model.find("/marka")] + "%2Fmarka_" + item_href_model[item_href_model.find("/marka")+7 : item_href_model.find("/model")] + "%2Fmodel_" + item_href_model[item_href_model.find("/model_")+7 : -1] + "&PAGEN_1=1"
            osnova(item_href_model, i, marka, model, name_zap, number_page)
        else:
            number_page += 1
            
        

a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие - ")
