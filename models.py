from peewee import *
from datetime import date
import sqlite3
from __main__ import dbname  # import name variable if run from separate script


db = SqliteDatabase(dbname)


class BaseModel(Model):
    class Meta:
        database = db  # This model uses the "people.db" database.


class Player(BaseModel):
    id = PrimaryKeyField()
    username = CharField(unique=True)
    games = IntegerField(default=0)
    score = FloatField(null=True)
    seasons = BlobField(null=True)  # store seasons user participated in


class Season(BaseModel):
    id = PrimaryKeyField()
    games = IntegerField(default=0)
    players = IntegerField(default=0)


class Game(BaseModel):
    id = PrimaryKeyField()
    season = IntegerField(null=True)
    result = TextField(null=True)
    white = ForeignKeyField(Player, related_name='white game')
    black = ForeignKeyField(Player, related_name='black game')
    link = TextField(unique=True)
    white_username = CharField()
    black_username = CharField()
    date_played = DateField(null=True)


if __name__ == "__main__":
    try:
        db.create_tables([Player, Game])
    except:
        print("There already exists a database with this name!")
