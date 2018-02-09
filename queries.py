"""
Summary: Contains some shortcut functions for peewee queries
Functions: Countplayers, findSeasons, gamesPlayed, playerInSeason, findPlayers, findNewPlayers
"""
from config import *
from models import *
from peewee import *
import numpy as np


def countPlayers():
    """Returns number of players for all seasons"""
    return Player.select().count()


def findSeasons(player):
    """Returns a sorted list of all the seasons (ints) the player (obj) played in"""
    return sorted(list(set([game.season for game in Game.select().where((Game.white == player) | (Game.black == player))])))


def proportionPlayed(player):
    return np.true_divide(len(findSeasons(player)), (last_season - min(findSeasons(player)) + 1))


def gamesPlayed(player):
    """Returns number of gamaes played by the player (obj)"""
    return Game.select().where((Game.white == player) | (Game.black == player)).count()


def playerInSeason(player, season):
    """Returns 1 or 0 depending on if player (obj) played in season (int)"""
    if season in findSeasons(player):  # this is slow...
        return 1
    else:
        return 0


def findPlayers(season):
    """Returns list of players (objs) which played season (int)"""
    result = []
    for player in Player.select():
        if season in findSeasons(player):
            result.append(player)
    return result


def countPlayersInSeason(season):
    """Returns number of players for seasons"""
    return len(findPlayers(season=season))


def findNewPlayers(season):
    """Returns list of players (objs) which played season (int) but no previous season"""
    result = []
    for player in findPlayers(season):
        if min(findSeasons(player)) == season:
            result.append(player)
    return result


def countCommonPlayers(season1, season2):
    return len(set(findPlayers(season1)) & set(findPlayers(season2)))
