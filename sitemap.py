# -*- coding: utf-8 -*-
from ftplib import FTP
import mysql.connector as mysql
from lxml import etree
import io
import configparser
config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini")
try:
    db_connection = mysql.connect(host="217.172.189.14", database="olegk202_kdm", user="olegk202_kdm", password="Kostiuk_6173")
    select_car_query = "SELECT mg_product.url FROM mg_product INNER JOIN mg_product_user_property ON mg_product.id=mg_product_user_property.product_id WHERE mg_product_user_property.property_id=166 AND mg_product_user_property.value='{0} {1}'".format(config['SITEMAP']['AUCTION'], config['SITEMAP']['AUCTIONDATE'])
    cursor = db_connection.cursor()
    cursor.execute(select_car_query)
    result = cursor.fetchall()
    xmlns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    xsi = "http://www.w3.org/2001/XMLSchema-instance"
    schemaLocation = "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
    urlset = etree.Element("urlset", attrib={"xmlns":xmlns}, nsmap={"xsi":xsi, "schemaLocation": schemaLocation})
    for res in result:
        url = etree.SubElement(urlset, "url")
        loc = etree.SubElement(url, "loc")
        loc.text = "https://kdm-auto.com.ua/"+res[0]
        lastmod = etree.SubElement(url, "lastmod")
        lastmod.text = config['SITEMAP']['AUCTIONDATE'].replace("/", "-")
        priority = etree.SubElement(url, "priority")
        priority.text = "1.0"
    tree = etree.ElementTree(urlset)
    tree.write('sitemap.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")
    ftps = FTP()
    ftps.connect("217.172.189.14")
    ftps.login("olegk202","Kostiuk_6173")
    ftps.mkd("/public_html/sitemaps/{0}/{1}/".format(config['SITEMAP']['AUCTION'], config['SITEMAP']['AUCTIONDATE'].replace("/", "-")))
    ftps.cwd("/public_html/sitemaps/{0}/{1}/".format(config['SITEMAP']['AUCTION'], config['SITEMAP']['AUCTIONDATE'].replace("/", "-")))
    ftps.storbinary("STOR sitemap.xml", fp=open("sitemap.xml", "rb"))
    ftps.quit()
except Exception as e:
    print(e)
