# -*- coding: utf-8 -*-
from ftplib import FTP
from lxml import etree
from io import BytesIO
import configparser
config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini")
try:
    ftps = FTP()
    ftps.connect("217.172.189.14")
    ftps.login("olegk202","Kostiuk_6173")
    ftps.cwd("/public_html/")
    with open( "sitemap.xml", 'wb' ) as file :
        ftps.retrbinary('RETR %s' % "sitemap.xml", file.write)
    #data = ftps.retrlines('LIST') 
    #print(data)
except Exception as e:
    print(e)
parser = etree.XMLParser(remove_blank_text=True)
tree = etree.parse("sitemap.xml",parser)
sitemapindex = tree.getroot()
sitemap = etree.SubElement(sitemapindex, "sitemap")
loc = etree.SubElement(sitemap, "loc")
loc.text = "https://kdm-auto.com.ua/sitemaps/{0}/{1}/sitemap.xml".format(config['SITEMAP']['AUCTION'], config['SITEMAP']['AUCTIONDATE'].replace("/", "-"))
wrtree = etree.ElementTree(sitemapindex)
wrtree.write('sitemap.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")
ftps.storbinary("STOR sitemap.xml", fp=open("sitemap.xml", "rb"))
ftps.quit()