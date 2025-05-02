import os

VERSION = "0.0.1"
current_dir = os.path.dirname(os.path.abspath(__file__))
storage_dir = os.path.join(current_dir, 'storage')
LOG_DIR = os.path.join(current_dir, 'logs')
database_dir = os.path.join(current_dir, 'database')
