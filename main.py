import os
from peewee import *

rawDataPath = "./rawdata"
dbname = "dbtest.db"


from utils import checkData
from models import *


last_season = 10  # can use this as raw input later?
seasons = range(1, last_season + 1)


def update():
    checkData(seasons=seasons)


update()

# check if want to update... then re-retrieve everything...?
# add a single season or retrieve all...


print("All seasons up to season {} have been downloaded, now creating player objects...")
