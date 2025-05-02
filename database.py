import os
import sqlite3
import constants


db_file = os.path.join(constants.database_dir, 'db.sqlite3')
os.makedirs(constants.database_dir, exist_ok=True)

def create_database():
    sql = """
            create table main.album
(
    id        integer
        constraint table_name_pk
            primary key autoincrement,
    album     integer not null
        constraint album_pk
            unique,
    file_name TEXT,
    uploaded  integer default 0
);

create table main.errors
(
    id integer not null
        constraint errors_pk
            unique
);






    
    """
    database = sqlite3.connect(db_file)
    cursor = database.cursor()
    cursor.execute(sql)
    database.commit()
    database.close()



if not os.path.exists(db_file):
    create_database()

class Database:
    def __init__(self):
        self.db = sqlite3.connect(db_file, check_same_thread=False)

    def add_album(self, album: int, file_name: str):
        cur = self.db.cursor()
        cur.execute("insert into album (album, file_name) values (?, ?)", (album, file_name))
        self.db.commit()
        cur.close()

    def get_all_album(self):
        cur = self.db.cursor()
        cur.execute("select * from album order by album DESC")
        albums = {row[1]: row for row in cur.fetchall()}
        cur.close()
        return albums

    def update_uploaded(self, album: int):
        cur = self.db.cursor()
        cur.execute("update album set uploaded = ? where album = ?", (1, album))
        self.db.commit()
        cur.close()

    def add_errors(self, album: int):
        cur = self.db.cursor()
        cur.execute("insert into errors (id) values (?)", (album,))
        self.db.commit()
        cur.close()


