import requests
from bs4 import BeautifulSoup
import csv
import configparser
import json
from Parser import Parser

config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini") 

session = requests.session()
session.headers.update(json.loads(config["DEFAULT"]["HEADERS"]))

def get_html(url):
    r = session.get(url)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', class_='tbl-t02').find_all('tr')
    links = []
    for tr in trs:
        a = tr.find('td', class_='align-l').find('p', class_='txt').find('a').get('href')
        links.append(a)
    return links

def get_login_button(url):
    s = session.post(url, data = config.get("DEFAULT", "LOGIN"))
    return s.text

def main():
    # lotteautoauction = Parser()
    # driver = lotteautoauction.get_html('https://www.lotteautoauction.net/')
    # driver = lotteautoauction.login(driver)
    # for cookie in driver.get_cookies(): 
    #     c = {cookie['name']: cookie['value']}
    #     print(driver.get_cookies())
    #lotteautoauction.get_auction(driver)
    url = config.get("DEFAULT", "HOST")
    all_links = get_login_button(url)
    print(all_links)

if __name__ == '__main__':
    main()