import requests

headers = {
    'authority': 'xarid-api-trade.uzex.uz',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'access-control-request-headers': 'content-type,language',
    'access-control-request-method': 'POST',
    'origin': 'https://xarid.uzex.uz',
    'referer': 'https://xarid.uzex.uz/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41',
}

response = requests.options(
    'https://xarid-api-trade.uzex.uz/Lib/GetProductsForInfo', headers=headers)


headers = {
    'authority': 'xarid-api-trade.uzex.uz',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'content-type': 'application/json; charset=UTF-8',
    'language': 'uz',
    'origin': 'https://xarid.uzex.uz',
    'referer': 'https://xarid.uzex.uz/',
    'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41',
}

json_data = {
    'region_ids': [],
    'from': 0,
    'to': 1000000,
    'keyword': 'Асал',
}

response = requests.post(
    'https://xarid-api-trade.uzex.uz/Lib/GetProductsForInfo', headers=headers, json=json_data)
print(response.text)
