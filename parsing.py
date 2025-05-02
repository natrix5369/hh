import logging
from bs4 import BeautifulSoup
import constants
import os
import random
import utils

log = logging.getLogger('main')



def parse_album_page(html_text: str):
    soup = BeautifulSoup(html_text, 'html')
    block_download = soup.find('div', attrs={'class': 'alert alert-success'})
    if not block_download:
        file_name = f'{random.randint(100000, 999999)}.html'
        html_file = utils.save_html(html_text, file_name)
        log.warning(f'Could not find a download block\n{html_file}')
    assert block_download
    block_a = block_download.find('a')
    if not block_a:
        file_name = f'{random.randint(100000, 999999)}.html'
        html_file = utils.save_html(html_text, file_name)
        log.warning(f"Could not find 'a' tag {html_file}")

    assert block_a, html_text
    if not 'href' in block_a.attrs:
        file_name = f'{random.randint(100000, 999999)}.html'
        html_file = utils.save_html(html_text, file_name)
        log.warning(f"Could not find 'href' attribute\n{html_file}")
    assert block_a['href'], block_a
    return block_a['href']

def parse_main(html_text: str) -> list:
    result = list()
    soup = BeautifulSoup(html_text, 'html')
    block_row = soup.find('div', attrs={'class': 'row'})
    if not block_row:
        file_name = f'{random.randint(100000, 999999)}.html'
        html_file = utils.save_html(html_text, file_name)
        log.warning(f"Could not find 'div' tag\n{html_file}")
        return result
    divs = block_row.find_all('div', attrs={'class': 'col-md-4'})
    for row in divs:
        a_block = row.find('a')
        if not a_block:
            file_name = f'{random.randint(100000, 999999)}.html'
            html_file = utils.save_html(html_text, file_name)
            log.warning(f"Could not find 'a' tag\n{html_file}")
        assert a_block
        if not 'href' in a_block.attrs:
            file_name = f'{random.randint(100000, 999999)}.html'
            html_file = utils.save_html(html_text, file_name)
            log.warning(f"Could not find 'href' attribute\n{html_file}")
        a_href = a_block['href']
        if not a_href:
            file_name = f'{random.randint(100000, 999999)}.html'
            html_file = utils.save_html(html_text, file_name)
            log.warning(f"Could not find 'href' attribute\n{html_file}")
        assert a_href
        result.append(a_href)
    return result