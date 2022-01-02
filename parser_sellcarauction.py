# -*- coding: utf-8 -*-
from deep_translator import GoogleTranslator
from multiprocessing import current_process, Pool
from bs4 import BeautifulSoup
from random import choice
from random import uniform
import mysql.connector as mysql
import time
import csv
import requests
import os
import shutil
import re
import html
import configparser
import fake_useragent
from ftplib import FTP
from io import BytesIO
from requests_html import HTMLSession, AsyncHTMLSession
import configparser
#підтягуємо усі настройки з файлу settings.ini
config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini") 
#заливка фаайлов сразу на FTP
#ftp = FTP("217.172.189.14")
#ftp.login("olegk202","lYgH51teND")
#ftp.cwd("public_html/uploads/tempimage")

#session = requests.Session()
#user = fake_useragent.UserAgent().random
#headers = { 'user-agent': user, 'accept': '*/*'}

#LOGIN PASSWORD TO SITE sellcarauction.co.kr
data = {
    "i_sUserId": "530901",
    "i_sPswd": "4275"
}    
if(config['SELLCAR']['AUTOCODE'] == '2'):
    try:
        db_connection = mysql.connect(host="217.172.189.14", database="olegk202_kdm", user="olegk202_kdm", password="Kostiuk_6173")
    except Exception as e:
        print(e)

#translate function 
def ko_translate(text, lan):
    try:
        if(len(text)>1 and len(text)<5000 and isinstance(text,str)):
            return GoogleTranslator(source='ko', target=lan).translate(text)
    except Exception as e:
        print('Failed to Translate text. Reason: %s' % e)
        res = ''
        return res

#read file function 
def read_file(file_name, delimiter):
    try:
        return open(file_name).read().split(delimiter)
    except Exception as e:
        print('Can\'t read %s. Reason %s.' % (file_name, e))


#удаляємо всі зайві пробіли, переноси строк і табуляції
def rm_new_line(string):
        try:
            string = html.unescape(string)
            string = re.sub("\s?\r?\n", "", string)
            string = re.sub("\>\s+\<", "><", string)
            string = re.sub("\<\s+", "<", string)
            string = re.sub("\s+\>", ">", string)
            string = re.sub("\/\s+", "/", string)
            string = re.sub("\-\s+\-", "--", string)
            string = re.sub("\<\!\s+", "<!", string)
            string = re.sub("\<[!\s-][\\a-z\S\s]*[^<>]*[\-\s]\>", "", string)
            string = re.sub("\<[!\s-][\S]+[\-\s]\>", "", string)
            string = re.sub("\s{2,}", " ", string)
            return string
        except Exception as e:
                print('Failed to delete White Space Tabs and New Line. Reason: %s' % e)

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

#удаляем недопустимие символи в названии авто 
def clear_car_name(car_name):
        try:
            if(isinstance(car_name, str) and car_name.strip() != ''):
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
#def login(login_link):
#    try:
#        return session.post(login_link, data=data, headers=headers)
#    except Exception as e:
#        print('Can\'t get HTML form %s. Reason %s.' % (login_link, e))

def login(login_link):
        try:
            session = HTMLSession()
            session.headers.update({'User-Agent': fake_useragent.UserAgent().random})
            login_data = {        
                "i_sUserId": "530901",
                "i_sPswd": "4275"            
            }
            time.sleep(uniform(4,6))
            r = session.request('POST', login_link, login_data, timeout=400, verify=True)
            if(r.status_code == 200):
                return session
            else:
                print("Error to Login", r.status_code)
                session.close()
        except Exception as e:
            print('Can\'t login. Reason %s.' % e)
            session.close()
            login(login_link)

def fetch(url):
    data = ""
    r = ""
    # p = current_process()
    # if(p.name != 'MainProcess' and p._identity[0] and os.getpid()):
    #     print('process counter:', p._identity[0], 'pid:', os.getpid())
    session = HTMLSession()
    session.headers.update({'User-Agent': fake_useragent.UserAgent().random})
    #session.max_redirects = 10
    print('parsing from proxy')
    proxy = { 'http': 'http://' + choice(read_file("proxies.txt","\n")) +'/' }
    session.proxies.update(proxy)
    time.sleep(uniform(1,6))
    try:
        r = session.request('GET', url)
        if(r.status_code == 200):
            r.html.render(timeout=400)
            data = r.html
            session.close()
            return data
        else:
            print("Error %d" % r.status_code)
            session.close()
    except Exception as e:
        print('Failed to get page %s. Reason: %s' % (url, e))

#витягуємо html із сесію
#def get_shtml(link):
#    try:
#        html = session.get(link)
#        if html.status_code == 200:
#            return html.text
#        else: 
#            return html.status_code
#    except Exception as e:
#        print('Can\'t get HTML with session. Reason %s.' % e)

#год первой регистрации автомобиля
def get_car_registration(html):
    if html:
        try:
            if(len(html.find("strong.text-right"))>2):
                res = re.findall("[0-9]+", rm_new_line(str(html.find("strong.text-right")[2].text)))
                if(len(res)>1):
                    return str(res[1][0:4]+"/"+res[1][4:6]+"/"+res[1][6:8])
                elif(len(res) == 1):
                    return str(res[0][0:4]+"/"+res[0][4:6]+"/"+res[0][6:8])
        except Exception as e:
            print('Can\'t get car registration. Reason %s.' % e)
            return "None"
#пробег
def get_distance_driven(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        res = re.findall("[0-9]+", rm_new_line(str(soup.find_all("strong", class_="text-right")[5].text.strip())))
        return "".join(res)
    except Exception as e:
        print('Can\'t get driven distance. Reason %s.' % e)
        return

#VIN номер авто
def get_car_vin(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        return str(soup.select("#body > section.con_top.gray-bg_fin > div:nth-child(1) > div.row.mt_5 > div.col-md-4.car-details-sidebar > div > ul > li:nth-child(2) > strong")[0].text.strip())
    except Exception as e:
        print('Can\'t get VIN number. Reason %s.' % e)

#топливо
def get_fuel(html):
    fulel_data = {
        "가솔린":"Бензин",
        "휘발유":"Бензин",
        "경유":"Дизель",
        "디젤":"Дизель",
        "LPG":"LPG",
        "하이브리드":"Гибрид",
        "LPI하이브리드":"LPG гибрид",
        "가솔린하이브리드":"Бензиновый гибрид",
        "디젤하이브리드": "Дизельный гибрид",
        "전기":"Электрокар",
        "가솔린/LPG":"Бензин/LPG",
        "겸용":"Комбинированное использование"
    }
    soup = BeautifulSoup(html, 'html.parser')
    try:
        return fulel_data[rm_new_line(str(soup.find_all("strong", class_="text-right")[4].text.strip()))]
    except Exception as e:
        print('Can\'t get fuel. Reason %s.' % e)
        return

#марка авто
def get_car_mark(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:     
        return text_len(rm_new_line(str(soup.select("#body > section.con_top.gray-bg_fin > div.container-fluid.wide_area.mt_1.car_view_check_area > div > div > div > table > tbody > tr:nth-child(7) > td:nth-child(2)")[0].text.strip())),"en")
    except Exception as e:
        print('Can\'t get car mark. Reason %s.' % e)
        return

#коробка передач
def get_transmission(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        if(len(soup.find_all("strong", class_="text-right"))>8):
            if(rm_new_line(str(soup.find_all("strong", class_="text-right")[8].text.strip()))=="오토"):
                return "Автомат"
            else:
                return "Механика"
    except Exception as e:
        print('Can\'t get transmission. Reason %s.' % e)
        return

#фото авто
def get_img_src(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all("img", class_ = "img-fluid")
        images = []
        for item in items:
            if item.has_attr('src'):
                match = re.search('\_S\.[jpeg|jpg|JPG|JPEG|gif|png]+$', item.get('src'))
                if match:
                    #download_images(item.get('src').replace('_S', '').replace('http://', 'https://'))
                    images.append(item.get('src').replace('_S', '').replace('http://', 'https://'))
                else: 
                    continue
        return images
    except Exception as e:
        print('Can\'t get img src. Reason %s.' % e)
        return

#переробляємо ссилки на фото в потрібні для імпорту строки
def get_img_str(imgs, html):
    try:
        title = get_car_title(html)
        img_str = ''
        for img in imgs :
            # str_arr = str(img).split('/')
            # str_arr.reverse()
            # img_name = clear_img_name(str_arr[0])
            img_str += img+'[:param:][alt='+title+'][title='+title+']|'
        return img_str[:-1]
    except Exception as e:
        print('Can\'t get Images str. Reason %s' % e)
        return

#двигатель
def get_car_displacement(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        res = re.findall("[0-9]+", rm_new_line(soup.find_all("strong", class_="text-right")[6].text.strip()))
        return "".join(res)
    except Exception as e:
        print('Can\'t get car displacement. Reason %s.' % e)
        return

#название авто
def get_car_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        return clear_car_name(ko_translate(rm_new_line(str(soup.find("h2", class_="tit_style2").text.strip())), "en"))
    except Exception as e:
        print('Can\'t get title. Reason %s.' % e)
        return

#лот аукциона
def get_lot_id(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        res = re.search("\[{1}\d+\]{1}", ko_translate(rm_new_line(str(soup.find("h2", class_="tit_style2").text.strip())), "en"))
        if(res):
            res = re.search("\[{1}\d+\]{1}", ko_translate(rm_new_line(str(soup.find("h2", class_="tit_style2").text.strip())), "en")).group()
            res = re.sub("\[{1}", "", res)
            res = re.sub("\]{1}", "", res)
            return res
    except Exception as e:
        print('Can\'t get title. Reason %s.' % e)
        return

#год автомобиля
def get_car_year(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        if(len(soup.find_all("strong", class_="text-right"))>2):
            res = re.match("[0-9]+", rm_new_line(str(soup.find_all("strong", class_="text-right")[2].text.strip())))
            if(res):
                return int(res.group())
    except Exception as e:
        print('Can\'t get car year. Reason %s.' % e)
        return

#цвет автомобиля
def get_car_color(html):
    color_data = {
        "흰색":"Белый",
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
        "빨강":"Красный"
    }
    soup = BeautifulSoup(html, 'html.parser')
    try:
        if(len(soup.find_all("strong", class_="text-right"))>9):
            return color_data[re.sub("\s.+","", rm_new_line(str(soup.find_all("strong", class_="text-right")[9].text.strip())))]
    except Exception as e:
        print('Can\'t get car color. Reason %s.' % e)
        return

#тип автомобиля
def get_car_type(html):
    car_type_data = {
        "승용 (7인승)":"Универсал",
        "승용 (11인승)":"Фургон",
        "승합 (3인승)":"Фургон",
        "화물 (3인승)":"Фургон",
        "승합 (15인승)":"Фургон",
        "승합 (11인승)":"Фургон",
        "승합 (12인승)":"Фура",
        # "Трактор",
        "승용 (5인승)":"Седан",
        "승합 (5인승)":"Седан",
        # "Родстер",
        # "Пикап",
        # "Мотоцикл",
        "승용 (9인승)":"Минивен",
        "승용 (6인승)":"Минивен",
        "화물 (6인승)":"Минивен",
        "승용 (4인승)":"Хэтчбек",
        # "Кроссовер",
        "승용 (2인승)":"Купе",
        "SUV픽업 (5인승)":"Внедорожник пикап"
        # "Кабриолет",
        # "Багги"
    }
    soup = BeautifulSoup(html, 'html.parser')
    try:
        if(len(soup.find_all("strong", class_="text-right"))>10):
            return car_type_data[rm_new_line(str(soup.find_all("strong", class_="text-right")[10].text.strip()))]
    except Exception as e:
        print('Can\'t get car type. Reason %s.' % e)
        return

#запись айди авто в файл
def write_car_id(file_name, data):
    try:
        return open(file_name, "a").write(data)
    except Exception as e:
        print('Can\'t wrine file %s. Reason %s.' % (file_name,e))

#цена автомобиля 
def get_car_price(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        return int(float(re.sub("\,", "", soup.find("strong", class_="i_comm_main_txt2").text.strip()))*10000/float(config['SELLCAR']['USD']))
    except Exception as e:
        print('Can\'t get car price. Reason %s.' % e)
        return
def car_img_description(text):
        return re.sub("\/images\/front\/","https://www.sellcarauction.co.kr/images/front/",text)

#описание авто 
def get_car_description(html, link):
    soup = BeautifulSoup(html, 'html.parser') 
    description = ''
    try:
        vr = "" if not re.search("[A-Z0-9]+$", link) else re.search("[A-Z0-9]+$", link).group()
    except Exception as e:
        print('Can\'t get car ID for VR 360 view auto. Reason %s.' % e)
    try:
        description += '<div class="timeline-heading"><h3>VR360 обзор авто</h3></div>'
        description += '<iframe frameborder="0" height="600" id="ovulyaciya" scrolling="no" src="http://www.sellcarauction.co.kr/newfront/receive/rc/receive_rc_view_vr.do?isLandscapeOpen=Y&amp;isBrowserOpen=Y&amp;receivecd=%s" width="900"></iframe>' % vr
    except Exception as e:
        print('Can\'t get car description "VR 360 view auto". Reason %s.' % e)
    try:
        description += '<div class="timeline-heading"><h3>Информация об оценке производительности</h3></div>'
        description += "" if not len(soup.select("#body > section.con_top.gray-bg_fin > div:nth-child(2) > div > div > div > table")) else text_len(rm_new_line(str(soup.select("#body > section.con_top.gray-bg_fin > div:nth-child(2) > div > div > div > table")[0])), "ru")
    except Exception as e:
        print('Can\'t get car description "Performance Evaluation Information". Reason %s.' % e)
    try:
        description += '<div class="timeline-heading"><h3>Информация о вариантах</h3></div>'
        description += "" if not len(soup.select("#body > section.con_top.gray-bg_fin > div:nth-child(3) > div > div > table:nth-child(2)")) else text_len(rm_new_line(str(soup.select("#body > section.con_top.gray-bg_fin > div:nth-child(3) > div > div > table:nth-child(2)")[0])), "ru")
    except Exception as e:
        print('Can\'t get car description "Option information". Reason %s.' % e)
    try:   
        description += "" if not len(soup.select("#body > section.con_top.gray-bg_fin > div:nth-child(3) > div > div > ul")) else text_len(rm_new_line(str(soup.select("#body > section.con_top.gray-bg_fin > div:nth-child(3) > div > div > ul")[0])), "ru")
    except Exception as e:
        print('Can\'t get car descritpion comm list. Reason %s.' % e)
    # try:

    #     divcar1 = soup.find_all("div", class_="car_01")[0]
    #     div = divcar1.find_all("div", class_="car_blueprint")[0]
    #     ul = div.find_all("ul", class_="p0201_0205")[0]
    #     # ul.find_all("li", class_="on")
    #     text = '<div class="korea-auc-damage aj type-car_01 position-relative">'
    #     text += '<img src="http://www.sellcarauction.co.kr/'+str(div.find("img", id="car_map").get('src'))+'" alt="" style="width: 736px; max-width: none">'
    #     text += '<div class="position-absolute" id="p0101_0107" style="">'
    #     text += '<div class="position-absolute" style="top:0; left:0;">'
        # for i in range(len(div.find_all("ul")[0].find_all("li.on"))):
        #     text += '<img src="'+str(div.find_all("ul")[0].find_all("li.on")[i].find("img").get('src'))+'" alt="" >' 
        #     text += '</div>'
        #     text += '<div id="'+str(div.find_all("ul")[0].find_all("li.on").get('id'))+'" style="" class="position-absolute ddi">'
        #     text += '<span class="text-danger">'
        #     text += car_img_description(str(div.find_all("ul")[0]).find("li.on span.txt_red"))
        #     text += '</span>'
        #     text += car_img_description(str(div.find_all("ul")[0]).find("li.on p"))
        #     text += '</div>'
    #     text = '<div class="img_map_area position-relative"><div class="all_car_layer" id="realImg">'
    #     text += '<div class="car_01">'
    #     text += text_len(rm_new_line(str(soup.find_all("div", class_="layer_photo1")[0])), "en")
    #     text += '<div class="car_blueprint">'
    #     text += car_img_description(str(div.find("img", id="car_map")))
    #     text += str(div.find("map", {"name":"Map"}))
    #     text += car_img_description(str(div.find_all("ul")[0]))
    #     text += car_img_description(str(div.find_all("ul")[1]))
    #     text += car_img_description(str(div.find_all("ul")[2]))
    #     text += '</div></div>'
    #     text += '</div></div>'
    #     description += text
    # except Exception as e:
    #     print('Can\'t get car description image. Reason %s.' % e)
    # try:
    #     description += '<div class="timeline-heading"><h3>Протокол осмотра</h3></div>'
    #     text = text_len(rm_new_line(str(soup.select("#body > section.con_top.gray-bg_fin > div.container-fluid.wide_area.mt_1.car_view_check_area > div > div > div > table")[0])), "ru")
    #     text = re.sub("\/newfront\/images\/","http://www.sellcarauction.co.kr/newfront/images/",text)
    #     description += text
    # except Exception as e:
    #     print('Can\'t get car description "Inspection protocol". Reason %s.' % e)
    return rm_new_line(description)

#категория для авто
def get_car_category(html):
    try:
        categoty_data = {
            "Genesis":"Genesis",
            "Kia":"Kia Motors",
            "Hyundai":"Hyundai",
            "Ssangyong":"SsangYong",
            "Renault":"Renault",
            "Benz":"Mercedes Benz",
            "Chevrolet":"Chevrolet",
            "Jaguar":"Jaguar",
            "BMW":"BMW",
            "Land":"Land Rover",
            "Peugeot":"Peugeot",
            "Volkswagen":"Volkswagen",
            "Ford":"Ford",
            "Nissan":"Nissan",
            "Jeep":"Jeep",
            "Lexus":"Lexus",
            "Lincoln":"Lincoln",
            "Mini":"Mini Cooper",
            "Cadillac":"Cadillac",
            "Toyota":"Toyota",
            "Tesla":"Tesla",
            "Audi":"Audi"
        }
        res = re.match("^[0-9]+\s(\w+)", get_car_title(html))
        if(res):
            res = res.group(1)
            if(res):
                return categoty_data[res]
    except Exception as e:
        print('Can\'t get car category. Reason %s.' % e)
        return

#link на категорію авто 
def get_car_category_url(html):
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
            "Nissan":"nissan",
            "Jeep":"jeep",
            "Lexus":"lexus",
            "Honda":"honda",
            "Lincoln":"lincoln",
            "Mini Cooper":"mini-cooper",
            "Cadillac":"cadillac",
            "Toyota":" ",
            "Tesla":"tesla",
            "Audi":"audi"
        }
        return categoty_url_data[get_car_category(html)]
    except Exception as e:
        print('Can\'t get car category url. Reason %s.' % e)
        return

#ID авто для парсингу
def get_car_id(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        items = soup.find_all("div", class_ = "car-title")
        for item in items:
            car_id = re.search('[A-Z]+[0-9]+', item.find("a").get('onclick'))
            if car_id:
                write_car_id("car_id.txt",car_id.group()+"\n")
    except Exception as e:
        print('Can\'t get car id. Reason %s.' % e)

#ID нових авто, что добавились, для парсингу 
def get_missed_car_id(html):
    if(html != ''):
        soup = BeautifulSoup(html, 'html.parser')
        try:
            items = soup.find_all("div", class_="car_list_con")
        except Exception as e:
            print('Can\'t get missed list car. Reason %s.' % e)
        for item in items:
            try:
                lot_id = str(item.find("div").find("strong", class_="i_comm_main_txt").text.strip())
                print("LOT ID", str(item.find("div").find("strong", class_="i_comm_main_txt").text.strip()))
            except Exception as e:
                print('Can\'t get lot id. Reason %s.' % e)
            try:
                car_name = clear_car_name(ko_translate(rm_new_line(str(re.sub("^\d+\s", "", item.parent.find("div", class_="car-title").find("a").text.strip()))), "en"))
                print("CAR NAME", car_name)
            except Exception as e:
                print('Can\'t get car name. Reason %s.' % e)
            car_price = 0
            try:
                if(re.sub("\,", "", item.nextSibling.nextSibling.find("div").find("strong", class_="i_comm_main_txt2").text.strip()) != "준비중"): 
                    car_price = int(float(re.sub("\,", "", item.nextSibling.nextSibling.find("div").find("strong", class_="i_comm_main_txt2").text.strip()))*10000/float(config['SELLCAR']['USD']))
                    print("CAR PRICE", car_price)
            except Exception as e:
                print('Can\'t get car price. Reason %s.' % e)
            select_car_query = "SELECT mg_product.id, mg_product.price, mg_product.title FROM mg_product LEFT JOIN mg_product_user_property ON mg_product.id = mg_product_user_property.product_id WHERE mg_product_user_property.property_id = 166 AND mg_product_user_property.value = 'sellcarauction " + config['SELLCAR']['DATE'] + "' AND LOWER(mg_product.title) LIKE LOWER('"+lot_id+" %') AND mg_product.activity=1;"
            print("Car id", re.search('[A-Z]+[0-9]+', item.parent.find("div", class_="car-title").find("a").get('onclick')).group())
            if db_connection.is_connected():
                cursor = db_connection.cursor()
                cursor.execute(select_car_query)
                result = cursor.fetchall()
                if(len(result) == 0):
                    print("MISSED CAR ID:" ,lot_id, "Car name:", car_name)
                    car_id = re.search('[A-Z]+[0-9]+', item.parent.find("div", class_="car-title").find("a").get('onclick'))
                    if car_id:
                        write_car_id("missed_car_id.txt",car_id.group()+"\n")
                elif(car_price != 0):
                    for row in result:
                        if (row[1] == 0):
                            print("Car price:", car_price, "Car id:", row[0], "Car Title:", row[2])
                            update_query = "UPDATE mg_product SET price = "+str(car_price)+" WHERE id = "+str(row[0])
                            cursor.execute(update_query)
                            db_connection.commit()

#парсимо сайт із сесії
def parser(link, func=None):
    if(link and link is not None):
        data = ''
        session = login(config['SELLCAR']['LOGIN_LINK'])
        try:
            #time.sleep(0.01)
            r = session.request('GET', link, verify=True)
            time.sleep(uniform(1,4))#2-3
            if r.status_code == 200:
                if func is not None:
                    data = func(r.html.html)
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
            session.close()

#парсимо всі ссилки на авто по сторінкам
def get_pages(page_start=1, page_end=2):
    for i in range(page_start,page_end+1):
        unf = uniform(3,6)
        time.sleep(unf)
        print("Page %d. Sleep %d." % (i, unf))
        print(config['SELLCAR']['URL']+"?i_iPageSize=&i_iNowPageNo="+str(i))
        parser(config['SELLCAR']['URL']+"?i_iPageSize=&i_iNowPageNo="+str(i), get_car_id)
    pass

#парсимо всі ссилки на недостаючі авто по сторінкам
def get_missed_car_pages(page_start=1, page_end=2):
    for i in range(page_start,page_end+1):
        unf = uniform(3,6)
        time.sleep(unf)
        print("Page %d. Sleep %d." % (i, unf))
        parser(config['SELLCAR']['URL']+"?i_iPageSize=&i_iNowPageNo="+str(i), get_missed_car_id)
    pass

#складаємо всі ссилки на авто в один файл
def get_all_links(car_link, file_name="car_id.txt"):
    return list(map( lambda x: '{}?receivecd={}'.format( car_link, x ), read_file(file_name, "\n")))

#закачуємо усі картинки
def download_images(img_urls, folder_name='py_img'):
    try:
        if(isinstance(img_urls, list)):
            for img_url in img_urls:
                str_arr = str(img_url).split('/')
                str_arr.reverse()
                name_arr = str_arr[0].split('.')
                name = name_arr[0]
                img_ext = name_arr[1].lower() 
                #img_name = clear_img_name(name)
                if(config['SELLCAR']['FTPCODE'] == '1'):
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
            if(config['SELLCAR']['FTPCODE'] == '1'):
                img_data = BytesIO(requests.get(img_urls).content) #without BytesIO if you whant download to local machine
                ftpCommand = "STOR %s"%name #comment if you whant download to local machine
                ftp.storbinary(ftpCommand, fp=img_data) #comment if you whant download to local machine
            else:
                img_data = requests.get(img_urls).content
                with open('./'+folder_name+'/'+name+'.'+img_ext, 'wb') as handler:
                    handler.write(img_data)
    except Exception as e:
        print('Failed download image. Reason: %s' % e)

#delete file CSV
def rm_csv(name = "data.csv"):
        try:
            os.remove(name)
            print("File "+name+" Removed!")
        except Exception as e:
                print('Failed to remove file %s. Reason: %s' % (name,e))

#create file CSV
def create_csv(name = "data.csv"):
    path = os.getcwd() + os.path.sep + name
    try:
        with open(path, 'w', encoding="utf-8", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Категория', 'URL категории', 'Товар', 'Вариант', 'Описание', 'Цена', 'URL', 'Изображение', 'Артикул', 'Количество', 'Активность', 'Заголовок [SEO]', 'Ключевые слова [SEO]', 'Описание [SEO]', 'Старая цена', 'Рекомендуемый', 'Новый', 'Сортировка', 'Вес', 'Связанные артикулы', 'Смежные категории', 'Ссылка на товар', 'Валюта', 'Свойства'])
    except Exception as e:
            print('Failed to create file "data.csv". Reason: %s' % e)

#записуємо усі данні у файл
def write_csv(data, name = "data.csv"):
    path = os.getcwd() + os.path.sep + name
    try: 
        with open(path, 'a', encoding="utf-8", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([data['category'], data['category_url'], data['title'], ' ', data['description'], data['price'], ' ', data['images'], data['article'], data['count'], data['activation'], data['title-seo'], ' ', ' ', ' ', data['recomended'], data['new'], ' ', ' ', ' ', ' ', ' ', data['currency'], data['properties']])
    except Exception as e:
        print('Can\'t write csv file. Reason %s' % e)

#створюємо папку
def create_folder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        print('Can\'t create folder in path %s. Reason %s' % path, e)

#витягуємо максимальне число сторінок
def get_max_page(html, pages=10):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        if(int(soup.find("span", {"class": "text_style7 i_comm_main_txt"}).text.strip()) % pages > 0):
            return int(int(soup.find("span", {"class": "text_style7 i_comm_main_txt"}).text.strip())/pages) + 2
        else:
            return int(int(soup.find("span", {"class": "text_style7 i_comm_main_txt"}).text.strip())/pages) + 1
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
    print("ALL FILES FROM FOLDER PY_IMG IS DELETED")

#витягуємо оцінку авто 
def get_car_estimate(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        item = soup.select("#body > section.con_top.gray-bg_fin > div:nth-child(2) > div > div > div > table > tbody > tr:nth-child(1) > td")[0]
        if item:
            return "".join(re.findall("[A-Z]", str(item)))
    except Exception as e:
        print('Can\'t get car estimate %s. Reason: %s' % e)

#витягуємо всі данні на авто
def get_car(link):
    car = {}
    p = current_process()
    if(p.name != 'MainProcess' and p._identity[0] and os.getpid()):
        print('process counter:', p._identity[0], 'pid:', os.getpid())
    #unf = uniform(1,4)
    #time.sleep(unf)
    #html = fetch(link)
    html = parser(link)
    print(link)
    if html:
        try:
            #year = get_car_year(html)
            #category = get_car_category(html)
            # if(isinstance(year,int) and (year < 2012)):
            #     return
            #color = get_car_color(html)
            #car_estimate = get_car_estimate(html)
            #car_type = get_car_type(html)
            #distance_driven = get_distance_driven(html)
            #displacement = get_car_displacement(html)
            #transmission = get_transmission(html)
            #fuel = get_fuel(html)
            #lot_number = get_lot_id(html)
            #car_registration = get_car_registration(html)
            #mark = "" if not category or not get_car_mark(html) else category +" "+get_car_mark(html).upper()
            #car_vin = get_car_vin(html)
            #mark_url = re.sub("\.", "", mark)            
            #mark_url = re.sub("\(", "", mark_url)                                
            #mark_url = re.sub("\)", "", mark_url)
            #mark_url = re.sub("\s", "-", mark_url)
            #car['url'] = car_vin.lower()+"-"+mark_url.lower()
            #car['category'] = category
            #car['category_url'] = get_car_category_url(html)
            #car['title'] = get_car_title(html)
            #car['title-seo'] = car['title']
            #car['price'] = get_car_price(html)
            #car['description'] = get_car_description(html, link)
            #car['images'] = get_img_str(get_img_src(html), html)
            #car['count'] = '0'
            #car['activation'] = '1'
            #car['currency'] = 'USD'
            #car['recomended'] = '0'
            #car['new'] = '0'
            #car['article'] = get_lot_id(html)
            #car['properties'] = 'Цвет=[type=assortmentCheckBox value=%s product_margin=Желтый|Белый|Серебро|Красный|Фиолетовый|Оранжевый|Зеленый|Серый|Золото|Коричневый|Голубой|Черный|Бежевый]&Кузов=[type=assortmentCheckBox value=%s product_margin=Универсал|Фургон|Фура|Трактор|Седан|Родстер|Пикап|Мотоцикл|Минивен|Хэтчбек|Кроссовер|Купе|Кабриолет|Багги]&Пробег=%s&Двигатель=%s&Год=%s&Первая регистрация=%s&Трансмиссия=[type=assortmentCheckBox value=%s product_margin=Механика|Автомат]&Топливо=[type=assortmentCheckBox value=%s product_margin=Дизель|Бензин|Газ]&Модель=%s&Марка=%s&Номер лота=%s&Оценка автомобиля=%s&VIN номер=%s&Аукцион=sellcarauction %s' % (color, car_type, distance_driven, displacement, year, car_registration, transmission, fuel, mark, category, lot_number, car_estimate, car_vin, config['SELLCAR']['DATE'])
            download_images(get_img_src(html))
            #write_csv(car)
        except Exception as e:
            print("Can\'t write car data to csv.")

#витягуємо курс валют 
def get_currency(): 
    try:
        html = parser("https://www.currencyconverterx.com/KRW/USD/1000000")
        soup = BeautifulSoup(html, 'html.parser')
        return str(soup.select("#converterForm > div.convert-form__result > strong > span.convert-form__c3")[0].text.strip())
    except Exception as e:
        print('Can\'t get currency. Reason: %s' % e)
        return
krw_to_usd = get_currency()

#головна функція запускає всі 
def main():
    time_start = time.time()
    max_page = parser(config['SELLCAR']['URL']+"?i_iPageSize=&i_iNowPageNo=1", get_max_page)
    if(config['SELLCAR']['AUTOCODE'] == '0'):
        rm_csv("car_id.txt")
        get_pages(1,max_page)
    elif(config['SELLCAR']['AUTOCODE'] == '1'):
        create_folder('./py_img')
        clear_folder('./py_img/')
        my_list = get_all_links(config['SELLCAR']['CAR_LINK'])
        with Pool(50) as p:
            p.map(get_car, my_list)
    elif(config['SELLCAR']['AUTOCODE'] == '2'):
        rm_csv("missed_car_id.txt")
        print(max_page)
        get_missed_car_pages(1,max_page)
    elif(config['SELLCAR']['AUTOCODE'] == '3'):
        print(max_page)
        rm_csv("car_id.txt")
        get_pages(1,max_page)
        create_folder('./py_img')
        clear_folder('./py_img/')
        my_list = get_all_links(config['SELLCAR']['CAR_LINK'])
        with Pool(50) as p:
            p.map(get_car, my_list)
        #rm_csv()
        #create_csv()
        #missed_list = get_all_links(config['SELLCAR']['CAR_LINK'], "missed_car_id.txt")
        #with Pool(40) as p:
            #p.map(get_car, missed_list)
    # ftp.quit()
    time_end = time.time() 
    print(time_end - time_start)

if __name__ == '__main__':
    main()
