# -*- coding: utf-8 -*-
from ftplib import FTP
from requests_html import HTMLSession
from multiprocessing import current_process, Pool
from deep_translator import GoogleTranslator
from random import uniform, choice
import mysql.connector as mysql
import urllib.parse
import requests
import time
import re
import os
import csv
import html
import fake_useragent
import configparser
from urllib import parse
from io import BytesIO
import shutil
from addnewproduct import AddNewProduct
config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini")

class JSParser:
    def __init__(self):
        self.user = fake_useragent.UserAgent().random
        #self.addprod = AddNewProduct()#создание класа добавление продукта сразу в базу данных
        self.session = HTMLSession()
        if(config['GLOVIS']['FTPCODE'] == '1'):
            self.ftp = FTP("217.172.189.14")
            self.ftp.login("olegk202","Kostiuk_6173")
            self.ftp.cwd("public_html/uploads/tempimage")

#read file function 
    def read_file(self, file_name, delimiter="\n"):
        try:
            return open(file_name).read().split(delimiter)
        except Exception as e:
            print('Can\'t read %s. Reason %s.' % (file_name, e))

#translate function 
    def ko_translate(self, text, lan):
        try:
            if(len(text)>1 and len(text)<5000 and isinstance(text,str)):
                return GoogleTranslator(source='ko', target=lan).translate(text)
        except Exception as e:
            print('Failed to Translate text. Reason: %s' % e)
            res = ''
            return res

#следит чтоб небило длины текста более 5000 символов
    def text_len(self, text, lang):
        new_text = ''
        if(isinstance(text,str) and len(text)>1):
            if(len(text)>5000):
                i = 0
                while (i <= int(len(text)/4999)):
                    if(i == int(len(text)/4999)):
                        new_text += self.ko_translate(text[i*4999:len(text)],lang)
                    else:        
                        new_text += self.ko_translate(text[i*4999:i+1*4999], lang)
                    i+=1
            else: 
                new_text = self.ko_translate(text, lang)
            return new_text
#створюємо папку
    def create_folder(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except Exception as e:
            print('Can\'t create folder in path %s. Reason %s' % path, e)
#очищаємо усі файли із папки
    def clear_folder(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
#удаляємо всі зайві пробіли, переноси строк і табуляції
    def rm_new_line(self, string):
        try:
            string = html.unescape(string)
            string = re.sub("\&\s*\#\s*13\;", "", string)
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
    def clear_img_name(self, img_name):
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

#очистка назв авто от непонятних символов
    def clear_car_name(self, car_name):
        try:
            if(isinstance(car_name, str) and car_name != ''):
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

#залогінюємось на сайті
    def login(self, login_link):
        try:
            self.session.headers.update({
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language': 'en-GB,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                #'Content-Length': '57',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'DNT': '1',
                'Host':'www.glovisaa.com',
                'Origin': 'https://www.glovisaa.com',
                'Pragma': 'no-cache',
                'Referer': 'https://www.glovisaa.com/login.do?returnUrl=jh2ISr6qitW90ERi3vig%2BXa%2B%2F2AbjWqZ%2FX5jbcCGxss%3D',
                'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
                'sec-ch-ua-mobile': '?0',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55',
                'X-Requested-With': 'XMLHttpRequest'
                })
            login_data = {
                "passno": "amo1NTA3Kio=",
                "idsaveyn": "Y",
                "id": "4292"
            }
            r = self.session.request('POST', login_link, login_data, allow_redirects=False)
            if(r.status_code == 200):
                return r.html
            else:
                return r.status_code
        except Exception as e:
            print('Can\'t get HTML form %s. Reason %s.' % (login_link, e))

#витягивание куки с ответа      
    def fetch(self, url, rend=0, prox=0):
        self.session.headers.update({'User-Agent': fake_useragent.UserAgent().random})
        data = ''
        p = current_process()
        if(p.name != 'MainProcess' and p._identity[0] and os.getpid()):
            print('process counter:', p._identity[0], 'pid:', os.getpid())
        if(prox != 0):
            #parsing from proxy
            print("parsing from proxy")
            proxy = { 'http': 'http://' + choice(self.read_file("proxies.txt","\n")) +'/' }
            self.session.proxies.update(proxy)
        try:
            r = self.session.request('GET', url, allow_redirects=False)
            time.sleep(uniform(3,6))
            if(r.status_code == 200 or r.status_code == 302):
                if(rend != 0):
                    r.html.render(timeout=30)
                data = r.html
            else:
                data = r.status_code
        except Exception as e:
            print('Failed to get page %s. Reason: %s' % (url, e))
        return data
#витягуємо максимальне число сторінок
    def get_max_page(self, html, pages=10):
        try:
            print(int(html.find("div.boarddv p.sti3 span.inlne span")[3].text))
            if(int(html.find("div.boarddv p.sti3 span.inlne span")[3].text) % pages > 0):
                return int(int(html.find("div.boarddv p.sti3 span.inlne span")[3].text)/pages) + 1
            else:
                return int(int(html.find("div.boarddv p.sti3 span.inlne span")[3].text)/pages)
        except Exception as e:
            print('Can\'t get max page. Reason %s' % e)

#витягуємо дату аукціону
    def get_auction_date(self, html):
        try:
            return "{}/{}/{}".format(str(html.find("div.boarddv p.sti3 span.inlne span")[0].text), str(html.find("div.boarddv p.sti3 span.inlne span")[1].text), str(html.find("div.boarddv p.sti3 span.inlne span")[2].text))
        except Exception as e:
            print('Can\'t get auction date. Reason %s' % e)

#витягивание карти повреждений
    def get_car_img(self, html):
        data = ''
        if(html != ""):
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
    def write_car_id(self, file_name, data):
        if(html != ""):
            try:
                return open(file_name, "a").write(data)
            except Exception as e:
                print('Can\'t wrine file %s. Reason %s.' % (file_name,e))

#ID авто для парсингу
    def get_car_id(self, html):
        if(html !=""):
            try:
                items = html.find("a.btn_view")
                for i, item in enumerate(items):
                    if i % 2 == 0:
                        self.write_car_id("car_id3.txt",urllib.parse.quote_plus(item.attrs['rc'])+"|"+urllib.parse.quote_plus(item.attrs['cd'])+"\n")
            except Exception as e:
                print('Can\'t get car id. Reason %s.' % e)

#парсимо всі ссилки на авто по сторінкам
    def get_pages(self, searchAuctno=209, page_start=1, page_end=2):
        for i in range(page_start,page_end+1):
            unf = uniform(1,4)
            time.sleep(unf)
            print("Page %d. Sleep %d." % (i, unf))
            link = '{}?&atn={}&ac={}&acc={}&page1={}&page={}'.format( config['GLOVIS']['URL'], str(searchAuctno), urllib.parse.quote_plus("TQhYt3GD6GvgPdVw1QX+Wg=="), urllib.parse.quote_plus("u9cesU3il5ljSzAzHZzmEg=="), page_start,  i)
            #print(link)
            html = self.fetch(link)
            self.get_car_id(html)
        pass

#складаємо всі ссилки на авто в один файл
    def get_all_links(self, car_link=config['GLOVIS']['CAR_LINK'], file_name="car_id3.txt"):
        data = self.read_file(file_name)
        res = list(map(lambda x: x.split('|'), data[:-1]))
        return list(map(lambda x: '{}?&rc={}&gn={}&ac={}&atn={}&acc={}'.format(car_link, x[0], x[1], urllib.parse.quote_plus("TQhYt3GD6GvgPdVw1QX+Wg=="), urllib.parse.quote_plus(str(config['GLOVIS']['ATN_NUM'])), urllib.parse.quote_plus("u9cesU3il5ljSzAzHZzmEg==")), res))

#год автомобиля
    def get_car_year(self, html):
        if(html != ''):
            try:
                if(len(html.find("div.dv03.short p"))):
                    res = re.match("[0-9]+", str(html.find("div.dv03.short p")[0].text))
                    if(res):
                        year = int(res.group())
                        if(isinstance(year,int)):
                            return year
                        else:
                            return int(2013)
            except Exception as e:
                print('Can\'t get car year. Reason %s.' % e)
                return "None"

#год первой регистрации автомобиля
    def get_car_registration(self, html):
        if(html != ''):
            try:
                if(len(html.find("div.view_info div.in ul:nth-child(2) li:nth-child(1) span"))):
                    res = re.findall("([0-9]{4}).+([0-9]{2}).+([0-9]{2})", str(html.find("div.view_info div.in ul:nth-child(2) li:nth-child(1) span")[1].text))
                    if(len(res)>0):
                        return str(res[0][0]+"/"+res[0][1]+"/"+res[0][2])
            except Exception as e:
                print('Can\'t get car registration. Reason %s.' % e)
                return "None"

#название авто
    def get_car_title(self, html):
        if(html != ''):
            try:
                if(len(html.find("p.carnm"))):
                    title = re.sub("\?", "", self.clear_car_name(self.ko_translate(html.find("p.carnm")[0].text, "en")))  
                    return title
                else:
                    return "None"
            except Exception as e:
                print('Can\'t get title. Reason %s.' % e)
                return "None"

#категория авто
    def get_car_category(self, html):
        if(html != ''):
            categoty_data = {
                    "Genesis":"Genesis",
                    "Kia":"Kia Motors",
                    "Hyundai":"Hyundai",
                    "Modern":"Hyundai",
                    "Ssangyong":"SsangYong",
                    "Renault":"Renault",
                    "Benz":"Mercedes Benz",
                    "Chevrolet":"Chevrolet",
                    "ChevroletDaewoo":"Chevrolet",
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
                    "Chrysler":"Chrysler",
                    "Volvo":"Volvo",
                    "Citroen":"Citroen",
                    "Infinity":"Infinity",
                    "Maserati":"Maserati"
                }
            try:
                if(len(html.find("p.carnm"))):
                    res = re.match("^(\[\w+\])", self.ko_translate(html.find("p.carnm")[0].text, "en"))
                    if(res):
                        res = res.group(1)
                        category = res[1:-1]
                        print(category)
                        return categoty_data[category]
            except Exception as e:
                print('Can\'t get car category. Reason %s.' % e)
                return "None"

#цвет автомобиля
    def get_car_color(self, html):
        if(html != ''):
            color_data = {
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
                "N5S)하이퍼실버": "Cерый"
            }
            try:
                if(len(html.find("div.view_info div.in ul:nth-child(2) li:nth-child(3) span")) and html.find("div.view_info div.in ul:nth-child(2) li:nth-child(3) span")[1].text):
                    return color_data[html.find("div.view_info div.in ul:nth-child(2) li:nth-child(3) span")[1].text]
            except Exception as e:
                print('Can\'t get car color. Reason %s.' % e)
                return "None"

#оцінка авто
    def get_car_estimate(self, html):
        if(html != ''):
            try:
                if(len(html.find("div.dv03 p:nth-child(2) strong"))):
                    return html.find("div.dv03 p:nth-child(2) strong")[0].text
            except Exception as e:
                print('Can\'t get car estimate %s. Reason: %s' % e)

#тип автомобиля
    def get_car_type(self, html):
        if(html != ''):
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
            try:
                return "Седан"
                #return car_type_data[self.rm_new_line(str(html.find("strong.text-right")[10].text))]
            except Exception as e:
                print('Can\'t get car type. Reason %s.' % e)
                return "None"

#пробег
    def get_distance_driven(self, html):
        if(html != ''):
            try:
                if(len(html.find("div.dv03.short p"))):
                    res = re.search("[0-9]{,3}\,[0-9]{3}km", html.find("div.dv03.short p")[0].text)
                    if(res):
                        res = res.group()
                        res = re.sub("\,", "", res)
                        res = re.sub("km", "", res)
                    return res
            except Exception as e:
                print('Can\'t get driven distance. Reason %s.' % e)
                return "None"

#двигатель
    def get_car_displacement(self, html):
        if(html != ''):
            try:
                if(len(html.find("div.dv03.short p"))):
                    res = re.search("[0-9]{,2}\,[0-9]{3}cc", html.find("div.dv03.short p")[0].text)
                    if(res):
                        res = res.group()
                        res = re.sub("\,", "", res)
                        res = re.sub("cc", "", res)
                    return res
            except Exception as e:
                print('Can\'t get car displacement. Reason %s.' % e)
                return "None"

#коробка передач
    def get_transmission(self, html):
        if(html != ''):
            try:
                return "Механика"
            except Exception as e:
                print('Can\'t get transmission. Reason %s.' % e)
                return "None"

#топливо
    def get_fuel(self, html):
        if(html != ''):
            fulel_data = {
                "가솔린":"Бензин",
                "휘발유":"Бензин",
                "경유":"Дизель",
                "디젤":"Дизель",
                "LPG":"LPG",
                "Hybrid":"Гибрид",
                "하이브리드":"Гибрид",
                "LPI하이브리드":"LPG гибрид",
                "가솔린하이브리드":"Бензиновый гибрид",
                "디젤하이브리드": "Дизельный гибрид",
                "전기":"Электрокар",
                "가솔린/LPG":"Бензин/LPG",
                "겸용":"Комбинированное использование"
            }
            try:
                if(len(html.find("div.view_info div.in ul:nth-child(1) li:nth-child(4) span:nth-child(2)"))):
                    return fulel_data[str(html.find("div.view_info div.in ul:nth-child(1) li:nth-child(4) span:nth-child(2)")[0].text)]
            except Exception as e:
                print('Can\'t get fuel. Reason %s.' % e)
                return "None"

#лот аукциона
    def get_lot_id(self, html):
        if(html != ''):
            try:
                if(len(html.find("div.vinfo div.dv02 span.nm"))):
                    return str(html.find("div.vinfo div.dv02 span.nm")[0].text)
                else:
                    return "None"
            except Exception as e:
                print('Can\'t get title. Reason %s.' % e)
                return "None"

#марка авто
    def get_car_mark(self, html):
        try:
            db_connection = mysql.connect(host="217.172.189.14", database="olegk202_kdm", user="olegk202_kdm", password="Kostiuk_6173")
        except Exception as e:
            print(e)
        if(html != ''):
            car_model = ''
            title_arr = []
            categoty_data = {
                    "Genesis":"Genesis",
                    "Kia":"Kia Motors",
                    "Hyundai":"Hyundai",
                    "Modern":"Hyundai",
                    "Ssangyong":"SsangYong",
                    "Renault":"Renault",
                    "Benz":"Mercedes Benz",
                    "Chevrolet":"Chevrolet",
                    "Daewoo":"Chevrolet",
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
                    "Volvo":"Volvo",
                    "Citroen":"Citroen",
                    "Kiasportage":"Kia Motors",
                    "Chevrolettrax":"Chevrolet",
                    "Chrysler":"Chrysler",
                    "Chevroletspark":"Chevrolet",
                    "Honda":"Honda",
                    "Subaru":"Subaru",
                    "Kiacarens":"Kia Motors",
                    "Chevroletraceti":"Chevrolet",
                    "Infinity":"Infinity"
                }
            try:
                if(len(html.find("p.carnm"))):
                    title = self.clear_car_name(self.ko_translate(html.find("p.carnm")[0].text, "en"))
                    title = re.sub(" All New", "", title)
                    title = re.sub(" The New", "", title)
                    title = re.sub(" The Next", "", title)
                    title = re.sub(" New", "", title)
                    title = re.sub(" LF", "", title)
                    title = re.sub(" Samsung", "", title)
                    title = re.sub("ChevroletDaewoo", "Chevrolet", title)
                    title = re.sub(" Daewoo", "", title)
                    title_arr = title.split()
                    car_model = categoty_data[str(title_arr[0])]
            except Exception as e:
                print('Can\'t get car mark. Reason %s.' % e)
            if(car_model and len(title_arr)>1):
                select_car_query = "SELECT value FROM mg_product_user_property WHERE property_id=157 AND UPPER(value) LIKE UPPER('"+car_model+" "+title_arr[1]+" %') LIMIT 1;"
                with db_connection.cursor() as cursor:
                    cursor.execute(select_car_query)
                    result = cursor.fetchall()
                db_connection.close()
                if(len(result) == 0):
                    print("NEW Car Category:", car_model, title_arr[1])
                    return car_model+" "+str(title_arr[1]).upper()
                else:
                    for row in result:
                        #print("EXIST Car Category:", row[0])
                        if(row[0]):
                            car_mark = row[0]
                            return car_mark

#VIN номер авто
    def get_car_vin(self, html):
        if(html != ''):
            try:
                if(len(html.find("div.view_info div.in ul:nth-child(1) li:nth-child(7) span:nth-child(2)"))):
                    return str(html.find("div.view_info div.in ul:nth-child(1) li:nth-child(7) span:nth-child(2)")[0].text)
            except Exception as e:
                print('Can\'t get VIN number. Reason %s.' % e)

#перетворюємо назву категорії в ссилку 
    def get_car_category_url(self, html):
        if(html != ''):
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
                    "Volvo":"volvo",
                    "Chrysler":"chrysler",
                    "Citroen":"citroen",
                    "Infinity":"infinity",
                    "Maserati":"maserati"
                }
            try:
                if(self.get_car_category(html)):
                    return categoty_url_data[self.get_car_category(html)]
            except Exception as e:
                print('Can\'t get car category url. Reason %s.' % e)
                return "None"

#цена автомобиля 
    def get_car_price(self, html):
        if(html != ''):
            try:
                price = re.sub(",", "", html.find("div.vinfo div.dv04 span.nm")[0].text)
                price = int(price)
                return int(price*10000/int(config['GLOVIS']['USD']))
            except Exception as e:
                print('Can\'t get car price. Reason %s.' % e)
                return "None"

#описание авто 
    def get_car_description(self, html):
        description = ''
        # try:
        #     description += '<h2 class="page-subtit mt60">Информация о транспортном средстве</h2>'
        #     description += '<div class="view_info info01">'+self.text_len(html.find("div.view_info.info01 div.in")[0].html, "ru")+'</div>'
        # except Exception as e:
        #     print('Can\'t get car description "Performance Evaluation Information". Reason %s.' % e)
        # try:
        #     description += '<h2 class="page-subtit mt60">Информация о вариантах</h2>'
        #     description += '<div class="view_info info02">'+self.text_len(html.find("div.view_info.info02")[0].html, "ru")+'</div>'
        # except Exception as e:
        #     print('Can\'t get car description "Option information". Reason %s.' % e)
        try: 
            description += '<h2 class="page-subtit mt60">Лист проверки производительности</h2>'
            img_src = re.sub("menuCd=", "menuCd=WCUA", str(html.find("div.view_info.info03 div.in ul li:nth-child(6) img")[0].attrs['src']))
            description += '<div class="car-status-map"><img src="https://www.glovisaa.com'+img_src+'"></div>'
            description += '<table class="tbl-v02"><colgroup><col style="width: 140px;"><col style="width: auto;"></colgroup><tbody><tr><th> Аббревиатура </th><td><p class="abbr"><span class="abbr-q"> Небольшая вмятина </span><span class="abbr-pp"> Косметический окрас </span><span class="abbr-ppq"> Косметический окрас/сейчас есть вмятина </span><span class="abbr-xx"> Замена </span><span class="abbr-xxa"> Была замена/сейчас есть мелкая царапина </span><span class="abbr-x"> Рекомендуется замена (на практике часто мелкий скол на стекле, фаре, зеркале) </span><span class="abbr-e"> Рекомендуется замена </span><span class="abbr-r"> Сколы/царапины </span><span class="abbr-w"> Ремонт/возможно шпаклëвка </span><span class="abbr-m"> Регулировка </span><span class="abbr-f"> Изгиб/залом металла </span><span class="abbr-а"> Мелкие Сколы/царапины </span><span class="abbr-с"> Коррозия </span></p></td></tr><tr style="display: none;"><th> Specials </th><td> Дефект сиденья, дефект материала внутренней части, дефект аварийной подушки, разгрузка двигателя, утечка моторного масла, шарнир двигателя, контрольная лампа двигателя, дефект миссии, дефект PS, дефект центровки, дефект глушителя, нижний шарнир, коррозия нижней части кузова </td></tr></tbody></table>'
        except Exception as e:
            print('Can\'t get car descritpion comm list. Reason %s.' % e)
        return self.rm_new_line(description)

#фото авто
    def get_img_src(self, html):
        try:
            items = html.find("div#navithumb ul.slides li")
            images = []
            for item in items:
                if "src" in item.find("img")[0].attrs:
                    images.append("https://www.glovisaa.com"+item.find("img")[0].attrs['src'])
            return images
        except Exception as e:
            print('Can\'t get img src. Reason %s.' % e)
            return "None"

#перетвоюємо ссилки на картинки у строки для запису в файл csv
    def get_img_str(self, imgs, html):
        try:
            img_ext = 'jpg'
            title = self.get_car_title(html)
            name = self.clear_car_name(title)
            name = name.lower()
            name = re.sub("\s","_", name)
            name = self.get_lot_id(html)+"_"+name
            img_str = ''
            for i, img in enumerate(imgs) :
                img_str += name+'_'+str(i)+'.'+img_ext+'[:param:][alt='+title+'][title='+title+']|'
            return img_str[:-1]
        except Exception as e:
            print('Can\'t get Images str. Reason %s' % e)
            return "None"
#удаляємо всі зайві пробіли, ненужні символи у назві картинки
    def clear_img_name(self, img_name):
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
#закачуємо усі картинки
    def download_images(self, html, img_urls, folder_name='py_img3'):
        time.sleep(uniform(1,2))
        try:
            img_ext = 'jpg'
            title = self.clear_car_name(self.get_car_title(html))
            title = title.lower()
            title = re.sub("\s","_", title)
            title = self.get_lot_id(html)+"_"+title
            if(isinstance(img_urls, list)):
                for i, img_url in enumerate(img_urls):          
                    img_name = title+"_"+str(i)+"."+img_ext
                    if(config['GLOVIS']['FTPCODE'] == '1'):
                        img_data = BytesIO(requests.get(img_url).content) #without BytesIO if you whant download to local machine
                        ftpCommand = "STOR %s"%img_name #comment if you whant download to local machine
                        self.ftp.storbinary(ftpCommand, fp=img_data) #comment if you whant download to local machine
                    else:
                        img_data = requests.get(img_url).content
                        with open('./' + folder_name + '/' + img_name, 'wb') as handler:
                            handler.write(img_data)
            else:
                img_name = title+"."+img_ext
                if(config['GLOVIS']['FTPCODE'] == '1'):
                    img_data = BytesIO(requests.get(img_urls).content) #without BytesIO if you whant download to local machine
                    ftpCommand = "STOR %s"%img_name #comment if you whant download to local machine
                    self.ftp.storbinary(ftpCommand, fp=img_data) #comment if you whant download to local machine
                else:
                    img_data = requests.get(img_urls).content
                    with open('./' + folder_name + '/' + img_name, 'wb') as handler:
                        handler.write(img_data)
        except Exception as e:
            print('Failed download image. Reason: %s' % e)

#записуємо усі данні у файл
    def write_csv(self, data, name = "data3.csv"):
        path = os.getcwd() + os.path.sep + name
        try: 
            with open(path, 'a', encoding="utf-8", newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([data['category'], data['category_url'], data['title'], ' ', data['description'], data['price'], data['url'], data['images'], data['article'], data['count'], data['activation'], data['title-seo'], ' ', ' ', ' ', data['recomended'], data['new'], '0', '0', ' ', ' ', ' ', data['currency'], data['properties']])
        except Exception as e:
            print('Can\'t write csv file. Reason %s' % e)

#удаление csv файла
    def rm_csv(self, name = "data3.csv"):
            try:
                os.remove(name)
                print("File "+name+" Removed!")
            except Exception as e:
                print('Failed to remove file %s. Reason: %s' % (name,e))

#создание пустого txt файла 
    def create_txt(self, name):
        path = os.getcwd() + os.path.sep + name
        try:
            open(path, 'w', encoding="utf-8", newline='')
        except Exception as e:
                print('Failed to create file %s. Reason: %s' % (name, e))

#создание пустого csv файла 
    def create_csv(self, name = "data3.csv"):
        path = os.getcwd() + os.path.sep + name
        try:
            with open(path, 'w', encoding="utf-8", newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['Категория', 'URL категории', 'Товар', 'Вариант', 'Описание', 'Цена', 'URL', 'Изображение', 'Артикул', 'Количество', 'Активность', 'Заголовок [SEO]', 'Ключевые слова [SEO]', 'Описание [SEO]', 'Старая цена', 'Рекомендуемый', 'Новый', 'Сортировка', 'Вес', 'Связанные артикулы', 'Смежные категории', 'Ссылка на товар', 'Валюта', 'Свойства'])
        except Exception as e:
            print('Failed to create file "data.csv". Reason: %s' % e)

#витягуємо всі данні на авто
    def get_car(self, link):                                           
        try:
            parsed_link = parse.parse_qs(parse.urlsplit(link).query)
        except Exception as e:
            print("Can\'t parse link %s" % e)	
        try: 
            html = self.fetch(link, 0, 1)
            #print(link)
            time.sleep(uniform(3,6))
            car = {}
            year = self.get_car_year(html)
            category = self.get_car_category(html)
            color = self.get_car_color(html)
            car_estimate = self.get_car_estimate(html)
            car_type = self.get_car_type(html)
            distance_driven = self.get_distance_driven(html)
            displacement = self.get_car_displacement(html)
            transmission = self.get_transmission(html)
            fuel = self.get_fuel(html)
            lot_number = self.get_lot_id(html)
            car_registration = self.get_car_registration(html)
            mark = self.get_car_mark(html)
            car_vin = self.get_car_vin(html)
            mark_url = re.sub("\.", "", mark)            
            mark_url = re.sub("\(", "", mark_url)                                
            mark_url = re.sub("\)", "", mark_url)
            mark_url = re.sub("\s", "-", mark_url)
            car['url'] = car_vin.lower()+"-"+mark_url.lower()
            car['category'] = category
            car['category_url'] = self.get_car_category_url(html)
            car['title'] = lot_number+" "+self.get_car_title(html)
            car['title-seo'] = car['title']
            car['price'] = self.get_car_price(html)
            car['description'] = self.get_car_description(html)
            car['images'] = self.get_img_str(self.get_img_src(html), html)
            car['count'] = '0'
            car['activation'] = '1'
            car['currency'] = 'USD'
            car['recomended'] = '0'
            car['new'] = '0'
            car['article'] = self.get_lot_id(html)
            car['properties'] = 'Цвет=[type=assortmentCheckBox value=%s product_margin=Синий|Желтый|Белый|Серебро|Красный|Фиолетовый|Оранжевый|Зеленый|Серый|Золото|Коричневый|Голубой|Черный|Бежевый]&Кузов=[type=assortmentCheckBox value=%s product_margin=Универсал|Фургон|Фура|Трактор|Седан|Родстер|Пикап|Мотоцикл|Минивен|Хэтчбек|Кроссовер|Купе|Кабриолет|Багги]&Пробег=%s&Двигатель=%s&Год=%s&Первая регистрация=%s&Трансмиссия=[type=assortmentCheckBox value=%s product_margin=Механика|Автомат]&Топливо=[type=assortmentCheckBox value=%s product_margin=Дизель|Бензин|Газ]&Модель=%s&Марка=%s&Номер лота=%s&Оценка автомобиля=%s&VIN номер=%s&Аукцион=glovisaauction %s' % (color, car_type, distance_driven, displacement, year, car_registration, transmission, fuel, mark, category, lot_number, car_estimate, car_vin, config['GLOVIS']['DATE'])
            self.write_csv(car)
            self.download_images(html, self.get_img_src(html))
        except Exception as e:
            print("Can\'t write car in csv. Reason %s." % e)
            self.write_car_id("missed_car_id3.txt",urllib.parse.quote_plus(parsed_link['rc'][0])+"|"+urllib.parse.quote_plus(parsed_link ['gn'][0])+"\n")
    
#витягуємо всі дані в базу данних     
    def get_car_mysql(self, link):
        try:
            parsed_link = parse.parse_qs(parse.urlsplit(link).query)
        except Exception as e:
            print("Can\'t parse link %s" % e)
        try: 
            html = self.fetch(link, 0, 1)
            time.sleep(uniform(3,6))
            cat_id = 1 #self.get_car_category(html)
            lot_id = self.get_lot_id(html)
            car_vin = self.get_car_vin(html)
            title = lot_id+" "+self.get_car_title(html)+" "+car_vin
            description = self.get_car_description(html)
            price = self.get_car_price(html)
            mark = self.get_car_mark(html)
            mark_url = re.sub("\.", "", mark)            
            mark_url = re.sub("\(", "", mark_url)                                
            mark_url = re.sub("\)", "", mark_url)
            mark_url = re.sub("\s", "-", mark_url)
            url = car_vin.lower()+"-"+mark_url.lower()
            image_url = self.get_img_str(self.get_img_src(html), html)
            self.addprod.addnewproduct(cat_id,title,description,price,url,image_url,code=car_vin,meta_title=title,meta_keywords=car_vin,meta_desc=car_vin,price_course=price,image_title=title,image_alt=title)
        except Exception as e:
            print("Can\'t write car in mysql. Reason %s." % e)
            self.write_car_id("missed_car_id3.txt",urllib.parse.quote_plus(parsed_link['rc'][0])+"|"+urllib.parse.quote_plus(parsed_link ['gn'][0])+"\n")
#ID нових авто, что добавились, для парсингу 
    def get_missed_car_id(self, html):
        if(html != ''):
            try:
                db_connection = mysql.connect(host="217.172.189.14", database="olegk202_kdm", user="olegk202_kdm", password="Kostiuk_6173")
            except Exception as e:
                print(e)
            try:
                items = html.find("div.boarddv ul.lnelist li")
            except Exception as e:
                print('Can\'t get missed list car. Reason %s.' % e)
            for item in items:
                try:
                    lot_id = str(item.find("div.txt div span.sp span.n")[1].text.strip())
                    print("LOT ID", lot_id)
                except Exception as e:
                    print('Can\'t get lot id. Reason %s.' % e)
                try:
                    car_name = self.clear_car_name(self.ko_translate(item.find("div.txt div.ti a.btn_view")[0].text, "en"))
                    print("CAR NAME", car_name)
                except Exception as e:
                    print('Can\'t get car name. Reason %s.' % e)
                car_price = 0
                try:
                    car_price = re.sub(",", "", item.find("div.txt div div.spright span.abso0 span.n2")[0].text)
                    car_price = int(car_price)
                    car_price =  int(car_price*10000/int(config['GLOVIS']['USD']))
                    print("CAR PRICE", car_price)
                except Exception as e:
                    print('Can\'t get car price. Reason %s.' % e)
                select_car_query = "SELECT mg_product.id, mg_product.price, mg_product.title FROM mg_product WHERE LOWER(mg_product.title) LIKE LOWER('"+lot_id+" %') AND mg_product.activity=1;"
                car_id = urllib.parse.quote_plus(item.find("div.thumn a.btn_view")[0].attrs['rc'])+"|"+urllib.parse.quote_plus(item.find("div.thumn a.btn_view")[0].attrs['cd'])
                print("Car id", car_id)
                with db_connection.cursor() as cursor:
                    cursor.execute(select_car_query)
                    result = cursor.fetchall()
                #db_connection.close()
                    if(len(result) == 0):
                        print("MISSED CAR ID:" ,lot_id, "Car name:", car_name)
                        if car_id:
                            self.write_car_id("missed_car_id3.txt", car_id+"\n")
                    elif(car_price != 0):
                        for row in result:
                            if (row[1] == 0):
                                print("Car price:", car_price, "Car id:", row[0], "Car Title:", row[2])
                                update_query = "UPDATE mg_product SET price = "+str(car_price)+" WHERE id = "+str(row[0])
                                cursor.execute(update_query)
                                db_connection.commit()

#парсимо всі ссилки на недостаючі авто по сторінкам
    def get_missed_car_pages(self, searchAuctno=209, page_start=1, page_end=2):
        for i in range(page_start,page_end):
            unf = uniform(1,4)
            time.sleep(unf)
            print("Page %d. Sleep %d." % (i, unf))
            link = '{}?&atn={}&ac={}&acc={}&page1={}&page={}'.format( config['GLOVIS']['URL'], str(searchAuctno), urllib.parse.quote_plus("TQhYt3GD6GvgPdVw1QX+Wg=="), urllib.parse.quote_plus("u9cesU3il5ljSzAzHZzmEg=="), page_start,  i)
            html = self.fetch(link)
            self.get_missed_car_id(html)
        pass