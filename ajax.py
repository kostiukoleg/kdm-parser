import requests
import json
headers = {'User-Agent': 'Mozilla/5.0','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
payload = {'email':'olegkostiuk@ukr.net','pass':'Kostiuk_6173'}
link = 'https://kdm-auto.com.ua/enter'
session = requests.Session()
resp = session.get(link,headers=headers)
cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
resp = session.post(link,headers=headers,data=payload,cookies=cookies)

url = "https://kdm-auto.com.ua/mg-admin/ajax"
csv_params={
    "mguniqueurl": "action%2FstartImport",
    "rowId": "0",
    "delCatalog": "false",
    "typeCatalog": "MogutaCMS",
    "identifyType": "name",
    "schemeType": "default"
    }
    
img_param = {
    "mguniqueurl": "action/startGenerationImagePreview"
}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38', 'Cache-Control': 'no-cache', 'Content-Length': '60', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'DNT': '1', 'x-requested-with': 'XMLHttpRequest'}
r = session.post( url = url, data = img_param, cookies = cookies,headers = headers )
print(json.loads(r.content))