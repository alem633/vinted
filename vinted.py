import sys
import requests
import pandas as pd

if len(sys.argv) < 2:
    print("missing args")
    print(sys.argv[0] + "[search query]")
    sys.exit(1)

query = sys.argv[1]
res = []

url = "https://www.vinted.it/api/v2/catalog/items"

querystring = {"page":"1","per_page":"960","search_text":f"{query}","catalog_ids":"","size_ids":"","brand_ids":"","status_ids":"","color_ids":"","material_ids":""}

payload = ""
headers = {
    "cookie": "_vinted_fr_session=NitZTjlOUkYybDd4NWRvMHVZT2lvc2huWTVoYWtIV1RKVlhpemlPK0VPTDU0d0FRaytrUzFrSXJDZnpIaU9OTXliNzVwdkpjb3lNL2l2djhtLzVRMWtnWnlFMElPWG1sZEZHOGk0YXRwQ2g5RnZTV0xodlk0TFJzTG5teEtjZXZPaW9SUzBXLzlhVm9SVHB5a1h4cTAzcFRBK0JVUCtvYnI3TnlHOXJFcUxlaTF5N2l1REpXTlphOUUyNG5rQy85cnhHcDZ2L1lJUkhSa0RmUDNWaWpOaFpXa3BobGRORjcrdkZKSUE4a1VnbVU0L3c1dExHUVVrRFlWazZSakRWaS0tTElBVUJhV29OS3hOU09JWlE3UlBZdz09--03e4081f5d14eda9ff7504a5369921c999e383ee; v_sid=6e946cb356278aced240e4e723139bc6",
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
    "Cookie": "v_udt=eUtrT1FHMUpqTGRNbnZiL0FZR0orOStrakxxLy0tQUEwY1lQbHVsMkNpWlFVMi0tNVRHOEQ0QmhXckdXbHpvWHNmeG1adz09; anonymous-locale=it-fr; anon_id=9e29b7c7-cf39-41e2-bceb-59037a7fb5a4; access_token_web=eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhcHBfaWQiOjQsImNsaWVudF9pZCI6IndlYiIsImF1ZCI6ImZyLmNvcmUuYXBpIiwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwiaWF0IjoxNzQyNzQxNTQ2LCJzaWQiOiI5YTkwMjc0ZS0xNzQyNzQxNTQ2Iiwic2NvcGUiOiJwdWJsaWMiLCJleHAiOjE3NDI3NDg3NDYsInB1cnBvc2UiOiJhY2Nlc3MifQ.czrZOmCDYDS_wB38leonjuTUT1kXsmkA4z2r5bGzaxl07IdNMNyOD8a3aiWjkCQjc4_gT0yAQYOAKz9NAdhFp2y_jQlsDcbxLiaXK-Kud1_CTTWLFbCnNYDoYpe3-LUOSmiDGhP4rlR2WSpiamRxfFnZvjN5p_4_hA_4RkSAwcPtsheerrzFLCO6wr6G7JOg0tgAKZOMZeOQrTGHhfVT-gzuSRx9yQSkCFNURAnftZrxbvugYEmJ7yyA2KzAdUEeWzOjtLEI7YXgY3fWP_pm2pmyluASfPDJkryANKN64G0zRzr2sGKqWcO_Nx_w3T5-fW_RM_5e59wAMHKvTIzy3Q; refresh_token_web=eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhcHBfaWQiOjQsImNsaWVudF9pZCI6IndlYiIsImF1ZCI6ImZyLmNvcmUuYXBpIiwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwiaWF0IjoxNzQyNzQxNTQ2LCJzaWQiOiI5YTkwMjc0ZS0xNzQyNzQxNTQ2Iiwic2NvcGUiOiJwdWJsaWMiLCJleHAiOjE3NDMzNDYzNDYsInB1cnBvc2UiOiJyZWZyZXNoIn0.pgOU_zWfRuY1hcrI6vrgjyyUSHdhI23oUHYsoIqzLTdotS79iNGSGLf3RxYbhsdKKyliWrUQzDCFucORLv29KFcs2fr5x6KJLAh7l2AUEbDhG9FdXfPnuHyTTgm8UQBsoTyADLN_0SEinwrokewqgYyUI-fqRObELLIHRvnhR6mwdRIF4qPvtpCnCR9zQytD5mWjXd_Gfh4e03yabfO7U2xAHb4i-rEOq6I-HGww9UcdDVev_h3q8aFN648a7mfznV91Sty5eRhANmKqaaGT49BUQDYZGU784H2MseK_8URnoGz4rIT4TYxlqKrRBT6yyyEHPbx554tyHraXq0sbfw; anon_id=9e29b7c7-cf39-41e2-bceb-59037a7fb5a4; banners_ui_state=FAILURE; viewport_size=1200; v_sid=908c95891ff420ab997f5119400338e4; _vinted_fr_session=eERMYkpyL1hVSW1RZDNIOW5HbTF1dUtrRG1tNHRGZTZMRUwrZ0VVODlMVGZOQVI2U25RdUIxZ0hlS244VzVMbVkyd3hSbVBRUFkrTEswVnlRRGJhYVVpOGs3djBpckZURDlvSEJNZkMvOUlKMy9GMm1VaENBOS9MQ2Z3V3dyVTkwYTh1R0NLQmR4bEMxbllyTmNnLzZXTzAyTFlZREJhM2xxSnZFeXdURzZUN1pYR21aZkg1SitRSEtiTERsRTBNMUFsUDRVQklwVHFldmFFNVdCbzFCQTMyUzgzSktXNEtqNU5OZ25oN0JLQmFJNzY1VUdiOS9WMkZjekJMUlJTRi0tdzNNSUR0b1VYMjYxSHU2SEQxdTVnZz09--801ed2c56180cd9146993442c6b794a421141e40; cf_clearance=VItDib3DkvdmN8f9JEHyYte_l_KjAuo0wcRcxRYbRNA-1742741555-1.2.1.1-1MBLNsballTFVoEnG75VKLDA12asXbUT4xwIDVyk01Q5AgL6MBg8Gbm8s9x_NmfSsE61ak6fb_Luy_5ZY0_egItWpbPEDMbnZyfCMDvYut6Yi2Zee2QloxahgMDH8N9Cj0vniodOG4W2_0OkFiHftRyKU1iYS0nw6T_P5idk.occGG5ZUdXfuHmW0Hdl.Xu_W87jKmspoYFP5gilWoIvnDJXkSmvgbiNtL53PWwxVYkF1eIZVBDLroxILE_9DQTLqsnkofdD7DmZA6IKSue4hDiwNPzHmaWXoE8i3QBGtqPTEi7lQbO10VSsyEw.y3.bCkwgsrbGJd4.PqJ3Mzz3OrkBWit8xN_VP8jE6J3jlQQ; domain_selected=true",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

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
