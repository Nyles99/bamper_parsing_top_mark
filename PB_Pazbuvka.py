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

slovo = input("Нужна разбивка, введи да, с маленькой буквы если нужна - ")
print("Не забудь добавить файл 'black-list.txt'")
summa_o = 0
#bot = Bot(token='6945695697:AAEOKj6ObwjrcC34Ysgbi5sNYzLE5gCJMQA')
#chat_id = 5514046199
text = 'Парсинг запущен'

#bot.send_message(6446161768, text)

#proxy = input("Введи прокси в формате логин:пароль@46.8.158.109:54376 - ")

headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

service = Service()
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
options.add_argument("--log-level=1")

driver = webdriver.Chrome(service = service, options = options)
#options.add_argument(f"--proxy-server={ip}")


driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol:
    '''
})



#input_name = input("Как назовем файл? - ")
#input_page = int(input("С какой странице начнем, ставь 0 если начало - "))
#bot.send_message(chat_id, f"{input_name} запустился, его прокси {proxy}, начали со страницы {input_page}")
#pricing = input("Введи цифру ценообразования от 1 до 5 - ")
#input_price = int(input("От какой суммы собираем в белках? - "))

"""proxies = {
    'http': f'{proxy}',
    'https': f'{proxy}'
}"""

summa = 0
"""black_list = []
black_model = []
cculka = []
book= load_workbook("Ценообразование.xlsx")
sheet= book["Лист1"]"""

"""file1 = open("black-list.txt", "r")
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
file1.close"""


marka_need_list = {}
model_need_list = {}       


"""folder_name =f"{input_name}_" + time.strftime('%Y-%m-%d')
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
                'Поставщик',
                'Артикул',
                'Закупка',
                'Ценообразование',
                'Марка',
                'Модель',
                'Год',
                'Объем двигателя',
                'Топливо',
                'Наименование запчасти',
                'Номера деталей', #(первые 5 номеров, дальше не надо, важно чтобы ничего не менялось, нули вначале и тд)
                'Номер детали', # (первый номер, важно чтобы ничего не менялось, нули вначале и тд)
                'Описание',
                'Фото', #(могу наверно сам генерировать)
                'Состояние',
                'Старница' #(запчасти новые до 30 т.р., ставить как бу)
                )
            )


with open('prouzbod.json', encoding="utf-8") as file:
    prouz = json.load(file)"""


def search(url_card):
    url_zapchast = str(url_card)
    print(url)
    #markah = url_zapchast[url_zapchast.find("marka_")+6 : url_zapchast.find("model_")-1 ]
    #modelh = url_zapchast[url_zapchast.find("model_")+6 : url_zapchast.find("god_")-1 ]
    #url_zapchast = f"https://bamper.by/zchbu/marka_{markah}/model_{modelh}/god_2012-2016/price-ot_300/price-do_999/store_y/?more=Y"
    try:
        driver.get(url=url_zapchast)
        time.sleep(1)

        with open(f"{1}.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        with open(f"{1}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, 'html.parser')

        count = soup.find_all("h5", class_="list-title js-var_iCount")
        
        #print(count)
        for item in count:
            item = str(item)
            if "<b>" in item:
                #print(item)
                num_page = item[item.find("<b>")+3: item.find("</b>")]
                num_page = int(num_page.replace(" ",""))
                print(num_page)
                summa = summa + num_page
                if num_page > 0 and num_page < 1201:
                    page = int(num_page / 20) + 1
                    zapchast00_1200[url_zapchast] = page
                elif num_page > 1200:
                    pass
    except Exception:
        print(f"Не загрузилась {url_zapchast} - загрузим позже, попробуй обновить вручную в браузере")                    




if slovo == "да":
    url = "https://bamper.by/catalog/modeli/"
    driver.get(url=url)
    time.sleep(20)

    spisok_1 = []
    file1 = open("1.txt", "r", encoding="utf-8")
    while True:
        # считываем строку
        line = file1.readline()
        line = line.replace("\n","").replace("'","").replace(" ","")
        # прерываем цикл, если строка пустая
        if not line:
            break
        # выводим строку
        spisok_1.append(line)
    file1.close

    zapchast00_1200 = {}
    zapchast1200 = {}
    null_or_xz = {}
    n=1

    for url in spisok_1:
        #item_text_model = item_text_model.replace("/","_")
        url_zapchast = str(url)
        #item_href_model = item_href_model[item_href_model.find("catalog/")+8 : len(item_href_model) -1]
        print(url)
        markah = url_zapchast[url_zapchast.find("marka_")+6 : url_zapchast.find("model_")-1 ]
        modelh = url_zapchast[url_zapchast.find("model_")+6 : url_zapchast.find("god_")-1 ]
        #url_zapchast = f"https://bamper.by/zchbu/marka_{markah}/model_{modelh}/god_2012-2016/price-ot_300/price-do_999/store_y/?more=Y"
        try:
            driver.get(url=url_zapchast)
            time.sleep(1)

            with open(f"{1}.html", "w", encoding="utf-8") as file:
                file.write(driver.page_source)

            with open(f"{1}.html", encoding="utf-8") as file:
                src = file.read()

            soup = BeautifulSoup(src, 'html.parser')

            count = soup.find_all("h5", class_="list-title js-var_iCount")
            
            #print(count)
            for item in count:
                item = str(item)
                if "<b>" in item:
                    #print(item)
                    num_page = item[item.find("<b>")+3: item.find("</b>")]
                    num_page = int(num_page.replace(" ",""))
                    print(num_page)
                    summa = summa + num_page
                    if num_page > 0 and num_page < 1201:
                        page = int(num_page / 20) + 1
                        zapchast00_1200[url_zapchast] = page
                    elif num_page > 1200:
                        href_zapchast = []
                        
                        item_href_categories = str(url_zapchast)
                        start_year_start = int(item_href_categories[item_href_categories.find("god_") + 4 : item_href_categories.find("/price-ot_") - 5])
                        end_year_start = int(item_href_categories[item_href_categories.find("god_") + 9 : item_href_categories.find("/price-ot_")])
                        
                        first_part = item_href_categories[ : item_href_categories.find("god_")+ 4]
                        second_part = item_href_categories[item_href_categories.find("/price-ot_") : ]
                        for year_s in range(start_year_start, end_year_start + 1):
                            url_zapchast = f"{first_part}{year_s}-{year_s}{second_part}"
                        
                            print(url_zapchast)
                            try:
                            #print(url_zapchast)
                                driver.get(url=url_zapchast)
                                time.sleep(1)

                                with open("excample.html", "w", encoding="utf-8") as file:
                                    file.write(driver.page_source)

                                with open("excample.html", encoding="utf-8") as file:
                                    src = file.read()

                                soup = BeautifulSoup(src, 'html.parser')

                                count = soup.find_all("h5", class_="list-title js-var_iCount")
                                #print(count)
                                for item in count:
                                    item = str(item)
                                    if "<b>" in item:
                                        #print(item)
                                        num_page = item[item.find("<b>")+3: item.find("</b>")]
                                        num_page = int(num_page.replace(" ",""))
                                        print(num_page)
                                        summa = summa + num_page
                                        if num_page > 0 and num_page < 1201:
                                            page = int(num_page / 20) + 1
                                            zapchast00_1200[url_zapchast] = page
                                        elif num_page > 1200:
                    
                                        
                                            ot = int(url_zapchast[url_zapchast.find("price-ot_")+9 : url_zapchast.find("/price-do_")])
                                            do = int(url_zapchast[url_zapchast.find("price-do_")+9 : url_zapchast.find("/store")])
                                            part_one = url_zapchast[: url_zapchast.find("price-ot_")+9]
                                            part_two = url_zapchast[url_zapchast.find("/store") :]
                                            period = int((do - ot)/10)
                                            for i in range(0,9):
                                                url_zapchast = str(part_one)+str(ot+period*i)+"/price-do_"+str(ot+period*(i+1))+str(part_two)
                                                driver.get(url=url_zapchast)
                                                time.sleep(1)

                                                with open("excample.html", "w", encoding="utf-8") as file:
                                                    file.write(driver.page_source)

                                                with open("excample.html", encoding="utf-8") as file:
                                                    src = file.read()

                                                soup = BeautifulSoup(src, 'html.parser')

                                                count = soup.find_all("h5", class_="list-title js-var_iCount")
                                                #print(count)
                                                for item in count:
                                                    item = str(item)
                                                    if "<b>" in item:
                                                        #print(item)
                                                        num_page = item[item.find("<b>")+3: item.find("</b>")]
                                                        num_page = int(num_page.replace(" ",""))
                                                        print(num_page)
                                                        summa = summa + num_page
                                                        if num_page > 0 and num_page < 1201:
                                                            page = int(num_page / 20) + 1
                                                            zapchast00_1200[url_zapchast] = page
                                                        elif num_page > 1200:
                                                            page = int(num_page / 20) + 1
                                                            zapchast1200[url_zapchast] = page
                                                        elif num_page == 0:
                                                            print(url_zapchast, "Страница с нулевым значением нам не нужна")
                                            url_zapchast = str(part_one)+str(ot+period*9)+"/price-do_"+str(do)+str(part_two)
                                            driver.get(url=url_zapchast)
                                            time.sleep(1)

                                            with open("excample.html", "w", encoding="utf-8") as file:
                                                file.write(driver.page_source)

                                            with open("excample.html", encoding="utf-8") as file:
                                                src = file.read()

                                            soup = BeautifulSoup(src, 'html.parser')

                                            count = soup.find_all("h5", class_="list-title js-var_iCount")
                                            #print(count)
                                            for item in count:
                                                item = str(item)
                                                if "<b>" in item:
                                                    #print(item)
                                                    num_page = item[item.find("<b>")+3: item.find("</b>")]
                                                    num_page = int(num_page.replace(" ",""))
                                                    print(num_page)
                                                    summa = summa + num_page
                                                    if num_page > 0 and num_page < 1201:
                                                        page = int(num_page / 20) + 1
                                                        zapchast00_1200[url_zapchast] = page
                                                    elif num_page > 1200:
                                                        page = int(num_page / 20) + 1
                                                        zapchast1200[url_zapchast] = page
                                                    elif num_page == 0:
                                                        print(url_zapchast, "Страница с нулевым значением нам не нужна")
                                                                
                                
                            except Exception:
                                print(f"Не загрузилась {url_zapchast} - загрузим позже, попробуй обновить вручную в браузере")
                        
                        
                        
            os.remove(f"{1}.html")
        except Exception:
            print(f"Страница {url_zapchast} отвалилась!!!!!!!!!!!!")

    with open("null_or_xz.json", "a", encoding="utf-8") as file:
        json.dump(null_or_xz, file, indent=4, ensure_ascii=False)

    with open("zapchastot60.json", "a", encoding="utf-8") as file:
        json.dump(zapchast00_1200, file, indent=4, ensure_ascii=False)

    with open("zapchastot60_1200.json", "a", encoding="utf-8") as file:
        json.dump(zapchast1200, file, indent=4, ensure_ascii=False)


    print(summa)


a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие - ")
