import requests
import os
import time
import logging

log = logging.getLogger('main')

class Api:
    base_url = 'https://happyhentai.co'
    alt_used = 'happyhentai.co'
    cookies = {
        'session': 'jbe2o7dvmlm4jqdrit5sa1o5tg',
        'darkMode': '0',
    }


    def __init__(self):
        self.session = requests.Session()

    def get_albums(self, id: int):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'DNT': '1',
            'Alt-Used': self.alt_used,
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
        }

        params = {
            'id': str(id),
        }
        data = {
            'type': '1',
        }
        _get = self.session.get(f'{self.base_url}/albums', headers=headers, params=params, cookies=self.cookies)

        header_post = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': self.base_url,
            'DNT': '1',
            'Alt-Used': self.alt_used,
            'Connection': 'keep-alive',
            'Referer': f'{self.base_url}/albums?id={id}',
            # 'Cookie': 'session=jbe2o7dvmlm4jqdrit5sa1o5tg; darkMode=0',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        for i in range(3):
            _post = self.session.post(_get.url, headers=header_post, cookies=self.cookies, data=data)
            if 'Buy Album' in _post.text:
                return _post.text
            if not 'Download URL:' in _post.text:
                log.warning(f"Not found Download URL for {_post.url}. Try again")
                time.sleep(0.5)
                continue
            return _post.text
        raise Exception(f"not found Download URL for {_get.url}")
    def download_file(self, url, output_path):
        downloaded_size = 0
        if os.path.exists(output_path):
            downloaded_size = os.path.getsize(output_path)

        headers = {
            'Range': f'bytes={downloaded_size}-',
        }

        with self.session.get(url, headers=headers, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('Content-Range', '0').split('/')[-1])
            with open(output_path, 'ab') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        percent = (downloaded_size / total_size) * 100 if total_size > 0 else 0
                        log.debug(
                            f"Downloaded {os.path.basename(output_path)} {downloaded_size} from {total_size} bytes ({percent:.2f}%)")
                        if percent >= 25 and (percent - 25) % 25 < (8192 / total_size) * 100:
                            log.info(f"Downloaded {os.path.basename(output_path)} {percent:.0f}%")
        return os.path.realpath(output_path)

    def get_main_page(self, page: int):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'DNT': '1',
            'Alt-Used': self.alt_used,
            'Connection': 'keep-alive',
            # 'Cookie': 'session=jbe2o7dvmlm4jqdrit5sa1o5tg; darkMode=0',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        params = {
            'page': str(page),
            'cat': '1',
        }
        resp = requests.get(self.base_url, headers=headers, cookies=self.cookies, params=params)
        resp.raise_for_status()
        return resp.text

