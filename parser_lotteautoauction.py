# -*- coding: utf-8 -*-
import time
import csv
import requests
import os
import shutil
import re
import html
import fake_useragent
import configparser
import mysql.connector as mysql
from ftplib import FTP
from io import BytesIO
from deep_translator import GoogleTranslator
from multiprocessing import current_process, Pool
from bs4 import BeautifulSoup
from random import choice
from random import uniform
from requests_html import HTMLSession
from urllib import parse
import urllib.parse
import logging

logging.basicConfig(level=logging.DEBUG)
#підтягуємо усі настройки з файлу settings.ini
config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini") 
if(config['LOTTE']['AUTOCODE'] == '2'):
    try:
        db_connection = mysql.connect(host="217.172.189.14", database="olegk202_kdm", user="olegk202_kdm", password="Kostiuk_6173")
    except Exception as e:
        print(e)

if(config['LOTTE']['FTPCODE'] == '1'):
    ftp = FTP("217.172.189.14")
    ftp.login("olegk202","lYgH51teND")
    ftp.cwd("public_html/uploads/tempimage")
#read file function 
def read_file(file_name, delimiter):
        try:
            return open(file_name).read().split(delimiter)
        except Exception as e:
            print('Can\'t read %s. Reason %s.' % (file_name, e))
# session.max_redirects = 60
#headers = {'Authorization':'Basic MTUyMDAwOjQyNzU=', 'user-agent': user, 'accept': '*/*'}
#set cookies
#parsing from proxy
#proxy = { 'http': 'http://' + choice(read_file("proxies.txt","\n")) }
#session.proxies.update(proxy)    

#translate function 
def ko_translate(text, lan='en'):
        if isinstance(text, str):
            try:
                if(len(text)>1 and len(text)<5000 and isinstance(text,str)):
                    return GoogleTranslator(source='ko', target=lan).translate(text)
            except Exception as e:
                print('Failed to Translate text. Reason: %s' % e)
        else: 
            print("TEXT is not STR translate Function")

#удаляємо всі зайві пробіли, переноси строк і табуляції
def rm_new_line(string):
        if isinstance(string, str):
            try:
                string = html.unescape(string)
                string = re.sub("\r?\n?","",string)
                string = re.sub("\t","",string)
                string = string.replace("> <", "><")
                string = string.replace("- -", "--")
                string = string.replace("< ", "<")
                string = string.replace(" >", ">")
                string = string.replace("/ ", "/")
                string = string.replace("<! ", "<!")
                string = re.sub("\<[!\s-][\\a-z\S\s]*[^<>]*[\-\s]\>", "", string)
                string = re.sub("\<[!\s-][\S]+[\-\s]\>", "", string)
                string = string.replace("\s{2,}", " ")
                return string
            except Exception as e:
                    print('Failed to delete White Space Tabs and New Line in string "%s". Reason: %s' % (string, e))
#удаляємо всі зайві пробіли, ненужні символи у назві картинки
def clear_img_name(img_name):
        try:
            img_name = img_name.split(".")
            if(len(img_name)==2):
                img_name[0] = img_name[0].lower()
                img_name[0] = re.sub("\(","",img_name[0])
                img_name[0] = re.sub("\)","",img_name[0])
                img_name[0] = re.sub("\{","",img_name[0])
                img_name[0] = re.sub("\}","",img_name[0])
                img_name[0] = re.sub("\[","",img_name[0])
                img_name[0] = re.sub("\]","",img_name[0])
                img_name[0] = re.sub("\<","",img_name[0])
                img_name[0] = re.sub("\>","",img_name[0])
                img_name[0] = re.sub("\$","",img_name[0])
                img_name[0] = re.sub("\#","",img_name[0])
                img_name[0] = re.sub("\%","",img_name[0])
                img_name[0] = re.sub("\~","",img_name[0])
                img_name[0] = re.sub("\@","",img_name[0])
                img_name[0] = re.sub("\^","",img_name[0])
                img_name[0] = re.sub("\&","",img_name[0])
                img_name[0] = re.sub("\*","",img_name[0])
                img_name[0] = re.sub("\+","",img_name[0])
                img_name[0] = re.sub("\=","",img_name[0])
                img_name[0] = re.sub("\,","",img_name[0])
                img_name[0] = re.sub("\"","",img_name[0])
                img_name[0] = re.sub("\'","",img_name[0])
                img_name[0] = re.sub("\/","",img_name[0])
                img_name[0] = re.sub("-","_",img_name[0])
                img_name[0] = re.sub("\s","_",img_name[0])
                img_name = ".".join(img_name)
            else:
                ext = img_name[-1]
                name = "_".join(img_name[:-1])
                img_name = name+"."+ext
            return img_name
        except Exception as e:
                print('Failed to clear image name. Reason: %s' % e)

def clear_car_name(car_name):
        if isinstance(car_name, str) and car_name != '' and car_name is not None:
            try:
                car_name = re.sub("\.","-",car_name)
                car_name = re.sub("\(","",car_name)
                car_name = re.sub("\)","",car_name)
                car_name = re.sub("\{","",car_name)
                car_name = re.sub("\}","",car_name)
                car_name = re.sub("\[","",car_name)
                car_name = re.sub("\]","",car_name)
                car_name = re.sub("\<","",car_name)
                car_name = re.sub("\>","",car_name)
                car_name = re.sub("\$","",car_name)
                car_name = re.sub("\#","",car_name)
                car_name = re.sub("\%","",car_name)
                car_name = re.sub("\~","",car_name)
                car_name = re.sub("\@","",car_name)
                car_name = re.sub("\^","",car_name)
                car_name = re.sub("\&","",car_name)
                car_name = re.sub("\*","",car_name)
                car_name = re.sub("\+","",car_name)
                car_name = re.sub("\=","",car_name)
                car_name = re.sub("\,","",car_name)
                car_name = re.sub("\"","",car_name)
                car_name = re.sub("\'","",car_name)
                car_name = re.sub("\/","",car_name)
                return car_name
            except Exception as e:
                print('Failed to clear car name. Reason: %s' % e)
        else:
            print("CLEAR Car Name EROOR", car_name)
#следит чтоб небило длины текста более 5000 символов
def text_len(text, lang):
        new_text = ''
        if(isinstance(text,str) and len(text)>1):
            if(len(text)>5000):
                i = 0
                while (i <= int(len(text)/4999)):
                    if(i == int(len(text)/4999)):
                        new_text += ko_translate(text[i*4999:len(text)],lang)
                    else:        
                        new_text += ko_translate(text[i*4999:i+1*4999], lang)
                    i+=1
            else: 
                new_text = ko_translate(text, lang)
            return new_text
        else:
            print("Translated Text is not STR or TEXT len more or equal 1")
            return
#витягуємо IP нашого парсера
def get_ip(html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            ip = soup.find('span', class_ = 'ip').text.strip()
            ua = soup.find('span', class_ = 'ip').find_next_sibling('span').text.strip()
            return (ip,ua)
        except Exception as e:
            print('Can\'t get MY IP. Reason %s.' % e)
#витягуємо html без сесії
def get_html(url, useragent=None, proxy=None):
    try:
        r = requests.get(url, headers=useragent, proxies=proxy)
        if r.status_code == 200:
            return r.text
        else: return r.status_code
    except Exception as e:
        print('Can\'t get HTML. Reason %s.' % e)
#залогінюємось на сайті
def login(login_link):
        try:
            session = HTMLSession()
            session.headers.update({'User-Agent': fake_useragent.UserAgent().random})
            login_data = {
                "userId": "152000",
                "userPwd": "4275",
                "resultCd": "",
                "checkId": "on"
            }
            r = session.request('POST', login_link, login_data, timeout=400)
            time.sleep(uniform(4,6))
            if(r.status_code == 200):
                return session
            else:
                print("Error to Login", r.status_code)
                session.close()
        except Exception as e:
            print('Can\'t login. Reason %s.' % e)
            session.close()
#пробег
def get_distance_driven(html):
        if(html != '' and html is not None):
            soup = BeautifulSoup(html, 'html.parser')
            try:
                res = re.findall("[0-9]+", str(soup.select("div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(1) > td:nth-child(4)")).strip())
                if(len(res)):
                    return int("".join(res))
            except Exception as e:
                print('Can\'t get driven distance. Reason %s.' % e)
                return
        else:
            print("Car Distance HTML is EMPTY or None")
            return
#топливо
def get_fuel(html):
        if(html != '' and html is not None):
            fulel_data = {
                "가솔린":"Бензин",
                "휘발유":"Бензин",
                "경유":"Бензин",
                "디젤":"Дизель",
                "LPG":"LPG",
                "하이브리드":"Гибрид",
                "LPI하이브리드":"LPG гибрид",
                "가솔린하이브리드":"Бензиновый гибрид",
                "디젤하이브리드": "Дизельный гибрид",
                "전기":"Электрокар",
                "가솔린/LPG":"Бензин/LPG"
            }
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if(len(soup.select("body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(4) > td:nth-child(4)"))):
                    return fulel_data[str(soup.select("body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(4) > td:nth-child(4)")[0].text.strip())]
            except Exception as e:
                print('Can\'t get fuel. Reason %s.' % e)
                return
        else:
            print("Car Fuel HTML is EMPTY or None")
            return
#марка авто
def get_car_mark(html):
        if(html != '' and html is not None):
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if(len(soup.select("body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > div > div > table > tbody > tr:nth-child(4) > td:nth-child(5)"))):
                    string = text_len(str(soup.select("body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > div > div > table > tbody > tr:nth-child(4) > td:nth-child(5)")[0].text.strip()),"en")
                    string = re.sub("\s?\?\s?","",string)
                    return string
                else:
                    return
            except Exception as e:
                print('Can\'t get car mark. Reason %s.' % e)
                return
        else:
            print("Car Mark HTML is EMPTY or None")
            return
#vin номер авто
def get_car_vin(html):
        if(html != '' and html is not None):
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if(len(soup.select("body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > div > div > table > tbody > tr:nth-child(7) > td"))):
                    return str(soup.select("body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > div > div > table > tbody > tr:nth-child(7) > td")[0].text.strip())
            except Exception as e:
                print('Can\'t get car vin code. Reason %s.' % e)
                return
        else:
            print("Car VIN HTML is EMPTY or None")
            return
#коробка передач
def get_transmission(html):
        if(html != '' and html is not None):
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if(len(soup.select("body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(2) > td:nth-child(4)"))):
                    if(soup.select("body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(2) > td:nth-child(4)")[0].text.strip() == "자동"):
                        return "Автомат"
                    else:
                        return "Механика"
            except Exception as e:
                print('Can\'t get transmission. Reason %s.' % e)
                return
        else:
            print("Car Transmission HTML is EMPTY or None")
            return
#фото авто
def get_img_src(html):
        if(html != '' and html is not None):
            soup = BeautifulSoup(html, 'html.parser')
            try:
                div = soup.find_all("div", class_="vehicle-thumbnail-detail")
                if(len(div)):
                    items = div[0].find_all("img")
                    images = []
                    counter = 0
                    numbers_photo = [1,3,6,10,11,12,16,19,25,26,27,28,29,30,31,32,33]         
                    for item in items:
                        counter = counter + 1
                        if(counter in numbers_photo):
                            if item.has_attr('src'):
                                download_images(item.get('src'))
                                images.append(item.get('src'))
                    return images      
            except Exception as e:
                print('Can\'t get img src. Reason %s.' % e)
                return
        else:
            print("SRC Images HTML is EMPTY or None")
            return
def get_img_str(imgs, html):
        if(html != '' and html is not None):
            try:
                title = get_car_title(html)
                if(title):
                    img_str = ''
                    for img in imgs :
                        str_arr = str(img).split('/')
                        str_arr.reverse()
                        name_arr = str_arr[0].split('.')
                        name = name_arr[0]
                        img_ext = name_arr[1].lower()
                        #img_name = clear_img_name(name)
                        img_str += name+'.'+img_ext+'[:param:][alt='+title+'][title='+title+']|'
                    return img_str[:-1]
            except Exception as e:
                print('Can\'t get Images str. Reason %s' % e)
                return
        else:
            print("Car Images HTML is EMPTY or None")
            return
#двигатель
def get_car_displacement(html):
        if(html != '' and html is not None):
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if(len(soup.select("body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(5) > td:nth-child(4)"))):
                    res = re.findall("[0-9]+", str(soup.select("body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(5) > td:nth-child(4)")[0].text.strip()))
                    return int("".join(res))
            except Exception as e:
                print('Can\'t get car displacement. Reason %s.' % e)
                return
        else:
            print("Car Engine HTML is EMPTY or None")
            return
#лот аукциона
def get_lot_id(html):
        soup = BeautifulSoup(html, 'html.parser')
        if(html != '' and html is not None): 
            try:
                if(len(soup.select("body > div.page-popup.exhibited-vehicle > div.vehicle-tit > p > strong"))):
                    return str(soup.select("div.vehicle-tit p.entry-num strong")[0].text.strip())
                else: 
                    return
            except Exception as e:
                print('Can\'t get lot id. Reason %s.' % e)
                return
        else:
            print("LOT ID ERROR", str(soup.select("div.vehicle-tit p.entry-num strong")[0].text.strip()))
#название авто
def get_car_title(html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            if(soup.find("h2", class_="tit")):
                print(clear_car_name(ko_translate(rm_new_line(soup.find("h2").text.strip()))))
                return clear_car_name(ko_translate(rm_new_line(soup.find("h2").text.strip())))
            else:
                print("Can\'t find TITLE (CAR NAME)")
                return
        except Exception as e:
            get_car_title(html)
            print('Can\'t get title. Reason %s.' % e)
#витягуємо оцінку авто
def get_car_estimate(html):
        if(html != '' and html is not None):
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if(len(soup.select("body > div.page-popup.exhibited-vehicle > div.clfix > div.vehicle-info > ul > li:nth-child(4) > strong"))):
                    return ko_translate(rm_new_line(str(soup.select("body > div.page-popup.exhibited-vehicle > div.clfix > div.vehicle-info > ul > li:nth-child(4) > strong")[0].text.strip())), "en")
            except Exception as e:
                print('Can\'t get car estimate. Reason %s.' % e)
                return
        else:
            print("Car Mark HTML is EMPTY or None")
            return
#год автомобиля
def get_car_year(html):
        if(html != '' and html is not None):
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if(len(soup.select("div.vehicle-detail > div.vehicle-detail-view > div.vehicle-detail > div.vehicle-detail_bar > table tr:nth-child(1) > td"))):
                    res = re.match("[0-9]+", str(soup.select("div.vehicle-detail > div.vehicle-detail-view > div.vehicle-detail > div.vehicle-detail_bar > table tr:nth-child(1) > td")[0].text.strip()))
                    if(res):
                        return int(res.group())
            except Exception as e:
                print('Can\'t get car year. Reason %s.' % e)
                return
        else:
            print("Car year HTML is EMPTY or None")
            return
#цвет автомобиля
def get_car_color(html):
        if(html != '' and html is not None):
            color_data = {
                "흰색":"Белый",
                "쥐색":"Серый",
                "은색":"Серебро",
                "검정":"Черный",
                "기타":"Так далее",
                "빨간":"Красный",
                "보라색":"Фиолетовый",
                "주황색":"Оранжевый",
                "초록":"Зеленый",
                "회색":"Серый",
                "금":"Золото",
                "푸른":"Голубой",
                "베이지":"Бежевый",
                "진주":"Жемчужина"
            }
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if(len(soup.select("div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(3) > td:nth-child(4)"))):
                    return color_data[re.sub("\s.+","", soup.select("div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(3) > td:nth-child(4)")[0].text.strip())]
            except Exception as e:
                print('Can\'t get car color. Reason %s.' % e)
                return
        else:
            print("Car color HTML is EMPTY or None")
            return
#тип автомобиля
def get_car_type(html):
        if(html != '' and html is not None):
            car_type_data = {
                "승용 (7인승)":"Универсал",
                "승용 (11인승)":"Фургон",
                "승합 (12인승)":"Фура",
                # "Трактор",
                "승용 (5인승)":"Седан",
                # "Родстер",
                "픽업":"Пикап",
                # "Мотоцикл",
                "화물":"Фрахт",
                "승용 (9인승)":"Минивен",
                "승용 (4인승)":"Хэтчбек",
                "승용/SUV": "Кроссовер",
                "승용 (2인승)":"Купе",
                "승합":"Кабриолет"
                # "Багги"
            }
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if(len(soup.select("div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(6) > td:nth-child(2)"))):
                    return car_type_data[soup.select("div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(6) > td:nth-child(2)")[0].text.strip()]
            except Exception as e:
                print('Can\'t get car type. Reason %s.' % e)
                return
        else:
            print("Car type HTML is EMPTY or None")
            return
#запись айди авто в файл
def write_car_id(file_name, data):
    try:
        return open(file_name, "a").write(data)
    except Exception as e:
        print('Can\'t wrine file %s. Reason %s.' % (file_name,e))
#цена автомобиля 
def get_car_price(html):
        if(html != '' and html is not None):
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if(len(soup.select("body > div.page-popup.exhibited-vehicle > div.clfix > div.vehicle-info > p > strong > em"))):
                    return int((float("".join(soup.select("body > div.page-popup.exhibited-vehicle > div.clfix > div.vehicle-info > p > strong > em")[0].text.strip().split(",")))*10000)/float(config['LOTTE']['USDCOURSE']))
            except Exception as e:
                print('Can\'t get car price. Reason %s.' % e)
                return
        else:
            print("Car price HTML is EMPTY or None")
            return
#описание авто 
def get_car_description(html):
    if(html != '' and html is not None):
        description = ''
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find_all("table", class_="tbl-v02")
        div = soup.find_all("div", class_="car-status-map")
        video = soup.find("div", id="yesMovie")
        if div:
            try:
                description += '<h2 class="page-subtit mt60">Протокол осмотра автомобилей, выставленных на аукцион</h2>'
                description += text_len(rm_new_line(str(table[0]).strip()), "ru")
            except Exception as e:
                print('Can\'t get car description "Performance Evaluation Information". Reason %s.' % e)
            try:
                description += '<h2 class="page-subtit mt60">Детали автомобиля</h2>'
                description += text_len(rm_new_line(str(table[1]).strip()), "ru")
            except Exception as e:
                print('Can\'t get car description "Option information". Reason %s.' % e)
            try:   
                description += '<h2 class="page-subtit mt60">Состояние кузова автомобиля</h2>'
                description += text_len(rm_new_line(str(div[0]).strip()), "ru")
                description += text_len(rm_new_line(str(table[2]).strip()), "ru")
            except Exception as e:
                print('Can\'t get car descritpion comm list. Reason %s.' % e)
            try:
                description += '<h2 class="page-subtit mt60">Видео автомобиля</h2>'
                description += re.sub('/uploadFiles/','https://imgmk.lotteautoauction.net/', str(video).strip())#str(video).strip() #
            except Exception as e:
                print('Can\'t get car description image. Reason %s.' % e)
        return description
    else:
        print("Car description HTML is EMPTY or None")
        return

#категория для авто
def get_car_category(cat):
        try:
            categoty_data = {
                "Genesis":"Genesis",
                "KI":"Kia Motors",
                "HD":"Hyundai",
                "SY":"SsangYong",
                "SS":"Renault",
                "BT":"Mercedes Benz",
                "DW":"Chevrolet",
                "JA":"Jaguar",
                "BM":"BMW",
                "LR":"Land Rover",
                "PU":"Peugeot",
                "VK":"Volkswagen",
                "NI":"Nissan",
                "Jeep":"Jeep",
                "Lexus":"Lexus",
                "LEXUS": "Lexus",
                "LI":"Lincoln",
                "Mini":"Mini Cooper",
                "CA":"Cadillac",
                "TO":"Toyota",
                "Tesla":"Tesla",
                "AD":"Audi",
                "BE":"Bentley",
                "AS":"Aston Martin",
                "CL":"Chrysler",
                "CT":"Citroen",
                "FE":"Ferrari",
                "FT":"Fiat",
                "FO":"Ford",
                "HO":"Honda",
                "LA":"Lamborghini",
                "LC":"Lancia",
                "MA":"Maserati",
                "MI":"Mitsubishi",
                "PO":"Porsche",
                "SA": "SAAB",
                "SR":"Subaru",
                "VO":"Volvo",
                "SZ":"Suzuki",
                "RR":"Rolls Royce",
                "TT":"Daewoo",
                "SOUL": "Kia Motors",
                "GRANDEUR": "Hyundai",
                "AVANTE": "Hyundai",
                "GENESIS": "Hyundai",
                "ACCENT": "Hyundai",
                "TUCSON": "Hyundai",
                "SONATA": "Hyundai",
                "SANTAFE": "Hyundai",
                "KONA": "Hyundai",
                "SOLATI": "Hyundai",
                "MAXCRUZ": "Hyundai",
                "ASLAN": "Hyundai",
                "K3": "Kia Motors",
                "PORTER": "Hyundai",
                "K8": "Kia Motors",
                "COLORADO": "Chevrolet",
                "I30": "Hyundai",
                "BONGO": "Kia Motors",
                "EQUIUS": "Hyundai",
                "VERACRUZ": "Hyundai",
                "FORTE": "Kia Motors"
            }
            if(cat is not None):
                return categoty_data[cat]
            else:
                print("Car category HTML is EMPTY or None")
                return
        except Exception as e:
            print('Can\'t get car category. Reason %s.' % e)
            return

#год первой регистрации автомобиля
def get_car_registration(html):
        if(html != '' and html is not None):
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if(len(soup.select("div.vehicle-detail div.vehicle-detail-view div.vehicle-detail_bar table.tbl-v02 tr:nth-child(2) td"))>2):
                    registration = soup.select("div.vehicle-detail div.vehicle-detail-view div.vehicle-detail_bar table.tbl-v02 tr:nth-child(2) td")[2].text.strip()
                    return re.sub("\.","/",registration)
            except Exception as e:
                print('Can\'t get car registration. Reason %s.' % e)
                return
        else:
            print("Car year first registration HTML is EMPTY or None")
            return
def get_car_category_url(category=None):
        try:
            categoty_url_data = {
                "Genesis":"genesis",
                "Kia Motors":"kia-motors",
                "Hyundai":"hyundai",
                "SsangYong":"ssangyong",
                "Renault":"renault",
                "Mercedes Benz":"mercedes-benz",
                "Chevrolet":"chevrolet",
                "Jaguar":"jaguar",
                "BMW":"bmw",
                "Land Rover":"land-rover",
                "Peugeot":"peugeot",
                "Volkswagen":"volkswagen",
                "Ford":"ford",
                "Audi":"audi",
                "Bentley":"bentley",
                "Cadillac":"cadillac",
                "Aston Martin":"aston-martin",
                "Chrysler":"chrysler",
                "Citroen":"citroen",
                "Ferrari":"ferrari",
                "Fiat":"fiat",
                "Ford":"ford",
                "Honda":"honda",
                "Lamborghini":"lamborghini",
                "Lancia":"lancia",
                "Maserati":"maserati",
                "Mitsubishi":"mitsubishi",
                "Porsche":"porsche",
                "SAAB": "saab",
                "Subaru":"subaru",
                "Volvo":"volvo",
                "Suzuki":"suzuki",
                "Rolls Royce":"rolls-royce",
                "Daewoo":"daewoo",
                "Nissan":"nissan",
                "Toyota":"toyota"
            }
            if(category is not None):
                return categoty_url_data[category]
        except Exception as e:
            print('Can\'t get car category url. Reason %s.' % e)
            return
#ID авто для парсингу
def get_car_id(html, marker):
    if(html != '' and html is not None):
        soup = BeautifulSoup(html, 'html.parser')
        try:
            items = soup.find_all("td", class_="align-l")
            for item in items:
                car_id = re.search('"([A-Z]{2})"."([A-Z]{2}\d{12})"."(\d)"', item.find("p", class_="txt").find("a", class_="a_list").get('onclick'))
                if car_id:
                    write_car_id("car_id2.txt",car_id.group(1)+"|"+car_id.group(2)+"|"+car_id.group(3)+"|"+marker+"\n")
        except Exception as e:
            print('Can\'t get car id. Reason %s.' % e)
            return
    else:
        print("Car ID HTML is EMPTY or None")
        return
#function working with mysql
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")
#ID нових авто, что добавились, для парсингу 
def get_missed_car_id(html):
    if(html != '' and html is not None):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find("table", class_="tbl-t02").select("tbody tr")
        for item in items: #index, enumerate(items)
            try:
                lot_id = item.select("td")[1].text.strip()
            except Exception as e:
                print('Can\'t get lot_id. Reason %s.' % e)
            try:
                car_name = clear_car_name(ko_translate(item.find("td", class_="align-l").find("p", class_="txt").find("a", class_="a_list").text.strip()))
            except Exception as e:
                print('Can\'t get car_name. Reason %s.' % e)
            try:
                car_name = re.sub("LF|ALL NEW|THE NEW|THE NEXT","",car_name)
            except Exception as e:
                print('Can\'t regular replace. Reason %s.' % e)
            res = car_name.split()
            result = execute_read_query(db_connection, "SELECT mg_product.id, mg_product.price, mg_product.title FROM mg_product WHERE LOWER(mg_product.title) LIKE LOWER('"+lot_id+"%') AND mg_product.activity=1;")
            if(len(result) == 0):
                category_name = execute_read_query(db_connection,"SELECT mg_category.title FROM mg_category LEFT JOIN mg_product ON mg_category.id = mg_product.cat_id WHERE mg_category.id = (SELECT mg_product.cat_id FROM mg_product WHERE LOWER(mg_product.title) LIKE LOWER('%"+res[0]+"%') LIMIT 1);")
                if(len(category_name) > 0):
                    if(len(category_name[0]) > 0):
                        category_name = category_name[0][0]
                        print("Car lot id:", lot_id, "Car name:", car_name, "Category name:", category_name)
                if(category_name):
                    cat_mark = None
                else:
                    cat_mark = res[0]
                if(category_name == "Renault"):
                    cat_mark = 'SS'
                elif(category_name == "Kia Motors"):
                    cat_mark = 'KI'
                elif(category_name == "Hyundai"):
                    cat_mark = 'HD'
                elif(category_name == "BMW"):
                    cat_mark = 'BM'
                elif(category_name == "Audi"):
                    cat_mark = 'AD'
                elif(category_name == "Chevrolet"):
                    cat_mark = 'DW'
                elif(category_name == "SsangYong"):
                    cat_mark = 'SY'
                elif(category_name == "Bentley"):
                    cat_mark = 'BE'
                elif(category_name == "Cadillac"):
                    cat_mark = 'CA'
                elif(category_name == "Aston Martin"):
                    cat_mark = 'AS'
                elif(category_name == "Mercedes Benz"):
                    cat_mark = 'BT'
                elif(category_name == "Jaguar"):
                    cat_mark = 'JA'
                elif(category_name == "Land Rover"):
                    cat_mark = 'LR'
                elif(category_name == "Peugeot"):
                    cat_mark = 'PU'
                elif(category_name == "Volkswagen"):
                    cat_mark = 'VK'
                elif(category_name == "Nissan"):
                    cat_mark = 'NI'
                elif(category_name == "Lincoln"):
                    cat_mark = 'LI'
                elif(category_name == "Toyota"):
                    cat_mark = 'TO'
                elif(category_name == "Chrysler"):
                    cat_mark = 'CL'
                elif(category_name == "Citroen"):
                    cat_mark = 'CT'
                elif(category_name == "Ferrari"):
                    cat_mark = 'FE'
                elif(category_name == "Fiat"):
                    cat_mark = 'FT'
                elif(category_name == "Ford"):
                    cat_mark = 'FO'
                elif(category_name == "Honda"):
                    cat_mark = 'HO'
                elif(category_name == "Lamborghini"):
                    cat_mark = 'LA'
                elif(category_name == "Lancia"):
                    cat_mark = 'LC'
                elif(category_name == "Maserati"):
                    cat_mark = 'MA'
                elif(category_name == "Mitsubishi"):
                    cat_mark = 'MI'
                elif(category_name == "Porsche"):
                    cat_mark = 'PO'
                elif(category_name == "SAAB"):
                    cat_mark = 'SA'
                elif(category_name == "Subaru"):
                    cat_mark = 'SR'
                elif(category_name == "Volvo"):
                    cat_mark = 'VO'
                elif(category_name == "Suzuki"):
                    cat_mark = 'SZ'
                elif(category_name == "Rolls Royce"):
                    cat_mark = 'RR'
                elif(category_name == "Daewoo"):
                    cat_mark = 'TT'
                car_id = re.search('"([A-Z]{2})"."([A-Z]{2}\d{12})"."(\d)"', item.find("p", class_="txt").find("a", class_="a_list").get('onclick'))
                if car_id:
                    write_car_id("missed_car_id2.txt",car_id.group(1)+"|"+car_id.group(2)+"|"+car_id.group(3)+"|"+cat_mark+"\n")
    else:
        return

#парсимо всі ссилки на недостаючі авто по сторінкам
def get_missed_car_pages(page_start=1, page_end=2):
    for i in range(page_start,page_end):
        unf = uniform(1,8)
        time.sleep(unf)
        print("Page %d. Sleep %d." % (i, unf))
        parser(config['LOTTE']['URL']+"?searchPageUnit=20&pageIndex="+str(i), get_missed_car_id)
    pass
#парсимо сайт із сесії
def parser(link, func=None, marker=None):
    if(link and link is not None):
        data = ''
        session = login(config['LOTTE']['LOGIN_LINK'])
        try:
            r = session.request('GET', link)
            time.sleep(uniform(2,3))
            if r.status_code == 200:
                #r.html.render(timeout=400)
                if func is not None and marker is None:
                    data = func(r.html.html)
                    session.close()
                    return data
                elif(func is not None and marker is not None):
                    data = func(r.html.html, marker)
                    session.close()
                    return data
                else:
                    data = r.html.html
                    session.close()
                    return data
            else:
                print("PARSE ERROR", r.status_code)
                session.close()
        except Exception as e:
            print('Can\'t get html from site. Reason %s.' % e)
            if(config['LOTTE']['FTPCODE'] == '1'):
                parsed_link = parse.parse_qs(parse.urlsplit(link).query)
                write_car_id("missed_car_id2.txt",urllib.parse.quote_plus(parsed_link['searchMngDivCd'][0])+"|"+urllib.parse.quote_plus(parsed_link['searchMngNo'][0])+"|"+urllib.parse.quote_plus(parsed_link['searchMngNo'][0])+"|"+urllib.parse.quote_plus(parsed_link['searchExhiRegiSeq'][0])+"|"+marker+"\n")
                session.close()

#парсимо всі ссилки на авто по сторінкам
def get_pages(page_start=1, page_end=2, page_unit=20, search_maker="KI"):
    for i in range(page_start,page_end+1):
        unf = uniform(2,6)
        time.sleep(unf)
        print("Page %d. Sleep %d." % (i, unf))
        parser(config['LOTTE']['URL']+"?searchPageUnit="+str(page_unit)+"&pageIndex="+str(i)+"&set_search_maker="+str(search_maker), get_car_id, search_maker)
    pass
#складаємо всі ссилки на авто в один файл
def get_all_links(car_link, file_name="car_id2.txt"):
    data = read_file(file_name, "\n")
    res = list(map(lambda x: x.split('|'), data[:-1]))
    return list(map(lambda x: ['{}?refererMode=login&searchMngDivCd={}&searchMngNo={}&searchExhiRegiSeq={}'.format(car_link, x[0], x[1], x[2]), x[3]], res))
#закачуємо усі картинки
def download_images(img_urls, folder_name='py_img2'):
    try:
        if(isinstance(img_urls, list)):
            for img_url in img_urls:
                str_arr = str(img_url).split('/')
                str_arr.reverse()
                name_arr = str_arr[0].split('.')
                name = name_arr[0]
                img_ext = name_arr[1].lower() 
                #img_name = clear_img_name(name)
                if(config['LOTTE']['FTPCODE'] == '1'):
                    img_data = BytesIO(requests.get(img_url).content) #without BytesIO if you whant download to local machine
                    ftpCommand = "STOR %s"%name #comment if you whant download to local machine
                    ftp.storbinary(ftpCommand, fp=img_data) #comment if you whant download to local machine
                else:
                    img_data = requests.get(img_url).content
                    with open('./'+folder_name+'/'+name+'.'+img_ext, 'wb') as handler:
                        handler.write(img_data)
        else:
            str_arr = str(img_urls).split('/')
            str_arr.reverse()
            name_arr = str_arr[0].split('.')
            name = name_arr[0]
            img_ext = name_arr[1].lower() 
            #img_name = clear_img_name(name)
            if(config['LOTTE']['FTPCODE'] == '1'):
                img_data = BytesIO(requests.get(img_urls).content) #without BytesIO if you whant download to local machine
                ftpCommand = "STOR %s"%name #comment if you whant download to local machine
                ftp.storbinary(ftpCommand, fp=img_data) #comment if you whant download to local machine
            else:
                img_data = requests.get(img_urls).content
                with open('./'+folder_name+'/'+name+'.'+img_ext, 'wb') as handler:
                    handler.write(img_data)
    except Exception as e:
        print('Failed download image. Reason: %s' % e)
def rm_csv(name = "data2.csv"):
        try:
            if(os.path.exists(name)):
                os.remove(name)
            print("File %s Removed!" % name)
        except Exception as e:
                print('Failed to remove file %s. Reason: %s' % (name, e))
def create_csv(name = "data2.csv"):
    path = os.getcwd() + os.path.sep + name
    try:
        with open(path, 'w', encoding="utf-8", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Категория', 'URL категории', 'Товар', 'Вариант', 'Описание', 'Цена', 'URL', 'Изображение', 'Артикул', 'Количество', 'Активность', 'Заголовок [SEO]', 'Ключевые слова [SEO]', 'Описание [SEO]', 'Старая цена', 'Рекомендуемый', 'Новый', 'Сортировка', 'Вес', 'Связанные артикулы', 'Смежные категории', 'Ссылка на товар', 'Валюта', 'Свойства'])
    except Exception as e:
            print('Failed to create file %s. Reason: %s' % (name, e))
def create_txt(name):
    path = os.getcwd() + os.path.sep + name
    try:
        open(path, 'w', encoding="utf-8", newline='')
    except Exception as e:
            print('Failed to create file %s. Reason: %s' % (name, e))
#записуємо усі данні у файл
def write_csv(data, name = "data2.csv"):
    path = os.getcwd() + os.path.sep + name
    try: 
        with open(path, 'a', encoding="utf-8", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([data['category'], data['category_url'], data['title'], ' ', data['description'], data['price'], data['url'], data['images'], data['article'], data['count'], data['activation'], data['title-seo'], ' ', ' ', ' ', data['recomended'], data['new'], '0', '0', ' ', ' ', ' ', data['currency'], data['properties']])
    except Exception as e:
        print('Can\'t write %s file. Reason %s' % (name, e))
#створюємо папку
def create_folder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        print('Can\'t create folder in path %s. Reason %s' % path, e)

#витягуємо максимальне число сторінок
def get_max_page(html, pages=20):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        max_page = soup.select("body > div.layout-wrap > div.layout-container > div.layout-content > div.exhibition-list-tbl > div.tbl-top > p:nth-child(2) > span > em")[0].text.strip()
        max_page = int(re.sub("\,","", max_page))
        if(max_page % pages > 0):
            return int(max_page/pages) + 1
        else:
            return int(max_page/pages)
    except Exception as e:
        print('Can\'t get max page. Reason %s' % e)

#очищаємо усі файли із папки
def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
#витягуємо курс валют 
# def get_currency(): 
#     try:
#         html = get_shtml("https://www.currencyconverterx.com/KRW/USD/1000000")
#         soup = BeautifulSoup(html, 'html.parser')
#         return float(soup.select("#converterForm > div.convert-form__result > strong > span.convert-form__c3")[0].text.strip())
#     except Exception as e:
#         print('Can\'t get currency. Reason: %s' % e)
#krw_to_usd = get_currency()
#витягуємо всі данні на авто
def get_car(link):
    # p = current_process()
    # if(p.name != 'MainProcess'):
    #     print('process counter:', p._identity[0], 'pid:', os.getpid())
    if(link):
        try:
            html = parser(link[0])
            if(html is not None):
                car = {}
                lot_number = get_lot_id(html) or "None"
                title = get_car_title(html) or "None"
                category = get_car_category(link[1]) or "None"

                car_mark = get_car_mark(html) or "None"
                if category != "None" and car_mark != "None" :
                    mark = category + ' ' + car_mark.upper()
                else:
                    mark = "None"

                year = get_car_year(html) or "2012"
                color = get_car_color(html) or "None"
                car_type = get_car_type(html) or "Седан"
                distance_driven = get_distance_driven(html) or "10000"
                displacement = get_car_displacement(html) or "None"
                transmission = get_transmission(html) or "Механика"
                fuel = get_fuel(html) or "Бензин"
                car_vin = get_car_vin(html) or "None"
                car_estimate = get_car_estimate(html) or "None"
                registration = get_car_registration(html) or "None"
                mark_url = re.sub("\.", "", mark)            
                mark_url = re.sub("\(", "", mark_url)                                
                mark_url = re.sub("\)", "", mark_url)
                mark_url = re.sub("\s", "-", mark_url)
                car['url'] = car_vin.lower()+"-"+mark_url.lower()
                car['category'] = category
                car['category_url'] = get_car_category_url(category)
                car['title'] = lot_number + " " + title
                car['title-seo'] = car['title']
                car['article'] = lot_number
                car['price'] = get_car_price(html) or "0"
                car['description'] = rm_new_line(get_car_description(html)) or "None"
                car['images'] = get_img_str(get_img_src(html), html) or "None"
                car['count'] = '0'
                car['activation'] = '1'
                car['currency'] = 'USD'
                car['recomended'] = '0'
                car['new'] = '0'
                car['properties'] = 'Цвет=[type=assortmentCheckBox value=%s product_margin=Желтый|Белый|Серебро|Красный|Фиолетовый|Оранжевый|Зеленый|Серый|Золото|Коричневый|Голубой|Черный|Бежевый]&Кузов=[type=assortmentCheckBox value=%s product_margin=Универсал|Фургон|Фура|Трактор|Седан|Родстер|Пикап|Мотоцикл|Минивен|Хэтчбек|Кроссовер|Купе|Кабриолет|Багги]&Пробег=%s&Двигатель=%s&Год=%s&Первая регистрация=%s&Трансмиссия=[type=assortmentCheckBox value=%s product_margin=Механика|Автомат]&Топливо=[type=assortmentCheckBox value=%s product_margin=Дизель|Бензин|Газ]&Модель=%s&Марка=%s&Номер лота=%s&Оценка автомобиля=%s&VIN номер=%s&Аукцион=lotteautoauction %s' % (str(color), str(car_type), str(distance_driven), str(displacement), str(year), str(registration), str(transmission), str(fuel), str(mark), str(category), str(lot_number), str(car_estimate), str(car_vin), str(config['LOTTE']['AUCTIONDATE']))
                if(title != "None" and lot_number != "None" and category != "None"):
                    return write_csv(car) 
                else:
                    print('Failed to get Car')
                    get_car(link)
            else:
                print('Get Car HTML IS NONE')
        except Exception as e:
            print('Failed to get Car %s. Reason: %s' % (link, e))

def main():
    time_start = time.time()
    if(config['LOTTE']['AUTOCODE'] == '0'):
        rm_csv("car_id2.txt")
        create_txt("car_id2.txt")
        categories = [config['LOTTE']['CATEGORY']] if not len(config['LOTTE']['CATEGORIES'].split(","))>1 else config['LOTTE']['CATEGORIES'].split(",")
        for category in categories:
            print(category)
            if(category == "Renault"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=SS&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SS')
            elif(category == "Kia Motors"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=KI&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'KI')
            elif(category == "Hyundai"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=HD&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'HD')
            elif(category == "BMW"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=BM&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'BM')
            elif(category == "Audi"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=AD&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'AD')
            elif(category == "Chevrolet"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=DW&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'DW')
            elif(category == "SsangYong"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=SY&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SY')
            elif(category == "Bentley"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=BE&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'BE')
            elif(category == "Cadillac"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=CA&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'CA')
            elif(category == "Aston Martin"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=AS&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'AS')
            elif(category == "Mercedes Benz"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=BT&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'BT')
            elif(category == "Jaguar"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=JA&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'JA')
            elif(category == "Land Rover"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=LR&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'LR')
            elif(category == "Peugeot"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=PU&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'PU')
            elif(category == "Volkswagen"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=VK&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'VK')
            elif(category == "Nissan"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=NI&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'NI')
            elif(category == "Lincoln"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=LI&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'LI')
            elif(category == "Toyota"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=TO&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'TO')
            elif(category == "Chrysler"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=CL&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'CL')
            elif(category == "Citroen"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=CT&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'CT')
            elif(category == "Ferrari"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=FE&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'FE')
            elif(category == "Fiat"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=FT&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'FT')
            elif(category == "Ford"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=FO&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'FO')
            elif(category == "Honda"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=HO&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'HO')
            elif(category == "Lamborghini"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=LA&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'LA')
            elif(category == "Lancia"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=LC&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'LC')
            elif(category == "Maserati"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=MA&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'MA')
            elif(category == "Mitsubishi"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=MI&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'MI')
            elif(category == "Porsche"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=PO&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'PO')
            elif(category == "SAAB"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=SA&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SA')
            elif(category == "Subaru"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=SR&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SR')
            elif(category == "Volvo"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=VO&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'VO')
            elif(category == "Suzuki"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=SZ&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SZ')
            elif(category == "Rolls Royce"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=RR&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'RR')
            elif(category == "Daewoo"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=TT&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'TT')
    elif(config['LOTTE']['AUTOCODE'] == '1'):
        rm_csv()
        create_csv()
        create_folder('./py_img2')
        clear_folder('./py_img2/')
        my_list = get_all_links(config['LOTTE']['CAR_LINK'])
        with Pool(20) as p:
            p.map(get_car, my_list) 
        if(config['LOTTE']['FTPCODE'] == '1'):
            ftp.quit()
    elif(config['LOTTE']['AUTOCODE'] == '2'):
        rm_csv("missed_car_id2.txt")
        max_page = parser(config['LOTTE']['URL']+"?searchPageUnit=20&pageIndex=1", get_max_page)
        print(max_page)
        get_missed_car_pages(1,max_page)#1,max_page
    elif(config['LOTTE']['AUTOCODE'] == '3'):
        rm_csv("car_id2.txt")
        create_txt("car_id2.txt")
        categories = [config['LOTTE']['CATEGORY']] if not len(config['LOTTE']['CATEGORIES'].split(","))>1 else config['LOTTE']['CATEGORIES'].split(",")
        for category in categories:
            print(category)
            if(category == "Renault"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=SS&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SS')
            elif(category == "Kia Motors"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=KI&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'KI')
            elif(category == "Hyundai"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=HD&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'HD')
            elif(category == "BMW"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=BM&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'BM')
            elif(category == "Audi"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=AD&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'AD')
            elif(category == "Chevrolet"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=DW&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'DW')
            elif(category == "SsangYong"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=SY&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SY')
            elif(category == "Bentley"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=BE&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'BE')
            elif(category == "Cadillac"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=CA&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'CA')
            elif(category == "Aston Martin"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=AS&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'AS')
            elif(category == "Mercedes Benz"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=BT&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'BT')
            elif(category == "Jaguar"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=JA&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'JA')
            elif(category == "Land Rover"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=LR&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'LR')
            elif(category == "Peugeot"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=PU&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'PU')
            elif(category == "Volkswagen"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=VK&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'VK')
            elif(category == "Nissan"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=NI&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'NI')
            elif(category == "Lincoln"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=LI&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'LI')
            elif(category == "Toyota"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=TO&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'TO')
            elif(category == "Chrysler"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=CL&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'CL')
            elif(category == "Citroen"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=CT&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'CT')
            elif(category == "Ferrari"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=FE&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'FE')
            elif(category == "Fiat"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=FT&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'FT')
            elif(category == "Ford"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=FO&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'FO')
            elif(category == "Honda"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=HO&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'HO')
            elif(category == "Lamborghini"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=LA&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'LA')
            elif(category == "Lancia"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=LC&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'LC')
            elif(category == "Maserati"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=MA&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'MA')
            elif(category == "Mitsubishi"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=MI&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'MI')
            elif(category == "Porsche"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=PO&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'PO')
            elif(category == "SAAB"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=SA&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SA')
            elif(category == "Subaru"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=SR&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SR')
            elif(category == "Volvo"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=VO&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'VO')
            elif(category == "Suzuki"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=SZ&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SZ')
            elif(category == "Rolls Royce"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=RR&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'RR')
            elif(category == "Daewoo"):
                s_page = parser(config['LOTTE']['URL']+"?set_search_maker=TT&searchPageUnit=20&pageIndex=1", get_max_page)
                get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'TT')
        rm_csv()
        create_csv()
        create_folder('./py_img2')
        clear_folder('./py_img2/')
        my_list = get_all_links(config['LOTTE']['CAR_LINK'])
        with Pool(20) as p:
            p.map(get_car, my_list) 
        if(config['LOTTE']['FTPCODE'] == '1'):
            ftp.quit()
    time_end = time.time() 
    print(time_end - time_start)
if __name__ == '__main__':
    main()