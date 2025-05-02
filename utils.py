import os
import constants

def save_html(html, filename):
    file_path = os.path.join(constants.LOG_DIR, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return os.path.realpath(file_path)