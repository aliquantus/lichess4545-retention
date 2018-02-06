from peewee import *
from __main__ import dbname, subdir_path

db = SqliteDatabase(dbname)


def openJson():
    for file in os.listdir(subdir_path):
        if file.endswith(".json"):
            print(os.path.join("/mydir", file))
