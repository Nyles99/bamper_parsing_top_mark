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

folder_name =f"{marka_vxod}_" + time.strftime('%Y-%m-%d')
if os.path.exists(folder_name):
    print("Папка уже есть")
else:
    os.mkdir(folder_name)

watermark = Image.open("moe.png")
if os.path.exists(f"{marka_vxod}.csv"):
    print("Папка уже есть")
else:
    with open(f"{marka_vxod}.csv", "w", encoding="utf-8") as file_data:
        writer = csv.writer(file_data)

        writer.writerow(
            (
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
                "НОМЕРА ЗАМЕН",
                "ОПИСАНИЕ",
                "ПОД ЗАКАЗ",
                "НОВАЯ",
                "ФОТО",
                "СТРАНИЦА окончания",
            )
        )

if os.path.exists(f"{marka_vxod}_added_num_zap.csv"):
    print("Папка уже есть")
else:
    with open(f"{marka_vxod}_added_num_zap.csv", "w", encoding="utf-8") as file_data:
        writer = csv.writer(file_data)

        writer.writerow(
            (
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
                "НОМЕРА ЗАМЕН",
                "ОПИСАНИЕ",
                "ПОД ЗАКАЗ",
                "НОВАЯ",
                "ФОТО",
                "СТРАНИЦА окончания",
            )
        )
with open('zapchast_and_href.json', encoding="utf-8") as file:
    catalog = json.load(file)

def osnova(href, n):
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
        #print(num_provider)
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





                    else:
                        print(" Запчасть очень старая, мы такими не торгуем")
                else: 
                    print("Цена запчасти меньше 5$")
            except Exception:
                print("какая-то хуйня с карточкой запчастей")

        else:
            print(href_to_zapchast + " находится в black-list, уже "+ str(zapchast_in_black_list) )
            zapchast_in_black_list += 1
            with requests.request("POST", href_to_zapchast, headers=headers) as report:
                print('report: ', report)

    href_part_pag = soup_1.find_all("ul", class_="pagination")
    if "След." in str(href_part_pag):
        href_part_pag = str(href_part_pag)
        #print(href_part)
        print("переходим на следующую")
        n += 1
        if n < 61:
            osnova(item_href_page, n)

for item_href_model, name_zap  in catalog.items():
    if marka_vxod_in in item_href_model:
        print(item_href_model)
        print(name_zap)
        marka = marka_vxod
        model = item_href_model[item_href_model.find("model")+6 : -1]
        print( marka,  model)
        i = 1
        item_href_model = "https://bamper.by/zchbu/zapchast_bryzgovik/marka_audi/model_a1/"
        item_href_model = item_href_model + "?ACTION=REWRITED3&FORM_DATA=" + item_href_model[item_href_model.find("zchbu")+6 : item_href_model.find("/marka")] + "%2Fmarka_" + item_href_model[item_href_model.find("/marka")+7 : item_href_model.find("/model")] + "%2Fmodel_" + item_href_model[item_href_model.find("/model_")+7 : -1] + "&PAGEN_1=1"
        osnova(item_href_model, i)
        
            
        break

a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие - ")
