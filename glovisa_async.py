# -*- coding: utf-8 -*-
from weakref import proxy
from async_timeout import asyncio
from random import uniform, choice
from deep_translator import GoogleTranslator
from addnewproduct import AddNewProduct
from datetime import datetime
import requests
import aiofiles
import urllib.parse
import mysql.connector as mysql
import configparser
import fake_useragent
import time
import os
import aiohttp
import re
import json
import csv
config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini")

class GlovisaAsync:
    add_p = AddNewProduct()
    sema = asyncio.BoundedSemaphore(5)

    # записуємо усі данні у файл
    def write_csv(self, data, name = "data3.csv"):
        path = os.getcwd() + os.path.sep + name
        try: 
            with open(path, 'a', encoding="utf-8", newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([data['category'], data['category_url'], data['title'], ' ', data['description'], data['price'], data['url'], data['images'], data['article'], data['count'], data['activation'], data['title-seo'], ' ', ' ', ' ', data['recomended'], data['new'], '0', '0', ' ', ' ', ' ', data['currency'], data['properties']])
        except Exception as e:
            print('Can\'t write csv file. Reason %s' % e)

    # translate function
    def ko_translate(self, text, lan):
        try:
            if(len(text)>1 and len(text)<5000 and isinstance(text,str)):
                return GoogleTranslator(source='ko', target=lan).translate(text)
        except Exception as e:
            print('Failed to Translate text. Reason: %s' % e)

    # read file function
    def read_file(self, file_name, delimiter="\n"):
        try:
            return open(file_name).read().split(delimiter)
        except Exception as e:
            print('Can\'t read File.')

    # get data function
    async def fetch(self, url):
        proxy = { 'http': 'http://' + choice(self.read_file("proxies.txt","\n")) +'/' }
        self.asession.proxies.update(proxy)
        try:
            time.sleep(uniform(4,6))
            r = await self.asession.get(url)
            return r
        except Exception as e:
            print('Fatch ERROR %s' % e)

    def get_category(self, title):
        categoty_data = {
            "Porsche": "Porsche",
            "Genesis": "Genesis",
            "Kia": "Kia Motors",
            "Hyundai": "Hyundai",
            "Modern": "Hyundai",
            "Ssangyong": "SsangYong",
            "SsangYong": "SsangYong",
            "Renault Samsung": "Renault",
            "Renault": "Renault",
            "Benz": "Mercedes Benz",
            "Chevrolet": "Chevrolet",
            "Chevrolet (Daewoo)": "Chevrolet",
            "Jaguar": "Jaguar",
            "BMW": "BMW",
            "Land Rover": "Land Rover",
            "Peugeot": "Peugeot",
            "Volkswagen": "Volkswagen",
            "Ford": "Ford",
            "Nissan": "Nissan",
            "Jeep": "Jeep",
            "Lexus": "Lexus",
            "Honda": "Honda",
            "Lincoln": "Lincoln",
            "Mini": "Mini Cooper",
            "Cadillac": "Cadillac",
            "Toyota": "Toyota",
            "Tesla": "Tesla",
            "Audi": "Audi",
            "Chrysler": "Chrysler",
            "Volvo": "Volvo",
            "Citroen": "Citroen",
            "Infinity": "Infinity",
            "Maserati": "Maserati",
            "Dodge": "Dodge"
        }
        category = re.findall(r'\[(.+)\]',title)[0]
        return categoty_data[category]

    def get_category_url(self, category):
        categoty_url_data = {
            "Porsche":"porsche",
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
            "Nissan":"nissan",
            "Jeep":"jeep",
            "Lexus":"lexus",
            "Honda":"honda",
            "Lincoln":"lincoln",
            "Mini Cooper":"mini-cooper",
            "Cadillac":"cadillac",
            "Toyota":"toyota",
            "Tesla":"tesla",
            "Audi":"audi",
            "Volvo":"volvo",
            "Chrysler":"chrysler",
            "Citroen":"citroen",
            "Infinity":"infinity",
            "Maserati":"maserati",
            "Dodge":"dodge"
        }
        return categoty_url_data[category]

    #цвет автомобиля
    def get_car_color(self, car_color):
        color_data = {
            "IM)티타늄실버(메탈포인트)":"Серебро",
            "GW7)스플래쉬블루":"Синий",
            "U4)백진주색":"Белый",
            "UYH)우유니화이트":"Белый", 
            "Y8Y)미스틱베이지":"Бежевый",
            "BAS)댄디블루":"Красный",
            "RAM)플라밍레드":"Красный",
            "A3D)은빛실버":"Серебро",
            "WAB)바닐라화이트":"Белый",
            "AEQ)아쿠아민트":"Акваминт",
            "T8T)플래티넘실버":"Серебро",
            "NA2)골드코스트실버":"Серебро",
            "N9V)이온실버":"Серебро", 
            "N4B)마리나블루":"Синий",  
            "A2R)샤이니레드":"Красный",
            "SWP)스노우 화이트 펄":"Белый",
            "D9B)딥크로마블루":"Синий",
            "2BS)댄디블루 투톤":"Голубой",
            "GV2)미스틱바이올렛":"Фиолетовый", 
            "EB)흑진주":"Черный",
            "U9G)루나그레이":"Серый",
            "PH3)비크블랙":"Черный",
            "Y2S)글로윙실버":"Серебро", 
            "검정":"Черный",
            "YN6)텐브라운":"Коричневый",
            "AA)블랙다이아몬드":"Черный",
            "YW6)마블화이트":"Белый",
            "PGU)크리스탈화이트":"Белый",
            "NW)순백색":"Белый",
            "(U9G)루나그레이":"Серый",
            "T2G)녹턴그레이":"Серый",
            "GK2)건그레이":"Серый",
            "PS5)레피스블루":"Синий",
            "XB3)더스크블루":"Синий",
            "W8U)오션뷰":"Синий",
            "UB7/UB8)문라이트클라우드":"Синий",
            "(WC9)화이트크림":"Белый",
            "UD)클리어화이트":"Белый",
            "GAZ)퓨어화이트":"Белый",
            "NCW)크리미화이트":"Белый",
            "PKW)퓨어화이트":"Белый",
            "GD8)번트코코넛":"Коричневый",
            "T6S)티타늄실버":"Серебро",
            "E6S)미네랄실버":"Серебро",
            "Z5G)페퍼그레이":" Серый",
            "ACT)테크노그레이":" Серый",
            "GYM)새틴스틸그레이":" Серый",
            "RB5/PB5)타임리스블랙":"Черный",
            "ZV)진청색":"Синий",
            "P7V)스틸그라파이트":"Серый",
            "GAN)스위치블래이드실버":"Серебро",
            "T2X)타이푼실버":"Серебро",
            "SAI)사일런트실버":"Серебро",
            "SAF)파인실버":"Серебро",
            "4SS)실키실버":"Серебро",
            "YG7)다크나이트":"Черный",
            "9H)체리블랙":"Черный",
            "P2S/P3S)하이퍼메탈릭":"Серый",
            "3D)은빛실버": "Серебро",
            "M2F)마그네틱포스": "Черный",
            "KCS)스파클링실버":"Серебро",
            "RB5)타임리스블랙":"Черный",
            "ABT)플라티늄그라파이드":"Серый",
            "WEA)슬릭실버":"Серебро",
            "N3S)슬릭실버":"Серебро",
            "YT3)아이언그레이":"Серый",
            "T8S)플래티넘실버":"Серебро",
            "WAA)그랜드화이트":"Белый",
            "P2M)판테라메탈":"Серый",
            "NKA)팬텀블랙":"Черный",
            "WW2)화이트크림":"Белый",
            "WW7)아이스화이트":"Белый",
            "9P)체리흑색":"Черный",
            "YAC)크리미화이트":"Белый",
            "P6W)초크화이트":"Белый",
            "GAR)프라하블랙":"Черный",
            "TB7)팬텀블랙":"Черный",
            "ABB)엘리스블루":"Белый",
            "RY5)로얄블루":"Синий ",
            "WHC)화이트크리스탈":"Белый",
            "MB9)블랙포레스트":"Черный",
            "MZH)팬텀블랙":"Черный",
            "(PG9)판테라그레이":"Серый",
            "PG9)판테라그레이":"Серый",
            "WAW)폴라화이트":"Белый",
            "B4U)그래비티블루":"Синий",
            "TS7)오로라실버":"Cеребро",
            "(TK9)카키메탈":"Cеребро",
            "WU6)코스트블루":"Синий",
            "BLA)포멀딥블루":"Синий",
            "W2B)글로잉옐로우":"Желтый",
            "V6S)폴리시드메달":"Желтый",
            "V5N)벨벳듄":"Желтый",
            "GN6)레모네이드옐로우":"Желтый",
            "Z1)갤럭시블랙":"Черный",
            "E5E)그레이스풀그레이":"Серый",
            "M9Y)밀키베이지":"Бежевый",
            "GV8)크리미베이지":"Бежевый",
            "Y7S)플래티넘실버":"Серебро",
            "N5M)카본메탈":"Серый",
            "KLG)스틸그레이":"Cерый",
            "YG6)코스모그레이":"Cерый",
            "FHM)하이퍼메탈릭":"Серебро",
            "IM)티타늄실버":"Серебро",
            "(N9V)이온실버":"Серебро",
            "RHM)슬릭실버":"Серебро",
            "U5S)플래티넘실버":"Серебро",
            "IM)티나늄실버":"Cеребро",
            "퓨어 화이트":"Белый",
            "UD)순백색":"Белый",
            "T5K)티타늄블랙":"Черный",
            "오로라 블랙 펄":"Черный",
            "NB9)미드나잇블랙":"Черный",
            "(NB9)미드나잇블랙":"Черный",
            "ABP)오로라블랙펄":"Черный",
            "V7S)폴리시드메탈":"Cерый",
            "YB6)오닉스블랙":"Черный",
            "ABT)플라티늄그라파이트":"Cерый",
            "ACG)토닉그레이":"Cерый",
            "SWP)스노우화이트펄":"Белый",
            "스노우 화이트 펄":"Бежевый",
            "OA)아이보리":"Бежевый",
            "LAK)스페이스블랙":"Черный",
            "WC9)화이트크림":"Бежевый",
            "SS7)레이크실버":"Серебро",
            "U5B)엠버브라운":"Коричневый",
            "K1P)체리핑크":"Красный",
            "4SS)실키실버":"Серебро",
            "R9A)비타민C":"Желтый",
            "Y6S)플래티넘실버":"Серебро",
            "SG5)스타게이징블루":"Синий",
            "GB0)모던블랙":"Черный",
            "NU7)나이트스카이":"Черный",
            "LAE)클래식블랙":"Черный",
            "P2S)하이퍼메탈릭":"Серебро",
            "Y5)슬릭실버":"Серебро",
            "GUE)스모키아이그레이": "Cерый",
            "PW6)화이트크리스탈": "Белый",
            "TW3)화이트크림": "Белый",
            "BU2)머큐리블루": "Синий",
            "U6G)어반그레이": "Cерый",
            "N5S)하이퍼실버": "Cерый",
            "WAW)폴라 화이트":"Белый",
            "7U)진청색투톤":"Синий",
            "YAW)크리미화이트":"Белый",
            "SSS)세빌실버":"Серебро",
            "PDW)퓨어화이트":"Белый"
        }
        return color_data[car_color]

    def get_car_type(self, type):
        car_type_data = {
            "3인승":"Фургон",
            "승용 (7인승)":"Универсал",
            "승용 (11인승)":"Фургон",
            "승합 (3인승)":"Фургон",
            "화물 (3인승)":"Фургон",
            "승합 (15인승)":"Фургон",
            "승합 (11인승)":"Фургон",
            "12인승":"Фура",
            "승합 (12인승)":"Фура",
            # "Трактор",
            "인승":"Седан",
            "4인승":"Седан",
            "5인승":"Седан",
            "승용 (5인승)":"Седан",
            "승합 (5인승)":"Седан",
            # "Родстер",
            # "Пикап",
            # "Мотоцикл",
            "6인승":"Минивен",
            "7인승":"Минивен",
            "9인승":"Минивен",
            "11인승":"Минивен",
            "승용 (9인승)":"Минивен",
            "승용 (6인승)":"Минивен",
            "화물 (6인승)":"Минивен",
            "승용 (4인승)":"Хэтчбек",
            # "Кроссовер",
            "2인승":"Купе",
            "승용 (2인승)":"Купе",
            "SUV픽업 (5인승)":"Внедорожник пикап"
            # "Кабриолет",
            # "Багги"
        }
        return car_type_data[type]

    #марка авто
    def get_car_mark(self, title):
        try:
            db_connection = mysql.connect(host="217.172.189.14", database="olegk202_kdm", user="olegk202_kdm", password="Kostiuk_6173")
        except Exception as e:
            print('DB CONNECT ERROR %s.' % e)
        category = self.get_category(title)
        try:
            title = re.sub("\[.+\]\s", "", title)  
            title_arr = title.split()
            if(len(title_arr)>3):
                select_car_query = f"SELECT value FROM mg_product_user_property WHERE property_id=157 AND UPPER(value) LIKE UPPER('{category} {title_arr[0]}%') OR UPPER(value) LIKE UPPER('{category} {title_arr[1]}%') OR UPPER(value) LIKE UPPER('{category} {title_arr[2]}%') OR UPPER(value) LIKE UPPER('{category} {title_arr[3]}%') LIMIT 1;"  
            elif(len(title_arr)>2):
                select_car_query = f"SELECT value FROM mg_product_user_property WHERE property_id=157 AND UPPER(value) LIKE UPPER('{category} {title_arr[0]}%') OR UPPER(value) LIKE UPPER('{category} {title_arr[1]}%') OR UPPER(value) LIKE UPPER('{category} {title_arr[2]}%') LIMIT 1;"
            else:
                select_car_query = f"SELECT value FROM mg_product_user_property WHERE property_id=157 AND UPPER(value) LIKE UPPER('{category} {title_arr[0]}%') OR UPPER(value) LIKE UPPER('{category} {title_arr[1]}%') LIMIT 1;" 
            cursor = db_connection.cursor()
            cursor.execute(select_car_query)
            result = cursor.fetchall()
        except Exception as e:
            print('CAR MARK ERROR %s.' % e)
            result = ''
        finally:
            db_connection.close()
        if(len(result) == 0):
            #print("NEW Car Category:", title_arr[0])
            if(title_arr[0]!="The" or title_arr[0]!="New" or title_arr[0]!="All" or title_arr[0]!="Next"):
                return f"{category} {title_arr[0].upper()}"
            elif(title_arr[0]=="The"):
                return f"{category} {title_arr[2].upper()}"
            else:
                return f"{category} {title_arr[1].upper()}"
        else:
            for row in result:
                if(row[0]):
                    return row[0]

    def get_car_mark_url(self, car_mark):
        car_mark_url = re.sub("\.", "", car_mark)            
        car_mark_url = re.sub("\(", "", car_mark_url)                                
        car_mark_url = re.sub("\)", "", car_mark_url)
        car_mark_url = re.sub("\s", "-", car_mark_url)
        return car_mark_url.lower()

    def download_images(self, img_urls, title, folder_name='py_img3'):
        time.sleep(uniform(1,2))
        try:
            img_ext = 'jpg'
            title = self.clear_str(title)
            title = re.sub("\s", "_", title).lower()
            if(isinstance(img_urls, list)):
                for i, img_url in enumerate(img_urls):          
                    img_name = title+"_"+str(i)+"."+img_ext
                    img_data = requests.get(img_url).content
                    with open('./' + folder_name + '/' + img_name, 'wb') as handler:
                        handler.write(img_data)
        except Exception as e:
            print('Failed download image. Reason: %s' % e)

    #асинхронна скачка файла    
    async def fetch_files(self, img_urls, title):
        if(isinstance(img_urls, list)):
            title = self.clear_str(title)
            title = re.sub("\s", "_", title)
            title = title.lower()
            for i, img_url in enumerate(img_urls):  
                async with self.sema, aiohttp.ClientSession() as session:
                    async with session.get(img_url) as resp:
                        if(resp.status == 200):
                            data = await resp.read()
                            async with aiofiles.open(
                                os.path.join('py_img3', title+"_"+str(i)+".jpg"), "wb"
                            ) as outfile:
                                await outfile.write(data)

    #очистка назв авто от непонятних символов
    def clear_str(self, text_str):
        try:
            if(isinstance(text_str, str) and text_str != ''):
                text_str = re.sub("\.","-",text_str)
                text_str = re.sub("\(","",text_str)
                text_str = re.sub("\)","",text_str)
                text_str = re.sub("\{","",text_str)
                text_str = re.sub("\}","",text_str)
                text_str = re.sub("\[","",text_str)
                text_str = re.sub("\]","",text_str)
                text_str = re.sub("\<","",text_str)
                text_str = re.sub("\>","",text_str)
                text_str = re.sub("\$","",text_str)
                text_str = re.sub("\#","",text_str)
                text_str = re.sub("\%","",text_str)
                text_str = re.sub("\~","",text_str)
                text_str = re.sub("\@","",text_str)
                text_str = re.sub("\^","",text_str)
                text_str = re.sub("\&","",text_str)
                text_str = re.sub("\*","",text_str)
                text_str = re.sub("\+","",text_str)
                text_str = re.sub("\=","",text_str)
                text_str = re.sub("\,","",text_str)
                text_str = re.sub("\"","",text_str)
                text_str = re.sub("\'","",text_str)
                text_str = re.sub("\/","",text_str)
            return text_str
        except Exception as e:
            print('Failed to clear car name. Reason: %s' % e)

    #перетвоюємо ссилки на картинки у строки для запису в файл csv
    def get_img_str(self, imgs, title):
        try:
            img_ext = 'jpg'
            name = self.clear_str(title)
            name = name.lower()
            name = re.sub("\s","_", name)
            img_str = ''
            img_alt = ''
            for i, img in enumerate(imgs) :
                #img_str += name+'_'+str(i)+'.'+img_ext+'[:param:][alt='+title+'][title='+title+']|'
                img_str += name+'_'+str(i)+'.'+img_ext+'|'
                img_alt += title+'|'
            return img_str[:-1], img_alt[:-1]
        except Exception as e:
            print('Can\'t get Images str. Reason %s' % e)
            return ""

    async def fetch_content(self, url, session):
        login_data = {
            "passno": "amo1NTA3Kio=",
            "id": "4292"
        }
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': fake_useragent.UserAgent().random
            }
        try:
            async with session.post(config['GLOVIS']['LOGIN_LINK'], data=login_data, headers=headers, timeout=1000) as response:
                if (response.status == 200):
                    data = json.loads(await response.text())
                    # if(data["result"]["status"] == True):
                    #     print("Login",data["result"]["status"])
                else:
                    print(response.status)
        except Exception as e:
            print('LOGIN ERROR %s. URL %s' % (e,url))
        try:
            await asyncio.sleep(uniform(3,6))
            #proxy_url = 'http://' + choice(self.read_file("proxies.txt","\n"))
            async with session.get(url, allow_redirects=True, timeout=1000) as response:
                car={}
                car['count'] = '0'
                car['activation'] = '1'
                car['currency'] = 'USD'
                car['recomended'] = '0'
                car['new'] = '0'
                car['description'] =''
                if (response.status == 200):
                    data = await response.text()
                    try:
                        car['article'] = re.findall(r'<span\sclass=\"nm\">(.+)<\/span>',data)[0]
                        car['lot_number'] = car['article'] 
                    except Exception as e:
                        print('CODE ERROR %s. URL %s' % (e,url))
                        car['article'] = ''
                        car['lot_number'] = car['article']
                    try:
                        car_vin = re.findall(r'<li>\s?<span>차대번호<\/span>\s?<span>(.+)<\/span>\s?<\/li>',data)[0]
                        car['car_vin'] = car_vin
                    except Exception as e:
                        print('CAR VIN ERROR %s. URL %s' % (e,url))
                        car_vin = ''
                        car['car_vin'] = car_vin
                    try:
                        title = str(self.ko_translate(re.findall(r'<p\sclass=\"carnm\">(.+)<\/p>',data)[0], "en"))
                        car['title'] = f"{car['article']} {title} {car_vin}"
                        car['title'] = re.sub("\[", "", car['title'])
                        car['title'] = re.sub("\]", "", car['title'])
                    except Exception as e:
                        print('TITLE ERROR %s. URL %s' % (e,url))
                        car['title'] = ''
                    car['title-seo'] = car['title']
                    car["meta_title"]=car['title']
                    car["meta_keywords"]=car['title']
                    car["meta_desc"]=car['title']
                    car_mark = self.get_car_mark(title)
                    car["mark"] = car_mark
                    try:
                        car['price'] = int(int(float(re.findall(r'<span\sclass=\"nm\">(.+)<\/span>',data)[2].replace(",", "")))*10000/int(config['GLOVIS']['USD']))
                        car["price_course"]=car['price']
                    except Exception as e:
                        print('PRICE ERROR %s. URL %s' % (e,url))
                        car['price'] = ''
                    try:
                        year = re.findall(r'<div\sclass=\"dv03 short\">\n?\s+<p>(\d{4})',data)[0]
                        car["year"] = year
                    except Exception as e:
                        print('YEAR ERROR %s. URL %s' % (e,url))
                        year = ''
                        car["year"] = year
                    try:
                        car_registration = re.findall(r'<li><span>최초등록일<\/span>\s?<span>\s+(\d{4})년',data)[0]
                        car["car_registration"] = car_registration
                    except Exception as e:
                        print('CAR REGISTRATION ERROR %s. URL %s' % (e,url))
                        car_registration = ''
                        car["car_registration"] = car_registration
                    try:
                        displacement = int(re.findall(r'<li>\s?<span>배기량\s?\/\s?인승<\/span>\s?<span>(.+)cc',data)[0].replace(",", ""))#обем двигателя 
                        car["displacement"] = displacement
                    except Exception as e:
                        print('DISPLACEMENT ERROR %s. URL %s' % (e,url))
                        displacement = ''
                        car["displacement"] = displacement
                    try:
                        distance_driven = int(re.findall(r'<li>\s?<span>주행거리<\/span>\s?<span>(.+)Km',data)[0].replace(",", ""))
                        car["distance_driven"] = distance_driven
                    except Exception as e:
                        print('DISTANCE DRIVEN ERROR %s. URL %s' % (e,url))
                        distance_driven = ''
                        car["distance_driven"] = distance_driven
                    try:
                        color = re.findall(r'<li>\s?<span>색상<\/span>\s<span>(.+)<\/span><\/li>',data)
                        if(len(color)>0):
                            color = str(color[0])
                            car_color = self.get_car_color(color)
                        else:
                            car_color = ''
                    except Exception as e:
                        print('COLOR. ERROR %s. URL %s' % (e,url))
                        car_color = ''
                    try:
                        transmission = re.findall(r'<li><span>미션<\/span>\s?<span>(.+)<\/span>\s?<\/li>',data)[0]
                        if(transmission == "A/T"):
                            transmission = "Автомат"
                            car['transmission'] = "Автомат"
                        else:
                            transmission = "Механика"
                            car['transmission'] = "Механика"
                    except Exception as e:
                        print('TRANSMISSION ERROR %s. URL %s' % (e,url))
                        transmission = ''
                        car['transmission'] = "Механика"
                    try:
                        fuel = re.findall(r'<li>\s?<span>연료형태<\/span>\s?<span>(.+)<\/span>\s?<\/li>',data)[0]
                        if(fuel == "디젤"):
                            fuel = "Дизель"
                            car["fuel"]=fuel
                        elif(fuel=="가솔린"):
                            fuel = "Бензин"
                            car["fuel"]=fuel
                        else:
                            fuel = "Газ"
                            car["fuel"]=fuel
                    except Exception as e:
                        print('FUEL ERROR %s. URL %s' % (e,url))
                        fuel = ''
                    try:
                        car_estimate = re.findall(r'\s?[ABCDF]?\s+\/\s+\d{1}\s?',data)[0].replace("\r\n", "")
                        car_estimate = re.sub("\s+", "", car_estimate)
                        car['car_estimate'] = car_estimate
                    except Exception as e:
                        print('CAR ESTIMATE ERROR %s. URL %s' % (e,url))
                        car_estimate = ''
                        car['car_estimate'] = car_estimate
                    try:
                        images = re.findall(r'src="\/cm\/fileDownMan\.do\?menuCd\=[A-Za-z&;%=0-9]+',data)
                        images = list(map(lambda x: "https://www.glovisaa.com"+x.replace('src="', ''), images))
                        car_defect_map = images.pop()
                        del images[0:2]
                        del images[0:int(len(images)/2)]
                        #self.download_images(images, car['title'])
                        #await self.fetch_files(images, car['title'])
                        print(len(images))
                    except Exception as e:
                        print('IMAGES ERROR %s. URL %s' % (e,url))
                        images = ''
                    try:
                        type = str(re.findall(r'<li>\s?<span>배기량\s?\/\s?인승<\/span>\s?<span>[0-9,]+cc\s?\/\s(.+)\s<\/span><\/li>',data)[0])
                        car_type = self.get_car_type(type)
                    except Exception as e:
                        print('CAR TYPE %s. ERROR %s. URL %s.' % (type,e,url))
                        car_type = ''
                    try:
                        car['category'] = self.get_category(title)
                        car['model'] = car['category']
                    except Exception as e:
                        print('CAR CATEGORY ERROR %s. URL %s' % (e,url))
                        car['category'] = ''
                        car['model'] = car['category']
                    try:
                        car['category_url'] = self.get_category_url(car['category'])
                    except Exception as e:
                        print('CAR CATEGORY URL ERROR %s. URL %s' % (e,url))
                        car['category_url'] = ''
                    try:
                        data_html = f"""<h2 class="page-subtit mt60">Лист проверки производительности</h2><div class="car-status-map"><img src="{car_defect_map}"></div><table class="tbl-v02"><colgroup><col style="width\: 140px\;"><col style="width\: auto\;"></colgroup><tbody><tr><th> Аббревиатура </th><td><p class="abbr"><span class="abbr-q"> Небольшая вмятина </span><span class="abbr-pp"> Косметический окрас </span><span class="abbr-ppq"> Косметический окрас/сейчас есть вмятина </span><span class="abbr-xx"> Замена </span><span class="abbr-xxa"> Была замена/сейчас есть мелкая царапина </span><span class="abbr-x"> Рекомендуется замена (на практике часто мелкий скол на стекле, фаре, зеркале) </span><span class="abbr-e"> Рекомендуется замена </span><span class="abbr-r"> Сколы/царапины </span><span class="abbr-w"> Ремонт/возможно шпаклëвка </span><span class="abbr-m"> Регулировка </span><span class="abbr-f"> Изгиб/залом металла </span><span class="abbr-а"> Мелкие Сколы/царапины </span><span class="abbr-с"> Коррозия </span></p></td></tr><tr style="display: none\;"><th> Specials </th><td> Дефект сиденья, дефект материала внутренней части, дефект аварийной подушки, разгрузка двигателя, утечка моторного масла, шарнир двигателя, контрольная лампа двигателя, дефект миссии, дефект PS, дефект центровки, дефект глушителя, нижний шарнир, коррозия нижней части кузова </td></tr></tbody></table>"""
                        data_html = data_html.replace("'", "\\'")
                        data_html = data_html.replace('"', '\\"')
                        car["description"] = data_html
                    except Exception as e:
                        print('CAR DESCRIPTION ERROR %s. URL %s' % (e,url))
                        car['description'] = ''
                    car['auction_date'] = f"glovisaauction {config['GLOVIS']['DATE']}"
                    car['url']=car_vin.lower()+"-"+self.get_car_mark_url(car_mark)
                    car['properties'] = 'Цвет=[type=assortmentCheckBox value=%s product_margin=Синий|Желтый|Белый|Серебро|Красный|Фиолетовый|Оранжевый|Зеленый|Серый|Золото|Коричневый|Голубой|Черный|Бежевый]&Кузов=[type=assortmentCheckBox value=%s product_margin=Универсал|Фургон|Фура|Трактор|Седан|Родстер|Пикап|Мотоцикл|Минивен|Хэтчбек|Кроссовер|Купе|Кабриолет|Багги]&Пробег=%s&Двигатель=%s&Год=%s&Первая регистрация=%s&Трансмиссия=[type=assortmentCheckBox value=%s product_margin=Механика|Автомат]&Топливо=[type=assortmentCheckBox value=%s product_margin=Дизель|Бензин|Газ]&Модель=%s&Марка=%s&Номер лота=%s&Оценка автомобиля=%s&VIN номер=%s&Аукцион=glovisaauction %s' % (car_color, car_type, distance_driven, displacement, year, car_registration, transmission, fuel, car_mark, car["category"], car['article'], car_estimate, car_vin, config['GLOVIS']['DATE'])
                    img_str, img_alt = self.get_img_str(images, car['title'])
                    car['images'] = img_str
                    car["image_title"] = img_alt
                    car["image_alt"] = img_alt
                    #await asyncio.wait([self.fetch_file(img, car['title'], i) for (i, img) in enumerate(images)])
                    lastid = self.add_p.addnewproduct(car)
                    self.add_p.updateproduct(lastid)
                    self.add_p.addproductproperty(lastid,car)
                    #self.write_csv(car)
                else:
                    print(response.status)
        except aiohttp.ClientConnectionError:
            # something went wrong with the exception, decide on what to do next
            print("Oops, the connection was dropped before we finished. GET DATA ERROR. URL %s" % url) 
        except aiohttp.ClientError:
            # something went wrong in general. Not a connection error, that was handled
            # above.
            print("Oops, something else went wrong with the request. GET DATA ERROR. URL %s" % url)

    async def get_data(self, urls):
        try:
            async with aiohttp.ClientSession() as session:
                return await asyncio.wait([self.fetch_content(url, session) for url in urls])
        except Exception as e:
            print('fetch_content ERROR %s' % e)
        finally:
            await session.close()

    #складаємо всі ссилки на авто в один файл
    def get_all_links(self, car_link=config['GLOVIS']['CAR_LINK'], file_name="car_id3.txt"):
        data = self.read_file(file_name)
        res = list(map(lambda x: x.split('|'), data))#[:-1] - удаляет перенос строки в списке car_id3.txt
        return list(map(lambda x: '{}?&gn={}&rc={}&searchtext=&ac={}&atn={}&acc={}&bmaker=undefined&bmodel=undefined'.format(car_link, x[1], x[0], urllib.parse.quote_plus("TQhYt3GD6GvgPdVw1QX+Wg=="), urllib.parse.quote_plus(str(config['GLOVIS']['ATN_NUM'])), urllib.parse.quote_plus("u9cesU3il5ljSzAzHZzmEg==")), res))