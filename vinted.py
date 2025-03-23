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
    "Referer": "https://www.vinted.it/catalog?search_text=nintendos&time=1742749245&disabled_personalization=true&page=1",
    "X-Money-Object": "true",
    "X-Anon-Id": "3a480e00-0373-4599-8a4b-f1186b8c25ce",
    "X-CSRF-Token": "75f6c9fa-dc8e-4e52-a000-e09dd4084b3e",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Cookie": "v_udt=VUJsd3VPZHBrNzIvV1czWGRDMzhtRTY3NXFPYy0tVlZrcFRvaXF6K2N1bWhSMi0tMnZHNjVQNE9HcEQxUWFESU1JN3B3UT09; anonymous-locale=it-fr; anon_id=3a480e00-0373-4599-8a4b-f1186b8c25ce; access_token_web=eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhcHBfaWQiOjQsImNsaWVudF9pZCI6IndlYiIsImF1ZCI6ImZyLmNvcmUuYXBpIiwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwiaWF0IjoxNzQyNzQ5MjM0LCJzaWQiOiIwODg2MGJiZS0xNzQyNzQ5MjM0Iiwic2NvcGUiOiJwdWJsaWMiLCJleHAiOjE3NDI3NTY0MzQsInB1cnBvc2UiOiJhY2Nlc3MifQ.FaXe7YkWMmuvVmNZdzHK5HKYTvnbjPdSbuFyoC6BTeHAM43iTAmSV2rnTjxexSixax3h5QVR6ZC0zlY4Zmy9ZRAHbRM2XeRIphMBHSCY3N4CrGgVUJWgXhzVsBmFPIx5vXwKp56dKb4VPYxI-GR_2hbDDQ6mpFWfXUyWRO0MdC7oWrXilXWYEHzlcjHGEE695orFixVCo1T514mn-L38285LGd7_zhdG0alqhrBDYJg0SCKdn_il03fMcKaqS_7VEEuDzV0TYAi8yZyBBa0kmvqv0d7AahNuMXunZgGm4KQ7xS7Su6mTq9heYEuGCyK6XNb4BLXemCy6mkgwzD74oA; refresh_token_web=eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhcHBfaWQiOjQsImNsaWVudF9pZCI6IndlYiIsImF1ZCI6ImZyLmNvcmUuYXBpIiwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwiaWF0IjoxNzQyNzQ5MjM0LCJzaWQiOiIwODg2MGJiZS0xNzQyNzQ5MjM0Iiwic2NvcGUiOiJwdWJsaWMiLCJleHAiOjE3NDMzNTQwMzQsInB1cnBvc2UiOiJyZWZyZXNoIn0.SxwP3i37bw0_faX6d_bjOz43wV-89cAD4wVxaPorGA4svn8cQYArNjI9fJWYS7S5C-HUvZaq9GEJFee2TF3IgRJNpxcBadgjhL7GZ256LusYtYOd6LdsFqyRlhJaYM0wXcP20yR7ZYti3i3uWp3ymMGgDjwS70cvgw6C1kW_2OlBhffLfJJOMEfWysFPIOJe3sURiKmeDFd437OVXTm1Z5vFLiCsBoIqZjGprmkr3aLHezVpaVrQy4BaetNykEj253f1nxfR_kx2dNWjsUK5Fo45k42fguguXKtfLhLG2zQvCIL33Ry_aX1UK81wOJyLoIVulDDax3QEsS8iLCNsmg; anon_id=3a480e00-0373-4599-8a4b-f1186b8c25ce; banners_ui_state=FAILURE; viewport_size=1800; v_sid=c6ca9fbc26229f681145d6c016aa0576; _vinted_fr_session=MkpTMDI2bTBXVFdBOXdiTGY1UWxaRkpHUmZJbCtHKzVsWHlFci9hQ0F6MVEwdER3RkZQeC9taFphelJVcm50aDVJRXEwQUx0aDN1Ym8zcDNjc1E5dE5jT3BYbFJrNm45aHJnSzY4UTl6RjBRRGJKY1RwYWZ3b213bEdwZk15SXVVWmkwRmg3UHNwdHpvVi9oMnJTd1dmUWlBbVRySFFWS0RGN1RTUTgrSDdwYjI1c214M0VqVG1yRUNDTnBiQitLQ3VYTUNzYmNJWXdQdDVvZzNONkY3WVREazgzdG1lWlRkblhwKyszZ24wdHVIaEd4SlpsWURjMlJkYlhWYTR2OS0tZjVoWjhsd1FoaWw2UU50bnhGUUwxZz09--9c6ca5088531d8afbbdc9e5ea5867f3017ca35bd; cf_clearance=aHmZbS7tQ3ydD7Z.6QnYD.2cJL9oAUn1o4S321Yfjv4-1742749237-1.2.1.1-mxNhYz1Opv2Opz14lX_gJ_rpp.pqS3UGUwH6p_4cqFS7veAKINRv69QswTUoxGap5kh_x1e1nr8IGGzECb9k4xylgUmT2XcSfdoxvVT.9HGsV5QjJmEEshT61Da9KBWeh8nGFV8.IjaMi___Zd0ychBC9X3Y01xTYsxg4AeYrWKIoqh2dJLBI18.RdzeJI1irj1npey3j6DJEm4hihZHNM6ZNwLVWaOcGqA35DAP329RG.cf48_C_ECYIL2.Z2IHo9Pq9IETzI9mkdhsrVfjqHO348iGuK5zGjrE63PQtCuylrIcaqy0blOcz8jLu.OIPS7mKbSxMYFAtvIvT0FeqBV11GNhauGBkHVSkoUAHuI; datadome=J2rjjFHHYW7txYcaq~5xUmTgejnsp7YV3r__OEHCdU9Hi31TNta~i4k~fs3BskNxGLKt~ehmJDkNZuA2rEWPIBOLm6lNsXVMbJBugk9rKoX3Qe~V6eDOeuHtzAJYjQRa; domain_selected=true",
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
