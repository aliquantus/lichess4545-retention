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
    return sorted([season.number for season in player.seasons])


def proportionPlayed(player):
    return np.true_divide(len(findSeasons(player)), (last_season - min(findSeasons(player)) + 1))


def gamesPlayed(player):
    """Returns number of gamaes played by the player (obj)"""
    return Game.select().where((Game.white == player) | (Game.black == player)).count()


def playerInSeason(player, season):
    """Returns 1 or 0 depending on if player (obj) played in season (int)"""
    if season in findSeasons(player):
        return 1
    else:
        return 0


def test(season, val):
    """Return the number of players who played val seasons before season"""
    number = season
    season = Season.get(Season.id == number)  # objectify
    print number
    print season
    quit()
    return Player.select().where(len(set([season for season in Player.seasons]) & set(range(1, number)) == val)).count()


def findPlayers(season):
    """Returns list of players (objs) which played season (int)"""
    return [player for player in Season.get(Season.id == season).players]


def countPlayersInSeason(season):
    """Returns number of players for seasons"""
    return Season.get(Season.id == season).players.count()


# this can be done more cleverly
def findNewPlayers(season):
    """Returns list of players (objs) which played season (int) but no previous season"""
    result = []
    for player in findPlayers(season):
        if min(findSeasons(player)) == season:
            result.append(player)
    return result


def countCommonPlayers(season1, season2):
    return len(set(findPlayers(season1)) & set(findPlayers(season2)))
