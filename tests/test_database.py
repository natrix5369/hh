import shutil
import hh_api
import parsing
import os
import constants
import logger
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor
import database
from sqlite3 import IntegrityError

logger.init_logger()
hapi = hh_api.Api()
if os.path.isdir(constants.storage_dir):
    shutil.rmtree(constants.storage_dir)

os.makedirs(constants.storage_dir, exist_ok=True)
threading_pool = ThreadPoolExecutor(max_workers=5)

log = logging.getLogger('main')

db = database.Database()

def test_database():
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
        try:
            db.add_album(album=id, file_name=file_name)
            log.info(f"ADD SUCCESS TO DB! {os.path.basename(file_name)}")
        except IntegrityError:
            log.warning(f'{link} already added to db')

def test_get_data():
    data_from_db = db.get_all_album()
    assert data_from_db


