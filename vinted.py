import sys
import os
import time
import requests
import pandas as pd
import pickle
import selenium.webdriver

if len(sys.argv) < 2:
    print("missing args")
    print(sys.argv[0] + "[search query]")
    sys.exit(1)

query = sys.argv[1]
res = []

# cookies
driver = selenium.webdriver.Firefox()

driver.get("https://www.vinted.it/")
time.sleep(5)
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
cookies = pickle.load(open("cookies.pkl", "rb"))
cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

driver.close()

url = "https://www.vinted.it/api/v2/catalog/items"

querystring = {"page":"1","per_page":"960","search_text":f"{query}","catalog_ids":"","size_ids":"","brand_ids":"","status_ids":"","color_ids":"","material_ids":""}

payload = ""
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "it-fr",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://www.vinted.it/catalog?search_text=nintendo",
    "X-Money-Object": "true",
    "X-Anon-Id": "9e29b7c7-cf39-41e2-bceb-59037a7fb5a4",
    "X-CSRF-Token": "75f6c9fa-dc8e-4e52-a000-e09dd4084b3e",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}

session = requests.Session()
session.cookies.update(cookies_dict)  # Aggiungi i cookie alla sessione
response = session.request("GET", url, data=payload, headers=headers, params=querystring)

if response.status_code != 200:
    print("Blocked")
    sys.exit(404)

print("success")
search_result = response.json()
print(len(search_result['items']))
for p in search_result['items']:
    res.append(p)

print(len(res))
data = pd.json_normalize(res)
print(data.columns)
data[["title", "favourite_count", "status", "total_item_price.amount", "price.currency_code", "url", "user.profile_url"]].to_csv(f'{query}.csv')

os.remove("cookies.pkl")
