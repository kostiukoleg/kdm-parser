# -*- coding: utf-8 -*-
from requests_html import HTMLSession, AsyncHTMLSession
import requests
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import current_process, Pool
from deep_translator import GoogleTranslator
from random import uniform
from random import choice
import asyncio
import time
import re
import os
import csv
import html
import fake_useragent
import configparser
from urllib import parse
import urllib.parse
from io import BytesIO
from ftplib import FTP
from bs4 import BeautifulSoup
import shutil
config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini") 

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
    print("Folder py_img is clean")
#створюємо папку
def create_folder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        print('Can\'t create folder in path %s. Reason %s' % path, e)
#заливка фаайлов сразу на FTP
if(config['SELLCAR']['FTPCODE'] == '1'):
    ftp = FTP("185.74.252.12")
    ftp.login("olegk202","lYgH51teND")
    ftp.cwd("public_html/uploads/tempimage")
#read file function 
def read_file(file_name, delimiter):
    try:
        return open(file_name).read().split(delimiter)
    except Exception as e:
        print('Can\'t read %s. Reason %s.' % (file_name, e))

#translate function 
def ko_translate(text, lan):
    try:
        if(len(text)>1 and len(text)<5000 and isinstance(text,str)):
            return GoogleTranslator(source='ko', target=lan).translate(text)
    except Exception as e:
        print('Failed to Translate text. Reason: %s' % e)
        res = ""
        return res

#следит чтоб небило длины текста более 5000 символов
def text_len(text, lang):
    new_text = ""
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

#удаляємо всі зайві пробіли, переноси строк і табуляції
def rm_new_line(string):
    if isinstance(string, str):
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

def clear_car_name(car_name):
    if(isinstance(car_name, str) and car_name is not None):
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
        #parsed_link = parse.parse_qs(parse.urlsplit(url).query)
        #write_car_id("missed_car_id.txt",urllib.parse.quote_plus(parsed_link['receivecd'][0])+"\n")
        #session.close()
        #return

#залогінюємось на сайті
def login(login_link):    
    session = requests.Session()
    user = fake_useragent.UserAgent().random
    headers = { 'user-agent': user, 'accept': '*/*'}

    #LOGIN PASSWORD TO SITE sellcarauction.co.kr
    data = {
        "i_sUserId": "546801",
        "i_sPswd": "9977"
    }    
    try:
        return session.post(login_link, data=data, headers=headers)
    except Exception as e:
        print('Can\'t get HTML form %s. Reason %s.' % (login_link, e))

#парсимо сайт із сесії
def parser(link, func):
    r = login(config['SELLCAR']['LOGIN_LINK'])
    print(r)
    try:
        time.sleep(uniform(1,6))
        html = r.get(link)
        if html.status_code == 200:
            return func(html.text)
        else:
            return 'Error code ' + html.status_code
    except Exception as e:
        print('Can\'t get html from site. Reason %s.' % e)

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

def get_car_img(html):
    data = ""
    if html:
        for i in range(len(html.find("#realImg>div"))):
            try:
                html.find("#realImg>div")[i].attrs
            except Exception as e:
                print('Can\'t div#realImg>div[i] attrs. Reason %s.' % e)
            if "style" in html.find("#realImg>div")[i].attrs:
                if html.find("#realImg>div")[i].attrs["style"] != "display:none":
                    data += "<div class='p-3'>"
                    try:
                        data += "<div class='korea-auc-damage aj type-"+html.find("div#realImg>div")[i].attrs["class"][0]+" position-relative'>"
                    except Exception as e:
                        print('Can\'t div#realImg>div class. Reason %s.' % e)
                    try:
                        data += '<img src="http://www.sellcarauction.co.kr'+html.find("div#realImg>div")[i].find("div:last-child>img")[0].attrs["src"]+'" alt="" style="width: 736px; max-width: none">'
                    except Exception as e:
                        print('Can\'t find div:last-child>img src. Reason %s.' % e)
                    for k in range(len(html.find("#realImg>div")[i].find("div:last-child>ul"))):
                        try:
                            html.find("#realImg>div")[i].find("div:last-child>ul")[k].attrs
                        except Exception as e:
                            print('Can\'t find div:last-child>ul attrs. Reason %s.' % e)
                        if "class" in html.find("#realImg>div")[i].find("div:last-child>ul")[k].attrs:
                            try:
                                data += "<div id='"+html.find("#realImg>div")[i].find("div:last-child>ul")[k].attrs["class"][0]+"' class='position-absolute'>"
                            except Exception as e:
                                print('Can\'t find div:last-child>ul class. Reason %s.' % e)
                            for j in range(len(html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li"))):
                                try:
                                    html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].attrs
                                except Exception as e:
                                    print('Can\'t find div:last-child>ul li attrs. Reason %s.' % e)
                                if "class" in html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].attrs:
                                    if (len(html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].attrs["class"]) > 0):
                                        try:
                                            data += "<div style='top:0; left:0;' class='position-absolute'>"
                                            data += "<img src='http://www.sellcarauction.co.kr"+html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].find("img")[0].attrs["src"]+"'>"
                                            data += "</div>"
                                        except Exception as e:
                                            print('Failed to get li img src. Reason: %s' % e)
                                        try:
                                            data += "<div id='"+html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].attrs["id"]+"' style='"+html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].find("p")[0].attrs["style"]+"' class='position-absolute ddi'>"
                                        except Exception as e:
                                            print('Failed to get li p style. Reason: %s' % e)
                                        try:
                                            data += "<span class='text-danger'>"+html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].find("p>span.txt_red")[0].text+"</span>"
                                        except Exception as e:
                                            print('Failed to get li span text. Reason: %s' % e)
                                        try:
                                            if(len(html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].xpath("//p/text()")) != 0):
                                                data += html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].xpath("//p/text()")[0]
                                        except Exception as e:
                                            print('Failed to get li out span text. Reason: %s' % e)
                                        data += "</div>"#END position-absolute ddi
                            data += "</div>"#END ID p0101_0107 CLASS position-absolute
                    data += "</div>"#END div class='korea-auc-damage aj type
                    data += '<div class="row mb-2"> <div class="col-12 font-size-sm font-weight-bold">История повреждений</div> <div class="col-lg-4 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold text-danger">X </span> <span class="tbl-caption">Замена</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">Была установлена новая деталь и окрашена</div> </div> </div> <div class="col-lg-4 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold text-danger">W </span> <span class="tbl-caption">Ремонт</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">Был выполнен ремонт и окраска детали</div> </div> </div> </div>'
                    data += '<div class="row"> <div class="col-12 font-size-sm font-weight-bold">Присутствующие дефекты</div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">A </span> <span class="tbl-caption">Царапина</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">На детали присутствуют незначительные царапины</div> </div> </div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">C </span> <span class="tbl-caption">Коррозия</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">На детали присутствует коррозия</div> </div> </div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">T </span> <span class="tbl-caption">Скол</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">На детали есть мелкий скол не требующий ремонта</div> </div> </div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">TX</span> <span class="tbl-caption">Трещина</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">Трещина на детали которая требует ремонта</div> </div> </div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">U </span> <span class="tbl-caption">Вмятина</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">На детали присутствует мелкая вметинка</div> </div> </div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">UR </span> <span class="tbl-caption">Вмятый скол</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">На детали присутствует скол с вмятиной не требует ремонта</div> </div> </div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">H </span> <span class="tbl-caption">Отверстие</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">На детали присутствует отверстие, требует ремонта</div> </div> </div> </div>'
                    data += "</div>"#END CLASS p-3
            else:
                data += "<div class='p-3'>"
                try:
                    data += "<div class='korea-auc-damage aj type-"+html.find("div#realImg>div")[i].attrs["class"][0]+" position-relative'>"
                except Exception as e:
                    print('Can\'t div#realImg>div class. Reason %s.' % e)
                try:
                    data += '<img src="http://www.sellcarauction.co.kr'+html.find("div#realImg>div")[i].find("div:last-child>img")[0].attrs["src"]+'" alt="" style="width: 736px; max-width: none">'
                except Exception as e:
                    print('Can\'t find div:last-child>img src. Reason %s.' % e)
                for k in range(len(html.find("#realImg>div")[i].find("div:last-child>ul"))):
                    try:
                        html.find("#realImg>div")[i].find("div:last-child>ul")[k].attrs
                    except Exception as e:
                        print('Can\'t find div:last-child>ul attrs. Reason %s.' % e)
                    if "class" in html.find("#realImg>div")[i].find("div:last-child>ul")[k].attrs:
                        try:
                            data += "<div id='"+html.find("#realImg>div")[i].find("div:last-child>ul")[k].attrs["class"][0]+"' class='position-absolute'>"
                        except Exception as e:
                            print('Can\'t find div:last-child>ul class. Reason %s.' % e)
                        for j in range(len(html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li"))):
                            try:
                                html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].attrs
                            except Exception as e:
                                print('Can\'t find div:last-child>ul li attrs. Reason %s.' % e)
                            if "class" in html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].attrs:
                                if (len(html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].attrs["class"]) > 0):
                                    try:
                                        data += "<div style='top:0; left:0;' class='position-absolute'>"
                                        data += "<img src='http://www.sellcarauction.co.kr"+html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].find("img")[0].attrs["src"]+"'>"
                                        data += "</div>"#END position-absolute
                                    except Exception as e:
                                        print('Failed to get li img src. Reason: %s' % e)
                                    try:
                                        data += "<div id='"+html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].attrs["id"]+"' style='"+html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].find("p")[0].attrs["style"]+"' class='position-absolute ddi'>"
                                    except Exception as e:
                                        print('Failed to get li p style. Reason: %s' % e)
                                    try:
                                        data += "<span class='text-danger'>"+html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].find("p>span.txt_red")[0].text+"</span>"
                                    except Exception as e:
                                        print('Failed to get li span text. Reason: %s' % e)
                                    try:
                                        if(len(html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].xpath("//p/text()")) != 0):    
                                            data += html.find("#realImg>div")[i].find("div:last-child>ul")[k].find("li")[j].xpath("//p/text()")[0]
                                    except Exception as e:
                                        print('Failed to get li out span text. Reason: %s' % e)
                                    data += "</div>"#END position-absolute ddi
                        data += "</div>"#END ID p0101_0107 CLASS position-absolute
                data += "</div>"#END div class='korea-auc-damage aj type
                data += '<div class="row mb-2"> <div class="col-12 font-size-sm font-weight-bold">История повреждений</div> <div class="col-lg-4 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold text-danger">X </span> <span class="tbl-caption">Замена</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">Была установлена новая деталь и окрашена</div> </div> </div> <div class="col-lg-4 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold text-danger">W </span> <span class="tbl-caption">Ремонт</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">Был выполнен ремонт и окраска детали</div> </div> </div> </div>'
                data += '<div class="row"> <div class="col-12 font-size-sm font-weight-bold">Присутствующие дефекты</div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">A </span> <span class="tbl-caption">Царапина</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">На детали присутствуют незначительные царапины</div> </div> </div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">C </span> <span class="tbl-caption">Коррозия</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">На детали присутствует коррозия</div> </div> </div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">T </span> <span class="tbl-caption">Скол</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">На детали есть мелкий скол не требующий ремонта</div> </div> </div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">TX</span> <span class="tbl-caption">Трещина</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">Трещина на детали которая требует ремонта</div> </div> </div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">U </span> <span class="tbl-caption">Вмятина</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">На детали присутствует мелкая вметинка</div> </div> </div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">UR </span> <span class="tbl-caption">Вмятый скол</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">На детали присутствует скол с вмятиной не требует ремонта</div> </div> </div> <div class="col-lg-3 mb-2"> <div class="tbl-wrap"> <div class="tbl-header font-size-sm"> <span class="tbl-symbol font-weight-bold">H </span> <span class="tbl-caption">Отверстие</span> </div> <div class="tbl-description font-weight-light" style="font-size: .7em">На детали присутствует отверстие, требует ремонта</div> </div> </div> </div>'
                data += "</div>"#END CLASS p-3
    return data

#запись айди авто в файл
def write_car_id(file_name, data):
    if html:
        try:
            return open(file_name, "a").write(data)
        except Exception as e:
            print('Can\'t wrine file %s. Reason %s.' % (file_name,e))

#ID авто для парсингу
def get_car_id(html):
    if html:
        try:
            items = html.find("div.car-title")
            print(html.find("div.car-title"))
            for item in items:
                if(len(item.find("a"))):
                    car_id = re.search('[A-Z]+[0-9]+', item.find("a")[0].attrs['onclick'])
                    print(item.find("a")[0])
                    print(car_id)
                    if car_id:
                        write_car_id("car_id.txt",car_id.group()+"\n")
        except Exception as e:
            print('Can\'t get car id. Reason %s.' % e)

#парсимо всі ссилки на авто по сторінкам
def get_pages(page_start=1, page_end=2):
    for i in range(page_start,page_end+1):
        unf = uniform(1,6)
        time.sleep(unf)
        print("Page %d. Sleep %d." % (i, unf))
        html = fetch(config['SELLCAR']['URL']+"?i_iPageSize=&i_iNowPageNo="+str(i))
        get_car_id(html)
    pass
#складаємо всі ссилки на авто в один файл
def get_all_links(car_link, file_name="car_id.txt"):
    return list(map( lambda x: '{}?receivecd={}'.format( car_link, x ), read_file(file_name, "\n")))

#год автомобиля
def get_car_year(html):
    if html:
        try:
            if(len(html.find("strong.text-right"))>2):
                res = re.search("[0-9]+", str(html.find("strong.text-right")[2].text))
                if(res):
                    year = res.group()
                    if(len(year) == 4):
                        return int(year)
                    else:
                        return int(year[0:4])
        except Exception as e:
            print('Can\'t get car year. Reason %s.' % e)
            return "None"
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
#название авто
def get_car_title(html):
    if html:
        try:
            if(len(html.find("h2.tit_style2"))):
                return clear_car_name(ko_translate(rm_new_line(str(html.find("h2.tit_style2")[0].text)), "en"))
        except Exception as e:
            print('Can\'t get title. Reason %s.' % e)
            return "None"

#категория авто
def get_car_category(html):
    if html:
        categoty_data = {
                "Genesis":"Genesis",
                "Kia":"Kia Motors",
                "Hyundai":"Hyundai",
                "Ssangyong":"SsangYong",
                "Renault":"Renault",
                "Benz":"Mercedes Benz",
                "Mercedes":"Mercedes Benz",
                "Daewoo":"Chevrolet",
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
                "Audi":"Audi",
                "Citroen":"Citroen",
                "Honda":"Honda",
                "Daechang":"Daechang Motors",
                "Chrysler":"Chrysler",
                "Porsche":"Porsche",
                "Dodge":"Dodge",
                "Volvo":"Volvo",
                "Infinity":"Infinity"
            }
        try:
            data = re.match("^[0-9]+\s(\w+)", get_car_title(html))
            if(data):
                if(data.group(1) and categoty_data[data.group(1)]):
                    return categoty_data[data.group(1)]
                else:
                    return "None"
        except Exception as e:
            print('Can\'t get car category. Reason %s.' % e)
            return "None"

#цвет автомобиля
def get_car_color(html):
    if html:
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
        try:
            if(len(html.find("strong.text-right"))>9):
                return color_data[re.sub("\s.+","", rm_new_line(str(html.find("strong.text-right")[9].text)))]
        except Exception as e:
            print('Can\'t get car color. Reason %s.' % e)
            return "None"

def get_car_estimate(html):
    if html:
        try:
            item = html.find("#body > section.con_top.gray-bg_fin > div:nth-child(2) > div > div > div > table > tbody > tr:nth-child(1) > td")[0].text
            if item:
                return "".join(re.findall("[A-Z]", str(item)))
        except Exception as e:
            print('Can\'t get car estimate %s. Reason: %s' % e)

#тип автомобиля
def get_car_type(html):
    if html:
        car_type_data = {
            "승합 (6인승)":"Универсал",
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
            "승합 (25인승)":"Автобус",
            "승합 (9인승)":"Минивен",
            "승용 (9인승)":"Минивен",
            "승용 (6인승)":"Минивен",
            "화물 (6인승)":"Минивен",
            "승용 (4인승)":"Хэтчбек",
            # "Кроссовер",
            "승용 (0인승)":"Купе",
            "승합 (2인승)":"Купе",
            "화물 (2인승)":"Купе",
            "승용 (2인승)":"Купе",
            "SUV픽업 (5인승)":"Внедорожник пикап"
            # "Кабриолет",
            # "Багги"
        }
        try:
            if(len(html.find("strong.text-right"))>10):
                return car_type_data[rm_new_line(str(html.find("strong.text-right")[10].text))]
        except Exception as e:
            print('Can\'t get car type. Reason %s.' % e)
            return "None"

#пробег
def get_distance_driven(html):
    if html:
        try:
            res = re.findall("[0-9]+", rm_new_line(str(html.find("strong.text-right")[5].text)))
            return "".join(res)
        except Exception as e:
            print('Can\'t get driven distance. Reason %s.' % e)
            return "None"

#двигатель
def get_car_displacement(html):
    if html:
        try:
            res = re.findall("[0-9]+", rm_new_line(html.find("strong.text-right")[6].text))
            return "".join(res)
        except Exception as e:
            print('Can\'t get car displacement. Reason %s.' % e)
            return "None"

#коробка передач
def get_transmission(html):
    if html:
        try:
            if(rm_new_line(str(html.find("strong.text-right")[8].text))=="오토"):
                return "Автомат"
            else:
                return "Механика"
        except Exception as e:
            print('Can\'t get transmission. Reason %s.' % e)
            return "None"

#топливо
def get_fuel(html):
    if html:
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
        try:
            if(len(html.find("strong.text-right"))>3):
                return fulel_data[rm_new_line(str(html.find("strong.text-right")[4].text))]
        except Exception as e:
            print('Can\'t get fuel. Reason %s.' % e)
            return "None"

#лот аукциона
def get_lot_id(html):
    if html:
        try:
            if(len(html.find("h2.tit_style2"))):
                res = re.search("\[{1}\d+\]{1}", ko_translate(rm_new_line(str(html.find("h2.tit_style2")[0].text)), "en"))
                if(res):
                    res = res.group()
                    res = re.sub("\[{1}", "", res)
                    res = re.sub("\]{1}", "", res)
                    return res
        except Exception as e:
            print('Can\'t get title. Reason %s.' % e)
            return "None"

#марка авто
def get_car_mark(html):
    if html:
        try:
            if(len(html.find("#body > section.con_top.gray-bg_fin > div.container-fluid.wide_area.mt_1.car_view_check_area > div > div > div > table > tbody > tr:nth-child(7) > td:nth-child(2)"))):     
                return ko_translate(rm_new_line(str(html.find("#body > section.con_top.gray-bg_fin > div.container-fluid.wide_area.mt_1.car_view_check_area > div > div > div > table > tbody > tr:nth-child(7) > td:nth-child(2)")[0].text)),"en")
        except Exception as e:
            print('Can\'t get car mark. Reason %s.' % e)
            return "None"

#VIN номер авто
def get_car_vin(html):
    if html:
        try:
            if(len(html.find("#body > section.con_top.gray-bg_fin > div:nth-child(1) > div.row.mt_5 > div.col-md-4.car-details-sidebar > div > ul > li:nth-child(2) > strong"))):
                return str(html.find("#body > section.con_top.gray-bg_fin > div:nth-child(1) > div.row.mt_5 > div.col-md-4.car-details-sidebar > div > ul > li:nth-child(2) > strong")[0].text)
        except Exception as e:
            print('Can\'t get VIN number. Reason %s.' % e)

def get_car_category_url(html):
    if html:
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
                "Toyota":"toyota",
                "Tesla":"tesla",
                "Audi":"audi",
                "Citroen":"citroen",
                "Daechang Motors":"daechang-motors",
                "Chrysler":"chrysler",
                "Porsche":"porsche",
                "Dodge":"dodge",
                "Volvo":"volvo",
                "Infinity":"infinity"
            }
        try:
            if(get_car_category(html)):
                return categoty_url_data[get_car_category(html)]
            else:
                return "None"
        except Exception as e:
            print('Can\'t get car category url. Reason %s.' % e)
            return "None"

#цена автомобиля 
def get_car_price(html):
    if html:
        try:
            if(len(html.find("strong.i_comm_main_txt2"))):
                price = int(re.sub("\,", "", html.find("strong.i_comm_main_txt2")[0].text))
                return int(price*10000/int(config['SELLCAR']['USD']))
        except Exception as e:
            print('Can\'t get car price. Reason %s.' % e)
            return "None"

#описание авто 
def get_car_description(html, link):
    description = ""
    if html:
        try:
            vr = re.search("[A-Z0-9]+$", link)
            if vr:
                vr = vr.group()
        except Exception as e:
            print('Can\'t get car ID for VR 360 view auto. Reason %s.' % e)
        try:
            description += '<div class="timeline-heading"><h3>VR360 обзор авто</h3></div>'
            description += '<iframe frameborder="0" height="600" id="ovulyaciya" scrolling="no" src="https://www.sellcarauction.co.kr/newfront/receive/rc/receive_rc_view_vr.do?isLandscapeOpen=Y&amp;isBrowserOpen=Y&amp;receivecd=%s" width="900"></iframe>' % vr
        except Exception as e:
            print('Can\'t get car description "VR 360 view auto". Reason %s.' % e)
        try:
            description += '<div class="timeline-heading"><h3>Информация об оценке производительности</h3></div>'
            description += text_len(rm_new_line(str(html.find("#body > section.con_top.gray-bg_fin > div:nth-child(2) > div > div > div > table")[0].html)), "ru")
        except Exception as e:
            print('Can\'t get car description "Performance Evaluation Information". Reason %s.' % e)
        try:
            description += '<div class="timeline-heading"><h3>Информация о вариантах</h3></div>'
            description += text_len(rm_new_line(str(html.find("#body > section.con_top.gray-bg_fin > div:nth-child(3) > div > div > table:nth-child(2)")[0].html)), "ru")
        except Exception as e:
            print('Can\'t get car description "Option information". Reason %s.' % e)
        try:   
            description += text_len(rm_new_line(str(html.find("#body > section.con_top.gray-bg_fin > div:nth-child(3) > div > div > ul")[0].html)), "ru")
        except Exception as e:
            print('Can\'t get car descritpion comm list. Reason %s.' % e)
        description += rm_new_line(get_car_img(html))
        # try:
        #     description += '<div class="timeline-heading"><h3>Протокол осмотра</h3></div>'
        #     text = text_len(rm_new_line(str(soup.select("#body > section.con_top.gray-bg_fin > div.container-fluid.wide_area.mt_1.car_view_check_area > div > div > div > table")[0])), "ru")
        #     text = re.sub("\/newfront\/images\/","http://www.sellcarauction.co.kr/newfront/images/",text)
        #     description += text
        # except Exception as e:
        #     print('Can\'t get car description "Inspection protocol". Reason %s.' % e)
        return rm_new_line(description)

#фото авто
def get_img_src(html):
    if html:
        try:
            items = html.find("img.img-fluid")
            images = []
            for item in items:
                if "src" in item.attrs:
                    match = re.search('\_S\.[jpeg|jpg|JPG|JPEG|gif|png]+$', item.attrs['src'])
                    if match:
                        #download_images(item.attrs['src'].replace('_S', ''))
                        images.append(item.attrs['src'].replace('_S', ''))
                    else: 
                        continue
            return images
        except Exception as e:
            print('Can\'t get img src. Reason %s.' % e)
            return "None"

def get_img_str(imgs, html):
    if html:
        try:
            title = get_car_title(html)
            img_str = ""
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
            return "None"

#записуємо усі данні у файл
def write_csv(data, name = "data.csv"):
    path = os.getcwd() + os.path.sep + name
    try: 
        with open(path, 'a', encoding="utf-8", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([data['category'], data['category_url'], data['title'], ' ', data['description'], data['price'], data['url'], data['images'], data['article'], data['count'], data['activation'], data['title-seo'], ' ', ' ', ' ', data['recomended'], data['new'], '0', '0', ' ', ' ', ' ', data['currency'], data['properties']])
    except Exception as e:
        print('Can\'t write csv file. Reason %s' % e)

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
                    ftpCommand = "STOR %s" % name #comment if you whant download to local machine
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

def rm_csv(name = "data.csv"):
        try:
            os.remove(name)
            print("File "+name+" Removed!")
        except Exception as e:
                print('Failed to remove file %s. Reason: %s' % (name,e))
def create_csv(name = "data.csv"):
    path = os.getcwd() + os.path.sep + name
    try:
        with open(path, 'w', encoding="utf-8", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Категория', 'URL категории', 'Товар', 'Вариант', 'Описание', 'Цена', 'URL', 'Изображение', 'Артикул', 'Количество', 'Активность', 'Заголовок [SEO]', 'Ключевые слова [SEO]', 'Описание [SEO]', 'Старая цена', 'Рекомендуемый', 'Новый', 'Сортировка', 'Вес', 'Связанные артикулы', 'Смежные категории', 'Ссылка на товар', 'Валюта', 'Свойства'])
    except Exception as e:
            print('Failed to create file "data.csv". Reason: %s' % e)

#витягуємо всі данні на авто
def get_car(link):
    car = {}
    p = current_process()
    if(p.name != 'MainProcess' and p._identity[0] and os.getpid()):
        print('process counter:', p._identity[0], 'pid:', os.getpid())
    # unf = uniform(1,4)
    # time.sleep(unf)
    html = fetch(link)
    print(link)
    if html:
        try:
            year = get_car_year(html)
            category = get_car_category(html)
            # if(isinstance(year,int) and (year < 2012)):
            #     return
            color = get_car_color(html)
            car_estimate = get_car_estimate(html)
            car_type = get_car_type(html)
            distance_driven = get_distance_driven(html)
            displacement = get_car_displacement(html)
            transmission = get_transmission(html)
            fuel = get_fuel(html)
            lot_number = get_lot_id(html)
            car_registration = get_car_registration(html)
            mark = "" if not category or not get_car_mark(html) else category +" "+get_car_mark(html).upper()
            car_vin = get_car_vin(html)
            mark_url = re.sub("\.", "", mark)            
            mark_url = re.sub("\(", "", mark_url)                                
            mark_url = re.sub("\)", "", mark_url)
            mark_url = re.sub("\s", "-", mark_url)
            car['url'] = car_vin.lower()+"-"+mark_url.lower()
            car['category'] = category
            car['category_url'] = get_car_category_url(html)
            car['title'] = get_car_title(html)
            car['title-seo'] = car['title']
            car['price'] = get_car_price(html)
            car['description'] = get_car_description(html, link)
            car['images'] = get_img_str(get_img_src(html), html)
            car['count'] = '0'
            car['activation'] = '1'
            car['currency'] = 'USD'
            car['recomended'] = '0'
            car['new'] = '0'
            car['article'] = get_lot_id(html)
            car['properties'] = 'Цвет=[type=assortmentCheckBox value=%s product_margin=Желтый|Белый|Серебро|Красный|Фиолетовый|Оранжевый|Зеленый|Серый|Золото|Коричневый|Голубой|Черный|Бежевый]&Кузов=[type=assortmentCheckBox value=%s product_margin=Универсал|Фургон|Фура|Трактор|Седан|Родстер|Пикап|Мотоцикл|Минивен|Хэтчбек|Кроссовер|Купе|Кабриолет|Багги]&Пробег=%s&Двигатель=%s&Год=%s&Первая регистрация=%s&Трансмиссия=[type=assortmentCheckBox value=%s product_margin=Механика|Автомат]&Топливо=[type=assortmentCheckBox value=%s product_margin=Дизель|Бензин|Газ]&Модель=%s&Марка=%s&Номер лота=%s&Оценка автомобиля=%s&VIN номер=%s&Аукцион=sellcarauction %s' % (color, car_type, distance_driven, displacement, year, car_registration, transmission, fuel, mark, category, lot_number, car_estimate, car_vin, config['SELLCAR']['DATE'])
            #download_images(get_img_src(html))
            write_csv(car)
        except Exception as e:
            print("Can\'t write car data to csv.")

#головна функція яка запускається
def main():
    time_start = time.time()
    if(config['SELLCAR']['AUTOCODE'] == '0'):
        rm_csv("car_id.txt")
        max_page = parser(config['SELLCAR']['URL']+"?i_iPageSize=&i_iNowPageNo=1", get_max_page)
        get_pages(1,max_page)
    elif(config['SELLCAR']['AUTOCODE'] == '1' or config['SELLCAR']['AUTOCODE'] == '2' or config['SELLCAR']['AUTOCODE'] == '3'):
        rm_csv()
        create_csv()
        #create_folder('./py_img')
        #clear_folder('./py_img/')
        
        my_list = get_all_links(config['SELLCAR']['CAR_LINK'])

        with Pool(25) as p:
            p.map(get_car, my_list) 

    time_end = time.time() 
    print(time_end - time_start)

if __name__ == '__main__':
    main()
