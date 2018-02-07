from peewee import *
from config import *
from models import *


def findSeasons(player):
    return sorted(list(set([game.season for game in Game.select().where((Game.white == player) | (Game.black == player))])))


def findPlayers(season):
    result = []
    for player in Player.select():
        if season in findSeasons(player):
            result.append(player)
    return result


def findNewPlayers(season):
    result = []
    for player in findPlayers(season):
        if min(findSeasons(player)) == season:
            result.append(player)
    return result
