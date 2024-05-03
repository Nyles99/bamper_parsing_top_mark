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
proxy = input("Введи прокси в формате логин:пароль@46.8.158.109:54376 - ")

headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}



input_name = input("Как назовем файл? - ")
input_page = int(input("С какой странице начнем, ставь 0 если начало - "))

pricing = input("Введи цифру ценообразования от 1 до 5 - ")
#input_price = int(input("От какой суммы собираем в белках? - "))

proxies = {
    'http': f'{proxy}',
    'https': f'{proxy}'
}

summa = 0
black_list = []
black_model = []
cculka = []

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


marka_need_list = {}
model_need_list = {}       

#https://bamper.by/zchbu/zapchast_steklo-lobovoe/god_2000-2001/price-ot_150/?more=Y
with open('zapchastot1000_2012.json', encoding="utf-8") as file:
    zapchast00_1200 = json.load(file)




folder_name =f"{input_name}_" + time.strftime('%Y-%m-%d')
if os.path.exists(folder_name):
    print("Папка уже есть")
else:
    os.mkdir(folder_name)

watermark = Image.open("moe.png")
if os.path.exists(f"{input_name}_zzap.csv"):
    print("файл csv уже есть")
else:
    with open(f"{input_name}_zzap.csv", "w", encoding="utf-8") as file_data:
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
            )
        )

if os.path.exists(f"{input_name}_drom.csv"):
    print("файл csv уже есть")
else:
    with open(f"{input_name}_drom.csv", "w", encoding="utf-8") as file_data:
        writer = csv.writer(file_data)

        writer.writerow(
            (
                "АРТИКУЛ",
                "НАИМЕНОВАНИЕ ДЕТАЛИ",
                "СОСТОЯНИЕ",
                "МАРКА",
                "МОДЕЛЬ",
                "ВЕРСИЯ",
                "НОМЕР ДЕТАЛИ",
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
                "Страница"
            )
        )

with open('prouzbod.json', encoding="utf-8") as file:
    prouz = json.load(file)




def osnova():
    print(first_page)
    req = requests.get(url=first_page, headers=headers, proxies=proxies)
    src = req.text
    soup_1 = BeautifulSoup(src, 'html.parser')
    href_part = soup_1.find_all("div", class_="add-image")
    #print(href_part)
    for item in href_part:
        item = str(item)
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
        if num_provider not in black_list:
            try:
                req = requests.get(url=href_to_zapchast, headers=headers, proxies=proxies)
                src = req.text

                soup = BeautifulSoup(src, 'html.parser')
                price_obj = soup.find_all("span", itemprop="offers")
                #print (price_obj)
                #if price_obj != []:
                for item_price in price_obj:
                    price = str(item_price)
                    price = price[price.find("~") + 1 : price.find("$")]
                price = int(price.replace(" ",""))
                print( price, " Цена в долларах")
                if price >= 5:
                    #print("больше 5")
                    if int(pricing) == 3:
                        #print("Цена в рублях будет по 3-ему ценообразованию")
                        if (4<price <20):
                            price_rub = price * 100 + 1500
                        elif price == 20:
                            price_rub = price * 170
                        elif (20 < price <31) :
                            price_rub = price * (186 -int(price))
                        elif (30 < price < 34) :
                            price_rub = price * 155
                        elif (33 < price < 36) :
                            price_rub = price * 154
                        elif (35 < price < 39) :
                            price_rub = price * 153
                        elif (38 < price < 42) :
                            price_rub = price * 152
                        elif (42 <= price <= 46) :
                            price_rub = price * 151
                        elif (47 <= price <= 53) :
                            price_rub = price * 150
                        elif (54 <= price <= 70) :
                            price_rub = price * 149
                        elif (71 <= price <= 81) :
                            price_rub = price * 148
                        elif (82 <= price <= 87) :
                            price_rub = price * 147
                        elif (88 <= price <= 93) :
                            price_rub = price * 146
                        elif (94 <= price <= 102) :
                            price_rub = price * 145
                        elif (103 <= price <= 113) :
                            price_rub = price * 144
                        elif (114 <= price <= 125) :
                            price_rub = price * 143
                        elif (126 <= price <= 135) :
                            price_rub = price * 142
                        elif (136 <= price <= 192) :
                            price_rub = price * 141
                        elif (193 <= price <= 215) :
                            price_rub = price * 140
                        elif (216 <= price <= 235) :
                            price_rub = price * 139
                        elif 236 <= price <= 907 :
                            price_rub = price * 138
                        elif (908 <= price <= 1245) :
                            price_rub = price * 137
                        elif (1246 <= price <= 1752) :
                            price_rub = price * 136
                        elif 1753 <= price :
                            price_rub = price * 135
                        #print("до сюда дошло")
                        price_rub -=price_rub %- 100
                    elif int(pricing) == 2:
                        #print("Цена в рублях будет по 3-ему ценообразованию")
                        if (4<price <20):
                            price_rub = price * 100 + 1500
                        elif price == 20:
                            price_rub = price * 142
                        elif (20 < price <28) :
                            price_rub = price * (162 -int(price))
                        elif (28 < price < 30) :
                            price_rub = price * 134
                        elif (29 < price < 32) :
                            price_rub = price * 133
                        elif (31 < price < 34) :
                            price_rub = price * 132
                        elif (33 < price < 36) :
                            price_rub = price * 131
                        elif (36 <= price <= 38) :
                            price_rub = price * 130
                        elif (39 <= price <= 41) :
                            price_rub = price * 129
                        elif (42 <= price <= 44) :
                            price_rub = price * 128
                        elif (45 <= price <= 48) :
                            price_rub = price * 127
                        elif (49 <= price <= 85) :
                            price_rub = price * 126
                        elif (86 <= price <= 93) :
                            price_rub = price * 125
                        elif (94 <= price <= 103) :
                            price_rub = price * 124
                        elif (104 <= price <= 116) :
                            price_rub = price * 123
                        elif (117 <= price <= 130) :
                            price_rub = price * 122
                        elif (131 <= price <= 149) :
                            price_rub = price * 121
                        elif (150 <= price <= 219) :
                            price_rub = price * 120
                        elif (220 <= price <= 1039) :
                            price_rub = price * 119
                        elif (1040 <= price <= 1562) :
                            price_rub = price * 118
                        elif 1563 <= price :
                            price_rub = price * 117
                        #print("до сюда дошло")
                        price_rub -=price_rub %- 100
                    elif int(pricing) == 4:
                        #print("Цена в рублях будет по 3-ему ценообразованию")
                        if (4<price <20):
                            price_rub = price * 100 + 1500
                        elif price == 20:
                            price_rub = price * 200
                        elif price == 21:
                            price_rub = price * 188
                        elif (21 < price <28) :
                            price_rub = price * (204 -int(price))
                        elif (27 < price < 30) :
                            price_rub = price * 176
                        elif price == 30:
                            price_rub = price * 175
                        elif (30 < price < 33) :
                            price_rub = price * 174
                        elif (32 < price < 35) :
                            price_rub = price * 173
                        elif (35 <= price <= 36) :
                            price_rub = price * 172
                        elif (37 <= price <= 39) :
                            price_rub = price * 171
                        elif (40 <= price <= 41) :
                            price_rub = price * 170
                        elif (42 <= price <= 44) :
                            price_rub = price * 169
                        elif (45 <= price <= 48) :
                            price_rub = price * 168
                        elif (49 <= price <= 82) :
                            price_rub = price * 167
                        elif (83 <= price <= 89) :
                            price_rub = price * 166
                        elif (90 <= price <= 97) :
                            price_rub = price * 165
                        elif (98 <= price <= 106) :
                            price_rub = price * 164
                        elif (107 <= price <= 116) :
                            price_rub = price * 163
                        elif (117 <= price <= 128) :
                            price_rub = price * 162
                        elif (129 <= price <= 142) :
                            price_rub = price * 161
                        elif (143 <= price <= 198) :
                            price_rub = price * 160
                        elif (199 <= price <= 218) :
                            price_rub = price * 159
                        elif (219 <= price <= 241) :
                            price_rub = price * 158
                        elif (242 <= price <= 346) :
                            price_rub = price * 157
                        elif (347 <= price <= 401) :
                            price_rub = price * 156
                        elif (402 <= price <= 468) :
                            price_rub = price * 155
                        elif (469 <= price <= 649) :
                            price_rub = price * 154
                        elif (650 <= price <= 752) :
                            price_rub = price * 153
                        elif (753 <= price <= 982) :
                            price_rub = price * 152
                        elif (983 <= price <= 1331) :
                            price_rub = price * 151
                        elif (1332 <= price <= 1844) :
                            price_rub = price * 150
                        elif 1845 <= price :
                            price_rub = price * 149
                        #print("до сюда дошло")
                        price_rub -=price_rub %- 100
                    else:
                        print(f"О ценообразовании №{pricing} нет информация а таблицах эксель будет сохраняться цена в долларах$(закупочная)!!!!")
                        price_rub = price
                            


                    marka_obj = soup.find_all("span", itemprop="name")
                    
                    for item_marka in marka_obj:
                        all_title_name = str(item_marka)
                        string = all_title_name[all_title_name.find("</b>") + 4 : ]
                        name_zap = all_title_name[all_title_name.find("<b>") + 3 : all_title_name.find("</b>")]
                        
                        model_and_year = string[string.find(' к ')+3 :]
                        marka = model_and_year[ : model_and_year.find(" ")]
                        if "Alfa" in marka:
                            marka = "Alfa Romeo"
                        if "Aston" in marka:
                            marka = "Aston Martin"
                        if "New" in marka:
                            marka = "New Holland"
                        if "John" in marka:
                            marka = "John Deer"
                        marka_len = len(marka)+1
                        model_string = model_and_year[marka_len : model_and_year.find("(")]
                        model = model_string[: model_string.find(",")].replace(",","").replace("   "," ").replace("  "," ").rstrip()
                        #version = model_string[model_string.find(" ")+1 : model_string.find(",")]                       
                        year = model_and_year[model_and_year.find("г.")-5 : model_and_year.find("г.")].replace(",","").replace('"',"")
                    #print(year)
                    
                    num_zap = " "
                    num_obj = soup.find_all("span", class_="media-heading cut-h-65")
                    #print(num_obj)
                    for item_num in num_obj:
                        num_zap = str(item_num.text).replace("  ","").replace('"',"")
                        num_zap = num_zap.replace(",","").replace("\n","")
                        num_zap = num_zap.replace("далее","").replace(';',"*#")
                        
                    #print(num_zap, "Номер запчасти")
                    one_num_zap = num_zap[ : num_zap.find(' ')]
                    num_zap = num_zap.rstrip().replace(" ","; ")
                    if (int(len(num_zap)) - int(len(one_num_zap))) == 1:
                            one_num_zap = num_zap
                    """all_num_zap = num_zap    
                    list_num_zap = num_zap.split()
                    print(list_num_zap, "Список номеров")"""
                    
                    artical_obj = soup.find_all("span", class_="data-type f13")
                    for item_artical in artical_obj:
                        artical = item_artical.text

                            
                    #print(marka, model, year, price, number_href)

                                
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
                    #print(status, "СТАТУС")
                    
                    
                    foto_href = str(soup.find_all("div", class_="detail-image"))
                    #print(foto_href, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    foto = "https://bamper.by" + foto_href[foto_href.find('src=') + 5 : foto_href.find('"/>')]
                    print(foto, "ССЫЛКА НА ФОТОГРАФИИ!!!!!!!!!!!!!!!!")

                    if "nophoto_car.png" not in foto:
                        try:
                            img = requests.get(url=foto, headers=headers, proxies=proxies)
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




                                foto = "http://171.25.166.53/~Reppart/reppart/"+ name_href + ".png"
                                img = Image.open(f"{folder_name}/{name_href}.png")
                                #print(foto)
                                #img = Image.open(f"fotku/{name_href}.png")    
                                img.paste(watermark,(-272,-97), watermark)
                                img.paste(watermark,(-230,1), watermark)
                                img.save(f"{folder_name}/{name_href}.png", format="png")
                                img_option.close

                                ftp = ftplib.FTP()
                                print(f'Conecting to FTP\nHost: {HOST}\nPort: {PORT}')
                                ftp.connect(HOST, PORT)
                                print(f'Conecting sucess!\nLogin as: {USER},Pass: 123456')
                                ftp.login(USER, PASSWORD)  
                                print('Login Succes!')
                                #https://bamper.by/zapchast_shleyf-rulya/9676-108946063/
                                """session = ftplib.FTP(host="171.25.166.53", PORT=3121, user="Reppart", passwd="Nikitos21@Artem")""" 
                                file = open(f"{folder_name}/{name_href}.png", "rb")
                                ftp.storbinary(f"STOR www/reppart/{name_href}.png", file)
                                file.close()
                                ftp.quit()
                                #os.remove("img.png")
                                #print(f"{name_href} - неверный формат или ерунда")
                            except UnidentifiedImageError:
                                    foto = "Битая фотка"
                                    print("Битая фотка")
                                    foto = "http://171.25.166.53/~Reppart/reppart/"+ name_href + ".png"
                                    #os.remove(f"{folder_name}/{name_href}.png")
                        except Exception:
                            print("Какая-то хуйня с ссылкой на фотографию")
                            #foto = " "
                            print(foto) 
                    else:
                        foto = "Нет фотографии"
                        print(name_href , "без фотки")
                            
                    benzik_obj = soup.find_all("div", style="font-size: 17px;")
                    fuel = "    "
                    transmission = "    "
                    #engine = " "
                    volume = "    "
                    car_body = "    "
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
                    status_new = ""
                    if status == "новая":
                        status_new = "Новая деталь"
                    else:
                        status_new = "Контрактная деталь, без пробега по России"
                    if num_zap == " " or num_zap == "" or num_zap == "  ":
                        num_zap_text = ""
                    else:
                        num_zap_text = f" Номер детали: {one_num_zap}, {num_zap}."
                    #print("Дошло до этого места")
                    proizvoditel = marka
                    for m_in, m_out in prouz.items():
                        #print(m_in)
                        if m_in in marka:
                            proizvoditel = m_out
                            #print(proizvoditel,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    
                    L_R = ""
                    F_R = ""
                    U_D = ""
                    if "левый" or "левая" or "левой" or "левые" or "левого" or "левое" or "левые" in name_zap:
                        L_R = "L"
                    elif "правый" or "правая" or "правой" or "правые" or "правого" or "правое" or "правые" in name_zap:
                        L_R = "R"
                    else:
                        L_R = ""
                    if "задний" or "задняя" or "задней" or "заднего" or "Задняя" or "задних" or "заднее" or "задние" in name_zap:
                        F_R = "R"
                    elif "передний" or "передняя" or "передней" or "переднего" or "Передняя" or "передних" or "переднее" or "передние" in name_zap:
                        F_R = "R"
                    else:
                        F_R = ""
                    if "верхняя" in name_zap:
                        U_D = "U"
                    elif "нижняя" in name_zap:
                        U_D = "D"
                    else:
                        U_D = ""

                    text_zzap = f"{marka} {model} {version} {year}г.в., {fuel}, {volume}, {transmission}, {car_body}. Будьте готовы назвать АРТИКУЛ: Z-{artical}.{num_zap_text} Склад: {pricing}_{price}_PB_{num_provider}. {status_new}.".replace(",     "," ").replace("     ","").replace("    .",".").replace("   .",".").replace("  .",".").replace(" .",".").replace(",  ",", ")
                    
                    text_drom = f"{name_zap} {marka} {model} {version} {year}г.в., {fuel}, {volume}, {car_body}. Будьте готовы назвать АРТИКУЛ: D-{artical}.{num_zap_text} Склад: {pricing}_{price}_PB_{num_provider}. {status_new}. Задавайте, пожалуйста, вопросы непосредственно перед заключением сделки, остатки меняются ежедневно. Доставку осуществляем ТК сразу в ваш город. Срок доставки до Москвы 2-4 дня, бывают исключения, где сроки доставки могут увеличиться. Состояние вы оцениваете сами, по предоставленным фотографиям). Если деталь не понадобилась - возврат не рассматривается! По VIN автомобиля запчасти не подбираем, строго по заводскому номеру, указанному на детали. С Уважением, компания REPPART!".replace(",     "," ").replace("     ","").replace("    .",".").replace("   .",".").replace("  .",".").replace(" .",".").replace(",  ",", ")
                    file = open(f"{input_name}_zzap.csv", "a", encoding="utf-8", newline='')
                    writer = csv.writer(file)

                    writer.writerow(
                        (
                            proizvoditel,
                            one_num_zap,
                            name_zap,
                            text_zzap,
                            price_rub,
                            status,
                            "2-4 дня",
                            foto,                                  
                        )
                    )
                    file.close()

                    file = open(f"{input_name}_drom.csv", "a", encoding="utf-8", newline='')
                    writer = csv.writer(file)

                    writer.writerow(
                        (
                            f"АРТИКУЛ: D-{artical}",
                            name_zap,
                            status,
                            marka,
                            model,
                            version,
                            num_zap,
                            volume,
                            year,
                            L_R,
                            F_R,
                            U_D,
                            "",
                            text_drom,
                            "1",
                            price_rub,
                            "под заказ",
                            "2-4 дня",
                            foto,
                            last_page,                                   
                        )
                    )
                    file.close()
                    #os.remove(f"{name_href}.html")
                    with requests.request("POST", href_to_zapchast, headers=headers, proxies=proxies) as report:
                        print('report: ', report)
                
                    
                else: 
                    print("Цена запчасти меньше 5$")
            except Exception:
                print("какая-то хуйня с карточкой запчастей")

        else:
            print(href_to_zapchast + " находится в black-list, уже ")
            with requests.request("POST", href_to_zapchast, headers=headers, proxies=proxies) as report:
                print('report: ', report)

last_page = 0
for url, page in zapchast00_1200.items():
        #print(url)
        #print(page)
    #    https://bamper.by/zchbu/marka_acura/model_integra/god_2016-2024/price-ot_1000/store_Y/?more=Y
        try:
            mark = url[url.find("marka_")+ 6 : url.find("/model")]
            mod = url[url.find("model_")+ 6 : url.find("/god")]
            year1 = url[url.find("/god_")+ 5 : url.find("/price")-5]
            year2 = url[url.find("/god_")+ 10 : url.find("/price")]
            pri = url[url.find("/price") + 10 : url.find("/store")]
            for i in range(1, int(page)+1):
                if input_page <= last_page:
                    last_page += 1
                    first_page = f"https://bamper.by/zchbu/marka_{mark}/model_{mod}/god_{year1}-{year2}/price-ot_1000/store_Y/?ACTION=REWRITED3&FORM_DATA=marka_{mark}%2Fmodel_{mod}%2Fgod_{year1}-{year2}%2Fprice-ot_1000%2Fstore_Y&more=Y&PAGEN_1={i}"
                    #print (first_page)
                    osnova()
                else:
                    last_page += 1                      

        except Exception:
            print ("ошибка при нахождении ссылки или не загрузился сайт бампер")
    

a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие - ")
