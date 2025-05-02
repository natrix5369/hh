import os
import logging
import shutil
from concurrent.futures import ThreadPoolExecutor
from sqlite3 import IntegrityError

import logger
import constants
import hh_api
import parsing
import webdav_mailru
import database

logger.init_logger()

log = logging.getLogger('main')
thread_pool = ThreadPoolExecutor(max_workers=5)
shutil.rmtree(constants.storage_dir, ignore_errors=True)
os.makedirs(constants.storage_dir)

class Prog:
    def __init__(self):
        self.db = database.Database()
        self.webdav = webdav_mailru.WebdavMailRu(os.getenv('WEBDAV_USERNAME'), os.getenv('WEBDAV_PASSWORD'))
        self.webdav.connect()
        self.hapi = hh_api.Api()
        self.thread_list = []


    def upload_album(self, id):
        id = int(id)

        def download_upload(link_download, output_path):
            error = None
            log.info(f"Try download {os.path.basename(output_path)}: {id}")
            for i in range(5):
                try:
                    down = self.hapi.download_file(link_download, output_path)
                    assert os.path.exists(output_path)
                    log.info(f"Upload webdav: {output_path}: {id}")
                    remote_file = f"{str(id)}_{os.path.basename(output_path)}"
                    res = self.webdav.upload_file(remote_file, output_path)
                    log.info(f"SUCCESS! {os.path.basename(output_path)}: {id}")
                    os.remove(output_path)
                    return True
                except Exception as e:
                    error = e
                    log.error(f"Error download: {os.path.basename(output_path)} {id}: {e}. Trying again.")
            log.critical(f"Download failed: {os.path.basename(output_path)}: {error}")
            return False


        try:
            album_html = self.hapi.get_albums(id)
            assert album_html
        except Exception as e:
            log.critical(f"Error get album page: {id}: {e}")
            raise e

        if not 'Download Album' in album_html:
            log.warning(f"Not found Download button for {id}")
            return False

        try:
            link_download = parsing.parse_album_page(album_html)
            assert link_download
        except Exception as e:
            log.debug(f"{id}: {album_html}")
            log.critical(f"Error parse album page. Not found link for download: {id}: {e}")
            raise e

        file_name = link_download.split('?')[0].split('/')[-1]
        try:
            self.db.add_album(id, file_name)
        except IntegrityError:
            pass

        output_path = os.path.join(constants.storage_dir, file_name)
        if download_upload(link_download, output_path):
            self.db.update_uploaded(int(id))
        return True


    def check_database(self):
        data_db = self.db.get_all_album()
        for album, data in data_db.items():
            if data[3] == 0:
                thread = thread_pool.submit(self.upload_album, album)
                self.thread_list.append(thread)

        for thread in self.thread_list:
            thread.result()
        return True


    def run(self):
        try:
            self.check_database()
            self.thread_list.clear()
            data_db = self.db.get_all_album()

            for page_number in range(9999):
                log.info(f"Try page: {page_number}")
                main_page_html = self.hapi.get_main_page(page_number)
                assert main_page_html
                links = parsing.parse_main(main_page_html)
                if not links:
                    log.info(f"Not found links on page: {page_number}. Stop work")
                    break

                for link in links:
                    id = int(link.split('=')[1].strip())
                    if id in data_db:
                        continue
                    thread = thread_pool.submit(self.upload_album, id)
                    self.thread_list.append(thread)
                    log.info(f"Added to download: {id}. Count threads: {len(self.thread_list)}")

            log.info(f"Wait complete all threads...")
            for thread in self.thread_list:
                thread.result()

            log.info(f"Work finished!")

        except Exception:
            log.exception('Exception occurred')



if __name__ == '__main__':
    Prog().run()


