import requests

cookies = {
    'session': 'jbe2o7dvmlm4jqdrit5sa1o5tg',
    'darkMode': '0',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Alt-Used': 'happyhentai.co',
    'Connection': 'keep-alive',
    # 'Cookie': 'session=jbe2o7dvmlm4jqdrit5sa1o5tg; darkMode=0',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

params = {
    'id': '5158',
}

response = requests.get('https://happyhentai.co/albums', params=params, cookies=cookies, headers=headers)
print(response.status_code)