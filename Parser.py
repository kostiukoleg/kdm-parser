from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from typing import Any, List, Dict
from deep_translator import GoogleTranslator
import time
import csv
import requests
import os
import shutil
import re
import inspect
import configparser

config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini") 

class Parser:

    def __init__(self, category, category_url, model):
        self.category = category
        self.category_url = category_url
        self.model = model

    def get_html(self, url: str) -> webdriver:
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.maximize_window()
            driver.get(url)
            return driver
        except Exception as e:
            print('Can\'t get Site HTML. Reason %s.' % e)
    
    def create_folder(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except Exception as e:
            print('Can\'t create folder in path %s. Reason %s' % (path, e))

    def clear_folder(self, folder: str) -> None:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    # def rm_last_tr(self, string:str) -> str:
    #     try:
    #         string = re.sub("(<\/tr><tr>.+<\/tr>(<\/tbody>))", "", string)
    #         return string.group(0)
    #     except Exception as e:
    #             print('Failed to delete White Space Tabs and New Line. Reason: %s' % e)

    def rm_new_line(self, string:str) -> str:
        try:
            string = re.sub("[\n\t\r]*", "", string)
            string = re.sub("<!-+(.|\s|\n)*?-+>", "", string)
            string = re.sub("\s{2,}", "", string) 
            string = re.sub("<\s+", "<", string) 
            string = re.sub("\s+>", ">", string) 
            string = re.sub("<\s+\/\s*", "</", string) 
            string = re.sub("&amp;", "&", string) 
            string = re.sub("&quot;", "\"", string) 
            string = re.sub("&apos;", "'", string) 
            string = re.sub("&gt;", "<", string) 
            string = re.sub("&lt;", ">", string) 
            return string
        except Exception as e:
                print('Failed to delete White Space Tabs and New Line. Reason: %s' % e)

    def rm_csv(self, name:str = "data.csv") -> str:
        try:
            os.remove(name)
            print("File Removed!")
        except Exception as e:
                print('Failed to remove file "data.csv". Reason: %s' % e)

    def create_csv(self, name:str = "data.csv") -> None:
        path = os.getcwd() + os.path.sep + name
        try:
            with open(path, 'w', encoding="utf-8", newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['Категория', 'URL категории', 'Товар', 'Вариант', 'Описание', 'Цена', 'URL', 'Изображение', 'Артикул', 'Количество', 'Активность', 'Заголовок [SEO]', 'Ключевые слова [SEO]', 'Описание [SEO]', 'Старая цена', 'Рекомендуемый', 'Новый', 'Сортировка', 'Вес', 'Связанные артикулы', 'Смежные категории', 'Ссылка на товар', 'Валюта', 'Свойства'])
        except Exception as e:
                print('Failed to create file "data.csv". Reason: %s' % e)

    def write_csv(self, data, name:str = "data.csv") -> None:
        path = os.getcwd() + os.path.sep + name
        try: 
            with open(path, 'a', encoding="utf-8", newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([data['category'], data['category_url'], data['title'], ' ', data['description'], data['price'], ' ', data['images'], data['article'], data['count'], data['activation'], data['title-seo'], ' ', ' ', ' ', data['recomended'], data['new'], ' ', ' ', ' ', ' ', ' ', data['currency'], data['properties']])
        except Exception as e:
            print('Can\'t write csv file. Reason %s' % e)

    def get_img_str(self, driver: webdriver) -> str:
        try:
            driver.implicitly_wait(5)
            imgs: List[str] = driver.find_elements_by_css_selector('body > div.page-popup.exhibited-vehicle > div.clfix > div.vehicle-photo-wrap > div.vehicle-thumbnail > ul > li > a > img')
            img_str: str = ''
            for img in imgs :
                src_str = img.get_attribute('src')
                str_arr = str(src_str).split('/')
                str_arr.reverse()
                img_str += str_arr[0]+'[:param:][alt='+self.ko_translate(driver.find_element_by_css_selector('body > div.page-popup.exhibited-vehicle > div.vehicle-tit > h2').text, "en")+'][title='+self.ko_translate(driver.find_element_by_css_selector('body > div.page-popup.exhibited-vehicle > div.vehicle-tit > h2').text, "en")+']|'
            return img_str[:-1]
        except Exception as e:
            print('Can\'t get Images str. Reason %s' % e)
            return None

    def get_img(self, driver: webdriver) -> List[str]:
        try:
            driver.implicitly_wait(5)
            imgs: List[str] = driver.find_elements_by_css_selector('body > div.page-popup.exhibited-vehicle > div.clfix > div.vehicle-photo-wrap > div.vehicle-thumbnail > ul > li > a > img')
            src: List[str] = []
            for img in imgs:
                src.append(img.get_attribute('src'))
            return src
        except Exception as e:
            print('Can\'t get Images SRC List. Reason %s.' % e)

    def download_images(self, img_urls: List[str]) -> None:
        try:
            for img_url in img_urls:
                str_arr = str(img_url).split('/')
                str_arr.reverse()
                img_data = requests.get(img_url).content
                with open('./py_img/' + str_arr[0], 'wb') as handler:
                    handler.write(img_data)
        except Exception as e:
            print('Failed download image. Reason: %s' % e)

    def get_manufactured(self, driver: webdriver, name: str) -> Any:
        try:
            # driver.implicitly_wait(5)
            # el = driver.find_element_by_id('searchCarMCd')
            el = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'searchCarMCd')))
            for option in el.find_elements_by_tag_name('option'):
                if option.text == name:
                    option.click()
                    break
        except Exception as e:
            print('Can\'t get manufactured. Reason %s.' % e)

    def get_model(self, driver: webdriver, name: str) -> Any:
        try:
            #driver.implicitly_wait(5)
            #el = driver.find_element_by_id('searchMdlCd')
            el = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'searchMdlCd')))
            for option in el.find_elements_by_tag_name('option'):
                if option.text == name:
                    option.click()
                    btn = el.find_element_by_xpath('//*[@id="frm"]/div/div[1]/div[3]/div[2]/button[2]')
                    btn.click()
                    break
        except Exception as e:
            print('Can\'t get model. Reason %s.' % e)

    def get_category(self, driver: webdriver) -> str:
        try:
            elements = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchCarMCd"]/option[@selected="selected"]')))
            return elements.text
        except Exception as e:
            print('Can\'t get Category Text. Reason %s.' % e)

    def get_type(self, driver: webdriver, i: int) -> str:
        try:
            element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="frm"]/div/div[2]/div[1]/div[1]/div/table/tbody/tr[3]/td[1]/font/font')))
            return element.text
        except Exception as e:
            print('Can\'t get Type Text. Reason %s.' % e)

    def get_year(self, driver: webdriver) -> str:
        try:
            element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="frm"]/div/div[2]/div[1]/div[1]/div/table/tbody/tr[2]/td[2]/font/font')))
            return element.text
        except Exception as e:
            print('Failed to get year. Reason: %s' % e)

    def get_price(self, driver: webdriver, i: int) -> str:
        try:
            element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/p/strong/em')))
            return element.text
        except Exception as e:
            print('Failed to get price. Reason: %s' % e)

    def alert_present(self, driver: webdriver) -> bool:
        alert: bool = True
        try:
            driver.switch_to.alert.accept()
            #print("alert accepted")
        except:
            #print("no alert")
            alert = False
        return alert 

    def get_car_data(self, driver: webdriver, i: int) -> None:
        c = inspect.currentframe()  
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[5]/table/tbody/tr[' + str(i) + ']/td[5]/p/a[@class="a_list"]'))).click()
        except Exception as e:
            print('Can\'t click on car %d. Reason %s' % (i, e))
            driver.refresh()
        if self.alert_present(driver):
            return False 
        tabs = driver.window_handles
        try:
            driver.switch_to.window(tabs[1])
        except Exception as e:
            print('Can\'t switch to new window. Reason %s' % e)
        self.download_images(self.get_img(driver))
        car: Dict[str] = {}
        car['category'] = self.category
        car['category_url'] = self.category_url
        try:
            car['title'] = self.ko_translate(driver.find_element_by_xpath('/html/body/div[1]/div[1]/h2').text, "en")
            car['title-seo'] = self.ko_translate(driver.find_element_by_xpath('/html/body/div[1]/div[1]/h2').text, "en")
        except:
            car['title'] = ''
            driver.refresh()
        try:
            car['price'] = int(driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/p/strong/em').text.replace(',', ''))*9.10
        except: 
            car['price'] = '' 
            driver.refresh()
        try:
            car['description'] = '<div class="paper-tit"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Протокол осмотра / осмотра автомобилей, выставленных на аукцион</font></font></div>'
            el = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > div > div > table')))
            if(len(el.get_attribute("outerHTML"))>5000):
                i = 0
                while (i <= int(len(el.get_attribute("outerHTML"))/4999)):
                    if(i == int(len(el.get_attribute("outerHTML"))/4999)):
                        car['description'] += self.rm_new_line(self.ko_translate(el.get_attribute("outerHTML")[i*4999:len(el.get_attribute("outerHTML"))], "ru"))
                    else:
                        car['description'] += self.rm_new_line(self.ko_translate(el.get_attribute("outerHTML")[i*4999:i+1*4999], "ru"))
                    i+=1
            else: 
                car['description'] += self.rm_new_line(self.ko_translate(el.get_attribute("outerHTML"), "ru"))
        except Exception as e:
            car['description'] += ''
            print(c.f_lineno) 
            print('Can\'t get protocol view. Reason %s' % e)
            driver.refresh()
        try:
            car['description'] += '<h2 class="page-subtit mt60"><font style="vertical-align: inherit"><font style="vertical-align: inherit">Детали автомобиля</font></font></h2>'
            el = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div.vehicle-detail-view > div.vehicle-detail > div.vehicle-detail_bar > table.tbl-v02')))
            car['description'] += self.rm_new_line(self.ko_translate(el.get_attribute("outerHTML"), "ru"))
        except Exception as e:
            car['description'] += ''
            print(c.f_lineno) 
            print('Can\'t get car details. Reason %s' % e)  
            driver.refresh()  
        try:
            car['description'] += '<h2 class="page-subtit mt60" id="view-status"><font style="vertical-align: inherit"><font style="vertical-align: inherit">Состояние кузова автомобиля</font></font></h2>'
            el = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div.vehicle-detail-view > div.tab-status')))
            car['description'] += self.rm_new_line(self.ko_translate(el.get_attribute("outerHTML"), "ru"))
        except Exception as e:
            car['description'] += ''
            print(c.f_lineno) 
            print('Can\'t get car condition. Reason %s' % e)    
            driver.refresh()   
        try:
            car['description'] += '<h2 class="page-subtit mt60"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Видео автомобиля</font></font></h2>'
            el = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div.vehicle-detail-view > div:nth-child(5)')))
            car['description'] += self.rm_new_line(self.ko_translate(el.get_attribute("outerHTML"), "ru"))
        except Exception as e:
            car['description'] += ''
            print(c.f_lineno) 
            print('Can\'t get car control list. Reason %s' % e) 
            driver.refresh()
        try:
            year = int(driver.find_element_by_css_selector('body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > div > div > table > tbody > tr:nth-child(5) > td:nth-child(4)').text)
        except Exception as e:
            print('Can\'t get car year. Reason %s' % e)
            driver.refresh()
        try:
            mark = self.ko_translate(driver.find_element_by_css_selector('body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > div > div > table > tbody > tr:nth-child(4) > td:nth-child(5)').text, "en")
        except Exception as e:
            print('Can\'t get car mark. Reason %s' % e)
            driver.refresh()
        try:
            color = self.ko_translate(driver.find_element_by_css_selector('body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(3) > td:nth-child(4)').text, "ru")
        except Exception as e:
            print('Can\'t get car color. Reason %s' % e)
            driver.refresh()
        try:
            fulel_data = {
                "가솔린":"Бензин",
                "디젤":"Дизель",
                "LPG":"LPG",
                "LPI하이브리드":"LPG гибрид",
                "가솔린하이브리드":"Бензиновый гибрид",
                "디젤하이브리드": "Дизельный гибрид",
                "전기":"Электрокар",
                "가솔린/LPG":"Бензин/LPG"
            }
            fuel = fulel_data[driver.find_element_by_css_selector('body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(4) > td:nth-child(4)').text]
        except Exception as e:
            fuel = "Дизель"
            print('Can\'t get car fuel. Reason %s' % e)
            driver.refresh()
        try:
            res = re.findall("\d+", driver.find_element_by_css_selector('body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(5) > td:nth-child(4)').text)
            displacement = int(''.join(res))
        except Exception as e:
            print('Can\'t get car displacement. Reason %s' % e)  
            driver.refresh()   
        try:
            transmission = driver.find_element_by_css_selector('body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(2) > td:nth-child(4)').text == "자동" if "Автомат" else "Механика"
        except Exception as e:
            print('Can\'t get car transmission. Reason %s' % e)   
            driver.refresh()
        try:
            car_type = self.ko_translate(driver.find_element_by_css_selector('body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(6) > td:nth-child(2)').text, "ru")
        except Exception as e:
            print('Can\'t get car type. Reason %s' % e) 
            driver.refresh()
        try:
            lot_number = self.ko_translate(driver.find_element_by_css_selector('body > div.page-popup.exhibited-vehicle > div.vehicle-tit > p > strong').text, "ru")
        except Exception as e:
            print('Can\'t get car type. Reason %s' % e) 
            driver.refresh()
        try:
            r = re.findall("\d+", driver.find_element_by_css_selector('body > div.page-popup.exhibited-vehicle > div.vehicle-detail > div > div.vehicle-detail > div > table > tbody > tr:nth-child(1) > td:nth-child(4)').text)
            distance_driven = int(''.join(r))
        except Exception as e:
            print('Can\'t get car distance driven. Reason %s' % e)
            driver.refresh() 
        car['images'] = self.get_img_str(driver)
        car['count'] = '0'
        car['activation'] = '1'
        car['currency'] = 'USD'
        car['recomended'] = '0'
        car['new'] = '0'
        car['weight'] = '0'
        car['article'] = lot_number
        car['properties'] = ('Цвет=[type=assortmentCheckBox value=%s product_margin=Желтый|Белый|Серебро|Красный|Фиолетовый|Оранжевый|Зеленый|Серый|Золото|Коричневый|Голубой|Черный|Бежевый]&Кузов=[type=assortmentCheckBox value=%s product_margin=Универсал|Фургон|Фура|Трактор|Седан|Родстер|Пикап|Мотоцикл|Минивен|Хэтчбек|Кроссовер|Купе|Кабриолет|Багги]&Пробег=%d&Двигатель=%d&Год=%d&Трансмиссия=[type=assortmentCheckBox value=%s product_margin=Механика|Автомат]&Топливо=[type=assortmentCheckBox value=%s product_margin=Дизель|Бензин|Газ]&Модель=%s&Марка=%s&Номер лота=%s&Аукцион=lotteautoauction' % (color, car_type, distance_driven, displacement, year, transmission, fuel, mark, self.category, lot_number))
        try:
            driver.close()
            driver.switch_to.window(tabs[0])
        except Exception as e:
            print('Can\'t switch to old window. Reason %s' % e)
        self.write_csv(car)

    def get_car(self, driver): 
        for i in range(1, len(driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[5]/table/tbody/tr')) + 1):
            print('Car index '+str(i))
            self.get_car_data(driver, i)

    def click_next_page(self, driver: webdriver, fnav, snav) -> None:
        try:
            for nav in range(fnav, snav):
                driver.execute_script("fnSearch("+ str(nav) +");return false; ")
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[5]/table/tbody/tr')))
                print("Page "+str(nav))
                print("Cars len "+str(len(driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[5]/table/tbody/tr'))))
                self.get_car(driver)
            driver.close()
        except Exception as e:
            print('Failed to Click Page Navigator %d. Reason: %s' % (nav, e))
            
    def ko_translate(self, text, lan):
        try:
            res = GoogleTranslator(source='ko', target=lan).translate(text)
        except Exception as e:
            print('Failed to Translate text. Reason: %s' % e)
            res = ''
        return res

    def manufactured(self, driver):
        try:
            driver.implicitly_wait(10)
            el = driver.find_element_by_link_text(str(self.model))
            el.click()
            driver.execute_script("fnSearch(1);")
        except Exception as e:
            print('Can\'t click to manufactured button. Reason %s' % e)

    def login(self, driver):
        c = inspect.currentframe()  
        try: 
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div/buttton')))
            driver.execute_script("javascript:location.href='/hp/auct/cmm/viewMain.do'")
            time.sleep(5)
        except Exception as e:
            print('Can\'t click to login button. Reason %s' % e)
        try:
            time.sleep(3)
            driver.find_element_by_id("userId").send_keys("152000")
        except Exception as e:
            print('Can\'t put login in input. Reason %s' % e)
        try:
            time.sleep(3)
            driver.find_element_by_id("userPwd").send_keys("4275")
        except Exception as e:
            print('Can\'t put password in input. Reason %s' % e)
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div/div[1]/div[1]/form/div/button")))
            driver.execute_script("javascript:actionLogin();")
        except Exception as e:
            print('Can\'t click on submit. Reason %s' % e)
        try:
            print(c.f_lineno) 
            time.sleep(10)
            tabs = driver.window_handles
            print(tabs)
            if( len(tabs) > 1 ):
                driver.switch_to.window(tabs[1])
                driver.close()
                driver.switch_to.window(tabs[0])
        except Exception as e:
            print('Can\'t switch tabs. Reason %s' % e)

    def get_auction(self, driver):
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/div[3]/div[1]/div[2]/div[2]/a")))
            driver.execute_script("javascript:fn_MovePage('1010200');")
        except Exception as e:
            print('Can\'t get Auction List. Reason %s' % e)

    def get_all_href(self, driver):
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[5]/table/tbody/tr')))
            cars = int(len(driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[5]/table/tbody/tr')))
            for i in range( 1, cars+1 ):
                element = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[5]/table/tbody/tr['+ str(i) +']/td[5]/p/a')
                onclick = re.search('\"([A-Z]+)\",\"([A-Z0-9]+)\".\"([0-9]+)\"', element.get_attribute('onclick'))
                link = 'https://www.lotteautoauction.net/hp/auct/myp/entry/selectMypEntryCarDetPop.do?searchMngDivCd=' + onclick.group(1) + '&searchMngNo=' + onclick.group(2) + '&searchExhiRegiSeq=' + onclick.group(3)
                print(link)
        except Exception as e:
            print('Can\'t get link. Reason %s' % e)

    def click_next(self, driver):
        try: 
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[7]/span/a')))
            el = driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[7]/span/a')
            for i in range(2, int(len(el))+2):
                print('Page ', i-1)
                self.get_all_href(driver)
                driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[7]/span/a['+ str(i) +']').click()
        except Exception as e:
            print('Can\'t click the next page. Reason %s' % e)

    def click_ten_pages(self, driver):
        try: 
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[4]/div[2]/div[7]/a[3]'))).click()
            el = driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div[7]/a[3]')
            n = int(re.search(r'\d+$', el.get_attribute('href')).group(0))
            for i in range(2, int(n/10)):
                self.click_ten_pages(driver)
                print(i)
        except Exception as e:
            print('Can\'t click the next ten page. Reason %s' % e)