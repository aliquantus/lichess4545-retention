"""
Summary: Contains classes for the database.
Classes: BaseModel with subclasses Player, Season, Game.
"""

from peewee import *
from datetime import date
import sqlite3
from config import *


db = SqliteDatabase(dbname)


class BaseModel(Model):
    class Meta:
        database = db


class Player(BaseModel):
    id = PrimaryKeyField()
    username = CharField(unique=True)
    games = IntegerField(default=0)
    score = FloatField(null=True)
    seasons = TextField(null=True)  # store seasons user participated in


class Season(BaseModel):
    id = PrimaryKeyField()
    number = IntegerField(unique=True)
    games = IntegerField(default=0)
    players = ManyToManyField(Player, backref='seasons')


class Game(BaseModel):
    id = PrimaryKeyField()
    season = IntegerField(null=True)
    result = TextField(null=True)
    white = ForeignKeyField(Player, related_name='white game')
    black = ForeignKeyField(Player, related_name='black game')
    link = TextField()  # should be unique but the database is flawed due to manual input in the early days
    white_username = CharField()
    black_username = CharField()
    white_team = TextField(null=True)  # should be foreignkey
    black_team = TextField(null=True)  # should be foreignkey


if __name__ == "__main__":
    try:
        db.create_tables([Season, Game, Player, Season.players.get_through_model()])
    except:
        print("There already exists a database with this name!")
