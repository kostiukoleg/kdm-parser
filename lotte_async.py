# -*- coding: utf-8 -*-
import urllib.parse
import re
import json
import csv
import aiofiles
import configparser
import aiohttp
from async_timeout import asyncio
from addnewproduct import AddNewProduct
from bs4 import beautifulsoup4
from glovisa_async import GlovisaAsync

config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini")


class LotteAsync:
    add_p = AddNewProduct()
    gl_async = GlovisaAsync()
