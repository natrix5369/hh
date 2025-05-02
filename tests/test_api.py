import shutil
import hh_api
import parsing
import os
import constants
import logger
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor
import webdav_mailru
import database
from sqlite3 import IntegrityError

logger.init_logger()
hapi = hh_api.Api()
if os.path.isdir(constants.storage_dir):
    shutil.rmtree(constants.storage_dir)

os.makedirs(constants.storage_dir, exist_ok=True)
threading_pool = ThreadPoolExecutor(max_workers=5)

log = logging.getLogger('main')
webdav = webdav_mailru.WebdavMailRu(os.getenv('WEBDAV_USERNAME'), os.getenv('WEBDAV_PASSWORD'))
webdav.connect()

db = database.Database()

def test_download_file():
    result = hapi.get_albums(5158)
    assert result
    pars = parsing.parse_album_page(result)
    assert pars
    file_name = pars.split('/data/')[1].split('?')[0].strip()
    down = hapi.download_file(pars, file_name)
    assert os.path.exists(down)
    os.remove(down)

def test_parse_main_page():
    main_page = hapi.get_main_page(1)
    assert main_page
    links = parsing.parse_main(main_page)
    assert links

def test_download_main_page():
    main_page = hapi.get_main_page(1)
    assert main_page
    links = parsing.parse_main(main_page)
    assert links
    for link in links:
        id = int(link.split('=')[1].strip())
        album = hapi.get_albums(id)
        assert album
        pars = parsing.parse_album_page(album)
        assert pars
        file_name = pars.split('?')[0].split('/')[-1]
        output_path = os.path.join(constants.storage_dir, file_name)
        down = hapi.download_file(pars, output_path)
        assert os.path.exists(output_path)
        os.remove(output_path)


def test_download_multiple_threads():
    def download_and_check(pars, output_path):
        log.info(f"RUN! {os.path.basename(output_path)}")
        for i in range(5):
            try:
                down = hapi.download_file(pars, output_path)
                assert os.path.exists(output_path)
                log.info(f"Upload webdav: {output_path}")
                res = webdav.upload_file(output_path)
                log.info(f"SUCCESS! {os.path.basename(output_path)}")
                os.remove(output_path)
                return
            except Exception as e:
                log.error(f"Error download: {os.path.basename(output_path)}: {e}. Trying again.")
        log.critical(f"Download failed: {os.path.basename(output_path)}")

    list_threads = []
    main_page = hapi.get_main_page(1)
    assert main_page
    links = parsing.parse_main(main_page)
    assert links
    for link in links:
        id = int(link.split('=')[1].strip())
        album = hapi.get_albums(id)
        assert album
        try:
            pars = parsing.parse_album_page(album)
            assert pars
        except AssertionError:
            log.warning(f'{link} ERROR!')
            continue
        file_name = pars.split('?')[0].split('/')[-1]
        output_path = os.path.join(constants.storage_dir, file_name)
        thread = threading_pool.submit(download_and_check, pars, output_path)
        list_threads.append(thread)
        break

    for thread in list_threads:
        result = thread.result()
        log.info(f"thread result: {result}")


