"""
Summary: Contains plot commands for the participation, evolution and staircase plots.
Functions: participation, evolution, staircase, plot.
"""

from config import *
from models import *
from peewee import *
from queries import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os


def retention(finalSeason):
    """Plots proportion of players who stay for the next season"""
    print("Plotting retention diagram...")
    x = range(1, finalSeason)
    y = [np.true_divide(countCommonPlayers(season, season + 1), countPlayersInSeason(season)) for season in range(1, finalSeason)]
    plt.xlim(xmin=1, xmax=finalSeason - 1)
    plt.xticks(range(1, finalSeason))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.ylim(ymin=0, ymax=1)
    plt.tick_params(top='off', right='off')
    plt.xlabel("Season")
    plt.ylabel("Proportion")
    plt.title("Proportion of players who stayed for the next season")
    plt.plot(x, y, linewidth=3)
    # plt.show()
    plt.savefig(os.path.join(subdir_figures, "retention_{}.png".format(finalSeason)))


def participation(finalSeason):
    """Plots participation history of players in finalSeason"""
    print("Plotting participation diagram...")
    players = [player for player in Player.select() if playerInSeason(player.id, finalSeason)]  # real stupid query...
    nPlayers = len(players)
    A = []
    for player in players:
        row = [playerInSeason(player, season) * len(findSeasons(player)) for season in range(1, finalSeason)]
        A.append(row)
    B = np.reshape(sorted(A, reverse=True), newshape=(nPlayers, finalSeason - 1))
    plt.imshow(B, aspect="auto", interpolation="nearest", cmap=plt.cm.gray_r)
    plt.xlabel("Season")
    plt.ylabel("Player")
    plt.tick_params(top='off', right='off')
    plt.xticks(range(0, season - 1), range(1, season))
    plt.title("Participation history of the players in season {}".format(finalSeason))
    # plt.show()
    plt.savefig(os.path.join(subdir_figures, "participation_{}.png".format(finalSeason)))
    plt.close()


def staircase(finalSeason):
    """Plots participation history for all players in the database"""
    print("Plotting staircase diagram...")
    nPlayers = countPlayers()
    A = []
    for player in Player.select():
        row = [playerInSeason(player, season) * len(findSeasons(player)) for season in range(1, finalSeason + 1)]
        A.append(row)

    B = np.reshape(sorted(A, reverse=True), newshape=(nPlayers, finalSeason))
    plt.imshow(B, aspect="auto", interpolation="nearest", cmap=plt.cm.gray_r)
    plt.xlabel("Season")
    plt.ylabel("Player")
    plt.tick_params(top='off', right='off')
    plt.xticks(range(0, finalSeason), range(1, finalSeason + 1))
    plt.title("Staircase plot of player retainment")
    # plt.show()
    plt.savefig(os.path.join(subdir_figures, "staircase_{}.png".format(finalSeason)))
    plt.close()


def evolution(finalSeason):
    """Plots the seasonal variation of new players / returning players"""
    print("Plotting evolution diagram...")
    xaxis = [0 for i in range(1, finalSeason + 1)]
    y1 = [len(findPlayers(season)) for season in range(1, finalSeason + 1)]
    y2 = [len(findNewPlayers(season)) for season in range(1, finalSeason + 1)]
    x = range(1, finalSeason + 1)

    plt.plot(x, y1, label="Returning players")
    plt.plot(x, y2, label="New players")
    plt.fill_between(x, 0, y2, facecolor="green")
    plt.fill_between(x, y1, y2, facecolor="blue")
    plt.xlim(xmin=1, xmax=finalSeason)

    plt.title("Evolution of the lichess4545 league")
    plt.xlabel("Season")
    plt.ylabel("Number of players")
    plt.tick_params(top='off', right='off')
    plt.legend(loc=0)
    plt.savefig(os.path.join(subdir_figures, "evolution_{}.png".format(finalSeason)))
    plt.close()


def plot(finalSeason):
    evolution(finalSeason)
    participation(finalSeason)
    staircase(finalSeason)
    retention(finalSeason)
